# Forza Tuning Knowledge Index

Use this file as the map for the skill's durable knowledge. Do not put long tuning manuals here. Load the smallest reference that answers the question.

## Source Priority

1. **Paramount Horizon tuning core**: Treat `How To Build & Tune in Forza Horizon 6  Basic Refresher & FH6 Changes Guide.txt` and `Tuning Basics Explained by a Forza Horizon Guru.txt` as the highest-priority sources for Horizon road, circuit, sprint, touge, and general build/tune decisions. Their shared principles override casual tips from other sources: test in the target environment, prioritize tires/brakes/weight/ARBs/diff before excess power, use telemetry when available, preserve a clear evidence trail, and tune build-dependent systems together.
2. **FH6-specific tie-breaker**: When the two paramount guides disagree, prefer the FH6 Basic Refresher for FH6-specific PI, tire, brake, aero, mechanical-balance, and class-meta changes. Use the Guru guide as the deeper process model for test design, telemetry interpretation, gearing, suspension/alignment relationships, and driver-consistency tradeoffs.
3. **Other FH6 race/build guides**: Useful support for examples, baselines, and alternate approaches, but lower priority than the two paramount guides unless they describe a more recent FH6-specific mechanic.
4. **FH6 drag guides**: Primary only for drag launch, tire heat, drag gearing, and drag suspension behavior. Exact values are car-specific examples.
5. **FH5 purist guide**: Useful for purist constraints and legacy Horizon build logic. Lower confidence for FH6 unless it agrees with the paramount Horizon tuning core or the user asks for FH5/purist.
6. **Forza Motorsport guides**: Useful for general mechanics, Motorsport classing, and Motorsport brake/diff/transmission tests. Lower confidence for Horizon meta because PI, physics, UI, and optimal pressures can differ.

## Reference Loading

- Load `build-decision-tree.md` for class targets, car archetypes, upgrades, tire family, engine swaps, drivetrain swaps, and build order.
- Load `event-decision-tree.md` for road, sprint, touge, drag, dirt/rally, cross country, drift, or purist event decisions.
- Load `setup-diagnosis.md` for tuning sliders, telemetry, and symptom-to-knob decisions.

## Local Expert Source Notes

Condense local transcripts into reusable rules, not verbatim passages. The FH6 Basic Refresher and Horizon Guru guides are the paramount sources and should be consulted first for Horizon road/build/tuning logic. Other useful expert files include pro race tune guides for examples, FH6 drag videos for drag-only launch/heat/gearing behavior, FH5 purist for restriction-preserving logic, and Forza Motorsport aero/brake/diff/transmission/YMBS guides for Motorsport-specific mechanics and test methods.

When a rule comes from Motorsport and the user is tuning Horizon, mark it as a caveat or lower-confidence fallback. When a rule comes from FH6 drag and the user is road racing, do not import it except for clearly shared mechanics such as tire heat awareness.


## Mapped Source Insights

Use this ledger when deciding where transcript knowledge belongs. Keep the one-line mapping compact; detailed rules belong in the three decision-tree files.

| Source | Durable insight | Target reference |
|---|---|---|
| `Aerodynamics Tuning Guide for Forza Motorsport (Forza Tips).txt` | Motorsport aero is a front/rear balance pair: front downforce rotates, rear downforce stabilizes, and low-power classes may lose too much speed to drag. | `setup-diagnosis.md` aero and Motorsport caveats |
| `Brakes Tuning Guide in Forza Motorsport (Forza Tips).txt` | Motorsport brake bias can be tuned with a straight-line ABS-off lockup test; target fronts locking just before rears, then confirm trail-brake behavior. | `setup-diagnosis.md` brake tests |
| `Differential Tuning Guide for Forza Motorsport - RWD, FWD, AWD (Forza Tips).txt` | Single-tire fire means accel lock is too open; lift-off rotation means decel is too open; AWD center split should be judged by power-on rotation. | `setup-diagnosis.md` diff diagnosis |
| `Tuning Transmissions in Forza Motorsport (Forza Tips).txt` | Build gearing from launch gear, top gear for the target track set, then middle gears for slow-corner exits and power band. | `setup-diagnosis.md` gearing workflow |
| `How to Build and Tune the Fastest Cars in Forza Motorsport - World Record Tuning Numbers - YMBS.txt` | Motorsport open-class meta values and geometry tricks are high-risk, title-specific, and should not become Horizon defaults. | `setup-diagnosis.md` Motorsport caveats |
| `How To Build & Tune in Forza Horizon 6  Basic Refresher & FH6 Changes Guide.txt` | Paramount FH6 source: tires, front tire width, brakes, stability, weight, balanced aero, mechanical balance, and target-event priorities define the FH6 default. | `build-decision-tree.md`, `setup-diagnosis.md`, `event-decision-tree.md` |
| `HOW TO TUNE in Forza Horizon 6! Full PRO GUIDE (Upgrades & Tuning).txt` | S1 all-round builds may favor rear tire width and rally/semi/slick compound choices while keeping front tire width conditional on handling need. | `build-decision-tree.md` tire and power order |
| `Forza Horizon 6 BEST Race Tune Guide - How To Make Any Car Faster.txt` | FH6 race baselines: small changes, pressure around 28/27-28 for AWD race, soft springs, damping around 18/18 rebound and 6/6 bump as an approachable baseline. | `setup-diagnosis.md` baselines |
| `HOW TO TUNE IN FORZA HORIZON 6 (Basics Tuning Guide).txt` | Beginner-safe rules: upgrades create potential, tuning controls it; grippier tires can be less communicative; change one variable at a time. | `SKILL.md` test loop and `setup-diagnosis.md` |
| `Tuning Basics Explained by a Forza Horizon Guru.txt` | Paramount Horizon tuning-process source: test in the target event, use telemetry, protect consistency, set top gear slightly beyond observed max speed, and respect suspension/alignment/damping relationships. | `event-decision-tree.md`, `build-decision-tree.md`, `setup-diagnosis.md` |
| `How to PURIST in Forza Horizon 5 (how to buildtune).txt` | Purist means no engine swaps, no drivetrain swaps, no Forza aero; use tires, weight, ARBs, diff type, suspension, roll cage, and front tire width as substitutes. | `event-decision-tree.md`, `build-decision-tree.md` |
| `FORZA HORIZON 6 - 2,790HP NISSAN GT-R FE RUNS 6.056! FULL DRAG TUNE + SHARE CODE.txt` | FH6 drag examples are car-specific, but tire heat, launch method standardization, early-gear tuning, and squat/wheelie control are reusable. | `event-decision-tree.md`, `setup-diagnosis.md` |
| `Forza Horizon 6  Fastest Drag Car In The Game!! (Forza Science).txt` | Drag comparisons need repeatable Rivals conditions, multiple attempts, tire-temperature awareness, shift timing, and trap-speed review. | `event-decision-tree.md` drag test loop |

## Knowledge Card Rule

When adding new knowledge, use compact decision cards with these fields: `Applies when`, `Symptom`, `Evidence`, `Likely causes`, `Primary knobs`, `Safe order`, `Contraindications`, `Test`, `Source priority`, `Confidence`.

Preserve contradictions as conditional branches. Store reusable rules, not raw transcript text or one-off tune values unless they teach a general rule.
