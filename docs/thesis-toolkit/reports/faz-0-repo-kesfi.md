# Faz 0: Repo Keşfi — Bulgu Raporu

> **Hazırlayan:** Claude Code (Thesis AI Assistant)  
> **Tarih:** 2026-05-02  
> **Repo:** https://github.com/quantizedeli/v10  
> **Branch:** `dev-updates` (GitHub'da "dev updates"; Git tire ile normalize etti)  
> **Yerel Kopya:** `thesis-nuclear-ai/repo/`  
> **Durum:** ✅ Keşif tamamlandı — Plan onayı bekleniyor

---

## 1. Proje Özeti

| Alan | Değer |
|------|-------|
| Proje Adı | Nuclear Physics AI Project |
| Sürüm | 2.0.0 (Production Ready) |
| Geliştirici | Kemal Bey |
| Tarih | Kasım 2025 — Nisan 2026 |
| Hedef | 267 çekirdeğin manyetik moment (MM) ve kuadrupol moment (QM) tahmini |
| Yaklaşım | Makine Öğrenmesi + ANFIS hibrit sistemi |
| Faz Sayısı | 13 faz (PFAZ 01–13); PFAZ 11 kasıtlı devre dışı |

---

## 2. Veri Kaynağı

### 2.1 Ana Veri Dosyası

**Konum:** `repo/data/aaa2.txt`  
**Format:** Tab-separated (TSV), başlık satırı mevcut  
**Kayıt sayısı:** 267 çekirdek  

**Kolonlar (aaa2.txt başlık satırından tespit edilmiştir):**

| Sütun | Açıklama | Örnek |
|-------|----------|-------|
| NUCLEUS | Çekirdek tanımlayıcısı | `3 Li 6` |
| A | Kütle numarası | 6 |
| Z | Proton sayısı | 3 |
| N | Nötron sayısı | 3 |
| SPIN | Spin kuantum sayısı | 1 |
| PARITY | Parite (+1 / -1) | 1 |
| P-factor | P faktörü | 0.5 |
| Beta_2 | Kuadrupol deformasyon parametresi | 1.024 (bazı çekirdekler için boş) |
| MAGNETIC MOMENT [µ] | Manyetik moment (µ_N birimi) | 0.82205667 |
| QUADRUPOLE MOMENT [Q] | Kuadrupol moment (barn) | -0.00083 |
| Nn | Valans nötron sayısı | 1 |
| Np | Valans proton sayısı | 1 |

**Türetilen özellik sayısı:** 44+ (PFAZ 1'de özellik mühendisliği ile elde edilir — SEMF, Woods-Saxon, Nilsson, Shell modeli katkıları dahil)

---

## 3. Repo Üst Düzey Yapısı (3 Seviye)

```
repo/
├── main.py                               ← Ana orkestratör (v6.0.0)
├── run_complete_pipeline.py              ← Tam pipeline çalıştırıcı
├── config.json                           ← Merkezi konfigürasyon (tüm fazlar)
├── pfaz_status.json                      ← Faz durum takibi (auto-managed)
├── requirements.txt                      ← Python bağımlılıkları
├── requirements-hpc.txt                  ← HPC versiyonu
├── CLAUDE.md                             ← Repo'nun kendi Claude kılavuzu
├── PFAZ_DEVELOPMENT_NOTES.md            ← Per-faz değişiklik günlüğü
├── PIPELINE_STATUS_REPORT.md            ← Son çalışma durum raporu
├── QA_WIRING_REPORT.md / QA_PROJECT_STATUS_REPORT.md
├── data/
│   └── aaa2.txt                          ← 267 çekirdeğin deneysel verisi
├── pfaz_modules/
│   ├── pfaz01_dataset_generation/        (14 .py dosyası)
│   ├── pfaz02_ai_training/               (11 .py dosyası)
│   ├── pfaz03_anfis_training/            (9 .py dosyası)
│   ├── pfaz04_unknown_predictions/       (4 .py dosyası)
│   ├── pfaz05_cross_model/               (6 .py dosyası)
│   ├── pfaz06_final_reporting/           (8 .py dosyası)
│   ├── pfaz07_ensemble/                  (6 .py dosyası)
│   ├── pfaz08_visualization/             (13 .py dosyası)
│   ├── pfaz09_aaa2_monte_carlo/          (5 .py dosyası)
│   ├── pfaz10_thesis_compilation/        (10 .py dosyası)
│   ├── pfaz11_production/                (5 .py dosyası — DEVRE DIŞI)
│   ├── pfaz12_advanced_analytics/        (6 .py dosyası)
│   └── pfaz13_automl/                    (8 .py dosyası)
├── core_modules/
│   ├── anomaly_detector.py
│   ├── constants.py                      ← Tüm sabitler, dataset boyutları, S70/S80
│   ├── feature_set_builder.py
│   ├── json_utils.py
│   └── progress_tracker.py
├── physics_modules/
│   ├── semf_calculator.py                ← Bethe-Weizsäcker SEMF
│   ├── woods_saxon.py                    ← Woods-Saxon potansiyeli
│   ├── nilsson_model.py                  ← Nilsson modeli
│   └── theoretical_calculations_manager.py
├── analysis_modules/
│   ├── model_interpretability.py
│   ├── real_data_integration_manager.py
│   └── robustness_validation_manager.py
├── visualization_modules/               ← Görselleştirme entegrasyon yardımcıları
├── utils/
│   └── warning_tracker.py               ← Pipeline-geneli uyarı takipçisi (singleton)
├── scripts/
│   ├── health_check.py
│   ├── check_pfaz_completeness.py
│   └── log_parser.py
├── tests/
│   ├── test_smoke/
│   ├── test_units/
│   └── test_integration/
└── reports/                             ← Çalışma zamanı çıktı raporları
```

---

## 4. Faz Yapısı

### 4.1 "Faz" Kavramının Kodda Temsili

Proje, "faz" kavramını **`pfaz_` ön ekli klasörler** ile ifade etmektedir (`pfaz` = "proje fazı" kısaltması). Her faz:
- `pfaz_modules/pfaz{NN}_*/` altında bağımsız Python paketi
- `pfaz_status.json` içinde durum kaydı (`pending / running / completed / failed / skipped`)
- `main.py` orkestratörü tarafından `PIPELINE_EXECUTION_ORDER` sırasına göre çağrılır

### 4.2 Faz Listesi (repo/CLAUDE.md + pfaz_status.json'dan)

| PFAZ | Ad | Ana Sınıf | .py | pfaz_status.json Durumu |
|------|-----|-----------|-----|------------------------|
| 01 | Veri Kümesi Üretimi | `DatasetGenerationPipelineV2` | 14 | running (50%) |
| 02 | Yapay Zeka Eğitimi | `ParallelAITrainer` | 11 | running (50%) |
| 03 | ANFIS Eğitimi | `ANFISParallelTrainerV2` | 9 | completed (100%) |
| 04 | Bilinmeyen Çekirdek Tahminleri | `UnknownNucleiPredictor` | 4 | completed (100%) |
| 05 | Çapraz Model Analizi | `CrossModelEvaluator` | 6 | completed (100%) |
| 06 | Final Raporlama | `ComprehensiveExcelReporter` | 8 | completed (100%) |
| 07 | Topluluk & Meta-Modeller | `EnsemblePipeline` | 6 | completed (100%) |
| 08 | Görselleştirme | `VisualizationSystem` | 13 | completed (100%) |
| 09 | Monte Carlo Analizi (aaa2) | `MonteCarloSimulationSystem` | 5 | completed (100%) |
| 10 | Tez Derleme (LaTeX) | `ThesisCompilationSystem` | 10 | running (50%) |
| 11 | Üretim Dağıtımı | — | 5 | **skipped (kasıtlı)** |
| 12 | İleri İstatistiksel Analitik | `StatisticalTestingSuite` | 6 | failed |
| 13 | AutoML Yeniden Eğitim | `AutoMLRetrainingLoop` | 8 | failed |

### 4.3 Doğru Yürütme Sırası

`main.py` içindeki `PIPELINE_EXECUTION_ORDER` sabiti (Bug #39 düzeltmesinden, `PFAZ_DEVELOPMENT_NOTES.md:57`):

```python
PIPELINE_EXECUTION_ORDER = [1, 2, 3, 4, 5, 7, 9, 12, 13, 6, 8, 10, 11]
```

Kritik bağımlılıklar:
- **PFAZ 6** (Raporlama) → PFAZ 9 ve 13'ün çıktılarından **sonra** çalışmalı
- **PFAZ 10** (Tez) → PFAZ 12 ve 13'ün içeriklerinden **sonra** çalışmalı
- **PFAZ 8** (Görselleştirme, 2. geçiş) → PFAZ 9/12/13 verilerini kullanır

---

## 5. Teknoloji Yığını

### 5.1 Temel Kütüphaneler (requirements.txt)

| Kategori | Kütüphaneler |
|----------|-------------|
| Bilimsel Hesaplama | numpy ≥1.24, pandas ≥2.0, scipy ≥1.10 |
| Makine Öğrenmesi | scikit-learn ≥1.3, xgboost ≥2.0, lightgbm ≥4.0, catboost ≥1.2 |
| Derin Öğrenme | tensorflow ≥2.13 (birincil); torch (opsiyonel, requirements'ta yorum satırında) |
| Hiper-parametre Optimizasyonu | optuna ≥3.3, hyperopt ≥0.2.7 |
| Görselleştirme | matplotlib ≥3.7, seaborn ≥0.12, plotly ≥5.17 |
| İstatistiksel Analiz | statsmodels ≥0.14, pingouin ≥0.5.3 |
| Model Yorumlanabilirlik | shap ≥0.43 |
| I/O & Raporlama | openpyxl, xlsxwriter, h5py, jinja2, pyarrow |
| Test | pytest ≥7.4, pytest-cov ≥4.1 |

> **Not:** Uproot, ROOT (CERN), MCNP wrapper gibi nükleer fizik özel kütüphaneleri **kullanılmamaktadır.** Tüm nükleer fizik hesapları özel geliştirilmiş `physics_modules/` modülleriyle yapılmaktadır.

### 5.2 Özel Nükleer Fizik Modülleri

| Modül | Dosya | Hesapladığı |
|-------|-------|-------------|
| Bethe-Weizsäcker SEMF | `physics_modules/semf_calculator.py` | Bağlanma enerjisi, kütle fazlası, pairing terimi |
| Woods-Saxon Potansiyeli | `physics_modules/woods_saxon.py` | Tek-parçacık enerji seviyeleri, spin-orbit terimi |
| Nilsson Modeli | `physics_modules/nilsson_model.py` | Deformasyon etkisi, Nilsson kuantum sayıları |
| Teorik Yönetici | `physics_modules/theoretical_calculations_manager.py` | Üç modülü koordine eder |

### 5.3 Veri Formatları

| Format | Kullanım |
|--------|---------|
| `.txt` (TSV) | Ham deneysel veri (aaa2.txt) |
| `.csv` | Üretilen veri kümeleri (PFAZ 1 çıktısı) |
| `.xlsx` | Excel raporları (PFAZ 6: 18 sayfa; PFAZ 7: ensemble sonuçları) |
| `.mat` | MATLAB formatı çıktıları (PFAZ 1) |
| `.pkl` | Eğitilmiş model arşivleri (joblib) |
| `.json` | Konfigürasyon, metadata, pfaz_status |
| LaTeX (`.tex`) | Tez belgesi (PFAZ 10) |

---

## 6. Yapay Zeka Mimarisi

### 6.1 Model Tipleri (config.json'dan)

| Model | Kısaltma | Tip |
|-------|----------|-----|
| Rastgele Orman | RF | Topluluk — Bagging |
| Gradyan Artırımı Makinesi | GBM | Topluluk — Boosting |
| Aşırı Gradyan Artırımı | XGBoost | Topluluk — Boosting |
| Derin Sinir Ağı | DNN | Derin Öğrenme |
| Bayesian Sinir Ağı | BNN | Olasılıksal Derin Öğrenme |
| Fizik-Bilgili Sinir Ağı | PINN | Kısıtlanmış Derin Öğrenme |
| Adaptif Ağ Bulanık Çıkarım Sistemi | ANFIS | Bulanık Mantık + YSA |

### 6.2 Eğitim Stratejisi

- Her model tipi için **50 konfigürasyon** (grid search)
- **5-kat çapraz doğrulama** (k=5)
- **Paralel eğitim:** 4 işçi (`n_workers=4`)
- **GPU:** CUDA 11.0+, opsiyonel (GTX 1650, 4 GB VRAM hedefi)
- **Başarı eşiği:** R² > 0.90; **hedef:** R² > 0.95
- **DNN minimum örnek:** `DNN_MIN_SAMPLES = 80` (core_modules/constants.py)

### 6.3 ANFIS Konfigürasyonları (config.json'dan)

8 konfigürasyon; Grid Partition ve Subcluster × 4 üyelik fonksiyonu:

| # | Bölümleme | Üyelik Fonksiyonu |
|---|-----------|------------------|
| 1 | Grid Partition | Üçgen (trimf) |
| 2 | Grid Partition | Gauss (gaussmf) |
| 3 | Grid Partition | Genelleştirilmiş Çan (gbellmf) |
| 4 | Grid Partition | Trapezoid (trapmf) |
| 5 | Subcluster | Üçgen (trimf) |
| 6 | Subcluster | Gauss (gaussmf) |
| 7 | FCM | Üçgen (trimf) |
| 8 | FCM | Gauss (gaussmf) |

### 6.4 Veri Kümesi Varyantları (PFAZ 1 çıktısı: 848 adet)

Her varyant şu kodlama şemasını izler:

```
{hedef}_{boyut}_{senaryo}_{özellik_seti}_{ölçekleme}_{örnekleme}[_NoAnomaly]
```

| Boyut | Değerler |
|-------|---------|
| Hedef | MM, QM, Beta_2, MM_QM |
| Boyut | 75, 100, 150, 200, ALL (197) |
| Senaryo | S70 (70/15/15 bölünme), S80 (80/10/10 bölünme) |
| Anomali | NoAnomaly varyantı: yalnızca boyut ≥150 için (IQR eşiği = 3.0) |

---

## 7. Pipeline Durum Özeti (pfaz_status.json — 2026-04-21 itibarıyla)

| PFAZ | Son Güncelleme | Durum | İlerleme |
|------|----------------|-------|----------|
| 01 | 2026-04-20 | running | %50 |
| 02 | 2026-04-06 | running | %50 |
| 03 | 2026-04-01 | completed | %100 |
| 04 | 2026-04-01 | completed | %100 |
| 05 | 2026-04-02 | completed | %100 |
| 06 | 2026-04-02 | completed | %100 |
| 07 | 2026-04-02 | completed | %100 |
| 08 | 2026-04-04 | completed | %100 |
| 09 | 2026-04-04 | completed | %100 |
| 10 | 2026-03-26 | running | %50 |
| 11 | 2026-03-24 | skipped | — |
| 12 | 2026-03-24 | failed | %0 |
| 13 | 2026-03-24 | failed | %0 |

> **Tez için not:** PFAZ 12 (istatistiksel testler) ve PFAZ 13 (AutoML) failed durumundadır. Bu fazlar tezin "Bulgular" ve "Tartışma" bölümlerine katkı sunacağından, analiz sırasında kaynak koddan teorik içerik çıkarılacaktır.

---

## 8. Önemli Konfigürasyon Değerleri (config.json)

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| `total_nuclei` | 267 | Veri kümesindeki çekirdek sayısı |
| `features` | 44 | Ham özellik sayısı |
| `n_configurations` | 50 | Her model tipi için konfigürasyon sayısı |
| `cv_folds` | 5 | Çapraz doğrulama katı |
| `n_workers` | 4 | Paralel işçi sayısı |
| `r2_min` | 0.90 | Başarı eşiği (R²) |
| `r2_target` | 0.95 | Hedef performans (R²) |
| `rmse_max` | 0.15 | RMSE üst sınırı |
| `monte_carlo.n_runs` | 1000 | Monte Carlo simülasyon sayısı |
| `monte_carlo.confidence_level` | 0.95 | Güven düzeyi |
| `anfis` konfigürasyon sayısı | 8 | Grid/SubClust × üyelik fonksiyonu |
| `gpu.device` | `cuda:0` | GPU cihazı |

---

## 9. Ana Giriş Noktaları

| Dosya | Rol | Temel Yapı |
|-------|-----|------------|
| `main.py` | Ana orkestratör v6.0.0 | `NuclearPhysicsAIOrchestrator` sınıfı |
| `run_complete_pipeline.py` | Tam pipeline çalıştırıcı | — |
| `generate_comprehensive_datasets.py` | Veri üretim betiği | — |
| `scripts/health_check.py` | Import ve sağlık kontrolü | — |
| `scripts/check_pfaz_completeness.py` | Beklenen çıktı dosyası kontrolü | — |

---

## 10. Açık Sorular

### 10.1 Teknik Belirsizlikler

- [ ] PFAZ 12 ve 13'ün neden failed olduğu bilinmiyor. Bu fazlar analiz edilirken kaynak koddan içerik çıkarılacak.
- [ ] PFAZ 01 ve 02 "running %50" — gerçekten yarıda kesilmiş mi yoksa önceki çalışmadan mı kaldı?
- [ ] Tüm 44 özelliğin tam listesi henüz çıkarılmadı — PFAZ 1 incelemesinde `core_modules/constants.py`'den alınacak.
- [ ] PFAZ 10 "running %50" — `outputs/thesis/` dizininde LaTeX çıktıları mevcut mu?

### 10.2 Tez için Akademik Kaynak Gereken Konular

- [ ] ANFIS için temel atıf: Jang (1993) "ANFIS: Adaptive-Network-Based Fuzzy Inference System" — doğrulanmalı.
- [ ] SEMF formülünün hangi versiyonu kullanılmış? (Bethe-Weizsäcker orijinal mi, güncel katsayılar mı?)
- [ ] Woods-Saxon potansiyeli parametreleri: hangi referansa göre ayarlanmış?
- [ ] Nilsson modeli: hangi shell model parametreleri? Nilsson (1955) mü?

---

## 11. Önerilen Faz Analiz Sırası (Plan Onayı İçin)

| Öncelik | PFAZ | Gerekçe | Tahmini Süre |
|---------|------|---------|-------------|
| **1** | PFAZ 01 | Temel — veri ve özellik mühendisliği; diğer tüm fazların girdisi | 45-60 dk |
| **2** | PFAZ 02 | AI eğitim çekirdeği; tezin birincil katkısı | 60-90 dk |
| **3** | PFAZ 03 | ANFIS — hibrit yaklaşımın ikinci ayağı | 45-60 dk |
| 4 | PFAZ 07 | Topluluk modeller — çoklu model kombinasyonu | 30-45 dk |
| 5 | PFAZ 09 | Monte Carlo — belirsizlik analizi | 30-45 dk |
| 6 | PFAZ 12 | İstatistiksel testler — failed ama içerik önemli | 30-45 dk |
| 7 | PFAZ 04 | Bilinmeyen çekirdek tahminleri | 30-40 dk |
| 8 | PFAZ 05 | Çapraz model analizi | 25-35 dk |
| 9 | PFAZ 06 | Final raporlama — tüm sonuçların birleşimi | 30-40 dk |
| 10 | PFAZ 13 | AutoML — failed ama içerik var | 25-35 dk |
| 11 | PFAZ 08 | Görselleştirme — şekil kataloğu | 25-35 dk |
| 12 | PFAZ 10 | Tez derleme — LaTeX yapısı | 20-30 dk |
| — | PFAZ 11 | Atlanıyor (kasıtlı devre dışı) | — |

**Toplam tahmini süre:** ~7-9 saat

---

*reports/faz-0-repo-kesfi.md | Analiz tarihi: 2026-05-02 | Durum: ✅ Tamamlandı*
