# Motion Reference Catalog

Use this catalog to gather concrete movement evidence before generating in-between frames. Prefer direct observation of frame sequences over generic animation adjectives.

For a searchable table of specific online references by animal type, pose/action, source, media type, rights note, and animation use, read `motion-reference-index.md` or filter `motion-reference-index.csv`.

## Source Priority

1. User-supplied keyframes, footage, model sheets, storyboards, or sprite frames.
2. Public-domain chronophotography and motion-study plates.
3. Open motion-capture libraries or official tool previews used only as pose/motion reference.
4. Newly created quick reference: pose sketches, stick-figure thumbnails, 3D mannequins, or simple filmed reference by the user.
5. Copyrighted film/game/anime footage only as high-level inspiration unless the user owns/provides rights.

## Public-Domain Chronophotography

- Library of Congress, Eadweard Muybridge `Animal locomotion`: https://www.loc.gov/item/97503994/
- Library of Congress Prints and Photographs records for Muybridge plates: https://www.loc.gov/pictures/search/?q=Muybridge%20Animal%20Locomotion
- University of Pennsylvania Archives, Muybridge collection context and selected items: https://archives.upenn.edu/digitized-resources/docs-pubs/muybridge/
- Biodiversity Heritage Library, `Animals in motion`: https://www.biodiversitylibrary.org/item/265827
- Smithsonian examples, including `Animal Locomotion. Plate 66.; Male, Running`: https://www.si.edu/object/animal-locomotion-plate-66-male-running%3Anmah_1885830
- Art Institute of Chicago, public-domain Muybridge plates: https://www.artic.edu/search/artworks?q=Muybridge%20Animal%20Locomotion
- Wikimedia Commons search for Muybridge public-domain plates: https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=Animal%20locomotion%20Muybridge
- Internet Archive scans of Muybridge books and plate compilations: https://archive.org/search?query=Muybridge%20Animal%20Locomotion

Look for sequences with multiple camera angles when the prompt needs rotation, gait, or weight transfer.

## Motion Capture And 3D Pose Sources

- Carnegie Mellon University Motion Capture Database: https://mocap.cs.cmu.edu/
  - Useful categories: locomotion, sports, dance, playground, interaction with environment, pantomime, everyday behavior.
  - Treat mocap as pose/timing evidence; convert mentally into clear silhouettes before prompting the image generator.
- Adobe Mixamo official help: https://helpx.adobe.com/creative-cloud/help/animate-characters-mixamo.html
  - Useful for previewing human actions, loops, and root motion. Check usage rights before using exported assets in deliverables.

## Animation Principle References

- Microsoft animation principles overview: https://learn.microsoft.com/windows/win32/lwef/animation-principles
- SIGGRAPH education notes on slow-in/slow-out: https://education.siggraph.org/static/Drupal_2025/education.siggraph.org/static/HyperGraph/animation/character_animation/principles/slow_in_and_out.html

Use these for timing, spacing, arcs, anticipation, follow-through, and slow-in/slow-out vocabulary.

## Movement Categories To Search

Human locomotion:
- walk cycle, run cycle, sprint start, jog, limp, sneak, stair climb, stumble, fall, get up, crawl, kneel, sit, stand, turn, pivot, jump, leap, landing, roll, cartwheel.

Hands and props:
- throw, catch, swing bat, swing sword, punch, kick, push, pull, lift, drag, open door, pick up object, pour, write, point, wave, clap.

Performance:
- head turn, blink, smile, frown, gasp, laugh, shout, whisper, lip sync, shoulder shrug, recoil, anticipation, double take.

Animals:
- horse walk/trot/canter/gallop, dog walk/run/jump, cat leap, bird wing flap, bird takeoff/landing, quadruped turn, tail follow-through.

Effects:
- bouncing ball, cloth flap, cape turn, hair swing, splash, smoke puff, fire burst, dust trail, debris impact, magic arc, speed smear.

## What To Extract From References

For every reference sequence, write a 5 to 10 line motion note:

```text
Action:
Source:
Useful frames or timestamps:
Key poses:
Contact points:
Center of mass path:
Silhouette changes:
Timing accents:
Secondary motion:
Risks for AI generation:
```

## Rotoscope-To-Prompt Conversion

1. Reduce each reference frame to landmarks: head, ribcage, pelvis, shoulders, elbows, wrists, knees, ankles, contacts, prop endpoints.
2. Describe the path of the center of mass and the path of the fastest limb.
3. Identify which frame is a key, breakdown, contact, passing position, extreme, or hold.
4. Translate the frame into the target character style and proportions; do not ask the generator to copy the reference subject.
5. Keep motion facts separate from identity/style facts so consistency constraints stay clear.
