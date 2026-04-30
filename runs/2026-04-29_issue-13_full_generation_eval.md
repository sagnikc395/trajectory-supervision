# Issue 13 - Full Generation Eval, Seed 42

Issue: #13
Notebook: `final/04_full_generation_eval.ipynb`
Completed notebook: `runs/completed_notebooks/04_full_generation_eval_seed42_completed.ipynb`
Seed: 42
Model: `meta-llama/Llama-3.1-8B-Instruct`
Eval limit: `EVAL_MAX_SAMPLES = None`
GPU: Colab Pro G4 session; exact `nvidia-smi` output was not captured in the notebook.

## Artifact Locations

Drive folder:

```text
https://drive.google.com/drive/folders/1tsoPTxmma0zwSq6joeECTWdvIRgmKMWq?usp=sharing
```

Local download folder used for verification:

```text
/Users/vishnuvardhan/Downloads/590NN_Final_Project
```

Repo-backed support files:

- `artifacts/checkpoint_manifest_seed42.md`
- `artifacts/partial/checkpoints_A_seed42/after_D1.json` through `after_D4.json`
- `artifacts/partial/checkpoints_B_seed42/after_D1.json` through `after_D4.json`

Large files remain out of git:

- `checkpoints_A_seed42.tar.gz`
- `checkpoints_B_seed42.tar.gz`
- `full_eval_A_seed42.json`
- `full_eval_B_seed42.json`
- `full_eval_summary_seed42.json`
- `full_eval_report_metrics_seed42.json`
- `full_eval_metrics_seed42.csv`
- `full_eval_final_by_block_seed42.csv`
- `full_eval_worst_apis_seed42.csv`
- full-eval PNG/PDF plots

## Runtime

- Condition A full eval: 24.0 minutes
- Condition B full eval: 30.8 minutes
- Total measured eval time: 54.8 minutes, excluding setup/download overhead

## Final Stage Metrics

Final exact full-call accuracy by eval block:

| Condition | D1 | D2 | D3 | D4 | Mean |
|---|---:|---:|---:|---:|---:|
| A | 35.7 | 43.3 | 32.0 | 45.8 | 39.2 |
| B | 57.9 | 61.5 | 44.7 | 63.6 | 56.9 |

Final API-name accuracy by eval block:

| Condition | D1 | D2 | D3 | D4 | Mean |
|---|---:|---:|---:|---:|---:|
| A | 64.3 | 62.5 | 60.2 | 79.4 | 66.6 |
| B | 73.8 | 82.7 | 67.0 | 73.8 | 74.3 |

Comparison:

- B minus A final exact full-call mean: +17.7 points
- B minus A final API-name mean: +7.7 points
- B minus A final name-plus-any-param mean: +13.3 points

## Full Matrices

Exact full-call accuracy matrix, rows are train stage D1-D4 and columns are eval block D1-D4.

Condition A:

```text
47.6  36.5  32.0  25.2
42.1  55.8  30.1  28.0
39.7  45.2  41.7  27.1
35.7  43.3  32.0  45.8
```

Condition B:

```text
61.1  57.7  42.7  43.9
55.6  67.3  45.6  49.5
52.4  62.5  53.4  51.4
57.9  61.5  44.7  63.6
```

API-name accuracy matrix, rows are train stage D1-D4 and columns are eval block D1-D4.

Condition A:

```text
87.3  60.6  54.4  56.1
74.6  84.6  49.5  56.1
69.8  65.4  69.9  61.7
64.3  62.5  60.2  79.4
```

Condition B:

```text
72.2  84.6  66.0  75.7
71.4  84.6  67.0  73.8
70.6  82.7  67.0  72.9
73.8  82.7  67.0  73.8
```

## Final Error Category Totals

Condition A:

```text
exact_full_call: 172
correct_api_some_params: 74
correct_api_wrong_params: 47
wrong_api: 102
malformed_or_no_call: 45
```

Condition B:

```text
exact_full_call: 251
correct_api_some_params: 54
correct_api_wrong_params: 22
wrong_api: 12
malformed_or_no_call: 101
```

## Verification

- Downloaded 15 `full_eval_*` files from Drive.
- Verified completed notebook JSON parses.
- Verified all 12 code cells in the completed 04 notebook executed with no error outputs.
- Verified A/B checkpoint and result hashes match `artifacts/checkpoint_manifest_seed42.md`.
