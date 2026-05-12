# Third-Party Notices

This directory contains code adapted from open-source projects. Their licenses are reproduced below.

---

## last30days-skill

The file `dates.py` (verbatim) is derived from [last30days-skill](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn. `signals.py`, `dedupe.py`, and `story.py` were also vendored on 2026-04-28 but were never wired into the audit/update pipeline; they were removed in v2.2.0 to keep `scripts/lib/` honest. If a future feature needs deduplication or signal scoring across update sources, re-vendor from the upstream repo.

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

- `dates.py` — verbatim copy. Used by `scripts/run_update.py` for date-range helpers.
- `signals.py`, `dedupe.py`, `story.py` — vendored alongside but **removed in v2.2.0** as they were never imported. See section above.
