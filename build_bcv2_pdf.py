#!/usr/bin/env python3
"""Render BC_v1.md to BCv2.pdf."""

from pathlib import Path

import markdown
from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "BC_v1.md"
DST = ROOT / "BCv2.pdf"

CSS_TEXT = """
@page {
  size: A4;
  margin: 16mm 14mm 18mm 14mm;
  @bottom-center {
    content: counter(page);
    font-family: "DejaVu Sans", sans-serif;
    font-size: 9pt;
    color: #666;
  }
}
html, body {
  font-family: "DejaVu Sans", "Liberation Sans", sans-serif;
  font-size: 10pt;
  line-height: 1.45;
  color: #1a1a1a;
}
h1 { font-size: 18pt; margin: 0 0 10pt; page-break-after: avoid; }
h2 { font-size: 13.5pt; margin: 16pt 0 8pt; page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: 12pt 0 6pt; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
hr { border: none; border-top: 1px solid #ccc; margin: 14pt 0; }
a { color: #1a5fb4; text-decoration: none; }
code, pre {
  font-family: "DejaVu Sans Mono", "Liberation Mono", monospace;
  font-size: 8.2pt;
}
code {
  background: #f3f3f3;
  padding: 0 3px;
  border-radius: 2px;
}
pre {
  background: #f4f4f4;
  border: 1px solid #ddd;
  padding: 8pt 10pt;
  white-space: pre-wrap;
  word-break: break-word;
  page-break-inside: avoid;
}
pre code { background: none; padding: 0; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 8pt 0 12pt;
  font-size: 9pt;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #ccc;
  padding: 4pt 6pt;
  vertical-align: top;
  text-align: left;
}
th { background: #eee; }
blockquote {
  margin: 8pt 0;
  padding: 4pt 10pt;
  border-left: 3px solid #888;
  color: #333;
}
"""


def main() -> None:
    md = SRC.read_text(encoding="utf-8")
    body = markdown.markdown(
        md,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )
    html = f"""<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>BCv2</title></head>
<body>{body}</body>
</html>"""
    HTML(string=html, base_url=str(ROOT)).write_pdf(
        DST, stylesheets=[CSS(string=CSS_TEXT)]
    )
    print(f"wrote {DST} ({DST.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
