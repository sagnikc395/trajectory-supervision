# Workshop Submission Package

Anonymized manuscript source and compiled PDF for the Meta-Agents Workshop
(NeurIPS 2026 Workshop: Managing Agents that Manage Agents).

## Files

- `main.tex`: anonymous full-paper manuscript.
- `main.pdf`: compiled seven-page PDF (main text ends on page 6; references and appendix follow).
- `iclr2027_conference.sty`, `iclr2027_conference.bst`, `natbib.sty`, `fancyhdr.sty`:
  official ICLR 2027 style files, unmodified, from
  <https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip>.
- `figures/`: figures referenced by the manuscript, copied locally so this directory compiles standalone.
- `../final/05_meta_controller.ipynb`: controller-driven A/B policy-selection experiment.

## Compile

From this directory:

```bash
tectonic -X compile main.tex
```

## Template

The workshop permits either the NeurIPS 2026 or the ICLR 2027 LaTeX template. This
manuscript uses the official ICLR 2027 template. The NeurIPS 2026 style file is
distributed only through Overleaf and has no public direct download, so the ICLR
2027 files were used to keep the build reproducible from this checkout.

`\iclrfinalcopy` is left commented out, which is what keeps the submission
anonymous; do not uncomment it before the camera-ready stage.

## Rule compliance

Audited against <https://meta-agents-workshop.github.io/>. All 16 checks pass.

| Rule | Status |
|---|---|
| Template: NeurIPS 2026 or ICLR 2027 | Official ICLR 2027, `.sty` vendored unmodified |
| Full Paper: at most 9 pages main text | Main text ends p8; 10 pages total |
| References/appendix excluded, after main text | Bibliography then appendix, both after Conclusion |
| Main text self-contained | No result or method deferred to the appendix |
| Double-blind | No names, affiliations, emails or acknowledgments in text or metadata |
| `\iclrfinalcopy` not invoked | Present only in comments; header reads "Under review" |
| Responsible-use statement | Section 8. Absence is grounds for desk rejection |
| Single PDF, English, US Letter | 612 x 792 pts, uniform across pages |
| Fonts embedded | All subsets embedded |
| No text outside margins | 0 overfull boxes |
| Citations and refs resolve | 28 cited = 28 bibitems, no orphans |
| Every float referenced | 7 tables/figures, all cross-referenced |
| Abstract single paragraph | 1 paragraph, 168 words |
| Non-archival, not previously published | Course project |

The NeurIPS 2026 style file is distributed only through Overleaf and has no public
direct download, which is why the ICLR 2027 template was used. The call for papers
permits either.

## Still to be done by a human

- Upload `main.pdf` to OpenReview:
  <https://openreview.net/group?id=NeurIPS.cc/2026/Workshop/Meta-Agents>
  Deadline: September 5, 2026 AoE.
- Add all authors to the OpenReview submission form and verify their profiles.
- Select the Full Paper track.

## Results status

The controller run is in `artifacts/meta_controller_seed42/` and the paper reports it.
Two things about it constrain what the paper can claim, and both are stated in the text:

- **The selection loop was degenerate.** The controller chose policy B at all four
  stages (margins 0.078-0.135), so on this stream it is behaviourally a fixed-B policy.
  The paper reports this as the run's primary empirical finding rather than framing the
  mechanism as adaptive.
- **Only the canonical stream order completed.** `reverse_heldout` and `rotate_heldout`
  were not run. The paper draws no stream-order conclusions and lists this under
  Limitations. Running them takes roughly 1.5 GPU-hours; the notebook resumes from the
  completed canonical run, so only the two missing orders would be trained.

Every figure in the paper was checked against the JSON in `artifacts/`.

## Evidence covered

The manuscript reports the recorded seed-42 A/B runs, full held-out generation results,
sampled continual-learning metrics, final error categories, hardware/run limitations,
and the repository's reproducibility workflow. The controller protocol adds disjoint
fit/validation/test API-family partitions, token-matched candidate training, adaptive
policy selection after every stage, and held-out stream-order evaluation. Large adapter
bundles remain outside git as documented by the project artifact manifest.
