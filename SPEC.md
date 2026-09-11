# WOODPECKER Specification

## 1. Identity

**Name:** WOODPECKER  
**Number:** Candidate EFMW Zoo Animal #48  
**Class:** Counterfactual discrimination / ablation / component attribution  
**Motto:** **Take it out. Run it again.**

## 2. Frozen operation

> **WOODPECKER removes or substitutes exactly one claimed-essential component while preserving all other admissible conditions, reruns the inference or system, and measures whether the claimed result materially changes.**

The operation MUST NOT be altered after outcome inspection.

## 3. Scope

WOODPECKER tests claims of:

- necessity;
- material contribution;
- mechanistic attribution;
- architectural indispensability;
- explanatory dependence.

It does not, by itself, establish:

- sufficiency;
- truth of an entire theory;
- causal identification under arbitrary confounding;
- uniqueness of a mechanism;
- generalization beyond the tested counterfactual.

## 4. Input contract

Required fields:

- `claim`
- `component`
- `baseline_value`
- `ablated_value`
- `metric`
- `higher_is_better`
- `epsilon`
- `contributory_fraction`
- `ablation`
- `preserved_conditions`
- `violations`
- `pre_registered`
- `proxy_leakage`
- `claim_type`

### claim_type

Accepted values:

- `necessity`
- `contribution`

Other claim types are rejected as outside WOODPECKER's fixed jurisdiction.

## 5. Decision procedure

Let:

- `B` = performance/effect with X present
- `A` = performance/effect with X ablated
- `epsilon` = frozen equivalence tolerance
- `f` = contributory fraction in `[0,1]`

Orient the metric so that larger is better.

Then compute:

```text
loss = B - A
```

after orientation.

### INDETERMINATE takes precedence

Return `INDETERMINATE` if:

- pre-registration is false;
- proxy leakage is true;
- one or more violations are declared;
- the claim type is outside jurisdiction;
- values are non-finite;
- epsilon is negative;
- contributory_fraction is outside `[0,1]`.

### REDUNDANT

If:

```text
loss <= epsilon
```

then `REDUNDANT`.

### NECESSARY

Define a practical destruction threshold:

```text
necessity_threshold = max(epsilon, abs(B) * (1 - f))
```

If:

```text
loss > necessity_threshold
```

return `NECESSARY`.

This reference rule is deliberately simple and must be replaced by a domain-specific frozen criterion when the science provides a better one.

### CONTRIBUTORY

Otherwise return `CONTRIBUTORY`.

## 6. Interpretation rules

### NECESSARY

Means:

> Under the prespecified ablation, removing/replacing X materially destroys the tested effect according to the frozen criterion.

It does not mean X is metaphysically or universally necessary.

### CONTRIBUTORY

Means:

> Under the tested ablation, X materially affects the result, but the result is not destroyed.

### REDUNDANT

Means:

> Under the tested ablation, the result survives within the frozen tolerance.

It does not mean X has no value in any other context.

### INDETERMINATE

Means:

> The test does not cleanly isolate X or violates the fixed WOODPECKER contract.

## 7. Required audit record

Every run SHOULD retain:

- timestamp;
- software/version identifier;
- dataset identifier;
- random seeds;
- hash of input JSON;
- ablation definition;
- frozen thresholds;
- output disposition;
- diagnostic notes.

## 8. Adversarial qualification battery

WOODPECKER must survive:

1. **Renaming attack** — mathematically/functionally equivalent replacement must not count as removal.
2. **Leakage attack** — proxy retains equivalent information.
3. **Confounding attack** — changing X also changes Z.
4. **Dead-code attack** — elaborate but unused component must be classified REDUNDANT.
5. **Synergy attack** — X matters only jointly with Z; universal conclusions are prohibited.
6. **Threshold attack** — post-hoc epsilon invalidates the run.
7. **Stochastic attack** — uncontrolled run variance triggers INDETERMINATE.
8. **Semantic attack** — deleting a label while retaining its functional content is not a true ablation.
9. **Catastrophic-null attack** — absurd null chosen only to make the system fail is invalid.
10. **Self-test** — replace a claimed EFMW-specific component with the strongest matched conventional alternative.

## 9. Canonical personality trait

WOODPECKER's personality is **persistent destructive curiosity**:

> When told that a component is essential, it immediately tries to remove exactly that component without disturbing anything else.
