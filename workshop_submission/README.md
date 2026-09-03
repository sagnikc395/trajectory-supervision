# Workshop Submission Package

This directory contains the anonymized manuscript source and compiled PDF for the Meta-Agents Workshop.

## Files

- `main.tex`: anonymous full-paper manuscript.
- `main.pdf`: compiled seven-page PDF.
- `README.md`: submission and verification checklist.
- `../final/05_meta_controller.ipynb`: controller-driven A/B policy-selection experiment.

## Compile

From this directory:

```bash
tectonic -X compile --keep-logs main.tex
```

The source currently uses the repository's local NeurIPS-style file so it can be compiled reproducibly in this checkout. Before uploading to OpenReview, replace that style dependency with the current official NeurIPS 2026 or ICLR 2027 style file specified by the workshop, then compile again and confirm that the anonymous workshop option is preserved.

Run the new meta-controller experiment from a GPU runtime after running `final/01_data_prep.ipynb` with the updated raw-entry export. The controller writes `meta_controller_seed42/`, including a disjoint API-family split manifest, per-order validation decisions, selected adapter paths, and final test-family metrics. It uses validation families for all policy decisions and never reads final-test metrics until the end of each stream-order run.

## Upload checklist

- Confirm the workshop deadline in OpenReview: September 5, 2026 AoE.
- Upload `main.pdf` only after compiling with the current official workshop-compatible style file.
- Keep the paper double-blind: do not add names, affiliations, emails, acknowledgments, repository links, or identifying supplementary material.
- Include the responsible-use statement in the submitted manuscript; its absence is grounds for desk rejection according to the workshop page.
- Add all authors to OpenReview and verify their profiles before submission.
- Check that the PDF has at most nine pages of main text and that references/appendix are placed after the main text.
- Run `final/05_meta_controller.ipynb` and include its results only after verifying the split manifest and selected policies.
- Report the controller as a component-level meta-agent that selects worker training policies; do not claim that it implements unrestricted self-improvement.
- Keep the pilot A/B result separate from the controller result; the pilot is single-seed and token-confounded, while the controller notebook enables token-matched candidate training.

## Evidence covered

The manuscript reports the recorded seed-42 A/B runs, full held-out generation results, sampled continual-learning metrics, final error categories, hardware/run limitations, and the repository's reproducibility workflow. The new controller protocol adds disjoint fit/validation/test API-family partitions, token-matched candidate training, adaptive policy selection after every stage, and held-out stream-order evaluation. Controller metrics are not included until the GPU notebook run has completed and its split manifest has been checked. Large adapter bundles remain outside git as documented by the project artifact manifest.
