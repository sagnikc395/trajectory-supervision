# Issue #11 - Final Analysis - A vs B - Seed 42

- Status: completed
- Issue: `#11`
- Notebook: `final/03_analysis.ipynb`
- Inputs:
  - `artifacts/results_A_seed42.json`
  - `artifacts/results_B_seed42.json`
- Outputs:
  - `final/analysis_results.json`
  - `final/final_results.png`
  - `final/final_results.pdf`

Analysis summary:
- Conditions analyzed: `A`, `B`
- Primary metric: exact full-call accuracy
- `A` average accuracy: `0.359375`
- `B` average accuracy: `0.5703125`
- `A` total train tokens: `1857169`
- `B` total train tokens: `2324314`

Artifact checksums:
- `artifacts/results_A_seed42.json`: `56c7b8ec8e202b5147f71d5d16138a2aa0158fdc31d189e4a250441ddcee92ee`
- `artifacts/results_B_seed42.json`: `1498f032528dc2dd334806b63a4ac76dccde4107baa846fb016de046a79116b7`
- `final/analysis_results.json`: `70aa4234343720e11c64387f4a82d2df169763c9cece98bffd64c519d97f7e11`
- `final/final_results.png`: `1d622679ba85fd794f7b72fb20850c372792f5dd01229cd5c6efcb8d92f2ebcc`
- `final/final_results.pdf`: `c70aae3843047bd48439da2bf1d26919243e313aaddac2ca4cf80ac35d157e67`

Mismatch status:
- No A/B artifact mismatch found in `final/analysis_results.json`.
- Both input files use seed `42` and expose the expected 4-block metric arrays.

Notes:
- This analysis uses the corrected condition-aware B rerun from `artifacts/results_B_seed42.json`.
- The B run keeps trajectory lines in evaluation prompts, matching B training format.
