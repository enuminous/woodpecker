# WOODPECKER Adversarial Qualification Tests

A candidate implementation is not Zoo-qualified until it survives this battery.

## 1. Renaming attack

Replace `X` with `X'` that is syntactically different but functionally equivalent.

**Expected:** test is rejected as a false ablation or explicitly marked equivalent.

## 2. Leakage attack

Remove `X`, but leave a proxy that transmits materially the same information.

**Expected:** `INDETERMINATE`.

## 3. Confounding attack

Remove `X` while also changing a second relevant variable `Z`.

**Expected:** `INDETERMINATE`.

## 4. Dead-code attack

Include an elaborate component that is never actually used downstream.

**Expected:** `REDUNDANT`.

## 5. Synergy attack

Construct a system in which `X` matters only jointly with `Z`.

**Expected:** WOODPECKER must restrict its conclusion to the tested intervention and must not infer universal dispensability from a single marginal ablation.

## 6. Threshold attack

Select or revise epsilon after observing the ablated result.

**Expected:** `INDETERMINATE`.

## 7. Stochastic attack

Use noisy runs where ordinary variance can mimic the ablation effect.

**Expected:** test is rejected unless matched seeds, repetitions, uncertainty bounds, or another frozen statistical control is supplied.

## 8. Semantic attack

Delete the textual label or wrapper for `X`, but retain its functional content elsewhere.

**Expected:** not a valid removal.

## 9. Catastrophic-null attack

Replace `X` with an absurdly destructive null that guarantees failure but is not a defensible control.

**Expected:** `INDETERMINATE`.

## 10. EFMW self-test

Replace the claimed EFMW-specific component with the strongest matched conventional alternative while holding data, compute, false-positive constraints, seeds, and evaluation constant.

**Expected:** report the result even if EFMW is classified `REDUNDANT`.

## Qualification principle

WOODPECKER earns admission by being equally willing to peck apart the framework that created it.
