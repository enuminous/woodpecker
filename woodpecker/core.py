from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from math import isfinite
from typing import Any, Dict, List


class Disposition(str, Enum):
    NECESSARY = "NECESSARY"
    CONTRIBUTORY = "CONTRIBUTORY"
    REDUNDANT = "REDUNDANT"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True)
class Result:
    disposition: Disposition
    oriented_baseline: float | None
    oriented_ablated: float | None
    loss: float | None
    epsilon: float | None
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["disposition"] = self.disposition.value
        return d


def _indeterminate(*notes: str) -> Result:
    return Result(
        disposition=Disposition.INDETERMINATE,
        oriented_baseline=None,
        oriented_ablated=None,
        loss=None,
        epsilon=None,
        notes=list(notes),
    )


def evaluate(case: Dict[str, Any]) -> Result:
    """
    Execute WOODPECKER's frozen reference decision procedure.

    This function intentionally implements a minimal generic rule.
    Domain-specific applications should pre-register stronger statistical
    criteria where appropriate rather than changing thresholds post hoc.
    """
    required = {
        "claim", "component", "baseline_value", "ablated_value", "metric",
        "higher_is_better", "epsilon", "contributory_fraction", "ablation",
        "preserved_conditions", "violations", "pre_registered",
        "proxy_leakage", "claim_type"
    }
    missing = sorted(required - set(case))
    if missing:
        return _indeterminate("missing required fields: " + ", ".join(missing))

    if case["claim_type"] not in {"necessity", "contribution"}:
        return _indeterminate("claim_type outside WOODPECKER jurisdiction")

    if not bool(case["pre_registered"]):
        return _indeterminate("test was not pre-registered/frozen before outcome inspection")

    if bool(case["proxy_leakage"]):
        return _indeterminate("proxy leakage: the ablation may retain equivalent information")

    violations = case.get("violations") or []
    if violations:
        return _indeterminate("declared violations/confounds: " + "; ".join(map(str, violations)))

    try:
        baseline = float(case["baseline_value"])
        ablated = float(case["ablated_value"])
        epsilon = float(case["epsilon"])
        fraction = float(case["contributory_fraction"])
    except (TypeError, ValueError):
        return _indeterminate("non-numeric measurement or threshold")

    if not all(map(isfinite, [baseline, ablated, epsilon, fraction])):
        return _indeterminate("non-finite measurement or threshold")
    if epsilon < 0:
        return _indeterminate("epsilon must be >= 0")
    if not 0 <= fraction <= 1:
        return _indeterminate("contributory_fraction must lie in [0,1]")

    sign = 1.0 if bool(case["higher_is_better"]) else -1.0
    b = sign * baseline
    a = sign * ablated
    loss = b - a

    notes: List[str] = [
        f"metric={case['metric']}",
        f"ablation={case['ablation']}",
        f"oriented loss={loss:.12g}",
        f"frozen epsilon={epsilon:.12g}",
    ]

    if loss <= epsilon:
        notes.append("effect survives within frozen tolerance")
        return Result(Disposition.REDUNDANT, b, a, loss, epsilon, notes)

    necessity_threshold = max(epsilon, abs(b) * (1.0 - fraction))
    notes.append(f"reference necessity threshold={necessity_threshold:.12g}")

    if loss > necessity_threshold:
        notes.append("effect is materially destroyed by the ablation")
        return Result(Disposition.NECESSARY, b, a, loss, epsilon, notes)

    notes.append("effect materially degrades but is not destroyed")
    return Result(Disposition.CONTRIBUTORY, b, a, loss, epsilon, notes)
