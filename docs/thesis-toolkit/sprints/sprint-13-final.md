# Sprint 13 Final Raporu — Codex Audit + Tez Plani

**Tarih:** 2026-05-14  
**Branch:** `sprint13-codex-and-thesis-plan`  
**Patch:** `sprint13-codex-and-thesis-plan.patch`  
**Önceki sprint:** Sprint 11+12 (`sprint-11-12-final-truba-ready.md`)

---

## Özet

Sprint 13, paralel AI ajanı Codex'in denetim raporundaki 4 kritik bulguyu + Claude'un ek 11 bulgusunu kapatır. Toplam **15 bug (BUG-85..99)**, **5 yeni kural (KURAL 29-33)**, **1 PFAZ5 genişletmesi**.

Tez teslim tarihi 1 hafta. TRUBA sonuçları bekleniyor.

---

## Bug Katalogu

| Bug | Seviye | Açıklama | Dosya |
|-----|--------|----------|-------|
| BUG-85 | KRİTİK | `${PIPESTATUS[0]}` -- job1/job2/truba_slurm_job.sh | truba/slurm_jobs/ |
| BUG-86 | KRİTİK | run_all_pfaz failed_phases + RuntimeError + sys.exit(1) | main.py |
| BUG-87 | YÜKSEK | optuna+lightgbm REQUIRED_PACKAGES'a eklendi | main.py |
| BUG-88 | YÜKSEK | strict_truba=true + PFAZ13 skipped→RuntimeError | main.py, config.json |
| BUG-89 | ORTA | ${PROJECT_DIR:-...} env override 4 job script | truba/slurm_jobs/ |
| BUG-90 | ORTA | submit_all.sh reset notu + OUTPUT_DIR env | submit_all.sh |
| BUG-91 | KRİTİK | PFAZ2 fail → PFAZ3 skip | job2_pfaz02_03.sh |
| BUG-92 | DÜŞÜK | _models_active_note config.json | config.json |
| BUG-93 | ORTA | automl_trials_details.xlsx (3 sheet) + PFAZ6 sheet | main.py, pfaz6_final_reporting.py |
| BUG-94 | ORTA | 4 MC alt sınıfa random_state=42 | monte_carlo_simulation_system.py |
| BUG-95 | ORTA | joblib.load exception→warning + failed_models özet | aaa2_control_group_complete_v4.py |
| BUG-96 | YÜKSEK | RobustnessTester aktif (noise/outlier/perturbation) | parallel_ai_trainer.py |
| BUG-97 | YÜKSEK | BootstrapCI aktif + ANFIS karşılaştırması PFAZ12 | main.py |
| BUG-98 | DÜŞÜK | AdvancedSensitivity dead code note | advanced_sensitivity_analysis.py |
| BUG-99 | DÜŞÜK | OptimizerComparison dead code note | optimizer_comparison_reporter.py |

### Ek: PFAZ5 AI_vs_ANFIS Genişletmesi (Sprint 13 kapsamında)

- `Model_Statistics` sheet: `Model_Type` (AI/ANFIS) + `R2` kolonu eklendi
- `AI_vs_ANFIS_Comparison` sheet: PFAZ3 `anfis_vs_ai_comparison.xlsx` + fallback özet
- Etkilenen dosya: `pfaz_modules/pfaz05_cross_model/faz5_cross_model_analysis.py`

---

## Yeni Kurallar

| Kural | İçerik |
|-------|--------|
| KURAL 29 | Plan sun, onay bekle, sonra hareket et |
| KURAL 30 | Runtime behavior simulation (3 senaryo: happy/tek fail/pipe fail) |
| KURAL 31 | Single Source of Truth -- aynı bilgiyi iki yerde yazma |
| KURAL 32 | VARSAYIM YASAĞI -- "muhtemelen" = hemen grep/view ile doğrula |
| KURAL 33 | Cross-layer failure chain audit (Python→sys.exit→Bash→Slurm→afterok) |

---

## Değişen Dosyalar

### Python (10 dosya)
- `main.py` — BUG-86/87/88/91/93/97
- `pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py` — BUG-96
- `pfaz_modules/pfaz02_ai_training/model_validator.py` — (import, BUG-96 için)
- `pfaz_modules/pfaz05_cross_model/faz5_cross_model_analysis.py` — PFAZ5 AI_vs_ANFIS
- `pfaz_modules/pfaz05_cross_model/optimizer_comparison_reporter.py` — BUG-99 dead note
- `pfaz_modules/pfaz06_final_reporting/pfaz6_final_reporting.py` — BUG-93 sheet
- `pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py` — BUG-94
- `pfaz_modules/pfaz09_aaa2_monte_carlo/aaa2_control_group_complete_v4.py` — BUG-95
- `pfaz_modules/pfaz12_advanced_analytics/bootstrap_confidence_intervals.py` — BUG-97 (aktif)
- `pfaz_modules/pfaz12_advanced_analytics/advanced_sensitivity_analysis.py` — BUG-98 dead note

### Bash (6 dosya)
- `truba/slurm_jobs/job1_pfaz01.sh` — BUG-85/89
- `truba/slurm_jobs/job2_pfaz02_03.sh` — BUG-85/89/91
- `truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh` — BUG-89
- `truba/slurm_jobs/job4_pfaz06_08_10.sh` — BUG-89
- `truba/slurm_jobs/submit_all.sh` — BUG-90
- `truba_slurm_job.sh` — BUG-85

### Config (1 dosya)
- `config.json` — BUG-88 strict_truba, BUG-92 _models_active_note

### Dokümanlar (yeni)
- `docs/thesis-toolkit/sprints/sprint-13-final.md` (bu dosya)
- `docs/thesis-toolkit/sprints/sprint-14-pfaz10-rewrite-plan.md`
- `docs/thesis-toolkit/guide/QA-ENGINEER-PLAYBOOK.md`
- `reports/ANTHROPIC-FEEDBACK-REPORT.md`

### Dokümanlar (güncellendi)
- `docs/thesis-toolkit/pipeline-hatalari.md` — BUG-85..99
- `docs/thesis-toolkit/claude-hatalarim-ve-dersler.md` — KURAL 29-33
- `docs/thesis-toolkit/CLAUDE.md` — pipeline status
- `docs/thesis-toolkit/sprints/SPRINT-PLAN.md` — Sprint 13 satırı
- `docs/thesis-toolkit/tez-yazim-not-defteri.md` — Sprint 13 özeti
- `docs/thesis-toolkit/v10-todo.md` — BUG-85..99 sync notu

---

## TRUBA Çalıştırma

```bash
# Patch uygula
cd Desktop/hpcv1
git checkout truba_v2
git am sprint13-codex-and-thesis-plan.patch
git push

# TRUBA'ya aktar
scp -r hpcv1/ ahmacar@172.16.6.11:/arf/home/ahmacar/
ssh ahmacar@172.16.6.11
cd /arf/home/ahmacar/hpcv1

# Temizlik (yeni başlatma için)
rm -rf /arf/scratch/ahmacar/hpcv1_outputs/pfaz_*/
rm -f pfaz_status.json

# Submit
chmod +x truba/slurm_jobs/*.sh setup_truba.sh
bash setup_truba.sh
./truba/slurm_jobs/submit_all.sh
```

**Beklenen süre:** Job1: 2-3h | Job2: 14-27h | Job3: 7-15h | Job4: 2-3h | **Toplam: 25-48h**

---

## Sonraki Adım: Sprint 14 — PFAZ10 Rewrite

Bkz: `sprint-14-pfaz10-rewrite-plan.md`

PFAZ10 şu an yanlış konu üretiyor (binding energy yazıyor, proje magnetic+quadrupole moments).
Sprint 14 planı Claude Code için hazır -- Kemal "bu dosyayı oku ve yap" diyecek.
