# PFAZ 02 Analiz Notu

> **Faz:** 02 -- Yapay Zeka Modeli Egitimi
> **Analiz Tarihi:** 2026-05-03
> **Durum:** Tamamlandi (v1.0)

---

## Analiz Ozeti

PFAZ 02 kaynak kodu tamamen okundu ve belgelendi. Asagidaki dosyalar analiz edildi:

- parallel_ai_trainer.py (2094 satir) -- ana egitim sistemi
- model_validator.py -- CrossValidationAnalyzer (5-fold CV)
- advanced_models.py -- BNN, PINN (devre disi)
- overfitting_detector.py -- OverfittingDetector (5 siddet sinifi)
- hyperparameter_tuner.py -- Optuna tuner (n_trials=50)
- seed_tracker.py -- SeedTracker (reproducibility)
- config.json -- proje konfigurasyonu

## Onemli Bulgular

### 1. Aktif Model Tipleri (Koddan Dogrulandi)

config.json yaniltici: [RF, GBM, XGBoost, DNN, BNN, PINN] yazıyor.
Gercek aktif tipler (parallel_ai_trainer.py:1760-1776):
  RF (her zaman), XGBoost, LightGBM, CatBoost, SVR (her zaman), DNN (use_advanced_models=True ise)

### 2. 50 Konfigurasyonun Dagilimi

  20 RF (RF_001-RF_020) + 15 XGBoost (XGB_021-XGB_035) + 15 DNN (DNN_036-DNN_050)
  LightGBM ve CatBoost icin konfigurasyonsuz -- varsayilan parametrelerle calisir.

### 3. Kalite Esikleri

  R2_MIN_SAVE_THRESHOLD = 0.5  (val_R2 < 0.5 --> POOR_R2_FILTER, PKL kaydedilmez)
  DNN sapma: val_R2 < -2.0 --> DIVERGED
  DNN boyut: train_size < 200 --> is olusturulmaz
  DNN minimum: DNN_MIN_SAMPLES = 80 --> ValueError

### 4. Veri Sizintisi Onlemi

  3 proxy sutun cikarilir: schmidt_moment, Q0_intrinsic, Beta_2_estimated
  metadata.json feature_names -- PFAZ09 Monte Carlo icin kritik bagimlilik

### 5. Bug Listesi

  DUSUK: seed=42 sabit (parallel_ai_trainer.py:1363)
  TASARIM KARARI: DNN default kapali (use_advanced_models=False)
  ORTA: LightGBM/CatBoost icin konfigurasyonsuz

## Kontrol Listesi

- [x] Aktif model tipleri koddan dogrulandi
- [x] 50 konfigurasyonun tam listesi cikartildi
- [x] DNN 15 konfigurasyon tablosu olusturuldu
- [x] Kalite filtreleri koddan onaylandi
- [x] Veri sizintisi onlemi belgelendi
- [x] 5-fold CV mekanizmasi belgelendi
- [x] Overfitting detector seviyeleri belgelendi
- [x] Cikti dizin yapisi belgelendi
- [x] PFAZ 04/05/07/09 bagimlilik zinciri belgelendi
- [x] Bug listesi (3 bug) belgelendi

## Uretilen Dokuman

phases/faz-02-yapay-zeka-egitimi.md -- 477 satir, 16 ana bolum

---

*PFAZ 02 Analiz Notu v1.0 | 2026-05-03*