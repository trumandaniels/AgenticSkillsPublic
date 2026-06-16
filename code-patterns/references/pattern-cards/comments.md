# Comment Pattern Cards

Source base: `book1` (*Code Simplicity*), especially `book1:chapter-7-simplicity`.

## Card: comment-why-not-what

```yaml
id: comment-why-not-what
name: Use comments for rationale, not for restating unclear code
category: comments
use_when:
  - a comment explains what code does line by line
  - code needs a comment because it is hard to understand
  - a future maintainer needs to know why a surprising choice exists
avoid_when:
  - removing the comment would erase important rationale or constraints
  - code cannot be made clearer safely in the current scope
required_context:
  - comment text
  - surrounding code clarity
  - hidden constraints, compatibility reasons, or historical decisions
  - tests or validation for any code rewrite
move: Make the code simpler when the comment explains what; keep or rewrite the comment when it explains why.
recipe:
  - classify the comment as what, why, constraint, or stale history
  - replace what-comments with clearer names or structure when safe
  - preserve rationale comments that protect non-obvious decisions
  - delete stale comments after confirming the code no longer needs them
tradeoffs:
  - fewer comments can improve readability when code carries the meaning
  - too few rationale comments can make maintainers remove important behavior
source_anchors:
  - book1:chapter-7-simplicity
  - book1:appendix-laws
conflicts:
  - remove-comments-vs-keep-rationale
validation:
  - the remaining code/comment pair explains intent without duplicating obvious behavior
  - no hidden rationale was lost
```
