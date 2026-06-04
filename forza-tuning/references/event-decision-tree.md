# Event Decision Tree

Use this after car archetype and before setup symptoms. Event type decides which compromises are acceptable.

## Event Matrix

| Event | Build priority | Setup priority | Avoid |
|---|---|---|---|
| Road/circuit | Tires, brakes, weight, balanced aero, diff, gearing | Phase balance: entry/mid/exit | Power-only builds that cannot brake or rotate |
| Sprint/speed road | Power, lower drag, enough brakes, final drive | Stability at speed and long-straight gearing | Max downforce if it kills trap speed |
| Touge/technical | Front tire width, brakes, weight, response, hairpin gearing | Entry rotation, front bite, clean exits | Heavy swaps and unstable rear rotation downhill |
| Drag | Power, drag tires, launch, first/second gear, tire heat | Squat, diff, shift timing, trap speed | Road-race suspension/aero assumptions |
| Dirt/rally | Surface tire, AWD, travel, compliance, gearing | Predictable slides and bump absorption | Low/stiff road stance |
| Cross country | Survival, ride height, landing stability, AWD, robust gearing | Landings, rough sections, water/bumps | Delicate low road builds |
| Drift | Rotation, throttle control, drift tire/suspension if desired | Angle, transition, controllable wheelspin | Grip-race stability advice unless requested |
| Purist/showcase | Preserve identity and restrictions | Make original drivetrain work | Engine/drivetrain/Forza aero unless allowed |

## Target Environment Test

This section is paramount Horizon Guru process guidance and should be emphasized in almost every tune response.

- Test in an environment that matches the intended event. Circuit tunes should be judged where trail braking and repeated direction changes matter; street/sprint tunes should be judged where stability, braking from speed, and surprise corners matter.
- Prefer Rivals or repeatable solo passes when comparing setup changes, especially for drag and tire-temperature-sensitive tests. Avoid judging a tune from one open-world pass with different weather, season, traffic, or launch conditions.
- Road circuits generally reward maneuverability and brake/turn overlap. Street races and speed-biased sprints reward stability, top-end, and a milder alignment because abrupt high-speed corners punish edgy cars.

## Road Or Circuit

- Build for the whole lap, not top speed. Tire compound/front tire width, brakes, weight reduction, ARBs, differential, and balanced aero are usually higher priority than raw power.
- Time attack and circuit rivals can justify high downforce. Gear for the longest straight without bouncing limiter early.
- If braking/cornering sectors lose more than straights gain, move PI back into grip/brakes/weight.

## Sprint Or Speed-Biased Road

- Lower total aero and add power when the route has long straights and fewer hard braking zones.
- Heavy engine swaps are more acceptable here than on technical layouts.
- Keep enough braking and front tire to survive major corners; do not turn the car into a drag tune unless the route is nearly straight.

## Touge Or Tight Technical

- Favor cars that rotate, brake, and change direction. Weight reduction, front tire width, brakes, and usable gearing beat peak horsepower.
- Downhill or bumpy touge punishes unstable brake bias, too-low decel, and stiff rear setups.
- Use shorter usable gearing only if it improves hairpin exit without wheelspin.

## Drag

- Standardize launch first: same tire heat, same launch method, same shift mode, same assists, same start surface, and same weather/season when possible. Rivals/drag meetup conditions beat open-world guessing.
- Make multiple attempts and compare launch quality, shift timing, trap speed, limiter hits, and tire heat before declaring a gearing or diff change faster.
- Tune first gear for clean release, then second gear so it neither bogs nor instantly hits limiter. If first is only a launch gear, tune second as the first real acceleration gear.
- If spinning, lengthen early gears or adjust tire pressure/squat before removing all diff lock. If bogging, shorten launch gearing or use a launch method that reaches the power band sooner.
- E-brake plus throttle, brake plus throttle, launch control, manual, manual with clutch, automatic, and traction control can each be faster on different cars. Test the launch method instead of assuming one rule.
- Slight wheelie/squat can be acceptable if it lands straight and improves 60-foot/quarter time; reduce it if it delays acceleration, wanders, or forces a lift.
- Exact drag ratios from one car are examples, not global defaults.

## Dirt Or Rally

- Pick surface tire first. Off-road race tires are usually dominant for rally/off-road events.
- Prefer AWD or balanced power delivery when exits are loose.
- Use rally/off-road suspension for travel and compliance; raise ride height enough to stop bottoming.
- Damping should absorb bumps without pogoing. Stable slides are more valuable than sharp road response.

## Cross Country

- Build for landings, impacts, and terrain speed. High ride height, travel, soft bump, controlled rebound, and AWD stability matter.
- Trucks/SUVs/heavy cars need brakes, weight control, and robust gearing before extra power.
- A tune that is fast on smooth road can be useless if it bottoms, flips, or loses throttle over rough terrain.

## Purist

- Preserve stated restrictions. The FH5 purist definition used here is no engine swaps, no drivetrain swaps, and no Forza aero.
- Use tires, weight reduction, ARBs, diff choice, tire width, suspension choice, gearing, and sometimes chassis reinforcement/roll cage to preserve identity while improving pace.
- Treat front tire width and roll cage as substitutes for front aero only when the car lacks rotation/high-speed grip and PI allows them; do not add them automatically.
- Keep stock suspension when it preserves useful factory behavior or makes a front-limited car rotate better than race suspension.
- Tell the user when a restriction blocks the fastest path and give the best within-rules alternative.
