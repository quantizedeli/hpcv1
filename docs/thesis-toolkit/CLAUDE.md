# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Nuclear Physics AI Pipeline v2.0.0** — A 13-phase ML pipeline that trains AI (RF, XGBoost, DNN, BNN, PINN) and ANFIS models to predict nuclear magnetic moment (MM) and quadrupole moment (QM) for 267 nuclei. The output is a compiled LaTeX PhD thesis.

**Primary data:** `repo/data/aaa2.txt` — 267 nuclei, 12 base columns → 44+ engineered features.  
**Active targets:** MM and QM only (Beta_2 and MM_QM are defined but not active in the pipeline).  
**Language:** Python 3.x, no web framework.

---

## Running the Pipeline

All commands run from `repo/`:

```bash
# Single phase
python main.py --pfaz 1 --mode run       # fresh start
python main.py --pfaz 1 --mode resume    # resume from checkpoint
python main.py --pfaz 1 --mode update    # re-run, overwrite outputs
python main.py --pfaz 1 --mode pass      # skip, use cached results

# All phases sequentially
python main.py --run-all
python main.py --run-all --start-from 5 --end-at 10

# Interactive menu
python main.py --interactive

# Single nucleus prediction (requires PFAZ 2/3 complete)
python main.py --predict "Z=26 N=30 A=56"
python main.py --predict pred_input.txt

# Diagnostics
python main.py --check-deps
python scripts/health_check.py
python scripts/check_pfaz_completeness.py
```

**Pipeline execution order** (not 1–13 sequential):
```
1 → 2 → 3 → 4 → 5 → 7 → 9 → 12 → 13 → 6 → 8 → 10
```
PFAZ 11 (production/Docker) is permanently disabled.

**Phase status:** `repo/pfaz_status.json` — set a phase to `"pending"` to force re-run.

---

## Running Tests

```bash
cd repo/
pytest tests/ -v                          # all tests
pytest tests/ -m smoke                    # fast sanity checks only
pytest tests/ -m unit
pytest tests/ -m integration
pytest tests/ --cov=. --cov-report=html   # coverage report
pytest tests/test_smoke/test_basic_smoke.py -v  # single file
```

Test markers: `smoke`, `unit`, `integration`, `system`, `slow`.

---

## Architecture

### Directory Layout
```
repo/
├── main.py                    # Orchestrator (2176 lines), CLI, phase dispatch
├── config.json                # All phase hyperparameters, model configs, thresholds
├── pfaz_status.json           # Per-phase status/progress tracking
├── pfaz_modules/              # 13 phase modules (pfaz01_* … pfaz13_*)
├── core_modules/              # Shared: constants, anomaly_detector, feature_set_builder, progress_tracker
├── physics_modules/           # SEMF, Woods-Saxon, Nilsson, Shell model, Schmidt
├── utils/                     # warning_tracker, checkpoint_manager, gpu_manager, reproducibility_manager
├── analysis_modules/          # SHAP, interpretability
├── visualization_modules/     # Shared plotting helpers
├── tests/                     # pytest suite (smoke / unit / integration)
├── scripts/                   # health_check, log_parser, check_pfaz_completeness
└── data/aaa2.txt              # Primary dataset (267 nuclei)
```

### Phase Responsibilities

| Phase | Module | What it does |
|-------|--------|--------------|
| PFAZ 01 | `pfaz01_dataset_generation/` | Generates 848 dataset variants (size × scenario × feature set × scaling × sampling) from aaa2.txt |
| PFAZ 02 | `pfaz02_ai_training/` | Trains RF/XGBoost/DNN/BNN/PINN × 50 configs; parallel via ThreadPoolExecutor; checkpoint/resume |
| PFAZ 03 | `pfaz03_anfis_training/` | Trains 8 ANFIS configs (Grid/SubClust × Trimf/Gauss/Bell/Trap); hybrid LSE + L-BFGS-B |
| PFAZ 04 | `pfaz04_unknown_predictions/` | Predicts MM/QM for nuclei outside training set; top-25 consensus; 95% CI |
| PFAZ 05 | `pfaz05_cross_model/` | AI vs ANFIS comparison; Good/Medium/Poor classification |
| PFAZ 06 | `pfaz06_final_reporting/` | 29+ sheet Excel workbook (dinamik; BUG-59: gercek sayi hedef x config kombinasyonuna gore degisir) + LaTeX report; reads PFAZ 7/9/12/13 outputs |
| PFAZ 07 | `pfaz07_ensemble/` | 4 voting (Simple, WeightedR2, WeightedRMSE, WeightedInvError) + 4 stacking (Ridge, Lasso, RF, GBM); stacking_MLP yok (BUG-60: eski CLAUDE.md "5+6+AdaBoost" yanlistı) |
| PFAZ 08 | `pfaz08_visualization/` | 70+ chart types (BUG-61: gercek sayi dogrulanmamis); 300 dpi PNG + Plotly HTML; two-pass (after PFAZ 6, then after PFAZ 9/12/13) |
| PFAZ 09 | `pfaz09_aaa2_monte_carlo/` | MC uncertainty (n=100 bootstrap/noise/dropout); top-50 models x 267 nuclei |
| PFAZ 10 | `pfaz10_thesis_compilation/` | Generates LaTeX thesis: 6 chapters (Giris, Literatur, Yontem, Bulgular, Tartisma, Sonuc) + 3-4 appendix (A-D); PDF compile optional |
| PFAZ 11 | `pfaz11_production/` | **DISABLED** (config: `"enabled": false`) |
| PFAZ 12 | `pfaz12_advanced_analytics/` | Paired t-test, Wilcoxon, Sobol/Morris sensitivity, NuclearPatternAnalyzer; **FAILED** (import error) |
| PFAZ 13 | `pfaz13_automl/` | Optuna TPE AutoML retraining for low-R² models; **FAILED** (1-line IndentationError in automl_retraining_loop.py:43) |

### Key Cross-Cutting Modules

- **`core_modules/constants.py`** — Feature mappings, magic numbers; **NOTE:** lists only 3 scaling methods (wrong). `scaling_manager.py` is authoritative (4 methods: NoScaling, Standard, Robust, MinMax).
- **`core_modules/feature_set_builder.py`** — 24 feature abbreviations expand into full column lists.
- **`utils/warning_tracker.py`** — Singleton accumulating all pipeline warnings → `outputs/pipeline_warnings.json`.
- **`utils/checkpoint_manager.py`** — Used by PFAZ 2/3 for resume support.

### Dataset Naming Convention
```
{TARGET}_{SIZE}_{SCENARIO}_{FEAT_SET}_{SCALING}_{SAMPLING}[_NoAnomaly].{ext}
```
Example: `MM_150_S70_AZSMC_NoScaling_Random_NoAnomaly.csv`

- Sizes ≤ 100: only S70, Basic+Standard feature sets.
- Sizes ≥ 150: S70+S80, +Physics, +NoAnomaly variant (IQR threshold=3.0, IsolationForest contamination=0.08).

### DISCRETE_FEATURES (never scaled)
`A, Z, N, Nn, Np, SPIN, PARITY, magic_character, magic_n, magic_p, magic_np`

### Physics Constants (physics_modules/)
- **SEMF:** `a_v=15.75, a_s=17.8, a_c=0.711, a_a=23.7, a_p=11.18 MeV`
- **Woods-Saxon:** `V0=51.0 MeV, r0=1.25 fm, a=0.67 fm`
- **Nilsson:** `omega0=41.0 MeV, kappa=0.05, mu=0.60`
- **HBAR_C = 197.3269804** — added to `constants.py:44` (BUG-02 fixed 2026-05-04). WS özellikleri artık çalışıyor.

---

## Known Critical Bugs

| ID | Severity | Location | Issue | Fix |
|----|----------|----------|-------|-----|
| BUG-01 | ~~CRITICAL~~ | `qm_filter_manager.py:153` | **GEÇERSİZ — Tasarım kararı**: Q=0 küresel çekirdekler aaa2.txt'te zaten yok; filtreleme intentional. | CLOSED |
| BUG-02 | ~~HIGH~~ | `woods_saxon.py:15` | **DÜZELTİLDİ 2026-05-04** — HBAR_C constants.py:44'e eklendi, V_so da eklendi. Yeniden eğitim gerekli. | DONE |
| BUG-31 | ~~HIGH~~ | `pfaz12_advanced_analytics/nuclear_band_analyzer.py` | **DÜZELTİLDİ 2026-05-09** — Sınıf adı `NuclearMomentBandAnalyzer`; alias `NuclearBandAnalyzer` eklendi. | DONE |
| BUG-32 | ~~HIGH~~ | `pfaz13_automl/automl_retraining_loop.py:539` | **DÜZELTİLDİ 2026-05-09** — `return []` sonrası 3 satır hatalı indent; silindi. pfaz06 aynı kalıp da düzeltildi (satır 1267). | DONE |
| BUG-37 | LOW | `pfaz10_thesis_compilation/pfaz10_thesis_orchestrator.py` | Hardcoded `/mnt/project` path (old v2.0, no longer active) | Informational |
| BUG-38 | ~~LOW~~ | `pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py` | **DÜZELTİLDİ 2026-05-09** — DEFAULT_MC_CONFIG n_bootstrap ve n_samples_per_level 100→1000 yapıldı. Tez K=1000 doğru. | DONE |

**Pipeline status (2026-05-12):** Sprint 1-8 tamamlandi. CV gate (BUG-62) aktif -- max_train_cv_gap=0.6. Son patch: sprint8-only.patch (commit 2f1e594). v10 Sprint 8 sync bekliyor.

---

## ML Models & Thresholds

- **R2_MIN_SAVE_THRESHOLD = 0.5** (PFAZ 2/3): models below this are discarded.
- **DUAL FILTER** (PFAZ 2, Sprint 8 aktif): cv_R2 >= 0.0 (Shang 2022) + gap < 0.6 (Utama 2016, Sprint 8: 0.5->0.6 kucuk N icin). [DUAL_FILTER] log mesajlari KABUL/RET gosterir.
- **DNN divergence:** val_R² < −2.0 → marked DIVERGED.
- **DNN size constraint:** train_size < 200 → no DNN job created (affects sizes 75, 100).
- **SVR:** Has its own internal StandardScaler (RBF, C=10.0) — independent of PFAZ 1 scaling.
- **5-fold CV:** train+val combined, test never included; `n_jobs=1` in parallel mode to prevent deadlock.
- **Seed:** 42 (fixed in `parallel_ai_trainer.py:1363`).
- **Data leakage guard:** `schmidt_moment`, `Q0_intrinsic`, `Beta_2_estimated` always removed.

## ANFIS Configs
8 configs: `GAU2MF, GAU3MF, BELLMF, TRIMF` × `GRIDP/SUBCLUST`  
Hybrid learning: LSE (consequent params) + L-BFGS-B (premise params).  
SubClust init uses KMeans, not MATLAB genfis2.

## Output Locations

| Phase | Output path |
|-------|-------------|
| PFAZ 1 | `outputs/generated_datasets/` |
| PFAZ 2 | `outputs/trained_models/` |
| PFAZ 3 | `outputs/anfis_models/` |
| PFAZ 4 | `outputs/unknown_predictions/` (7-sheet Excel) |
| PFAZ 5 | `outputs/cross_model_analysis/MASTER_CROSS_MODEL_REPORT.xlsx` |
| PFAZ 6 | `outputs/reports/THESIS_COMPLETE_RESULTS.xlsx` (29 sheets) |
| PFAZ 7 | `outputs/ensemble_results/evaluation/comprehensive_report.json` |
| PFAZ 8 | `outputs/visualizations/` (PNG 300dpi + HTML) |
| PFAZ 9 | `outputs/aaa2_results/` |
| PFAZ 10 | `outputs/thesis/` (main.tex + chapters + compile.bat) |
| PFAZ 12 | `outputs/advanced_analytics/` |
| PFAZ 13 | `outputs/automl_results/` |
| Logs | `logs/main_YYYYMMDD_HHMMSS.log` (200 MB × 5 rotating) |
| Warnings | `outputs/pipeline_warnings.json` + `pipeline_warnings_report.xlsx` |

---

## Phase Documentation

Turkish-language analysis notes for each phase:
- `phases/faz-XX-*.md` — methodology and design decisions per phase
- `reports/faz-XX-*.md` — analysis notes and findings
- `reports/faz-XX-final-rapor.md` — final reports

Update these documents after completing any phase or fixing bugs. This is non-negotiable — past sessions have repeatedly missed this step.

---

## CRITICAL: Claude Calisma Kurallari

### KURAL: Asla tek basina karar verme

Her degisiklik, her script, her commit icin ONCE plan sun, ONAY al, SONRA hareket et.
"Bariz gorunuyor" veya "onceki sohbetten biliyorum" gerekcesiyle onaysiz hareket etme.
Bu kural istisna kabul etmez.

### Git Workflow (Claude sandbox -> Kemal'in makinesi)

Claude dogrudan GitHub'a push edemez. Akis:

1. Claude sandbox'ta branch acar, dosyalari duzenler, commit yapar
2. `git format-patch` ile .patch dosyasi uretir
3. Kemal patch'i **VS Code'daki proje klasorune** koyar:
   - hpcv1 icin: `C:\Users\<Kullanici>\Desktop\hpcv1\`  (veya neredeyse)
   - v10 icin:   `C:\Users\<Kullanici>\Desktop\arastirma\v10\`
4. VS Code terminali (veya PowerShell) acilir, proje klasorunde:
   ```powershell
   git checkout truba-fixes   # (veya dev-updates, vs.)
   git am sprint9b-only.patch
   git push origin truba-fixes
   ```
5. Onay mesaji geldikten sonra Claude bir sonraki adima gececek

### TRUBA Workflow

TRUBA scripti veya konfigurasyonu degistirmeden once:
1. Kemal'den TRUBA'da calistirdigi komutlarin ciktisini iste
2. Ciktilar olmadan TAHMIN etme -- tahmin = yanlis script = job FAILED
3. Plan sun: "X'i Y olarak degistirmeyi oneririm, neden: Z" -> Kemal onayla -> sonra yaz

### SSH Adresi

```powershell
# Windows PowerShell veya Terminal (OpenVPN bagli olmali)
ssh ahmacar@levrek.ulakbim.gov.tr
# VPN uzerinden ic IP de olabilir -- Kemal'e sor hangi adres calisiyor
```

