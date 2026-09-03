# Repository Knowledge

## Project

This is the CS 590NN/690NN final-project repository for studying post-only versus trajectory supervision in continual tool-use learning. The experiments use API-Bank dialogues, split into four sequential domain blocks, and compare a stripped-context condition A with a trajectory-context condition B using Llama 3.1 8B Instruct and QLoRA.

Key locations:

- `final/01_data_prep.ipynb`: downloads/preprocesses API-Bank data and constructs the condition A/B streams.
- `final/02_train_eval.ipynb`: trains and evaluates the sequential QLoRA runs.
- `final/03_analysis.ipynb`: analyzes saved results and creates visualizations.
- `final/04_full_generation_eval.ipynb`: regenerates full held-out generation predictions from saved adapters.
- `small_experiment.ipynb`: earlier all-in-one experiment notebook; prefer the numbered final notebooks for the final workflow.
- `scripts/smoke_test.py`: checks that training and evaluation preserve or strip trajectories consistently.
- `scripts/build_final_presentation.py`: builds `final/final_presentation.pptx` from analysis figures.
- `artifacts/`: result JSONs, partial checkpoint metadata, and preprocessed data archives.
- `runs/`: Markdown run ledger and completed notebook copies.
- `CS_590NN_690NN_Final_Project_Template/`: LaTeX report/proposal source and figures.

## Commands

There is no repository-level package manifest, lockfile, Makefile, or declared test runner. Commands below are the verified workflows.

From the repository root:

```bash
python3 scripts/smoke_test.py
python3 scripts/build_final_presentation.py
```

The smoke test requires either `preprocessed_data/preprocessed.pkl` or `artifacts/preprocessed_data.zip`. It should pass before any long training run.

Run the final notebooks in order with Jupyter/Colab:

```text
final/01_data_prep.ipynb
final/02_train_eval.ipynb
final/03_analysis.ipynb
final/04_full_generation_eval.ipynb
```

Notebook cells install their own runtime dependencies. The data-prep notebook installs `transformers`, `datasets`, `huggingface_hub`, `numpy`, and `tqdm`; training installs `transformers`, `accelerate`, `peft`, `bitsandbytes`, `trl`, `huggingface_hub`, and `tqdm`; full generation additionally uses `matplotlib`. The notebooks are designed for a GPU runtime, especially an NVIDIA H100 for the documented QLoRA setup.

## Conventions And Gotchas

- The canonical pilot uses seed `42`; results and checkpoints are named accordingly. Multiple seeds are planned but are not implemented as a general workflow.
- Condition A strips `API-Request:` and `API-Response:` trajectory lines. Condition B preserves the full trajectory. Keep the training format and generation-prompt format matched.
- Run `scripts/smoke_test.py` before training. It also reports samples whose prompt length reaches `max_seq_len` and therefore may receive no gradient signal.
- The documented comparison is not token-budget matched: condition B has more training tokens than A. Treat performance differences as pilot evidence, not an isolated causal effect of trajectory context.
- The current final experiment targets `meta-llama/Llama-3.1-8B-Instruct`; older notebook material may refer to Mistral formatting and needs careful review before reuse.
- The evaluation focuses on next API-call behavior and reports API-name, exact full-call, parameter, and malformed/no-call outcomes. It is not a complete end-to-end task-success benchmark.
- Large adapter bundles are kept outside git, typically in the shared Google Drive folder documented in `README.md` and `artifacts/checkpoint_manifest_seed42.md`. Only small metadata/results are mirrored under `artifacts/`.
- Record meaningful runs in `runs/` with the notebook, condition, seed, runtime, GPU, artifact paths, and any deviation from the intended setup.
- Preserve existing notebooks and generated artifacts when making changes; this repository is primarily a reproducibility record rather than a conventional application codebase.
