# v10 Sync To-Do (TRUBA Sonrasi)

**Tarih:** 2026-05-13 (Sprint 12 sonu)
**Hedef:** hpcv1'deki Sprint 10-12 fix'lerini v10 dev branch'ine tasi.

Kemal: "Daha sonra tum hatalari vs. sana v10'da duzeltmeni isticem. Simdi degil not alda yeri geldiginde unutmayalim."

## v10 ve hpcv1 Iliskisi

- **v10**: Desktop dev branch, `github.com/quantizedeli/v10`, branch `dev-updates`
- **hpcv1**: TRUBA production branch, `github.com/quantizedeli/hpcv1`, branch `truba-fixes`
- v10 dev surekli devam ediyor (yeni feature'lar), hpcv1 TRUBA'ya akiyor

## Tasinmasi Gereken Bug'lar (Sprint 10-12, BUG-65..84)

### Sprint 10 (10 fix)
- [ ] BUG-65: PFAZ13 dataset path -> generated_datasets
- [ ] BUG-66: PFAZ13 metadata-aware CSV okuma
- [ ] BUG-67: PFAZ13 acik status (skipped_no_*)
- [ ] BUG-68: Job 3/4 exit code propagation (eger v10'da Slurm scriptleri varsa)
- [ ] BUG-69: run_complete_pipeline.py deprecated guard
- [ ] BUG-70: HPC_MODE worker limiti (gpu_manager)
- [ ] BUG-71: config.json data_file top-level
- [ ] BUG-72: config.json n_workers notu
- [ ] BUG-73: PFAZ9 ANFIS path explicit
- [ ] **BUG-74**: PFAZ2 Target sutunu (en kritik!)

### Sprint 11 (4 fix)
- [ ] BUG-75: PFAZ3 selector PFAZ2 path explicit
- [ ] BUG-76: PFAZ8 reports_dir + 3 path explicit
- [ ] BUG-77: training_configs_50.json deterministik
- [ ] BUG-78: submit_all.sh afterok chain

### Sprint 12 (6 fix)
- [ ] BUG-79: PFAZ3 robustness datasets_dir helper
- [ ] **BUG-80**: PFAZ8 helper-based path (22 sub-method, 6 yeni param)
- [ ] BUG-81: BandAnalyzer pfaz4_excel_path explicit
- [ ] BUG-82: PFAZ6 cross_model/unknown/datasets explicit
- [ ] BUG-83: PFAZ6 pfaz9 fallback dogru klasor
- [ ] BUG-84: TRUBA -c 110 -> 112 (sadece TRUBA'da gecerli, v10 desktop'a etmez ama yorum guncel kalsin)

## Tasima Stratejisi

1. **Manuel cherry-pick degil** -- 14 commit, conflict beklenir.
2. Daha iyi yaklasim:
   ```bash
   cd Desktop/arastirma
   git checkout dev-updates
   git fetch origin
   git merge origin/master  # hpcv1'i merge et (varsayim: v10 hpcv1'i takip ediyor)
   # ... veya patch-by-patch:
   git am sprint10-full.patch
   git am sprint11-truba-ready.patch (Sprint 11+12 birlesik patch beklenir)
   ```

3. **Onceki sync'ler:**
   - Sprint 7 v10'a tasinmis (commit f8f28c1)
   - Sprint 8 v10'a tasinmis (commit 2dee889)
   - Sprint 10-12 henuz tasinmadi

## Test Stratejisi (v10 sync sonrasi)

- Desktop'ta `python main.py --pfaz 1 --pfaz 2 --pfaz 3` mini koşu
- PFAZ3 log'da "ANFISDatasetSelector aktif: X -> 200 dataset secildi (Top=50/Mid=50/Low=100)" mesaji aranmali
- PFAZ8 visualizations/ icinde 14 klasor uretilmeli

## v10'da Olmayabilecek Ozel Durumlar

- v10 desktop'ta `HPC_MODE=1` set edilmez -> BUG-70 fix'i desktop davranisini etkilemez (yine min(16,...) kullanir)
- v10 TRUBA scriptleri olmayabilir -> BUG-68, 78, 84 atlanir
- v10 PFAZ13 farkli durumda olabilir -- BUG-65, 66, 67 fix'i v10'da test edilmeli

---

*Sprint 12 sonu | v10 sync to-do | Kemal'in talebi "yeri geldiginde unutmayalim"*

---

## Sprint 13 Eki (2026-05-14) — BUG-85..99

Sprint 13 fix'leri de v10'a tasinmali (TRUBA sonrasi):

### Sprint 13 (15 fix)
- [ ] **BUG-85**: PIPESTATUS[0] -- job1/job2/truba_slurm_job.sh (sadece TRUBA Slurm'a etki eder, v10 desktop atlanabilir)
- [ ] **BUG-86**: run_all_pfaz failed_phases + RuntimeError + sys.exit(1) -- **v10'da da OLMALI** (production kalite)
- [ ] **BUG-87**: REQUIRED_PACKAGES optuna+lightgbm -- **v10'da da OLMALI**
- [ ] **BUG-88**: strict_truba config + PFAZ13 skipped→RuntimeError -- v10 desktop'ta `strict_truba: false` yapilabilir
- [ ] BUG-89: ${PROJECT_DIR:-...} env override -- TRUBA'ya ozel, v10 atlanabilir
- [ ] BUG-90: submit_all.sh reset notu -- TRUBA'ya ozel
- [ ] **BUG-91**: PFAZ2 fail→PFAZ3 skip -- **v10'da da OLMALI**
- [ ] BUG-92: _models_active_note config -- dokumantasyon, v10'da da eklenebilir
- [ ] **BUG-93**: automl_trials_details.xlsx -- **v10'da da OLMALI** (tez materyal)
- [ ] **BUG-94**: MC random_state=42 -- **v10'da da OLMALI** (reproducibility)
- [ ] **BUG-95**: joblib.load warning + failed_models ozet -- **v10'da da OLMALI**
- [ ] **BUG-96**: RobustnessTester aktif -- **v10'da da OLMALI** (tez materyal)
- [ ] **BUG-97**: BootstrapCI + ANFIS karsilastirmasi -- **v10'da da OLMALI** (tezin ana istatistiksel analizi)
- [ ] BUG-98: AdvancedSensitivity dead note -- v10'da da eklenebilir
- [ ] BUG-99: OptimizerComparison dead note -- v10'da da eklenebilir
- [ ] **PFAZ5 AI_vs_ANFIS sheet** -- **v10'da da OLMALI** (tez materyal, BUG-97 ile baglantili)

### v10'da Oncelikli (kalın): BUG-86, 87, 91, 93, 94, 95, 96, 97 + PFAZ5 fix

*Sprint 13 eki | 2026-05-14*
