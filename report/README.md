# Apart Research hackathon report (LaTeX)

LaTeX version of the Apart Research hackathon report template. It reproduces the
look of the official Google Docs template (Old Standard TT, US Letter, 1-inch
margins, 1.15 line spacing, the yellow guidance box). Compile with **pdfLaTeX**
(the Overleaf default). On Overleaf: Menu > Compiler > pdfLaTeX, main document `main.tex`.

## Layout

| Path | What it is |
|---|---|
| `main.tex` | Title block, authors, abstract wrapper, and the list of sections |
| `apartreport.sty` | All formatting. You should not need to edit it |
| `sections/*.tex` | One file per section. Write your report here |
| `figures/` | Images. `\includegraphics{name}` looks in this folder |
| `tables/*.tex` | One file per table. `\input{tables/name}` where it belongs |
| `references.bib` | Bibliography. Cite with `\cite{key}` |

## Writing the report

- The italic text in each section is the template's guidance. Replace it with your
  own content (upright, i.e. without `\textit{}`).
- Before submitting, delete the line `\input{sections/info_box}` in `main.tex`.
- Paragraphs are separated with `\blankline`, which inserts one empty line as in the
  Google Doc. A plain blank line in the source starts a new paragraph with no gap.
- Numbered lists: `enumerate`. Dash bullets: `itemize`. "(a) (b)" lists: `alphlist`.
- Figures: put the file in `figures/`, then use the commented example at the end of
  `sections/4_results.tex`. Tables: copy `tables/example_table.tex`.
- References: add entries to `references.bib` and `\cite{}` them. Remove `\nocite{*}`
  from `sections/references.tex` once you have real citations, otherwise every entry
  in the .bib file is listed.
