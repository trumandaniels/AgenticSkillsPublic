# Extraction Examples

Source base: `book1:chapter-8-complexity`.

## Feature-Driven Redesign

Before shape:

```text
add new backend support by sprinkling backend-specific if/else branches at every data access site
```

After shape:

```text
standardize one existing data access operation
create one focused helper for one nonstandard operation
migrate one caller group
test old behavior
repeat
```

Decision reason: spreading special cases increases total system complexity. Small-step boundary redesign lets the system support the new feature while making future maintenance easier.

Avoid condition: do not create a broad backend abstraction before the current feature demonstrates what operations actually need to vary.

## Complex Function

Before shape:

```text
one long routine validates input, transforms data, writes records, and formats user-facing output
```

After shape:

```text
caller orchestrates the known flow
validation helper owns validation rules
transformation helper owns data conversion
output helper owns presentation details
```

Decision reason: a complex piece can be redesigned by splitting off one understandable subpiece at a time, validating after each move.

Avoid condition: do not split so aggressively that a reader must jump through many tiny helpers to understand a short local behavior.
