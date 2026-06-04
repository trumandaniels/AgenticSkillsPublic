#!/usr/bin/env python3
"""Create a dependency-free HTML contact sheet for reviewing animation frames."""

import argparse
import html
from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}


def iter_images(inputs: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            paths.extend(
                child
                for child in sorted(path.iterdir())
                if child.suffix.lower() in IMAGE_EXTENSIONS
            )
        elif path.suffix.lower() in IMAGE_EXTENSIONS:
            paths.append(path)
    return sorted(dict.fromkeys(paths), key=lambda p: p.name.lower())


def image_src(frame: Path, output: Path) -> str:
    try:
        rel = frame.resolve().relative_to(output.parent.resolve())
        return html.escape(rel.as_posix(), quote=True)
    except ValueError:
        return html.escape(frame.resolve().as_uri(), quote=True)


def build_sheet(frames: list[Path], output: Path, columns: int, thumb_size: int) -> None:
    if not frames:
        raise SystemExit("No image frames found.")
    if columns < 1:
        raise SystemExit("--columns must be at least 1")

    output.parent.mkdir(parents=True, exist_ok=True)
    cards = []
    for index, frame in enumerate(frames, start=1):
        label = html.escape(f"{index:03d}  {frame.name}")
        src = image_src(frame, output)
        cards.append(
            f"""    <figure class=\"frame\">
      <img src=\"{src}\" alt=\"{label}\">
      <figcaption>{label}</figcaption>
    </figure>"""
        )

    document = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Animation Contact Sheet</title>
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ margin: 24px; font: 14px/1.4 system-ui, -apple-system, Segoe UI, sans-serif; }}
    h1 {{ font-size: 18px; margin: 0 0 16px; }}
    .grid {{ display: grid; grid-template-columns: repeat({columns}, minmax(0, 1fr)); gap: 12px; }}
    .frame {{ margin: 0; border: 1px solid #bbb; padding: 8px; background: Canvas; }}
    img {{ display: block; width: 100%; max-height: {thumb_size}px; object-fit: contain; background: #fff; }}
    figcaption {{ margin-top: 6px; word-break: break-word; font-size: 12px; }}
  </style>
</head>
<body>
  <h1>Animation Contact Sheet ({len(frames)} frames)</h1>
  <main class=\"grid\">
{chr(10).join(cards)}
  </main>
</body>
</html>
"""
    output.write_text(document, encoding="utf-8")
    print(f"Wrote {output} with {len(frames)} frames")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Frame image files or directories")
    parser.add_argument("-o", "--output", default="contact-sheet.html", help="Output HTML path")
    parser.add_argument("--columns", type=int, default=6, help="Number of columns")
    parser.add_argument("--thumb-size", type=int, default=240, help="Maximum image preview height in pixels")
    args = parser.parse_args()
    build_sheet(iter_images(args.inputs), Path(args.output), args.columns, args.thumb_size)


if __name__ == "__main__":
    main()
