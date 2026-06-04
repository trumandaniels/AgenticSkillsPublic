---
name: animation
description: "Use for frame-consistent AI image animation workflows: generating in-between frames from keyframes, filling missing animation frames, planning pose-to-pose motion, using rotoscope or motion-study references, checking character/object/background consistency across frames, building sprite or contact-sheet frame sequences, and revising generated frames for timing, arcs, silhouette, anatomy, costume, lighting, and camera continuity."
---

# Animation

## Overview

Use the built-in image generator as a frame painter, not as a magic interpolator. Build a motion plan, lock visual invariants, generate small batches of in-between frames, and inspect them against the adjacent keyframes and reference motion before continuing.

## Workflow

1. Identify the frame problem.
   - Ask for or infer: start frame, end frame, target frame count, frame rate, aspect ratio, style, camera motion, and whether the output should loop.
   - If the user supplies images, treat them as keyframes or style/model references. Preserve their concrete visual facts.
   - If the user has no keyframes, create a model sheet or first key pose before generating a sequence.

2. Gather motion reference before prompting.
   - Read `references/motion-reference-catalog.md` when the action needs body mechanics, animal gait, sports motion, dance, effects motion, cloth/hair drag, or a rotoscope-like source.
   - Prefer public-domain or user-provided references. Use copyrighted footage only for high-level observation unless the user owns it or explicitly provides it for transformation.
   - Extract pose facts: line of action, contact points, weight-bearing limb, pelvis/shoulder angle, head direction, limb arcs, silhouette changes, overlap/follow-through, and timing accents.

3. Build a timing chart.
   - Mark keys, breakdowns, contacts, passing positions, extremes, anticipations, holds, and overshoots.
   - Use more frames near slow-in/slow-out poses, holds, direction changes, impacts, and expression changes.
   - Use fewer frames through fast travel, smears, or motion blur.

4. Lock invariants before image generation.
   - Character: identity, proportions, face, hair shape, costume, accessories, handedness, color palette, texture, line weight.
   - Scene: camera, lens feel, lighting direction, shadows, background layout, horizon, props, scale, render style.
   - Motion: contact feet/hands, center of mass, arcs, squash/stretch limits, secondary action lag.

5. Generate in-between frames in narrow spans.
   - Generate 1 to 3 frames at a time between two known neighbors.
   - Prompt each frame with: frame number, interpolation percentage, adjacent keyframes, pose landmarks, invariant sheet, motion reference notes, and explicit "do not change" constraints.
   - For difficult motion, generate the main breakdown first, approve/repair it, then subdivide the remaining gaps.

6. Check consistency after each batch.
   - Read `references/inbetweening-checklist.md` for the inspection pass.
   - If local frame images exist, run `scripts/contact_sheet.py` to make a review sheet.
   - Compare the new frame to both neighbors, not only the previous frame.
   - Revise frames that drift in identity, camera, anatomy, contact, lighting, silhouette, or timing before filling more gaps.

7. Package the result.
   - Return frames in numbered order and include a short timing note.
   - If asked for a GIF/video/sprite sheet, assemble only after the still frames pass consistency checks.

## Prompt Template

Use this structure for each generated frame:

```text
Create animation frame {frame_number} of {total_frames}, an in-between at {percent}% from keyframe A to keyframe B.

Preserve exactly:
- Character/model: {identity, proportions, face, hair, costume, accessories}
- Style: {medium, line, color, render, grain}
- Camera/scene: {angle, lens feel, lighting, background, props}

Pose for this frame:
- Line of action: {description}
- Center of mass: {description}
- Contacts: {feet/hands/props touching surfaces}
- Limbs: {landmarks and arcs}
- Expression/secondary motion: {face, hair, cloth, held objects}

Motion reference notes:
{rotoscope or motion-study observations}

Do not add new objects, change the costume, change the camera, change the face, skip the contact pose, or make the action arrive early.
```

## Generation Strategy

- Use pose-to-pose, not straight-ahead generation, for identity-critical characters.
- Generate the primary breakdown at 50 percent first when both keyframes are known.
- For walks and runs, key the contact, down, passing, and up poses before polishing in-betweens.
- For jumps, key anticipation, takeoff, airborne apex, landing contact, squash/recovery.
- For turns, key readable silhouettes at quarter turns; do not rely on vague "rotate slightly" prompts.
- For facial animation, separate mouth/eye/brow timing from head/body timing when consistency matters.
- For effects animation, describe physical cause: gravity, drag, turbulence, emission source, dissipation, or impact.
- For loops, compare the final frame against frame 1 before export; avoid duplicate end frames unless the target format needs them.

## Revision Tactics

- If identity drifts: regenerate from the nearest approved frame plus the model sheet; reduce pose ambition.
- If anatomy breaks: specify joint landmarks and contact points; use a simpler silhouette.
- If timing feels floaty: move contact/impact frames closer together and add holds near extremes.
- If motion pops: insert a breakdown frame or revise the silhouette arc, not just the style.
- If camera/background shifts: include the prior approved frame as the composition anchor and restate the locked camera.
- If all frames look too similar: increase spacing in the motion chart rather than asking for "more motion" generally.

## Resources

- `references/motion-reference-catalog.md`: public-domain and permissive motion reference source strategy.
- `references/motion-reference-index.md` and `references/motion-reference-index.csv`: searchable table of animal, human, effects, and principle references by subject, pose/action, source, media type, rights note, and animation use.
- `references/inbetweening-checklist.md`: frame consistency checklist and common fixes.
- `scripts/contact_sheet.py`: make a numbered HTML contact sheet from local frame images for visual review.
