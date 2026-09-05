# COMPSCI 590NN Final Project

This repo contains the final project notebooks, run ledgers, and small reproducibility artifacts for the API-Bank continual-learning experiments.

## Shared Artifacts

Large Colab outputs and checkpoint bundles are stored in Google Drive:

https://drive.google.com/drive/folders/1tsoPTxmma0zwSq6joeECTWdvIRgmKMWq?usp=sharing

The Drive folder includes the seed 42 A/B checkpoint bundles, result JSONs, preprocessed data zip, the completed full-generation evaluation notebook, and report-ready full-eval CSV/JSON/PNG/PDF outputs.

## Final Deliverables

- `final/final_report.pdf`: compiled 7-page NeurIPS-format final report.
- `CS_590NN_690NN_Final_Project_Template/main.tex`: report source.
- `final/final_presentation.pptx`: 8-slide final presentation deck.
- `final/presentation_speaker_notes.md`: slide-by-slide speaking notes for an approximately 8-minute presentation.
- `scripts/build_final_presentation.py`: reproducible deck builder.

## Main Notebooks

- `final/01_data_prep.ipynb`
- `final/02_train_eval.ipynb`
- `final/03_analysis.ipynb`
- `final/04_full_generation_eval.ipynb`
- `final/05_meta_controller.ipynb` — meta-controller A/B policy-selection experiment.
  Self-contained: it rebuilds the API-Bank blocks itself, so it can be run on Colab
  without running `01_data_prep.ipynb` first. Requires a GPU runtime (A100 or better
  for the full run) and an `HF_TOKEN` Colab secret. Set `SMOKE_TEST = True` for a
  fast dry run on a free T4 before the real one. Section 7 bundles the run's JSON
  results into a zip and downloads it; unzip it into `artifacts/` to commit them.

Completed notebook copies and run notes are kept under `runs/`.
