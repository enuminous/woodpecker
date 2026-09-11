# WOODPECKER — EFMW Zoo Animal #48

**Ablation • Counterfactual Necessity • Component Attribution**

> **Take it out. Run it again.**

WOODPECKER tests whether a claimed-essential component is actually doing the work attributed to it.

## Fixed operation

> **WOODPECKER removes or substitutes exactly one claimed-essential component while preserving all other admissible conditions, reruns the inference or system, and measures whether the claimed result materially changes.**

This operation is frozen. WOODPECKER may not change its test after seeing the result.

## Purpose

WOODPECKER addresses a specific cognitive gap:

- A method may produce a result without being necessary for that result.
- A component may look important while merely duplicating information already present elsewhere.
- A claimed mechanism may survive ordinary verification while failing a controlled ablation.
- Correlation between "component present" and "success" does not establish that the component caused or materially contributed to the success.

WOODPECKER therefore asks:

**Would the result still occur if the claimed-essential part were removed, replaced, permuted, or nullified under a defensible control?**

## Formal structure

Original system:

```text
(A, X, D) --F--> Y
```

Counterfactual system:

```text
(A, X', D) --F--> Y'
```

Where:

- `A` = explicit assumptions
- `X` = claimed-essential component
- `X'` = prespecified null/removal/substitute/permutation
- `D` = fixed data or environment
- `F` = frozen inference/system
- `Y` = original output
- `Y'` = ablated output

WOODPECKER measures:

```text
ΔX = d(Y, Y')
```

against a predeclared tolerance `epsilon`.

## Principal outputs

WOODPECKER returns exactly one primary disposition:

- **NECESSARY** — removal/substitution materially destroys the claimed effect.
- **CONTRIBUTORY** — the effect remains, but is materially degraded.
- **REDUNDANT** — the effect survives within the frozen tolerance.
- **INDETERMINATE** — the ablation fails to isolate the component cleanly.

`REDUNDANT` does **not** mean the broader claim is false. It means the tested component has not been shown to be necessary under this ablation.

## Inputs

See [`SPEC.md`](SPEC.md) and [`schema/input.schema.json`](schema/input.schema.json).

Minimum conceptual inputs:

1. target claim
2. claimed-essential component
3. original output
4. ablated output
5. frozen comparison metric
6. frozen tolerance
7. ablation method
8. preserved conditions
9. known violations/confounds

## Failure conditions

WOODPECKER must return **INDETERMINATE** when, among other cases:

- the null/control was selected after observing the result;
- removing `X` changes another relevant variable;
- `X'` leaks equivalent information about `X`;
- the ablation makes the system undefined;
- the success threshold was changed post hoc;
- stochastic variation is not controlled;
- the original claim was not a necessity/contribution claim;
- the chosen null is indefensible;
- the test changes more than one causal component without justification.

## Reference implementation

Requires Python 3.10+ and no third-party packages.

```bash
python -m woodpecker examples/redundant.json
python -m woodpecker examples/necessary.json
python -m woodpecker examples/indeterminate.json
```

Run the adversarial qualification suite:

```bash
python -m unittest discover -s tests -v
```

## Example

```json
{
  "claim": "Component X is essential to the detector's warning advantage.",
  "component": "X",
  "baseline_value": 16.5,
  "ablated_value": 16.2,
  "metric": "paired_median_gain",
  "higher_is_better": true,
  "epsilon": 1.0,
  "contributory_fraction": 0.25,
  "ablation": "replace X with matched conventional substitute",
  "preserved_conditions": [
    "same data",
    "same seeds",
    "same false-positive constraint",
    "same compute budget"
  ],
  "violations": [],
  "pre_registered": true,
  "proxy_leakage": false,
  "claim_type": "necessity"
}
```

If the effect remains within tolerance, WOODPECKER returns `REDUNDANT`.

## Zoo personality

WOODPECKER is annoying on purpose.

Whenever someone says:

> "This part is essential."

WOODPECKER immediately pecks that exact part out.

## Status

**Candidate Zoo Animal #48**

This repository defines the operation, proof obligations, failure states, reference implementation, and qualification tests needed before canonical admission.

## Scientific caution

WOODPECKER is a methodological instrument, not a proof oracle. An ablation can support or weaken a necessity/contribution claim only to the extent that the counterfactual is well-defined and competing explanations are adequately controlled.
