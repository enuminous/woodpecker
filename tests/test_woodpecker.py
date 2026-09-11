import unittest

from woodpecker import evaluate, Disposition


def base_case():
    return {
        "claim": "X is essential.",
        "component": "X",
        "baseline_value": 10.0,
        "ablated_value": 10.0,
        "metric": "score",
        "higher_is_better": True,
        "epsilon": 0.5,
        "contributory_fraction": 0.25,
        "ablation": "remove X",
        "preserved_conditions": ["same data", "same seed"],
        "violations": [],
        "pre_registered": True,
        "proxy_leakage": False,
        "claim_type": "necessity",
    }


class WoodpeckerQualificationTests(unittest.TestCase):
    def test_dead_code_attack_redundant(self):
        c = base_case()
        c["ablated_value"] = 9.8
        self.assertEqual(evaluate(c).disposition, Disposition.REDUNDANT)

    def test_strong_destruction_necessary(self):
        c = base_case()
        c["ablated_value"] = 1.0
        self.assertEqual(evaluate(c).disposition, Disposition.NECESSARY)

    def test_partial_loss_contributory(self):
        c = base_case()
        c["ablated_value"] = 7.0
        self.assertEqual(evaluate(c).disposition, Disposition.CONTRIBUTORY)

    def test_leakage_attack_indeterminate(self):
        c = base_case()
        c["proxy_leakage"] = True
        self.assertEqual(evaluate(c).disposition, Disposition.INDETERMINATE)

    def test_confounding_attack_indeterminate(self):
        c = base_case()
        c["violations"] = ["removing X also changed Z"]
        self.assertEqual(evaluate(c).disposition, Disposition.INDETERMINATE)

    def test_threshold_attack_indeterminate_if_not_preregistered(self):
        c = base_case()
        c["pre_registered"] = False
        self.assertEqual(evaluate(c).disposition, Disposition.INDETERMINATE)

    def test_wrong_claim_type(self):
        c = base_case()
        c["claim_type"] = "sufficiency"
        self.assertEqual(evaluate(c).disposition, Disposition.INDETERMINATE)

    def test_lower_is_better(self):
        c = base_case()
        c.update({
            "baseline_value": 2.0,
            "ablated_value": 8.0,
            "higher_is_better": False,
            "epsilon": 0.5,
        })
        self.assertEqual(evaluate(c).disposition, Disposition.NECESSARY)

    def test_negative_epsilon_invalid(self):
        c = base_case()
        c["epsilon"] = -1
        self.assertEqual(evaluate(c).disposition, Disposition.INDETERMINATE)

    def test_missing_fields_invalid(self):
        c = base_case()
        del c["ablation"]
        self.assertEqual(evaluate(c).disposition, Disposition.INDETERMINATE)


if __name__ == "__main__":
    unittest.main()
