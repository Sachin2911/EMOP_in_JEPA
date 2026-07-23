# Agent notes

## Compress paper PDFs before committing

Papers under `docs/papers/` often ship with high-resolution embedded figures and can be tens of megabytes each. After adding or replacing any PDF in that tree, compress it with Ghostscript `/ebook` (downsamples images ~150 DPI; does **not** remove images or text).

```bash
# Compress one paper in place (only replace if smaller)
in="docs/papers/.../Paper.pdf"
tmp="${in}.tmp.pdf"
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
  -dNOPAUSE -dQUIET -dBATCH \
  -sOutputFile="$tmp" "$in"
# if tmp is smaller than in: mv "$tmp" "$in"; else rm "$tmp"
```

Batch all papers:

```bash
find docs/papers -name '*.pdf' -print0 | while IFS= read -r -d '' f; do
  tmp="${f}.tmp.pdf"
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
    -dNOPAUSE -dQUIET -dBATCH -sOutputFile="$tmp" "$f"
  if [ -s "$tmp" ] && [ "$(stat -c%s "$tmp")" -lt "$(stat -c%s "$f")" ]; then
    mv "$tmp" "$f"
  else
    rm -f "$tmp"
  fi
done
```

Quality presets if `/ebook` figures look too soft: `/printer` (~300 DPI, larger) or `/screen` (~72 DPI, smaller). Prefer `/ebook` by default.
