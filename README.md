# Molecular GNN Property Prediction

A learning-focused project for molecular property prediction with Graph Neural Networks (GNNs).

## Scope

- **BBBP** — binary classification: blood-brain barrier permeability.
- **Tox21** — multi-label classification: 12 toxicity-related targets.
- **ESOL** — regression: aqueous solubility.

Planned model comparison: GCN, GAT, GIN and a Graph Transformer. This project compares models using consistent data splits and evaluation protocols. Predictions are not medical diagnoses or validated drug-discovery results.

## Structure

```text
├── configs/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
├── outputs/
│   ├── figures/
│   └── metrics/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── training/
│   └── evaluation/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup on Windows (PowerShell)

Recommended: Python 3.11.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install a PyTorch build compatible with your machine using the official selector:
https://pytorch.org/get-started/locally/

Then install dependencies:

```powershell
pip install -r requirements.txt
```

Check the installation:

```powershell
python -c "import torch, torch_geometric, rdkit; print('torch:', torch.__version__); print('PyG:', torch_geometric.__version__); print('RDKit: OK')"
```

## Docker (CPU development image)

```powershell
docker build -t molecular-gnn:dev .
docker run --rm -v "${PWD}/data:/workspace/data" molecular-gnn:dev
```

The Docker image uses CPU-only PyTorch. GPU support should only be added if the machine and Docker runtime support it.

## First milestone: download datasets

```powershell
python -m src.data.download_datasets --datasets BBBP Tox21 ESOL
```

Datasets are stored under `data/raw/` and are excluded from Git.

## Planned milestones

1. Download, inspect and validate BBBP, Tox21 and ESOL.
2. Verify graph fields and define atom/bond features.
3. Establish reproducible scaffold splits and simple baselines.
4. Implement GCN, GAT and GIN.
5. Implement and validate the Graph Transformer.
6. Train, evaluate and compare all models.
7. Add a Streamlit demo only after the prediction pipeline is reliable.

## Evaluation plan

- **BBBP:** ROC-AUC primary; also PR-AUC, F1, precision and recall.
- **Tox21:** ROC-AUC per task and mean ROC-AUC over valid tasks; use masked loss for missing labels.
- **ESOL:** MAE and RMSE; optionally R².

Use the same scaffold split for every model on a given dataset. Fit preprocessing only on training data. Record seeds, hyperparameters and results.

## Engineering rules

- Do not commit datasets, checkpoints, virtual environments or experiment artifacts.
- Do not compare models on different train/test splits.
- A Graph Transformer is not automatically better; experiments determine that.
- Keep all reported results and CV claims tied to measured outcomes.
