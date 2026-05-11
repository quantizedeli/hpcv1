# Sprint 8 -- Eksik Fix Tamamlama (BUG-62/63/64)
## Durum: TAMAMLANDI 2026-05-12 | Oncelik: KRITIK

> **Bu sprint neden var:**
> Sprint 6 Claude Code analizi ortaya koydu ki Sprint 1/2/4 belgeleri
> "TAMAMLANDI" yazmasina ragmen kod gercegi farkli. KURAL 18 vakasi.
> En kritik: CV gate (Sprint 1) hic calismiyor -- constructor parametreleri
> kabul etmiyordu, main.py geciriyor ama hepsi sessizce kayboluyordu.

---

## Tespit Edilen Eksiklikler

### BUG-62 [KRITIK] -- CV Gate Hic Calismiyordu (Sprint 1 eksigi)

**Sorun:** ParallelAITrainer.__init__ imzasinda cv_r2_min_threshold,
max_train_cv_gap, cv_folds, cv_folds_large_n, cv_large_n_threshold parametreleri YOKTU.
main.py 5 parametreyi geciriyordu ama constructor kabul etmiyordu -- hepsi kayboldu.
Sonuc: tum modeller kaydediliyordu, CV gate hic devrede degildi.

**Fix:**
- Constructor imzasina 5 parametre eklendi
- DUAL_FILTER blogu model kaydinin ONCESINE tasinmasi
- Adaptif fold: N<150 -> cv_folds=3, N>=150 -> cv_folds_large_n=5
- [DUAL_FILTER] KABUL/RET log mesajlari
- Eski CV blogu (kayittan sonraki) kaldirildi
- max_train_cv_gap=0.6 (kucuk N icin 0.5 yanlis alarm uretti -- Vabalas 2019)

### BUG-63 [DUSUK] -- _configurations_note config'e Eklenmemis (Sprint 2 eksigi)

**Fix:** config.json pfaz03_anfis_training altina not eklendi.

### BUG-64 [ORTA] -- MC Sinif Default'lari Eksik (Sprint 4/BUG-38 eksigi)

**Sorun:** BUG-38'de DEFAULT_MC_CONFIG 100->1000 yapildi ama sinif __init__
default'lari guncellenmedi: MCDropoutSimulator=100, FeatureDropoutSimulator=500.

**Fix:** Her iki sinif __init__ default'i 1000'e cikartildi.

### Dual R2 Baglamli Mesajlar (Sprint 4 eksigi)

pfaz04/05/07'ye bos model durumunda DUAL_FILTER_RET baglami eklendi.

---

## Etkilenen Dosyalar

| Dosya | Degisiklik | Bug |
|-------|-----------|-----|
| pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py | Constructor + DUAL_FILTER gate | BUG-62 |
| pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py | MC default 1000 | BUG-64 |
| pfaz_modules/pfaz04_unknown_predictions/unknown_nuclei_predictor.py | Dual R2 uyari | Sprint 4 |
| pfaz_modules/pfaz05_cross_model/cross_model_evaluator.py | Dual R2 baglam | Sprint 4 |
| pfaz_modules/pfaz07_ensemble/pfaz7_complete_ensemble_pipeline.py | n_models=0 guard | Sprint 4 |
| config.json | _configurations_note + max_train_cv_gap=0.6 | BUG-63 |
| docs/thesis-toolkit/phases/faz-02-yapay-zeka-egitimi.md | 0.6 gerekce | doc |
| docs/thesis-toolkit/sprints/sprint-01-dual-r2-filtresi.md | 0.6 guncelleme | doc |
| docs/thesis-toolkit/pipeline-hatalari.md | BUG-62/63/64 eklendi | doc |
| docs/thesis-toolkit/tez-yazim-not-defteri.md | Sprint 8 ozeti | doc |

---

## Dogrulama

- 5/5 py_compile OK
- DUAL_FILTER blogu < Save pozisyonu: DOGRULANDI
- MC default'lar 1000: DOGRULANDI
- max_train_cv_gap=0.6: config.json DOGRULANDI

## Commit

hpcv1:  (sprint8-missing-fixes branch)
Patch: sprint8-only.patch

---

*Sprint 8 v1.0 | 2026-05-12 | BUG-62/63/64 + CV gate gercek implementasyon*
