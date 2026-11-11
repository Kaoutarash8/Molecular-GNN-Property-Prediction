# Data Preprocessing Decisions

## 1. Project Scope

**Project:** Molecular Property Prediction Using Graph Neural Networks

**Datasets:**
- BBBP — Blood-Brain Barrier Penetration
- Tox21 — Toxicity Prediction (12 tasks)
- ClinTox — Clinical Toxicity and FDA Approval (2 tasks)
- SIDER — Adverse Drug Effects (27 tasks)
- ESOL — Aqueous Solubility Prediction

**Objective:** Establish a reproducible preprocessing pipeline and evaluate alternative data-handling strategies before training GCN, GAT, GIN and Graph Transformer architectures.

---

## 2. Missing Label Handling

**Affected datasets:** Tox21, ClinTox, SIDER (after verifying their actual missing-label distributions).

| Approach | Advantages | Disadvantages |
|---|---|---|
| Remove incomplete molecules | Simple implementation; complete labels | Potentially substantial data loss |
| Replace missing labels with 0 | Simple implementation | Introduces incorrect negative labels |
| Mean/mode imputation | Produces complete matrices | Creates artificial targets and can introduce bias |
| Masked loss | Preserves all available labels | Requires custom loss and masked evaluation |

**Candidate approach:** Masked loss.

**Comparison experiment:** Masked loss versus removing incomplete molecules, where the resulting dataset size permits a meaningful comparison.

**Evaluation:** Number of retained molecules and valid labels, ROC-AUC and PR-AUC per task.

**Decision status:** Pending experiments.

---

## 3. Class Imbalance Handling

**Affected datasets:** BBBP, Tox21, ClinTox and SIDER, depending on the distribution of each task.

| Approach | Advantages | Disadvantages |
|---|---|---|
| Original distribution | Preserves all observations and the natural class distribution | Majority-class bias may occur |
| Random undersampling | Reduces majority-class dominance | Discards potentially useful observations |
| Random oversampling | Retains original observations and increases minority representation | Can cause overfitting through repeated samples |
| Class-weighted loss | Uses all observations and penalizes minority-class errors more strongly | Requires appropriate weight selection |
| Focal loss | Gives more attention to difficult examples | Adds hyperparameters and may not improve performance |

**Candidate experiments:**
1. Standard loss with original training distribution.
2. Class-weighted loss.
3. Random undersampling of the training set.
4. Random oversampling of the training set.

**Important constraints:**
- Apply resampling only after train/validation/test splitting.
- Never resample validation or test sets.
- Keep the test distribution unchanged.
- For multi-label datasets, assess imbalance independently for each task.

**Evaluation:** ROC-AUC, PR-AUC, precision, recall, F1-score and confusion matrices.

**Decision status:** Pending experiments.

---

## 4. Duplicate Molecule Handling

| Approach | Advantages | Disadvantages |
|---|---|---|
| Keep all records | Preserves original records | Repeated molecules may receive excessive influence |
| Remove identical SMILES | Simple duplicate detection | Different SMILES can represent the same molecule |
| Canonicalize molecular structures | Better identification of equivalent molecular representations | Requires RDKit and careful handling of conflicting labels |

**Candidate approach:** Canonicalize SMILES using RDKit, identify duplicate molecular structures and investigate conflicting labels before deciding whether to remove or merge records.

**Important:** Duplicate structures must not be allowed to leak across training and test sets.

**Decision status:** Pending data inspection.

---

## 5. Invalid Molecule Handling

| Approach | Advantages | Disadvantages |
|---|---|---|
| Exclude invalid molecules | Prevents graph-construction errors | Reduces dataset size |
| Attempt molecule sanitization | May recover some structures | Can change or misinterpret problematic structures |

**Candidate approach:** Validate SMILES using RDKit and exclude molecules that cannot be converted into valid molecular graphs. Record the number and reason for exclusions.

**Decision status:** Pending validation.

---

## 6. Molecular Graph Features

| Approach | Advantages | Disadvantages |
|---|---|---|
| Basic atom and bond features | Efficient baseline; straightforward implementation | Limited chemical information |
| Rich atom and bond features | Captures more chemical properties | Requires additional feature engineering |
| Additional molecular descriptors | May provide complementary chemical information | Adds complexity and possible feature leakage if handled incorrectly |

**Candidate approach:** Start with chemically meaningful atom and bond features.

Atom features:
- Atomic number
- Degree
- Formal charge
- Hydrogen count
- Hybridization
- Aromaticity

Bond features:
- Bond type
- Conjugation
- Ring membership
- Stereochemistry

Additional molecular descriptors can be evaluated in a separate experiment.

**Decision status:** Initial feature representation to be implemented and validated.

---

## 7. Dataset Splitting

| Approach | Advantages | Disadvantages |
|---|---|---|
| Random split | Simple and computationally efficient | Similar molecular scaffolds may occur in different subsets |
| Stratified random split | Better class distribution preservation | Does not guarantee scaffold separation |
| Scaffold split | Evaluates generalization to structurally different molecules | More challenging and potentially imbalanced |

**Candidate approach:** Scaffold splitting as the primary evaluation strategy.

**Comparison experiment:** Random or stratified random splitting as a secondary evaluation where appropriate.

**Constraints:**
- Use identical splits for all four GNN architectures on each dataset.
- Fix random seeds.
- Keep test data separate from model selection.
- Fit preprocessing transformations using training data only.

**Decision status:** Pending split validation.

---

## 8. Regression Target Handling — ESOL

| Approach | Advantages | Disadvantages |
|---|---|---|
| Original target values | Directly interpretable predictions | Different numerical scale may affect optimization |
| Standardized targets | Can improve optimization stability | Predictions must be converted back to the original scale |

**Candidate experiment:** Compare original ESOL targets with standardized targets.

If standardization is used, calculate the mean and standard deviation using the training set only.

**Evaluation:** MAE, RMSE and R² on the original solubility scale.

**Decision status:** Pending experiments.

---

## 9. Experimental Protocol

To ensure fair comparisons:

1. Inspect the original datasets.
2. Record dataset sizes, missing labels and class distributions.
3. Validate molecular structures.
4. Identify duplicate molecular structures and label conflicts.
5. Establish fixed dataset splits.
6. Implement alternative preprocessing strategies independently.
7. Train models using identical experimental conditions.
8. Compare results using appropriate metrics.
9. Document the selected approach and its justification.

### Experimental Control

- Fixed random seeds.
- Identical molecular splits across architectures.
- No preprocessing fitted on validation or test data.
- No resampling of validation or test sets.
- Separate experiments for individual preprocessing decisions.
- Record hyperparameters and dataset versions.

---

## 10. Final Decision Log

| Issue | Selected approach | Experimental evidence | Status |
|---|---|---|---|
| Missing labels | To be determined | Pending | Open |
| Class imbalance | To be determined | Pending | Open |
| Duplicate molecules | To be determined | Pending | Open |
| Invalid molecules | To be determined | Pending | Open |
| Molecular features | To be determined | Pending | Open |
| Dataset splitting | To be determined | Pending | Open |
| ESOL target scaling | To be determined | Pending | Open |

**Final principle:** No preprocessing strategy will be selected solely because it is commonly used. Each decision must be supported by data inspection, technical justification and experimental evidence.