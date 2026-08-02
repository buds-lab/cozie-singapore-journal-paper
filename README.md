# Cozie Singapore journal manuscript

LaTeX source and publication figures for the Cozie Singapore manuscript prepared for the *International Journal of Urban Sustainable Development*.

## Repository contents

- `cozie_sg.tex` — manuscript source using the Taylor & Francis `interact` class.
- `cozie_singapore_references.bib` — project bibliography; cite entries with `\citep{key}` or `\citet{key}`.
- `figures/` — rendered manuscript figures only. See [`figures/README.md`](figures/README.md) for source and regeneration mapping.
- `interact.cls` and `*.sty` — publisher-template class and local style dependencies.

This repository does not include raw survey data, participant locations, or analysis notebooks. Figure provenance is documented in `figures/README.md`.

## Build

Compile from this directory with a TeX distribution that includes `latexmk`, `apacite`, and `natbib`:

```bash
latexmk -pdf cozie_sg.tex
```

The generated PDF is `cozie_sg.pdf`. Temporary LaTeX build products are excluded through `.gitignore`.

## Manuscript status

The source contains author-facing placeholders for manuscript text, captions, author details, and declarations. References render only when cited in the manuscript.

## Use of AI tools

AI assistance has been used to help structure and polish the manuscript and organize its LaTeX source and figure assets. The authors retain responsibility for the research, analysis, interpretation, manuscript content, and final approval.
