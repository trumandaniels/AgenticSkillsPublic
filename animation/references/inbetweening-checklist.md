# In-Betweening Consistency Checklist

Use this checklist after every generated batch and before assembling a GIF, sprite sheet, or video.

## First Pass: Frame Identity

- Same character/object identity, age, species, face, hairstyle, costume, accessories, and proportions.
- Same palette, line weight, texture, render style, grain, and level of detail.
- Same camera angle, focal length feel, background layout, lighting direction, shadow style, and horizon.
- No new props, logos, text, fingers, limbs, jewelry, costume panels, or background objects unless planned.
- No disappearing details unless hidden by pose or motion blur.

## Motion Pass

- The new frame sits between both neighbors in pose, not merely after the previous frame.
- Center of mass follows the intended path.
- Contacts are plausible: feet do not slide, hands remain attached to held objects, impacts occur on the intended frame.
- Limb arcs are continuous; elbows, knees, wrists, and ankles do not teleport.
- Silhouette remains readable and does not collapse into tangles unless a smear is intentional.
- Timing matches the chart: holds are held, impacts are sharp, slow-in/slow-out frames are clustered correctly.
- Secondary motion lags the primary action: hair, cloth, tails, straps, smoke, and props do not move in lockstep unless rigid.

## Anatomy And Volume

- Head, ribcage, pelvis, hands, and feet retain volume across the sequence.
- Foreshortened limbs still have believable joints and relative lengths.
- Weight-bearing limbs show compression or stable support.
- Facial features stay attached to the head turn and do not drift independently.
- Hands keep the intended finger count and grip shape.

## Loop Pass

- Last frame connects cleanly to first frame.
- Avoid duplicate final frame when the playback system already loops.
- Preserve root motion intentionally: choose either traveling motion or in-place loop.
- Check footfalls for sliding at the loop boundary.

## Common Fixes

- Identity drift: regenerate with the approved model sheet and nearest approved neighbor, and reduce the number of visual changes in the prompt.
- Pose pop: insert or revise a breakdown frame with explicit landmarks and center-of-mass position.
- Foot slide: restate the planted foot contact and ground location; use the contact frame as the anchor.
- Camera drift: specify fixed camera and background landmarks; regenerate from a contact sheet reference.
- Costume drift: list costume components from head to toe and mark what is hidden by pose.
- Mushy motion: use a timing chart and name the exact pose type: contact, down, passing, up, anticipation, overshoot, settle.
- Over-smoothed result: ask for a stronger silhouette, clearer line of action, or intentional smear between fast extremes.
