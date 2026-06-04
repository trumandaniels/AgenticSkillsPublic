# Setup Diagnosis

Use this after build and event fit are plausible. Diagnose by phase, then choose the smallest coherent set of changes.

## Setup Priority Map

Use this when the user asks for a complete tune, priority order, or whether a setting matters. Include all relevant families, but change only the highest-priority controls that match the symptom. Use these labels exactly: **Top**, **High**, **Medium High**, **Medium**, **Medium Low**, **Low**, **Very Low**.

| Typical priority | Tune family | Use first for | Move later when |
|---|---|---|---|
| Top/High | Build/unlocks | Tires, ARBs, diff, brakes, suspension type, aero availability, weight, drivetrain fit | The build already supports the event and class |
| High | Tire compound and width | Grip ceiling, heat window, braking, traction, front/rear grip balance | The compound/width already fit the class and event |
| High | Tire pressure | Global grip, heat, sluggishness, nervousness | Pressure is in a sane range and symptoms are phase-specific |
| High/Medium High | Alignment/camber/caster | Turn-in, braking contact, steady-state grip, stability | Tire temps/contact are acceptable or the issue is clearly diff/gearing |
| High/Medium High | ARBs | Entry/mid balance, rotation, platform response | The problem is bumps, braking, power delivery, or high-speed aero |
| High/Medium High | Brakes | Heavy braking distance, entry push/rotation, trail-brake feel | The car already stops cleanly and the issue appears off-brake |
| High/Medium High | Differential | Entry stability/rotation and throttle-on exit behavior | The symptom is not tied to lift/brake/throttle phase |
| High/Medium High | Gearing | Limiter, bogging, exit traction, wrong power band | Speed and shift points already match the route |
| Medium High/Medium | Aero | High-speed rotation/stability and braking confidence | The event is low speed or aero drag costs more than stability gains |
| Medium High/Medium | Springs/ride height | Bottoming, platform support, roll timing, response, aero platform | ARB/diff/alignment can fix balance without hurting compliance |
| Medium/Medium Low | Damping | Bounce, curb recovery, harshness, weight-transfer timing | The car is stable over bumps and only needs balance trim |
| Low | Toe | Last-mile turn-in or stability trim | Earlier controls have not established baseline balance |
| Low/Very Low | Brake pressure | Pedal/controller feel and lockup management | Bias or braking hardware is the real issue |

Priority does not mean importance. Springs and damping can be decisive, but for road race balance they are usually second-layer controls unless the car bottoms, hops, floats, or cannot keep tire contact.

### Tire And Upgrade Dependency Rules

Tire choice is both a build decision and a tuning baseline. Do not give tire pressures as universal values without naming the tire family or saying they must be retested.

- **Compound changes**: Retune pressure first, then camber, ARB balance, springs/damping, and braking feel. Softer/grippier compounds often tolerate different pressure and camber than stock/street tires; rally/drift/semi/slick tires should not inherit one pressure target blindly.
- **Width changes**: Retune front/rear pressure split and ARB balance. More front tire width can reduce entry/mid push and may allow less aggressive rear rotation; more rear tire width can require more rotation from ARB/diff/gearing.
- **Different tire heat windows**: If telemetry or feel shows overheating, pressure and camber move before spring/damper guesses. If tires are cold and lazy, raise pressure or reduce excessive grip/drag before adding power.
- **Suspension/aero/weight changes**: Recheck pressure and camber after major build changes because load transfer and contact patch behavior changed.

### Complete Layout Status Rules

When listing every potential change, use one status plus one priority per row. Use `Buy` for upgrade purchases, `Change` for tuning sliders to move now, `Baseline` for settings to set/check but not chase yet, and `Skip` for low-value or wrong-event items. Keep active changes small, but do not hide skipped or baseline families when the user asked for a complete layout.

| Status | Meaning | Example |
|---|---|---|
| Buy | Spend PI or unlock a part now | Front tire width, ARBs, diff, brakes |
| Change | Move a tuning slider in the next test | Brake bias 1 click rearward, lower rear diff accel 5 |
| Baseline | Set/check a sane starting point before judging symptoms | Pressure by compound, final drive, aero balance |
| Skip | Avoid unless rules, PI, or event changes | Heavy engine swap in tight road A-class |

## Paramount Horizon Process Rules

These rules come from the FH6 Basic Refresher and Horizon Guru guides and should shape default Horizon road/circuit/sprint/touge tuning.

- Test where the car will race. Circuit, street, sprint, touge, wet, and mixed-surface conditions ask different things from the same car.
- Establish the build before chasing sliders: tire family, front tire width/rear tire width, brakes, ARBs, diff, suspension type, weight, aero, power, and transmission can change every tuning baseline.
- Keep an evidence trail. Change one major variable at a time unless applying a known package, then retest the same segment with the same braking point, steering input, throttle timing, and shift plan.
- Use telemetry when available, especially tire heat/contact, suspension travel, speed at straight end, RPM after shifts, and tire smoke/temperature evidence for diff/gearing/pressure decisions.
- Favor consistency before peak aggression. A tune that gains one corner but becomes unpredictable over bumps, braking, or power delivery is not done.
- When FH6-specific behavior conflicts with older Horizon process advice, keep the Guru test method but use the FH6 Basic Refresher for the actual tire/brake/aero/mechanical-balance direction.

## Baselines And Knob Rules

- **Pressure**: Lower pressure adds grip but can feel slower, less responsive, and hotter. Higher pressure sharpens response and speed but loses grip if too high. FH6 low-spec compounds and rally often start around 26-28 PSI; very light rally-tire examples may live around 21-26 PSI; semi/slick/drift often around 32 PSI; AWD road race can start near 28 front and 27-28 rear. Weight, downforce, compound, tire width, and heat all affect the final number. Adjust about 0.5 PSI at a time and verify with telemetry or repeatable feel.
- **Camber**: FH6 often wants less camber than defaults. General race baselines can start around -1.5 to -2.0 front and -1.0 to -1.5 rear for approachable builds, or closer to -0.7/-0.4 for some optimized all-round grip builds. RWD often likes more front than rear; FWD can like more rear; AWD tends balanced. Too much camber hurts braking/accel; too little can roll onto the outside and understeer.
- **Telemetry alignment check**: For detailed tuning, use tire heat/contact telemetry under hard cornering. Rear camber is simpler: if the outside heats faster than the inside, add negative camber; if the inside is much hotter, reduce it. Front camber/caster interact, so change one at a time.
- **Toe**: Use late and small. Front toe-out adds entry response; rear toe-in adds power-on stability; rear toe-out is rare and mostly a FWD rotation tool. 0.1-0.2 is meaningful; avoid more than about 0.3 unless solving an extreme case.
- **Caster**: Higher values, often 5.5-7, improve stability and dynamic camber when they feel good. Do not blindly max caster if telemetry or feel shows mid-corner unpredictability from too much dynamic camber.
- **ARB**: Softer end gains grip; stiffer end responds faster and can lose grip. In FH6, ARB balance can target mechanical balance around 0.55-0.65 when that stat is available. If a big ARB change fixes balance but hurts stability, compensate lightly with springs/damping in the opposite direction.
- **Springs/ride height**: FH6 AWD/grip builds can be fast with soft springs. Stiffen only enough for response, aero platform, and bottoming control. Treat springs as P2 for normal road balance, but move them to P1 when the car bottoms, rolls too slowly to take a set, hops over curbs, feels floaty, or needs aero platform support. Keep springs broadly related to weight distribution unless a symptom requires a balance change.
- **Damping**: Rebound controls extension; bump controls compression. Rebound usually stays much higher than bump. Approachable FH6 AWD race baselines can start near 18/18 rebound and 6/6 bump; softer-spring meta setups often live around 12-20 rebound and 5-7 bump. Bouncy means more rebound; harsh/twitchy/skipping means less rebound or bump. Use damping to control motion after springs/ride height are plausible.
- **Aero**: More front adds rotation; more rear adds stability. FH6 often likes balanced aero more than old max-front/min-rear habits. If aero balance stat exists, around 0.40-0.45 is a useful starting region. Set overall downforce for event speed first, then trim front/rear balance. Circuit/time attack can run high downforce; sprint/speed routes usually need less drag. Motorsport can often run max front/rear or max front with trimmed rear, but low-power classes may lose too much speed.
- **Brakes**: FH6 slider text is fixed: toward front means more front brake. Front bias stabilizes and can understeer; rear bias rotates and can destabilize. Move bias sparingly because small changes matter; 48-49% can be a conservative rearward-rotation start on some FH6 race builds, while 50% or more frontward is safer. Pressure near 100 is usually fine unless the driver can use sharper brakes. In Motorsport, a straight-line lockup/brake-distance test can tune balance and pressure, but do not import Motorsport pressure habits blindly into Horizon.
- **Diff**: More accel lock improves two-wheel drive until it causes power under/oversteer. Less accel can rotate but may single-tire fire; visible inside-tire smoke/heat means accel is too open. More decel stabilizes entry; less decel rotates but can be nervous or cause lift-off oversteer. Motorsport guidance often pushes high accel and low decel; FH6 road baselines are more conservative unless evidence supports extremes.
- **Gearing**: Final drive should approach useful top speed near the end of the longest straight without hitting limiter early. Keep the car in the useful power band and avoid bogging through corner exits. Lengthen lower gears for traction-limited RWD/AWD; shorten launch gear only when the car bogs, and remember an extremely short first gear may make second gear the real slow-corner gear.

### Test Discipline

- Change one major variable at a time unless you are deliberately applying a known package. If you change ARB, springs, and damping together, you lose the evidence trail.
- For road/circuit, use one repeatable corner or sector with the same braking point and throttle timing. For drag, use repeatable conditions, tire heat, launch method, shift mode, and at least 3 passes.
- Bring back observations in phase language: entry, mid, exit, straight, launch, shift, bump/landing, tire heat.

### Gearing Workflow

1. Set the launch/first gear. It should release without bogging or uncontrolled spin; AWD low-power cars may need a short first, while high-power RWD may need a longer first.
2. Set the final/top gear for the event. For a single track, aim near peak useful power at the end of the longest straight. For a shared/general tune, leave 10-20 mph beyond the observed max speed or enough room for slipstream.
3. Fill the middle gears around slow-corner exits and the power band. If first is launch-only, make second the slow-corner gear.
4. Check shift timing. Hitting limiter before the shift or crossing the line in the wrong gear is evidence to adjust individual ratios, not only final drive.

### Brake Test Workflow

- Motorsport: disable ABS for the test if needed, run a long straight, apply 100% brake, and watch tire lockup. If fronts lock far before rears, move bias rearward; if rears lock first, move bias forward. Target fronts locking just before rears, then confirm the car still trail-brakes safely.
- Horizon: use the same logic only as a caveat. Start near 100 pressure and small bias moves, then judge entry push/rotation and stopping consistency.
- If brake hardware changes, retune bias/pressure before diagnosing entry balance elsewhere.

### Motorsport-Specific Meta Caveat

- Motorsport open-class guidance can include extreme bump, anti-dive, roll-center, brake-pressure, and tire choices that exploit Motorsport physics and geometry sliders. Use only when the user explicitly asks for Forza Motorsport/open-class/meta tuning.
- High bump/anti-dive setups can be fast but punishing: FWD tends to punish mistakes with severe understeer, RWD with abrupt traction loss. Offer mid-aggression alternatives when the user wants consistency.
- Horizon does not expose the same geometry controls, so translate only the general lesson: more platform support can carry speed, but extreme support raises the penalty for curb/grass/bump mistakes.

## Phase Diagnosis

### Entry understeer

- **Evidence**: Front washes before apex; more steering does not rotate; braking while turning worsens push.
- **Likely causes**: Front overload, too much front brake, decel too locked, front too stiff, rear too planted, insufficient front tire width/brakes in FH6.
- **Safe order**: Confirm build grip; move brake slightly rearward if stable; lower decel 3-8 but avoid unstable floor; soften front ARB or stiffen rear; adjust camber/aero.
- **Do not**: Move brake rearward or lower decel if the rear already steps out.

### Entry oversteer

- **Evidence**: Rear rotates on braking/lift before apex.
- **Likely causes**: Brake too rearward, rear too stiff, decel too open, rear contact poor, too much front bite.
- **Safe order**: Move brake forward; raise decel 3-8; soften rear ARB/spring/damping; add rear aero for high speed.

### Mid-corner understeer

- **Evidence**: Stable push at maintenance throttle; front heat; lift helps rotate.
- **Likely causes**: Front steady-state grip shortage, rear too planted, aero/mechanical balance rear-biased.
- **Safe order**: Adjust ARB balance; target useful mechanical balance if available; add front aero only for high speed; fix pressure/camber; add front tire width if build-limited.

### Mid-corner oversteer

- **Evidence**: Rear slides at apex without throttle being the trigger.
- **Likely causes**: Rear roll/spring too stiff, poor rear contact, front too sharp, not enough rear aero.
- **Safe order**: Soften rear ARB; compensate springs if needed; add rear aero for high speed; fix rear pressure/camber.

### Exit understeer

- **Evidence**: Car reaches apex then pushes wide on throttle, especially FWD/AWD.
- **Likely causes**: Front accel too locked, AWD front torque too high, low gears too short, front overloaded.
- **Safe order**: Lower front accel 5-10 if above useful range; shift AWD center rearward carefully; lengthen early gears; improve pre-apex rotation.
- **FH6 note**: Front/AWD accel above about 95 can restrict turn-in.

### Exit oversteer

- **Evidence**: Rear breaks loose on throttle; short-shifting helps.
- **Likely causes**: Rear accel too locked, low gears too short, rear too stiff, insufficient rear tire/aero.
- **Safe order**: Lower rear accel 5-10; lengthen offending gears; soften rear ARB/spring/damping; add rear aero if high speed.

### Bumps, curbs, landings

- **Evidence**: Problem tracks surface changes, jumps, curbs, or bottoming.
- **Likely causes**: Too low, too stiff, bump too high, rebound too high/low for recovery.
- **Safe order**: Raise ride height; soften bump; soften springs if widespread; control rebound so it settles without pogo.

### Weak race gearing

- **Evidence**: Limiter early, bog after shifts, poor exit despite grip, wrong rpm at straight end, low-power AWD launch bog.
- **Safe order**: Final drive first; individual gears only if needed; lengthen early gears for traction; shorten launch gear only if it bogs; keep engine in useful power band. If first becomes launch-only, tune second as the slow-corner gear.

### Drag launch

- **Evidence**: Tire heat changes launch; first/second gear make or break the pass; wheelie/squat changes 60-foot and straightness; shift timing affects trap speed and elapsed time.
- **Safe order**: Standardize tire heat and launch method; run 3 passes; tune first; tune second; adjust final drive/top gear; tune pressure/squat/wheelie; chase trap speed last.
- **Method branch**: Test e-brake plus throttle, brake plus throttle, launch control/no launch control, manual/manual with clutch/automatic, and traction control when the car is inconsistent. Pick the method by elapsed time and repeatability, not ideology.

## Drivetrain Diff Baselines

- **FH6 AWD/FWD**: Keep accel high but watch for turn-in restriction above about 95; keep decel low but avoid below 5-10 if unstable.
- **FH6 RWD**: Start around 50-60 accel and 10-20 decel; raise accel only if throttle management and tires can handle it.
- **FH6 AWD center**: Do not go below 50. Road cars often live around 60-90 rearward; off-road is usually more balanced. Higher rear bias rotates more; lower/rebalanced center diff calms oversteer.
- **Motorsport caveat**: Motorsport guides often push accel as high as possible and decel as low as possible, and brake tuning can use measured stopping-distance/lockup passes. Use those mainly for Motorsport or when Horizon evidence supports the same behavior.
