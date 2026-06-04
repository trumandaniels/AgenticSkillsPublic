# Build Decision Tree

Use this before setup diagnosis. A bad build cannot be tuned into a good event car.

Treat the FH6 Basic Refresher as the primary FH6 build source and the Horizon Guru guide as the primary process/validation source. When in doubt, follow their shared order: choose the event, build the platform and tires correctly, validate in the target environment, then fill PI with power.

## Build Order

1. Identify ruleset, natural class, target class, and class ceiling. For FH6, use C500, B600, A700, S1 800, S2 900, and R1000. Do not import FH5/Horizon-legacy A800 assumptions into FH6. Keep most cars within one or two classes of stock unless the event clearly rewards a stretch.
2. Judge real performance with power-to-weight, lateral G, weight, weight distribution, drivetrain, and power band. Treat global 0-10 stat cards and raw horsepower as hints, not build verdicts.
3. Choose event fit: handling, speed, launch, loose surface, rough terrain, purist.
4. Check conversions and body/widebody before engine upgrades because they can unlock tire width, aero, diff behavior, aspiration, or weight changes. Use body kits when they improve tire/aero/stability/weight enough for the event; skip them when drag, weight, or PI cost overwhelms the benefit.
5. Pick tire family, front tire width, and rear tire width. In FH6, tire compound and width are build-defining: bad tires feel worse, good tires feel better, and front tire width is often worth PI for braking and turn-in on handling routes.
6. Consider front track width and rear track width separately from front/rear tire width when stance/stability/handling stats justify the PI. Track width can be cheap/free; more overall track adds grip/stability, more front track width relative to rear improves turn-in, and more rear track width improves stability.
7. Treat rim size separately from tire width and track width; change it only for wheel diameter/sidewall/weight/PI reasons. Rim style/weight can make a build fit PI, but heavier rims can hurt feel.
8. Buy cheap control unlocks: ARBs and an appropriate adjustable differential. In FH6, experiment with race/rally/drift/off-road diff type when the hidden handling behavior matters, but do not overstate this ahead of the main build.
9. Add brakes if stock brakes cause long stops, lockups, entry push, or underbraking. FH6 makes brakes more valuable than old Horizon habits imply, especially when stock/street brakes meet better tires.
10. Add weight reduction. Race weight reduction is often one of the most PI-efficient upgrades when available.
11. Add suspension type for the event, but do not assume race suspension is always better. Keep good factory suspension when it preserves special behavior such as factory four-wheel steering, strong stock alignment, or a useful stock handling model.
12. Choose transmission/clutch/driveline intentionally: sport transmission can be a cheap final-drive unlock; race transmission often removes clutch-upgrade value; clutch is mostly for auto with stock/sport gearbox; driveline is usually PI filler.
13. Fill remaining PI with power, then tune gearing to the power band. Heavy power/engine swaps belong more in sprint/speed builds than technical road/touge unless the PI math clearly supports them.

## Class Ceiling Rules

- Always confirm the game/ruleset before converting a class letter into a PI target.
- FH6 classing: C is up to PI 500, B is up to PI 600, A is up to PI 700, S1 is up to PI 800, S2 is up to PI 900, and R is up to PI 1000. A stock PI 647 car has only about 53 PI to spend before the FH6 A ceiling.
- FH5/Horizon-legacy or custom classing may differ; use A800 only when the user specifies that ceiling or an S1 800 target.
- Motorsport/FM-style classing may differ from FH6; verify the title/ruleset before prescribing upgrades.
- If the user says a class letter and a stock/current PI that conflicts with the assumed ceiling, state the assumption or ask before prescribing upgrades.

## Upgrade Prioritization

Use these labels exactly when ranking possible build changes: **Top**, **High**, **Medium High**, **Medium**, **Medium Low**, **Low**, **Very Low**. Priority is contextual: a Top item removes the current event/class bottleneck; a Very Low item is usually skipped unless the user has spare PI or a special goal.

- Start with the event bottleneck, then spend PI where it removes the biggest lap-time limit. For road/circuit, prioritize platform control and cornering time before raw power.
- Usually rank adjustable diff, ARBs, correct tire family, and class-appropriate suspension/brakes as Top or High when they unlock needed tuning or fix an event mismatch.
- Usually rank tire compound, front tire width, and rear tire width as Top/High when grip, braking, tire heat, or traction is the bottleneck. Front tire width is often High for front-limited cars; rear tire width is High when exit traction is limiting.
- Usually rank brakes and weight reduction as High/Medium High for heavy road cars or hard-braking tracks when PI-efficient.
- Usually rank front track width and rear track width as Medium High/Medium when they are cheap and support the desired axle behavior; rank rim size as Medium Low/Low unless sidewall/weight/PI needs justify it.
- Usually rank aero as Medium High/Medium for circuit/time attack and Medium/Low for speed-biased sprint unless it also unlocks tire width or solves high-speed instability.
- Usually rank transmission as Medium High when final-drive tuning is needed, clutch as Medium Low/Low except auto plus stock/sport gearbox, and driveline as Low/Very Low PI filler.
- Usually rank engine swaps and drivetrain swaps as Low/Very Low for technical road or purist builds unless the target class/event demands the change.
- Explain skipped upgrades when PI is tight. FH6 A700 builds may need fewer parts than S1 800 builds, so do not import S1-style tire/brake/weight/power bundles blindly.

### In-Category Upgrade Order

When a category is recommended, also rank the likely upgrades inside that category. Use `Top`, `High`, `Medium High`, `Medium`, `Medium Low`, `Low`, and `Very Low` within the category; do not just say `Power: Medium` if the user needs a build path.

| Category | Usual inside order | Notes |
|---|---|---|
| Tires | Compound first, then front tire width, rear tire width, front track width, rear track width, rim size | Choose compound for event/class, then use tire width for contact patch and axle grip balance. Use track width for stance/response/stability; it is not tire size. Rim size is usually sidewall/weight/PI trim. |
| Power | Airflow/weight-efficient parts and aspiration first when PI-efficient, then cams/power-band parts, exhaust/intake/fuel/ignition, displacement, turbo/supercharger upgrades, intercooler/oil/cooling last unless heat or power route demands them | Favor parts that fit the engine power band and event. Treat heavy adders cautiously on technical builds because they can add weight or shift balance. |
| Engine swap | Stock engine/light useful power-band swap first, heavier power swap only for sprint/speed or class stretch, novelty/high-weight swaps last | Compare PI, weight, torque curve, and target event before swapping. |
| Drivetrain | Keep native drivetrain first, AWD for launch/high-power/off-road consistency, RWD for rotation/top-end efficiency, FWD only when native or class/event supports it | Swaps reset diff, gearing, weight, and driving style assumptions. |
| Platform | ARBs/diff unlocks first, brakes when stopping/entry is weak, weight reduction when PI-efficient, suspension type for surface/compliance, cage only when stiffness/PI tradeoff is justified | Cheap tuning unlocks can outrank raw grip because they let the tune work. |
| Aero/body | Aero only if event speed and car need justify drag/PI, front aero for high-speed rotation, rear aero for stability, widebody only if it unlocks useful tire/track/stability for the cost | Balance aero with mechanical grip; FH6 is less dependent on max-front/min-rear old habits. |
| Transmission/driveline | Sport transmission for cheap final-drive unlock, race transmission when individual gears/sequential behavior are worth it, clutch mainly for auto plus stock/sport gearbox, driveline as PI filler | Gearing benefit matters more than stat-card speed. |

### Tire Width Sizing Guidance

When recommending front tire width or rear tire width, state how large to go. Use exact in-game sizes when the user provides them or when known; otherwise use stock, one step wider, or max available.

- Max front tire width is often the first tire-width target for front-limited road, touge, heavy front-engine, FWD, and hard-braking builds when PI allows.
- Max rear tire width is often right for high-power RWD, traction-limited AWD/RWD exits, drag, rear-heavy cars, or all-round S1 AWD builds where rear stability and launch/exit traction are cheap pace.
- Front tire width and rear tire width can trade priority by event: front tire width rises for braking, turn-in, touge, circuit, FWD, and nose-heavy cars; rear tire width rises for power, launch, rear stability, and low-speed exit traction.
- One step wider is the default when PI is tight, the car only needs a small balance correction, or max width forces skipping higher-priority brakes, diff, ARBs, weight reduction, or compound.
- Stock tire width is acceptable when the class is very tight, the tire is not the bottleneck, or the event rewards power/drag more than cornering.
- Do not automatically recommend max front plus max rear. Say why each axle needs stock, one step, or max, and what to drop if PI does not fit.

Inside-order is contextual. If the current bottleneck is exit traction, rear tire width may outrank front tire width; if the route is long sprint, power and drag may outrank brakes; if the car cannot stop or rotate, brakes/front tire/weight can outrank power even when power is available.

### Build Changes That Reset Tune Baselines

Any build recommendation should mention the tune families it may force the user to revisit.

| Upgrade change | Retune after change | Why |
|---|---|---|
| Tire compound | Tire pressure, camber, ARBs, springs/damping | Grip level, heat window, sidewall, and slip behavior change |
| Front tire width/rear tire width | Pressure split, ARB balance, brake bias, diff accel/decel, gearing | Grip balance and traction capacity move between axles |
| Front track width/rear track width | ARBs, alignment, damping feel | Stance changes stability and response without changing tire size |
| Rim size | Pressure feel, damping, ride quality | Sidewall and weight change response and compliance |
| Suspension type | Springs, ride height, damping, alignment | Travel, stiffness range, and platform assumptions change |
| Aero | Springs, ride height, damping, gearing | Downforce needs platform support and adds drag |
| Brakes | Brake bias, pressure, entry balance | Stronger brakes can create new front overload or rear rotation |
| Weight reduction | Springs, damping, brake bias, gearing | Mass and weight transfer change across all phases |
| Power/engine | Gearing, diff accel, tire pressure, rear tire need | Torque curve and traction demand change |
| Drivetrain | Diff, gearing, ARBs, brake/throttle habits | Power delivery and rotation model change |

## Wheel Upgrade Terms

- Tire compound: rubber family. Choose this for surface, class, heat, and grip budget.
- Tire width: front tire width and rear tire width are tire size and contact patch. Use this for braking, turn-in, steady-state grip, and traction capacity.
- Track width: front track width and rear track width are wheel stance/axle width. Use this for stance, stability, responsiveness, or handling-stat tuning; it does not make the tire itself wider.
- Rim size: wheel diameter/sidewall/weight/PI choice. Do not recommend rim size when the intended fix is wider tire width or wider track width.
- Keep all four width families explicit in build advice: front tire width, rear tire width, front track width, and rear track width. If the user says "width," ask or infer from context whether they mean tire width or track width before prescribing an upgrade. Never output ambiguous "front width" or "rear width" rows.

## Car Archetype Routing

| Archetype | Main risk | Build bias | Setup bias |
|---|---|---|---|
| Front-engine or nose-heavy | Front overload, entry/mid understeer, brake push | Front tire width, brakes, weight reduction, rear rotation | Reduce front overload, use rear to help rotate |
| Mid/rear-engine | Snap rotation, high-speed rear instability | Rear tire support, rear aero if fast, smooth power | Stabilize entry and power transitions |
| Heavy car | Long braking, tire heat, lazy transitions | Weight/brakes/tires before power | Support mass without making it skate |
| Lightweight/short wheelbase | Nervousness, snap, wheelspin | Grip/stability before big power | Smooth diff/gearing/damping |
| High-power/low-grip | Wheelspin, power under/oversteer | More tire, longer gears, AWD only if justified | Tune exit and throttle delivery first |

## Class Strategy

| Target | Typical priority | Tire guidance | Swap guidance |
|---|---|---|---|
| Low class | PI efficiency and natural strengths | Stock/street can work; FWD may need rally/drag/slick depending on grip | Avoid heavy swaps; cheap unlocks matter |
| Mid class | Balanced power, grip, weight | Rally/drift often beat sport for road; semis become viable, especially RWD/tight tracks | Stock/light engines often best; AWD not mandatory |
| High class | Tire/aero/brake platform | Semi/full slicks become valuable; rally/drift can still work case-by-case | Power is useful only after platform survives it |
| Drag/unlimited | Launch and power delivery | Drag tires/width and pressure split matter | Max power can be valid if launch is solved |

## Body, Widebody, And Chassis Decision

- Widebody/body kits are competitive only when the event uses what they unlock: wider front tire width/rear tire width, useful adjustable aero, stability, or weight reduction. Skip them when they add too much drag, weight, or PI for a low-class or speed-biased build.
- Adjustable front and rear aero from a kit can justify the kit on all-round/circuit builds; it is less compelling on low-power sprint builds where drag dominates.
- Chassis reinforcement/roll cage is a situational mechanical-grip and transition-stability tool. It rises in priority for older, low-aero, loose, or high-transition cars; it falls for modern grippy cars, PI-tight builds, and cars made worse by added weight.
- If unsure on a cage, compare the final class-limit build with and without it using acceleration, lateral G, and a short target-event run. Do not buy it only because it is available.
- Stock suspension can be the correct purist or PI-efficient choice when race suspension makes a front-limited car too balanced/understeery or removes useful factory behavior.

## Tire Family Decision

- Lower FH6 classes: RWD/AWD can often stay stock or street; FWD may need drag, rally, or even slicks if front grip is the bottleneck and PI/drivability allow it.
- Mid FH6 classes: rally and drift tires can be better on-road choices than sport. Semis become viable, especially for RWD or tighter tracks.
- S1 all-round FH6 road builds often compare Rally, Semi Slick Race, and Slick Race instead of assuming the grippiest compound wins. Rally can be PI-efficient and forgiving; semis/slicks rise when handling grip matters more than PI savings.
- High FH6 classes: semis and slicks gain value, especially for RWD. Rally/drift remain situational.
- Rally/off-road: off-road race tires are usually the surface-first choice.
- Front tire width is now a real PI lever in FH6. Leave room for at least one front tire-width step on handling, touge, or tight road builds; use further width if braking/cornering is still the bottleneck.
- Use tire width before jumping a full compound when the car only needs a small grip correction and PI is tight.
- Grippier compounds can be faster but less communicative: slicks reward staying under the limit and punish breakaway more sharply than lower-end tires. For learning or casual stability, do not over-tire the car blindly.
- Rain/wet: avoid blindly applying drift-tire advice from FH5 purist sources because drift tires were called out as weak in rain. Rally tires rise in wet or mixed-surface contexts.

## Power And Aspiration Decision

Use power to fill the remaining PI only after the platform can use it.

- Check power band before raw peak power. Engines or parts that make their best power near/after the automatic shift point can be PI-efficient for manual drivers, but only if the gearing and shift plan use that power.
- Aspiration is case-specific. Centrifugal superchargers are often strong when available because power rises with RPM; turbo and supercharger choices depend on lag, weight, sound, and event needs.
- Power order: exhaust and other weight-saving power parts first, then useful fuel/intake/manifold/ignition/valves/cams according to the power curve, then displacement/boost upgrades when the class needs them.
- Cams are valuable when the engine falls off before the desired shift point or needs a higher-rpm power band; skip or down-rank them when they expose more power to PI without improving average power through the gears.
- Intercooler and oil/cooling upgrades come late because they add weight and can shift balance. A rough rejection test from purist/Horizon logic: if added weight is more than about three times the horsepower gain, treat it as low value unless the power route demands it.
- Flywheel and driveline are final-fit tools. Use them to spend leftover PI or improve response, but do not let them crowd out tires, brakes, weight, diff, ARBs, or the event-critical power part.

## Engine Swap Decision

Use this branch before recommending power upgrades.

1. If purist: no engine swaps unless the user relaxes the rule.
2. If technical road/touge/circuit: prefer stock engines or lightweight swaps with useful high-rpm power bands. Avoid heavy swaps unless straight-line gain clearly beats handling loss.
3. If sprint/speed: heavier power swaps can be acceptable because power is prioritized over handling.
4. If target class demands more power than stock can provide: compare aspiration and engine swaps for PI efficiency and power band.
5. Treat intercooler and heavy power adders cautiously because added weight can shift distribution; use them late when extra power is truly needed.

## Drivetrain Swap Decision

- RWD remains competitive through high classes and often keeps rotation/top-end efficiency.
- AWD helps launches, high-power exits, and off-road consistency, but can add weight and power-on understeer.
- FWD can be strong but is front-tire limited; front tire width, front diff, and gearing matter.
- Off-road and cross country usually favor AWD.
- Do not swap drivetrain for purist builds unless explicitly allowed.

## Differential Type Decision

- Install an adjustable diff when possible; it is a core control unlock.
- FH6 all-round native AWD can use race diff when it feels consistent. AWD swaps may prefer drift diff when the car needs more rearward center-bias behavior or sharper rotation.
- Rally diff is often the stability/smoother-transition choice for RWD or road cars that snap from grip to oversteer. Off-road diff can help FWD or loose-surface builds reduce power-on understeer.
- If the same numeric diff settings feel wrong, try a different adjustable diff type before chasing extreme sliders; diff types can have hidden lock speed/preload behavior.
- FH5 purist guidance cycles drift diff for more rotation and rally diff for more stability/road usability. Treat as lower-priority in FH6 but useful when the same behavior is desired.

## Suspension Type Decision

- Race suspension: use for smoother road builds, high-speed aero support, and naturally grippy handling cars that benefit from full alignment/ride-height/damping control.
- Off-road/rally suspension: use when the car is too stiff, needs ride height, needs travel, or must handle dirt/cross country. FH6 full guide notes off-road springs can be PI-efficient and softer.
- Stock suspension: keep it when factory behavior is valuable, such as four-wheel steering, good stock alignment, a special stock handling model, or a purist/PI-tight build where race suspension makes the car push.
- Sport/drift suspension: avoid as a default for performance builds unless a specific drift angle/steering behavior is requested.
- ARBs are near-mandatory control unlocks because they cost little PI and enable balance tuning.
