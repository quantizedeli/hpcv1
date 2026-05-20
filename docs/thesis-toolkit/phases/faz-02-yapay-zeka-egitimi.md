# PFAZ 02 -- Paralel Yapay Zeka Egitimi
**Surum:** v3.0 | **Ilk Tarih:** 2026-05-03 | **Son Guncelleme:** 2026-05-14 (Sprint 13)
**TRUBA Job:** Job 2 (`truba/slurm_jobs/job2_pfaz02_03.sh`, 1 gun limit, -c 112)

---

## 1. Faz Karti

| Alan | Deger |
|------|-------|
| Faz No | PFAZ 02 |
| Ana Sinif | `ParallelAITrainer` |
| Modul | `pfaz_modules/pfaz02_ai_training/` |
| Durum (2026-05-03) | running 50% (aktif hesap devam ediyor) |
| Giris | PFAZ 01 ciktisi: train.csv / val.csv / test.csv |
| Cikti | `outputs/trained_models/{dataset}/{model}/{config}/` |
| Aktif Modeller | **RF, XGBoost** (Sprint 15 sonrasi -- LGB/CB/SVR/DNN cikarildi: BUG-104, KURAL 38) |
| Resmi Konfig | **20** (top RF/XGB) -- Sprint 15 oncesi 50 (cikti taramasi sonucu 30 cop config) |
| CV Stratejisi | 5-fold (CrossValidationAnalyzer) |
| Paralel | ThreadPoolExecutor |
| Seed | 42 sabit (parallel_ai_trainer.py:1363) |
| R2 Kayit Esigi | val_R2 >= 0.5 (POOR_R2_FILTER) + cv_R2 >= 0.0 + gap < 0.6 (DUAL_FILTER, Sprint 8 BUG-62 ile gercekten aktif) |
| RobustnessTester | AKTIF (Sprint 13 BUG-96): noise + outlier + perturbation testleri her AI modeli icin |
| Konfig Kaynagi | `training_configs_50.json` (Sprint 12 BUG-78): hardcoded `_create_default_configs()` artik degil |
| PFAZ Bagimliligi | PFAZ2 FAIL --> PFAZ3 SKIP (Sprint 13 BUG-91) |

---

## 2. Amac ve Bilimsel Motivasyon

PFAZ 02, PFAZ 01'in urettigi 848+ veri kumesi uzerinde 6 farkli ML algoritmasini sistematik
bicimde egitir; val_R2 >= 0.5 esigini gecen modelleri PKL olarak kaydeder; ileri fazlar icin
(PFAZ 04/05/06/07/09) kullanilabilir en iyi model havuzunu olusturur.

### Neden 6 Farkli Algoritma?

267 cekirdeklik nukleer veri seti, ML dunyasinda 'kucuk orneklem' sinifindadir. Bu durumda
tek bir algoritmayla en iyi sonucu almak teorik olarak garantilenemiyor. Her model farklı bir
matematiksel yaklasimi temsil eder ve birbirini tamamlar:

| Algoritma | Matematiksel Kok | Nukleer Fizik Gerekcesi |
|-----------|-----------------|------------------------|
| RF | Bootstrap aggregation + CART | 267 ornekle guvenilir, overfitting direnci yuksek |
| XGBoost | Gradient boosting + reg. | Nonlineer MM/QM iliskileri; Z^2, N-Z etkilesimleri |
| LightGBM | Leaf-wise boosting | Buyuk ozellik setlerinde (24 ozellik) hiz + derinlik |
| CatBoost | Ordered boosting | PARITY ve magic_character gibi kategorik ozellikler |
| SVR | SRM + RBF kernel | Kucuk orneklem garanti (SRM); margin maximization |
| DNN | Derin temsil ogrenmesi | Ust-duzey etkilesimler; yalnizca boyut>=200 |

Bu 6 model bir araya geldiginde hem teorik saglamlik hem de pratik kapsamlilik saglanir.
Ensemble (PFAZ 07) bu modellerin en iyi tahminlerini birlestirerek daha guclu sonuclar uretir.

### config.json ile Kod Arasindaki Uyumsuzluk

config.json dosyasi modeller listesini ['RF', 'GBM', 'XGBoost', 'DNN', 'BNN', 'PINN'] seklinde
gosterse de aktif pipeline'da yalnizca RF, XGBoost, LightGBM, CatBoost, SVR, DNN calisir.
GBM/BNN/PINN, ana egitim dongusuне (train_all_models_parallel) entegre edilmemistir.
DNN ise varsayilan olarak use_advanced_models=False nedeniyle devre disi; acik aktivasyon gerektirir.

---

## 3. Mimari Genel Bakis

```
ParallelAITrainer.train_all_models_parallel()  # 9-adim ana akis
|
+-- Adim 1: Dataset tarama   outputs/generated_datasets/
+-- Adim 2: Is parcasi uret  (dataset x config) kombinasyonlari
+-- Adim 3: Paralel egitim   ThreadPoolExecutor, seed=42
+-- Adim 4: Kalite filtresi  val_R2 < 0.5 -> POOR_R2_FILTER
+-- Adim 5: PKL kayit        model_*.pkl + metrics_*.json
+-- Adim 6: Checkpoint       completed.json, resume destekli
+-- Adim 7: 5-fold CV        train+val birlestirme, test dahil degil
+-- Adim 8: Overfitting det. 5 siddet sinifi (none/mild/moderate/severe/extreme)
+-- Adim 9: Ozet rapor       summary.json + summary.xlsx
|
+-- Model Siniflar:
    RF     -> RandomForestTrainer      (sklearn)
    XGB    -> XGBoostTrainer           (xgboost)
    LGB    -> LightGBMTrainer          (lightgbm)
    CAT    -> CatBoostTrainer          (catboost)
    SVR    -> SVRTrainer               (sklearn, ic SS)
    DNN    -> DNNTrainer               (tensorflow, ic SS, Huber)
```

---## 4. 6-Model Karsilastirma Tablosu

### 4.1 Algoritma Profili

| Ozellik | RF | XGBoost | LightGBM | CatBoost | SVR | DNN |
|---------|-----|---------|----------|----------|-----|-----|
| Tur | Bagging | Boosting | Boosting | Boosting | Kernel | Derin Ag |
| Konfig sayisi | 20 | 15 | 1 (def.) | 1 (def.) | 1 (def.) | 15 |
| Konfig ID | RF_001-020 | XGB_021-035 | LGB_default | CAT_default | SVR_default | DNN_036-050 |
| n_estimators | 50-300 | 50-300 | 100 | 1000 | N/A | N/A |
| max_depth | 5-None | 3-8 | 31 (def.) | 6 (def.) | N/A | N/A |
| learning_rate | N/A | 0.01-0.3 | 0.1 (def.) | 0.03 (def.) | N/A | 0.0003-0.001 |
| Kernel | N/A | N/A | N/A | N/A | RBF C=10 | N/A |
| Mimari | N/A | N/A | N/A | N/A | N/A | 2-4 katman |
| Ic olcekleme | Hayir | Hayir | Hayir | Hayir | Evet (SS) | Evet (SS) |
| GPU | Hayir | Opsiyonel | Opsiyonel | Opsiyonel | Hayir | Evet (TF) |
| Feature imp. | SHAP | SHAP | SHAP | SHAP | Yok | Permutation |
| Min ornek (is) | 30 | 30 | 30 | 30 | 30 | 200 |
| Kategorik | Label enc. | Label enc. | Label enc. | Dogal | Label enc. | Label enc. |
| Yorumlanabilir | Yuksek | Yuksek | Orta | Orta | Dusuk | Cok dusuk |
| Egitim hizi | Orta | Orta | Hizli | Yavas | Hizli | Cok yavas |

*SS = StandardScaler (ic; PFAZ01 olceklemesinden bagimsiz)*

### 4.2 Model Performans Ozeti (Ensemble Sonuclarindan, PFAZ 07)

PFAZ 07 (Ensemble) sonuclari PFAZ 02 modellerinin birlesik gucunu ortaya koyar:

| Ensemble Yontemi | R2 | RMSE |
|-----------------|----|------|
| Stacking MLP (en iyi) | 0.9794 | 0.5625 |
| Stacking Ridge | 0.9789 | -- |
| Stacking RF | 0.9744 | -- |
| Simple Voting | 0.9675 | -- |
| AdaBoost (en kotu) | 0.8282 | -- |
| Ortalama | 0.9616 | -- |
| Std. Sapma | 0.0405 | -- |

*Kaynak: repo/ensemble_results/evaluation/comprehensive_report.json (12 ensemble yontemi)*

### 4.3 Neden Bu Model Secimi? — Tasarim Kararlari

**RF — Ana Referans (20 konfigurasyon)**
Kucuk orneklemde overfitting direnci nedeniyle en fazla konfigurasyona sahip model.
Random feature selection ve bootstrap aggregation ile bias-variance dengesi optimal.
SHAP uyumluluguyla tez metodoloji bolumune dogrudan katki saglar.
20 farkli n_estimators/max_depth kombinasyonu, veri kumesi buyuklugune gore en iyi
ag derinligini otomatik bulmaya olanak verir.

**XGBoost — Performans Motoru (15 konfigurasyon)**
Gradient boosting'in olgunlasmis uygulamasi; L1+L2 regularizasyon ile guvenli.
Z^2/A^(1/3) gibi nukleer formullerdeki karesel ve kesirli bagintilari yakalamada
RF'ten genellikle ustundur. learning_rate araligı (0.01-0.3) ile hem hizli hem
dikkatli ogrenme senaryolari test edilir.

**LightGBM — Verimlilik Cozumu (1 varsayilan konfigurasyon)**
Physics ve Advanced ozellik setlerinin (20-24 ozellik) işlendiginde hiz avantaji ortaya cikar.
Leaf-wise buyume ile derin karar sinirları; histogram-based ile hafiza verimliligi.
Tek konfigurasyon, varsayılan parametrelerin kucuk-orta olcekli nuclear veri setlerinde
yeterli performansi kanitlanmis olmasi nedeniyle secilmistir.

**CatBoost — Kategorik Uzmanlik (1 varsayilan konfigurasyon)**
PARITY ({-1,+1}) ve magic_character ({0,1,2,3}) gibi fiziksel kategorik ozelliklerin dogal
islenmesi, target leakage riskini en aza indirir. Ordered boosting ile test seti bilgisi
egitimi etkilemez — kucuk split boyutlarinda kritik.

**SVR — Teorik Kalkan (1 varsayilan konfigurasyon)**
Structural Risk Minimization prensibi, kucuk N ile yuksek boyutlu uzayda genellesme
garantisi saglar. Ic StandardScaler ile PFAZ01 olceklemesinden bagimsiz calismasi
olcekleme bugu riskini sifirlar. RBF kernel, radyal simetrik nukleer kuvvet alanlarini
modellemekle sezgisel bir baglantiya sahiptir.

**DNN — Kapasite Yatirimi (15 konfigurasyon)**
Ust-duzey ozellik etkilesimlerini ogrenme kapasitesi. Ancak DNN_MIN_SAMPLES=200 kisiti
nedeniyle yalnizca boyut>=200 veri kumelerinde calisir (75/100 boyutlu veri kumelerinde
is uretilmez). Huber loss ile outlier dayanikliligi; EarlyStopping ile asiri egitim onlemi.

---## 5. Konfigurасyon Detaylari

### 5.1 RF Konfigurasyonlari (RF_001 - RF_020)

*Kaynak: parallel_ai_trainer.py:1907-1916 _create_default_configs()*

| ID | n_estimators | max_depth | min_samples_split | Strateji |
|----|-------------|-----------|-------------------|---------|
| RF_001 | 50 | 5 | 2 | Sığ, hafif |
| RF_002 | 50 | 10 | 2 | Orta derinlik |
| RF_003 | 50 | 15 | 2 | Derin, az agac |
| RF_004 | 50 | None | 2 | Tam derinlik, az agac |
| RF_005 | 100 | 5 | 2 | Sığ, standart |
| RF_006 | 100 | 10 | 2 | Dengeli |
| RF_007 | 100 | 15 | 2 | Derin, orta agac |
| RF_008 | 100 | None | 2 | Tam derinlik, orta agac |
| RF_009 | 200 | 5 | 2 | Sığ, fazla agac |
| RF_010 | 200 | 10 | 2 | Orta, fazla agac |
| RF_011 | 200 | 15 | 2 | Derin, fazla agac |
| RF_012 | 200 | None | 2 | Tam derinlik, fazla agac |
| RF_013 | 100 | 10 | 5 | Buyuk split min |
| RF_014 | 100 | 10 | 10 | Cok buyuk split min |
| RF_015 | 200 | 15 | 5 | Buyuk split min, derin |
| RF_016 | 200 | 15 | 10 | Cok buyuk split min, derin |
| RF_017 | 150 | 8 | 3 | Denge odaklı |
| RF_018 | 150 | 12 | 4 | Denge odakli v2 |
| RF_019 | 300 | 10 | 2 | Cok agac, orta derinlik |
| RF_020 | 300 | 20 | 5 | Maksimum kapasiteli RF |

### 5.2 XGBoost Konfigurasyonlari (XGB_021 - XGB_035)

*Kaynak: parallel_ai_trainer.py:1919-1927 _create_default_configs()*

| ID | n_estimators | learning_rate | max_depth | Strateji |
|----|-------------|---------------|-----------|---------|
| XGB_021 | 50 | 0.10 | 3 | Hizli, sığ |
| XGB_022 | 50 | 0.10 | 6 | Hizli, derin |
| XGB_023 | 50 | 0.30 | 3 | Agresif, sığ |
| XGB_024 | 50 | 0.30 | 6 | Agresif, derin |
| XGB_025 | 100 | 0.10 | 3 | Dengeli, sığ |
| XGB_026 | 100 | 0.10 | 6 | Dengeli, derin |
| XGB_027 | 100 | 0.30 | 3 | Agresif-orta, sığ |
| XGB_028 | 100 | 0.30 | 6 | Agresif-orta, derin |
| XGB_029 | 200 | 0.05 | 5 | Yavas, orta |
| XGB_030 | 200 | 0.10 | 5 | Standart-orta |
| XGB_031 | 200 | 0.20 | 5 | Hizli-orta |
| XGB_032 | 150 | 0.15 | 4 | Denge |
| XGB_033 | 150 | 0.20 | 6 | Agresif-orta v2 |
| XGB_034 | 300 | 0.10 | 4 | Fazla agac, orta derinlik |
| XGB_035 | 300 | 0.05 | 8 | Maksimum kapasiteli XGB |

### 5.3 DNN Konfigurasyonlari (DNN_036 - DNN_050)

*Kaynak: parallel_ai_trainer.py:1930-1957 _create_default_configs()*
*NOT: use_advanced_models=True gerektirir; train_size < 200 -> is uretilmez*

| ID | Mimari | Dropout | LR | Batch | Not |
|----|--------|---------|-----|-------|-----|
| DNN_036 | [128,64,32] | [0.1,0.1,0.0] | 0.001 | 32 | Temel referans |
| DNN_037 | [256,128,64] | [0.1,0.1,0.1] | 0.001 | 32 | Buyutulmus |
| DNN_038 | [512,256,128,64] | [0.2,0.2,0.1,0.1] | 0.001 | 64 | 4 katman, genis |
| DNN_039 | [128,64] | [0.1,0.0] | 0.001 | 32 | Ince 2-katman; lr fix 0.01->0.001 |
| DNN_040 | [256,128] | [0.2,0.1] | 0.001 | 64 | Orta 2-katman |
| DNN_041 | [512,256] | [0.2,0.2] | 0.0005 | 64 | Genis 2-katman, dusuk LR |
| DNN_042 | [256,256,128] | [0.1,0.1,0.1] | 0.001 | 32 | Uniform genislik |
| DNN_043 | [128,128,64,32] | [0.1,0.1,0.1,0.0] | 0.001 | 32 | 4-katman ortasi |
| DNN_044 | [512,256,128] | [0.3,0.2,0.1] | 0.0005 | 128 | Buyuk batch, yuksek dropout |
| DNN_045 | [256,128,64,32] | [0.2,0.1,0.1,0.0] | 0.001 | 64 | Azalan piramit |
| DNN_046 | [128,64,32,16] | [0.1,0.1,0.1,0.0] | 0.001 | 32 | Ince piramit; lr fix 0.002->0.001 |
| DNN_047 | [512,384,256] | [0.2,0.2,0.1] | 0.001 | 64 | Genis-orta piramit |
| DNN_048 | [384,256,128,64] | [0.2,0.2,0.1,0.1] | 0.001 | 64 | Denizci piramit |
| DNN_049 | [256,192,128,64] | [0.1,0.1,0.1,0.1] | 0.001 | 32 | Ince gecis |
| DNN_050 | [512,512,256,128] | [0.3,0.2,0.2,0.1] | 0.0003 | 128 | Max kapasite, en dusuk LR |

*lr fix = Gecmiste irilesme (divergence) olanlar icin duzeltilmis ogrenme hizi*

---

## 6. Egitim Sureci Detaylari

### 6.1 Kalite Filtreleme Mekanizmasi

Bir model egitimden sonra 5 adimlik kontrol surecine tabi tutulur (Sprint 1 — 2026-05-08):

```
val_R2 hesapla
   |
   +-- val_R2 < 0.5    -> POOR_R2_FILTER etiketi, PKL kaydedilmez
   |
   +-- DNN'de val_R2 < -2.0  -> DIVERGED etiketi, erken cik
   |
   +-- val_R2 >= 0.5   -> CV calistir (N<150: 3-fold, N>=150: 5-fold)
                             |
                             +-- cv_R2 < 0.0  -> DUAL_FILTER_RET, PKL kaydedilmez
                             |
                             +-- gap >= 0.6   -> DUAL_FILTER_RET, PKL kaydedilmez
                             |
                             +-- tum kriterler gecti -> PKL kaydet + metrikleri yaz
```

> **Sprint 8 Duzeltme Notu (BUG-62, 2026-05-12):**
> Sprint 1 belgesi bu akisi tanimlamisti ancak `ParallelAITrainer.__init__` imzasinda
> `cv_r2_min_threshold`, `max_train_cv_gap` vb. parametreler **yoktu**. main.py
> parametreleri geciriyordu ama constructor kabul etmiyordu -- CV gate hic calismadi.
> Sprint 8'de constructor imzasina 5 parametre eklendi ve DUAL_FILTER blogu model
> kaydinin ONCESINE tasinarak gate gercekten aktif hale getirildi (commit 2f1e594).
> Bkz. KURAL 22: constructor imza + atama + kullanim uclu dogrulama.

**Cift R2 Filtresi Literatur Destegi:**
- cv_R2 >= 0.0: Shang et al. (2022) — nukleer ozellik tahmininde val R2 tek basina yetersiz
- gap < 0.6: Utama et al. (2016) — nukleer kutle BNN calismasi; train-test R2 fark analizi
  *(Not: Sprint 8'de 0.5'ten 0.6'ya revize edildi. N<100 dataset'lerde 3-fold CV yuksek
  varyans uretiyor; 0.5 esigi bu durumlarda yanlis alarm veriyordu. Vabalas et al. 2019
  kucuk orneklem CV varyansi referans. gap >= 0.6 hala guclu overfit olarak isaretlenir.)*

Bu filtre, log analizinde tespit edilen asiri uyum modellerinin (train_R2=0.99 ama cv_R2=-0.31)
ileri fazlara tasmasini onler. [DUAL_FILTER] log mesajlari: KABUL/RET bilgisi verir.

### 6.2 Veri Sizintisi Onlemi

Asagidaki kolonlar egitim oncesi veri kumesinden cikarilir:

| Kolon | Neden Cikarilir |
|-------|-----------------|
| `schmidt_moment` | MM hedefinin dogrudan fizik hesabi (MM proxy) |
| `Q0_intrinsic` | QM hedefinin ic degeri (QM proxy) |
| `Beta_2_estimated` | Beta_2 tahmini (Beta_2 proxy) |

### 6.3 5-Fold Capraz Dogrulama

- **Sinif:** CrossValidationAnalyzer (model_validator.py)
- **Veri:** train + val birlestirme; test hicbir zaman dahil edilmez
- **n_jobs:** _inner_n_jobs() -> 1 (eger _PFAZ_PARALLEL_ACTIVE=1) | -1 (yoksa)
- **Amac:** Test seti bias olmadan genellesme performansi olcumu
- **Cikti:** cv_mean_r2, cv_std_r2, cv_fold_scores

### 6.4 Asiri Uyum Tespiti

OverfittingDetector, train_R2 ile val_R2 farkini izler:

| Sinif | Gap Aralik | Anlami |
|------|-----------|--------|
| none | < 5% | Saglikli genellesme |
| mild | 5-10% | Hafif, kabul edilebilir |
| moderate | 10-20% | Orta, izlenmeli |
| severe | 20-40% | Ciddi, regularizasyon gerekli |
| extreme | >= 40% | Asiri, kullanilmamali |

### 6.5 Cift R2 Filtresi (Sprint 1 — 2026-05-08)

**Gerekcesi:** Log analizi (2026-04-30) train_R2=0.9967 ama cv_R2=-0.31 olan modellerin
kaydedildigini gosterdi. Tek val_R2 filtresi 15 orneklik dogrulama seti uzerinden
hesaplandigi icin kucuk N'de yaniltici olabilir.

**Yeni Kriter (3 kosul birden saglandi):**
- `val_R2 >= 0.5` (mevcut — POOR_R2_FILTER)
- `cv_R2 >= 0.0` (yeni: en az ortalamadan iyi — genel ML standardı)
- `gap = train_R2 - cv_R2 < 0.5` (yeni: asiri uyum kontrolu)

**Adaptif Fold Sayisi:**
- N < 150 ornekli egitim seti → 3-fold CV (fold basi ~33 ornek)
- N >= 150 ornekli egitim seti → 5-fold CV

**Literatur Destegi:**
- Shang et al. (2022): nükleer özellik tahmininde train-test gap >0.2-0.3 asiri uyum sinyali
- Utama et al. (2016): nukleer kutle ML'de CV zorunlu; R2=0.96 basan
- Genel ML: cv_R2 < 0 → model anlamsız (ortalamadan kötü)

**Log Mesajlari:**
- `[DUAL_FILTER] ... KABUL` — 3 kriter geçildi, model kaydedildi
- `[DUAL_FILTER_RET] ... cv_R2=X < 0.0` — cv_R2 eşiği geçilemedi
- `[DUAL_FILTER_RET] ... gap=X >= 0.6` — gap eşiği geçilemedi

**Tez Notu:** Cift filtrenin istatistiksel gerekçesi Metodoloji §3.5'e girmeli.
Seckili cumle: "cv_R2 >= 0.0 kosulu Shang et al. (2022) metodolojisini temel alir..."

## 7. Gercek Pipeline Ciktilari

### 7.1 Durum (pfaz_status.json, 2026-05-03)

| Alan | Deger |
|------|-------|
| Durum | running |
| Ilerleme | 50% |
| Aciklama | Aktif hesap devam ediyor (3 gundur) |
| PKL model (mevcut) | 0 (tamamlanmamis calisma) |

Onceki tamamlanmis calismanin en iyi sonuclari PFAZ 07 Ensemble tarafindan tutuluyor.

### 7.2 Cikti Dizin Yapisi

```
outputs/trained_models/
  {dataset_name}/                  # ornek: MM_150_S70_Standard_Standard_Random
    {model_type}/                  # RF | XGBoost | SVR | ...
      {config_id}/                 # RF_001 | XGB_021 | DNN_036 | ...
        model_{config_id}.pkl      # Egitilmis model (val_R2>=0.5 ise)
        metrics_{config_id}.json   # R2, MAE, RMSE, CV, overfitting
        completed.json             # Checkpoint (resume icin)

  training_summary.json            # Tum is sonuclari
  training_summary.xlsx            # Excel: 3 sayfa (ozet/basarisiz/CV)
  seed_tracking_report.json        # Her modelin seed kaydi
```

### 7.3 metrics_{config_id}.json Icerigi

```json
{
  "config_id": "RF_001",
  "model_type": "RF",
  "dataset": "MM_150_S70_Standard_Standard_Random",
  "train_r2": 0.97, "val_r2": 0.89, "test_r2": 0.87,
  "train_mae": 0.21, "val_mae": 0.38, "test_mae": 0.41,
  "cv_mean_r2": 0.88, "cv_std_r2": 0.04,
  "overfitting_severity": "mild",
  "overfitting_gap_pct": 8.2,
  "filter_status": "passed",
  "seed": 42
}
```

---

## 8. Bilinen Hatalar

| Oncelik | Konum | Davranis | Mevcut Etkisi | Duzeltme |
|---------|-------|---------|--------------|---------|
| YUKSEK | woods_saxon.py:15 | HBAR_C import hatasi | WS ozellikleri 0/NaN | constants.py'e HBAR_C=197.327 ekle |
| ORTA | woods_saxon.py:73-75 | V_so/r_so/a_so eksik | Bug1 nedeniyle tetiklenmiyor | Bug1 duzeltildikten sonra ekle |
| DUSUK | parallel_ai_trainer.py:1363 | Seed hardcoded='Currently hardcoded' | Reproducibility kisıtli | config.json'a tasi |
| DUSUK | pipeline_v2.py:1193 | data_file_mat key hatasi | MAT egitimi kaldirildi | Try/except ile sarıl |

---

## 9. Sonraki Fazlara Bagimlilik

| Faz | Hangi Ciktıyı Kullanıyor | Kritik Metadata Alani |
|-----|--------------------------|----------------------|
| PFAZ 03 (ANFIS) | Yoktur (bagimsiz egitim) | -- |
| PFAZ 04 (Tahmin) | Top-25 PKL modeli | val_r2, feature_names, scaler_path |
| PFAZ 05 (Cross-Model) | Tum PKL modeller | model_type, config_id, val_r2 |
| PFAZ 06 (Raporlama) | summary.xlsx | Tum metrik alanlari |
| PFAZ 07 (Ensemble) | Top PKL modeller | val_r2 ile siralama |
| PFAZ 09 (Monte Carlo) | Per-model feature set | feature_names (metadata.json'dan) |

---

## 10. Kontrol Listesi

### Koddan Dogrulanan Parametreler

- [x] Aktif model listesi: RF, XGBoost, LightGBM, CatBoost, SVR, DNN (kod:1760-1776)
- [x] 50 konfig: 20 RF + 15 XGB + 15 DNN (kod:1894, _create_default_configs)
- [x] R2_MIN_SAVE_THRESHOLD = 0.5 (kod onceden dogrulandi)
- [x] DNN_MIN_SAMPLES degil; train_size < 200 -> is uretilmez (kod analizi)
- [x] seed=42 sabit (kod:1363 'Currently hardcoded' yorumu)
- [x] Veri sizintisi: 3 kolon cikarilir (schmidt_moment, Q0_intrinsic, Beta_2_estimated)

### Uretilen Ciktilar

- [ ] outputs/trained_models/{dataset}/{model}/{config}/model_*.pkl
- [ ] outputs/trained_models/training_summary.json
- [ ] outputs/trained_models/training_summary.xlsx
- [ ] outputs/trained_models/seed_tracking_report.json

### Ileri Faz Uyumluluğu

- [ ] PFAZ 04: top-25 model PKL mevcut mu?
- [ ] PFAZ 07: ensemble icin yeterli PKL var mi?
- [ ] feature_names metadata.json'a dogru yazildi mi?

---

*PFAZ 02 Belgesi v2.0 | 2026-05-03 | Kaynak: parallel_ai_trainer.py (2094 satir)*
### training_results_summary.xlsx -- Gercek Sayfa Yapisi (Kaynak Koddan)

**Kaynak:** `parallel_ai_trainer.py:1579-1663` -- `save_summary_report()`

| Sayfa | Icerik | Sutunlar | Neden Var? |
|-------|--------|---------|-----------|
| All_Results | Tum model sonuclari (300+ satir) | Model_Type, Config_ID, Dataset, PKL_Saved, Status_Note, Train_R2, Train_RMSE, Train_MAE, Val_R2, Val_RMSE, Val_MAE, Test_R2, Test_RMSE, Test_MAE, Training_Time_s, Error | Tek yerden tum egitim geri bakisi; Val_R2 sirali |
| RF_Models | RF sonuclari (filtreli) | Ayni sutunlar, Model_Type=RF | 20 konfigurasyonun performansi; n_estimators/max_depth etkisi |
| XGBoost_Models | XGBoost sonuclari | Ayni sutunlar, Model_Type=XGBoost | 15 konfigurasyonun performansi; n_estimators/lr/max_depth ucelisi |
| DNN_Models | DNN sonuclari | Ayni sutunlar, Model_Type=DNN | 15 konfigurasyonun performansi; sadece train_size>=200 ornekler |
| LightGBM_Models | LightGBM sonuclari (varsa) | Ayni sutunlar | -- |
| CatBoost_Models | CatBoost sonuclari (varsa) | Ayni sutunlar | -- |

**Ek JSON Ciktisi:** `training_summary.json`
```
{ job_id, model_type, config_id, dataset_name, success, training_time,
  metrics: { val: { r2, rmse, mae }, test: { r2, rmse, mae } },
  model_path, error }
```

**PKL_Saved Kolonu:** True = val_R2>=0.5 + cv_R2>=0.0 + gap<0.6 (DUAL_FILTER) kosullari saglandi, model kaydedildi; False = POOR_R2_FILTER veya CV_GATE_RET.
**Status_Note Kolonu:** POOR_R2_FILTER | CV_GATE_RET | DIVERGED | SMALL_DATASET | SUCCESS
**Training_Time_s Kolonu:** Saniye cinsinden; hiz karsilastirmasi icin.

---

## 11. Sprint 4-13 Guncellemeleri (2026-05-11 -> 2026-05-14)

Ilk surum 2026-05-03 tarihlidir. Asagidaki guncellemeler bu fazi dogrudan etkileyen sprint sonuclarini ozetler.

### 11.1 Sprint 8 BUG-62 -- CV Gate Gercekten Aktif

Sprint 1 (2026-05-08) "cv_R2>=0.0 + gap<0.5 filtresi eklendi" demisti. Sprint 8 (2026-05-12) Claude Code analizinde ortaya cikti ki **ParallelAITrainer constructor bu parametreleri kabul etmiyordu**. main.py 5 parametreyi geciriyordu ama hepsi sessizce kayboluyordu -- filtre hic calismiyordu.

**Sprint 8 duzeltmesi:**
- Constructor imzasina 5 parametre eklendi: `cv_r2_min_threshold`, `max_train_cv_gap`, `cv_folds`, `cv_folds_large_n`, `cv_large_n_threshold`
- Gate blogu kayit oncesine tasindi
- `max_train_cv_gap`: 0.5 -> **0.6** (kucuk N varyans toleransi, Vabalas et al. 2019)

**Tez metni:**
> "Model seciminde val_R2 esigine (>=0.5) ek olarak capraz dogrulama R2 esigi (>=0.0) ve train-CV ayrim aralig (gap<0.6) birlikte uygulanmistir. Bu cift filtre kucuk orneklem dogrulama kumesinin (N~15) yaniltici yuksek R2'sine karsi ek guvence saglar (Shang et al., 2022; Utama et al., 2016)."

### 11.2 Sprint 12 BUG-78 -- training_configs_50.json Deterministik

50 konfigurasyon hardcoded `_create_default_configs()` cagrisindan disari alindi:

- Dosya: `pfaz_modules/pfaz02_ai_training/training_configs_50.json`
- Icerik: 20 RF + 15 XGB + 15 DNN konfig
- Loglama: `[CFG-SOURCE] training_configs_50.json` mesaji TRUBA log'unda gozukur
- Yararlanim: TRUBA ve PC arasinda konfig farkı engellendi (KURAL 31 - Single Source of Truth)

### 11.3 Sprint 13 BUG-91 -- PFAZ2 FAIL -> PFAZ3 SKIP

run_all_pfaz akisinda yeni davranis:
- PFAZ2 status='failed' donerse, PFAZ3 otomatik 'skipped' isaretlenir
- Sebep: AI egitim ciktisi olmadan ANFIS dataset seciminin anlamsiz oldugu (BUG-91)
- main.py'de `_check_upstream_failure(pfaz_id)` helper ile

### 11.4 Sprint 13 BUG-96 -- RobustnessTester Aktif

Her AI modeli icin egitim sonrasi 3 robustness testi:
1. **Noise sensitivity:** Input ozelliklerine Gaussian gurultu (sigma=0.05) ekle, R2 dusus oranı
2. **Outlier impact:** Test setine sentetik outlier (IQR > 4) ekle, MSE artisi
3. **Feature perturbation:** Her ozelligi tek tek karistir (permutation), R2 dususu

Cikti dosyalari:
- `outputs/trained_models/robustness_summary.xlsx` (model x test matrisi)
- `outputs/trained_models/robustness_per_model/*.png` (PFAZ 8 ile entegre)

Tez metni icin §4.4 Saglamlik Analizi:
> "Egitilen modellerin saglamlik analizi uc agirlikli senaryoyla yapilmistir: girdi ozelliklerine sigma=0.05 standartlasmis Gaussian gurultu uygulanarak R^2 dususu olculmus; test seti sentetik IQR>4 outlier ile zenginlestirilmis ve MSE artisi raporlanmis; her ozellik tek tek permutation ile karistirilarak ozellik onem siralamasi cikarilmistir."

### 11.5 Sprint 13 BUG-87 -- optuna ve lightgbm REQUIRED_PACKAGES

`main.py:REQUIRED_PACKAGES` listesine eklendi -- artik opsiyonel degil. TRUBA strict_truba modunda eksiklik dogrudan RuntimeError verir.

### 11.6 TRUBA Operasyonel Notlar

- **Job:** `truba/slurm_jobs/job2_pfaz02_03.sh` (PFAZ2+PFAZ3 birlikte)
- **Sure limiti:** 1 gun (gercek ~14-27 saat beklenir)
- **Bellek:** TF GPU off (`CUDA_VISIBLE_DEVICES=""`), CPU-only
- **Memory leak guard:** `tf.keras.backend.clear_session() + gc.collect()` (Sprint 7 BUG-53)
- **Cikti:** `/arf/scratch/ahmacar/hpcv1_outputs/outputs/trained_models/`

### 11.7 KURAL Guncellemeleri (PFAZ 02'yi Etkileyenler)

| Kural | Icerik | PFAZ 02 Etkisi |
|-------|--------|---------------|
| KURAL 18 | "Belge != gercek fix"; kod dogrulama zorunlu | BUG-62 keşfi bu kuralla yapildi |
| KURAL 19 | Inter-PFAZ veri akisi her sprint sonu denetlenir | metadata.json zorunlu okuma |
| KURAL 29 | Plan sun, onay bekle | Yeni model tipi ekleme icin |
| KURAL 30 | Runtime behavior simulation (3 senaryo) | CV gate akış simulasyonu |
| KURAL 32 | VARSAYIM YASAGI; "muhtemelen" yerine grep/view | BUG-62 keşif yontemi |
| KURAL 33 | Cross-layer failure chain audit | PFAZ2 FAIL -> PFAZ3 SKIP zinciri |

---

*PFAZ 02 Belgesi v3.0 | Son Guncelleme: 2026-05-14*
*Kaynak: parallel_ai_trainer.py (2094 satir) + training_configs_50.json*

---

## 12. Sprint 15 Guncellemesi (2026-05-20) -- Kriz Sonrasi Yeniden Yapilandirma

### 12.1 Aktif Model Listesi: 6 -> 2 (RF + XGBoost)

**Onceki:** RF, XGBoost, LightGBM, CatBoost, SVR, DNN (kutuphane kuruluysa otomatik dahil).
**Sonra:** Sadece RF + XGBoost.

**Gerekce (BUG-104, KURAL 38):**
- Kod LightGBM/CatBoost/SVR'i `if X_AVAILABLE:` ile otomatik ekliyordu -- niyet vs davranis uyumsuzlugu
- TRUBA kalite haritasi (61283 model): DNN ort test_R² -0.020 (RF/XGB'nin yarisi), >0.8 sayisi 143
- LGB/CB/SVR koşulmus ama dizin yapisi BUG-103 ile tutarsiz (`SVR/RF_018/...`) -- guvenilir veri yok
- 105-200 ornek kucuk-veride agac modelleri (RF/XGB) literatur uyumlu en iyi secim (Grinsztajn 2022)

**Fix:** `config.json` -> `pfaz02.model_types = ["RF", "XGBoost"]`. Kod buradan okur (SSoT, KURAL 31).

### 12.2 Config Sayisi: 50 -> 20

Iyi 9 feature setinde 50 config taramasinda en iyi 20 config = 9 XGB + 11 RF (DNN'ler altta). Top-20 ort 0.226 ile genel ort 0.221 farki **0.005** -- istatistiksel olarak anlamsiz. Geriye kalan 30 config silinmiyor, sadece bu kosuda kullanilmiyor.

**Yeni dosya:** `training_configs_20.json` -- top 20 config (Sprint 11 BUG-78 ile tum config'ler `training_configs_50.json`'da; Sprint 15 alt-kume olusturuyor).

### 12.3 BUG-101 Resume Fix

`train_single_job` 5 erken-cikis yolundan 4'u (DIVERGED, POOR, dual cv RET, dual gap RET) `.pkl` ve `completed.json` yazmiyordu. Reddedilen ~54000 model her resume tekrar egitiliyordu. Yeni `_save_checkpoint()` helper'i eklendi; basari **ve** kalite-red yolu checkpoint yaziyor. Exception yolu (geçici hata) checkpoint yazmaz (B kararı, KURAL 35).

```python
# YENI: kalite filtresine takilan modeller icin checkpoint
def _save_checkpoint(out_dir, job_id, model_type, config_id, dataset_name,
                     success, metrics, training_time, error_message=None):
    """Resume'un is'i tekrar denememesi icin. Basarisiz da olsa 'denendi' demek."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'completed.json', 'w', encoding='utf-8') as f:
        json.dump({...}, f, indent=2)
```

Cagri 4 noktada: satir 1346 (POOR), 1368 (DIVERGED), 1423 (dual cv RET), 1438 (dual gap RET).

### 12.4 BUG-103 model_type x config Cikti Tutarsizligi

`create_training_jobs` 6 model_type × 50 config = 300 is/dataset uretiyordu. config_id prefix'i (RF_/XGB_/DNN_) ile model_type eslesmiyordu -> `SVR/RF_018/` tarzi cikti.

**Fix:** Job uretimi sirasinda prefix kontrolu zorunlu kilindi.

### 12.5 Yeni Kapsam (PFAZ1'den geliyor)

Sprint 15 kapsami (config.json -> pfaz01):
- **Feature setleri:** 9 iyi (AZB2EMCS, AZSB2E, AZS, ZB2EMCS, AZSMC, AZSMCB2E, AZSMCBEPA, AZSBEPA, AZSNNNP)
- **Senaryo:** Sadece S80
- **Anomaly modu:** Sadece vanilla
- **Boyut:** 150 + ALL
- **Sampling:** Random + Stratified
- **Scaling:** Sadece NoScaling

**Toplam dataset:** 36 (1468 -> 36, 40× azalma)
**Toplam AI is:** 36 × 2 model × 20 config = **1440 is** (250× azalma)
**Tahmini sure:** 110 worker × 250s ort = **~1 saat**

### 12.6 KURAL Guncellemeleri (Sprint 15)

| Kural | Icerik | PFAZ 02 Etkisi |
|-------|--------|----------------|
| KURAL 34 | Kriz aninda once teshis | TRUBA timeout'ta acil kalite haritasi |
| KURAL 35 | Checkpoint felsefesi (denendi mi, basarili mi degil) | BUG-101 fix temeli |
| KURAL 36 | AI/ANFIS feature seti ayrimi | DNN cikarildi, ANFIS ayri kapsamla |
| KURAL 37 | Negatif sonuc tez katkisi | Cop 15 FS feature ablation kaniti |
| KURAL 38 | Memory niyet != kod davranisi | BUG-104 keşfi |
| KURAL 39 | Inter-PFAZ tarama | PFAZ8 BUG-106 tespiti |
| KURAL 40 | Veri-bazli kucultme | Bu sprintin temel ilkesi |

---

*PFAZ 02 Belgesi v4.0 | Son Guncelleme: 2026-05-20 (Sprint 15)*
*Sprint 15 ekleri: BUG-101/103/104 fix, model listesi RF+XGB, config 20, KURAL 34-40*
