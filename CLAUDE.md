# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nuclear physics AI research project predicting nuclear **magnetic moments (MM)** and **quadrupole moments (QM)** for 267 nuclei using ML models (RF, GBM, XGBoost, DNN, BNN, PINN) and ANFIS. The pipeline consists of 13 numbered phases called **PFAZ 0–13** (PFAZ 11 is intentionally skipped/disabled).

Primary data source: `data/aaa2.txt` — 267 nuclei with 44+ engineered features.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run a single phase
python main.py --pfaz 1 --mode run

# Resume an interrupted phase
python main.py --pfaz 1 --mode resume

# Skip a phase (use cached results)
python main.py --pfaz 1 --mode pass

# Update outputs of a completed phase
python main.py --pfaz 1 --mode update

# Run all phases sequentially
python main.py --run-all

# Interactive mode (guided phase selection)
python main.py --interactive

# Single nucleus prediction (Z and N minimum)
python main.py --predict "Z=26 N=30 A=56"
```

To force re-run a phase that already shows `completed` or `failed`, edit `pfaz_status.json` and set its `status` to `"pending"`.

## Utility Scripts

```bash
python scripts/health_check.py            # Verify imports, data files, and PFAZ module availability
python scripts/check_pfaz_completeness.py # Check each phase's expected output files exist
python scripts/log_parser.py              # Parse logs/main_*.log for errors and warnings
```

## Testing

```bash
pytest tests/test_smoke -v              # Quick sanity checks (~seconds)
pytest tests/test_units -v              # Unit tests
pytest tests/test_integration -v        # Multi-component tests
pytest tests/ -v --cov                  # Full suite with coverage
pytest tests/ -m "not slow" -v          # Skip slow tests
pytest tests/test_smoke/test_basic_smoke.py::test_config_file_valid_json -v  # Single test
```

Test markers: `smoke`, `unit`, `integration`, `system`, `slow`.

## Architecture: PFAZ Pipeline

Phases run sequentially. Each phase reads outputs from prior phases. Status is tracked in `pfaz_status.json` (states: `pending` / `running` / `completed` / `failed` / `skipped`).

| Phase | Module | Primary Class | Purpose |
|-------|--------|---------------|---------|
| PFAZ 1 | `pfaz01_dataset_generation/` | `DatasetGenerationPipelineV2` | Load `aaa2.txt`, engineer features (SEMF, Woods-Saxon, Nilsson, Shell models), apply anomaly detection and SHAP-based selection, export **848 datasets** in CSV/Excel/MAT formats |
| PFAZ 2 | `pfaz02_ai_training/` | `ParallelAITrainer` | Train 6 model types × 50 configs each in parallel; 5-fold CV; GPU optional |
| PFAZ 3 | `pfaz03_anfis_training/` | `ANFISParallelTrainerV2` | Real TakagiSugeno ANFIS (8 configs: Grid/SubClust × Gauss/Bell/Tri/Trap); hybrid LSE+L-BFGS-B; adaptive n_mfs; MATLAB optional (Python fallback) |
| PFAZ 4 | `pfaz04_unknown_predictions/` | `UnknownNucleiPredictor` | Predict MM/QM for nuclei outside training set (top-25 models); single nucleus via `SingleNucleusPredictor`; 95% CI; `GeneralizationAnalyzer` |
| PFAZ 5 | `pfaz05_cross_model/` | `CrossModelEvaluator` | PKL model + test.csv prediction; Good (R²>0.90) / Medium / Fair classification; `MASTER_CROSS_MODEL_REPORT.xlsx` |
| PFAZ 6 | `pfaz06_final_reporting/` | `ComprehensiveExcelReporter` | 18-sheet Excel (95k AI + 5.5k ANFIS rows); LaTeX; anomaly vs NoAnomaly; `ExcelStandardizer` |
| PFAZ 7 | `pfaz07_ensemble/` | `EnsemblePipeline` | Voting (simple/weighted) and stacking (ridge, lasso, RF, GBM, MLP) ensembles |
| PFAZ 8 | `pfaz08_visualization/` | `VisualizationSystem` | Two-pass: pass 1 standard (PFAZ6 data), pass 2 supplemental (PFAZ9/12/13 — MC9/ST12/AM13 graphs) |
| PFAZ 9 | `pfaz09_aaa2_monte_carlo/` | `MonteCarloSimulationSystem` | Top-50 models × 267 nuclei; per-model feature set from metadata; 95% CI |
| PFAZ 10 | `pfaz10_thesis_compilation/` | `ThesisCompilationSystem` | 11 chapters + 2 appendices; TR/EN abstract; PFAZ12/13 content; `compile.bat`; `compile_pdf=False` default |
| PFAZ 11 | `pfaz11_production/` | — | **Disabled by design** — web interface / API / Docker (skipped) |
| PFAZ 12 | `pfaz12_advanced_analytics/` | `StatisticalTestingSuite` | Paired t-test, Wilcoxon, Friedman, Bootstrap (n=5000); `NuclearPatternAnalyzer`; sensitivity analysis |
| PFAZ 13 | `pfaz13_automl/` | `AutoMLRetrainingLoop` | Optuna (TPE+MedianPruner); retrain low-R² models; `automl_improvement_report.xlsx` |

## Key Data Flow

```
aaa2.txt (267 nuclei, 44 features)
  → PFAZ 1: 848 datasets (train/val/test splits, CSV/Excel/MAT)
  → PFAZ 2: trained_models/ (AI)
  → PFAZ 3: anfis_models/ (ANFIS)
  → PFAZ 4: unknown_predictions/ (with uncertainty)
  → PFAZ 5: cross_model_analysis/
  → PFAZ 6: reports/ (Excel 18-sheet, LaTeX)
  → PFAZ 7: ensemble_results/
  → PFAZ 8: visualizations/
  → PFAZ 9: aaa2_results/ (Monte Carlo)
  → PFAZ 10: thesis/
```

Dataset variants encode: `{target}_{size}_{scenario}_{feature_set}_{scaling}_{sampling}[_NoAnomaly]`
- Targets: MM, QM, Beta_2, MM_QM
- Sizes: 75, 100, 150, 200, ALL(197) — sizes ≤100 only produce S70 + Basic/Standard feature sets
- Scenarios: S70 (70/15/15 split), S80 (80/10/10 split)
- NoAnomaly variants: only for 150/200/ALL sizes (IQR threshold=3.0)

## Configuration

`config.json` — central config for all phases including hyperparameters, paths, CV folds, GPU flags, and per-target thresholds.

`pfaz_status.json` — auto-managed status file; edit manually only to force re-runs (set `status` to `"pending"`).

## Module Layout

```
pfaz_modules/pfaz{01-13}_*/          # Phase modules
core_modules/                        # Shared utilities (constants, progress, anomaly detection)
analysis_modules/                    # Interpretability, robustness, real-data integration
visualization_modules/               # Plot integration helpers
physics_modules/                     # Shell model calculations (SEMF, Woods-Saxon, Nilsson)
utils/warning_tracker.py             # Pipeline-wide WARNING/ERROR tracker (singleton: get_tracker())
scripts/                             # Developer utilities (health_check, log_parser, etc.)
data/aaa2.txt                        # Primary dataset
logs/main_*.log                      # Rotating logs (200 MB × 5 files)
outputs/pipeline_warnings.json       # Real-time warning accumulator
outputs/generated_datasets/          # 848 datasets (CSV/XLSX/MAT + metadata.json each)
outputs/trained_models/              # {dataset}/{model_type}/{config}/model_*.pkl + metrics_*.json
outputs/anfis_models/                # {dataset}/{config}/model_*.pkl + metrics_*.json
outputs/reports/THESIS_COMPLETE_RESULTS_*.xlsx
outputs/visualizations/              # Standard + supplemental/ (MC9/ST12/AM13)
outputs/thesis/                      # LaTeX + compile.bat
```

## Critical Coding Rules

- **No emoji/Unicode in log messages** — Windows console encoding; use ASCII only (`[OK]` not `✓`)
- **Always use `pathlib.Path`** — no hardcoded paths, no Linux `/mnt/...` paths
- **Wrap every optional module call in `try/except Exception`** and call `get_tracker().warn(...)` on failure
- **`_AVAILABLE` flag pattern** — each phase `__init__.py` wraps optional imports in `try/except` and exports a `MODULE_NAME_AVAILABLE` bool; callers must check this flag before using the class
- **DNN minimum samples**: `DNN_MIN_SAMPLES = 80` — raise ValueError to skip, not warning to continue
- **Document every change** in `PFAZ_DEVELOPMENT_NOTES.md` under the relevant PFAZ section

## Reference Files (Most Up-to-Date)

1. `PFAZ_DEVELOPMENT_NOTES.md` — per-phase change log (most comprehensive)
2. `PIPELINE_STATUS_REPORT.md` — current runtime status per phase (last run: 2026-04-21)
3. `QA_WIRING_REPORT.md` — which optional modules are wired vs. pending vs. deleted
4. `QA_PROJECT_STATUS_REPORT.md` — QA audit summary
5. `VISUALIZATIONS_INDEX.md` — all plot outputs catalog

## System Requirements

- Python 3.8+, RAM ≥ 16 GB, Disk ≥ 50 GB
- CUDA 11.0+ and GPU ≥ 8 GB VRAM (optional, for PFAZ 2/3 acceleration)
- MATLAB engine (optional, for native ANFIS in PFAZ 3; Python fallback exists)

---

## Sprint 15 Scope Changes (2026-05-20)

**KAPSAMLI DEGISIKLIK:** TRUBA Job2 timeout krizi sonrasi veri-bazli kucultme. Detaylar `docs/thesis-toolkit/sprints/sprint-15-truba-kriz-ve-iyilestirme.md`.

### Active Models
**Eski:** RF, GBM, XGBoost, DNN, BNN, PINN (belgede) / RF, XGBoost, LightGBM, CatBoost, SVR, DNN (kodda otomatik)
**Yeni (Sprint 15+):** **Sadece RF + XGBoost** (config.json -> pfaz02.model_types)

### Dataset Scope
**Eski:** 848-1468 dataset (24 FS × 2 senaryo × 3 scaling × 2 anomaly × 4 boyut × 2 sampling)
**Yeni:** **36 dataset** (9 FS × 1 senaryo S80 × 1 anomaly vanilla × 1 scaling NoScaling × 2 boyut 150+ALL × 2 sampling)

### Config Count
**Eski:** 50 (training_configs_50.json)
**Yeni:** **20** (training_configs_20.json -- top RF/XGB)

### Tahmini Sure
**Eski:** Job1: 2-3h | Job2: 14-27h | Job3: 7-15h | Job4: 2-3h | Toplam: 25-48h
**Yeni:** Job1: 5dk | Job2+3 (RF+XGB+ANFIS): ~1h | Job4 (PFAZ4-12): ~30dk | **Toplam: ~2h**

### Yeni BUG'lar
BUG-101..108 (Sprint 15 fix), BUG-109/110 (Sprint 17 ertelendi). Detaylar `pipeline-hatalari.md`.

### Yeni KURAL'lar
KURAL 34..40. Detaylar `claude-hatalarim-ve-dersler.md`.

### Sprint 15 Tezsel Bulgular (10 niceliksel)
Detaylar `tez-yazim-not-defteri.md` Sprint 15 eki. Ana iki bulgu:
- **B2E (Beta_2) ve Spin (S) feature'lari kritik** -- iceren setler test_R²>0.3, icermeyenler <0
- **Anomali cikarmak performansi DUSURUR** (vanilla 728 model >0.8, NoAnomaly 55 -- 13× fark)

### Tez Cercevesi Degisikligi
**Eski:** "R²>0.96 yuksek dogruluk"
**Yeni:** "Feature secimi belirleyici + kucuk-veri sinirlari" (R² max gozlemlenen ~0.92, R²>0.85 alt bolge literatur kiyasinda rekabetci)
