# Third-Party Notices

This directory contains code adapted from open-source projects. Their licenses are reproduced below.

---

## last30days-skill

The files `dates.py` (verbatim) and `signals.py` + `dedupe.py` (adapted) are derived from [last30days-skill](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn.

**Original repository:** https://github.com/mvanhorn/last30days-skill
**Vendored on:** 2026-04-28
**Original commit:** depth=1 clone of `main` branch on the vendor date

### License (MIT)

```
MIT License

Copyright (c) 2026 Matt Van Horn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Modifications made

- `dates.py` — verbatim copy.
- `signals.py` — replaced upstream `schema.SourceItem` with a local `story.Story` dataclass; removed text-overlap relevance scoring (not needed because ad-platform queries are pre-filtered by source/keyword upstream); added an `official_changelog` source class with a 2x quality boost since vendor changelogs are ground truth.
- `dedupe.py` — replaced `schema.SourceItem` with `story.Story`; kept hybrid trigram + token Jaccard at 0.7 threshold.
