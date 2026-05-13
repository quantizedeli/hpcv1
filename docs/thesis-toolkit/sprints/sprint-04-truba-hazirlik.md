# Sprint 4 — TRUBA Hazırlık + Bug Temizlik
## Durum: TAMAMLANDI 2026-05-11 | Öncelik: YÜKSEK

> **Bu sprint neden var:**
> Sprint 1-3 (Dual R² filtresi, config sync, belge sync) tamamlandıktan sonra,
> pipeline'ın TRUBA HPC'de sorunsuz çalışabilmesi için kalan kritik bug'ların
> temizlenmesi gerekiyordu. Özellikle:
> - PC error log'unda (2026-05-04, Elif K) PFAZ 06, 08, 10 `pending`, PFAZ 13 `failed`
> - WS özellikleri çalışmıyor (BUG-02 — HBAR_C tanımsız)
> - PFAZ 12 import zinciri kırık (BUG-31 — NuclearBandAnalyzer alias eksik)
> - Monte Carlo örnekleme yetersiz (K=100, akademik standart K≥1000)
>
> **Bağlam dosyaları:**
> - `pc error.md` — gerçek run log'u (Elif K, 2026-05-04)
> - `pipeline-hatalari.md` — BUG kayıtları
> - `tez-yazim-not-defteri.md` — K=1000 kararı (Efron & Tibshirani 1993)
> - `sprints/SPRINT-PLAN.md` — sprint zinciri

---

## Hedef

TRUBA'ya geçmeden önce **pipeline'ı stabil hale getir**:
1. Fizik sabit eksikliklerini kapat (BUG-02, BUG-03)
2. Sınıf alias/import drift'lerini düzelt (BUG-31)
3. Indent hatalarını gider (BUG-32)
4. Monte Carlo örneklemeyi akademik standarda çıkar (BUG-38)
5. Overfit detector eksik metodu tamamla (BUG-39)
6. Hardcoded Unix path'leri kaldır (BUG-20)
7. Dual R² bağlamını hata mesajlarına yaydırma (PFAZ 04, 05, 07)

---

## Etkilenen Dosyalar

### Fizik ve Sabitler
| Dosya | Satır | Değişiklik | Bug |
|-------|-------|-----------|-----|
| `core_modules/constants.py` | 44 | `HBAR_C = 197.3269804` ekle (MeV·fm) | BUG-02 |
| `core_modules/constants.py` | 72-74 | `V_so`, `r_so`, `a_so` spin-yörünge parametreleri ekle | BUG-03 |

### Import ve Alias
| Dosya | Satır | Değişiklik | Bug |
|-------|-------|-----------|-----|
| `pfaz_modules/pfaz12_advanced_analytics/__init__.py` | 33 | `NuclearBandAnalyzer` import + try/except | BUG-31 |
| `pfaz_modules/pfaz12_advanced_analytics/nuclear_band_analyzer.py` | 1177 | `NuclearBandAnalyzer = NuclearMomentBandAnalyzer` alias | BUG-31 |

### Indent Hataları
| Dosya | Satır | Değişiklik | Bug |
|-------|-------|-----------|-----|
| `pfaz_modules/pfaz13_automl/automl_retraining_loop.py` | 537-539 | `return []` sonrası gereksiz indent satırları silindi | BUG-32 |
| `pfaz_modules/pfaz06_final_reporting/pfaz6_final_reporting.py` | 1264-1268 | Aynı pattern (5 anlamsız satır) silindi | BUG-32 (mirror) |

### Monte Carlo
| Dosya | Satır | Değişiklik | Bug |
|-------|-------|-----------|-----|
| `pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py` | DEFAULT_MC_CONFIG | `n_bootstrap` 100→1000, `n_samples_per_level` 100→1000 (Efron & Tibshirani 1993) | BUG-38 |

### Overfit Detector
| Dosya | Satır | Değişiklik | Bug |
|-------|-------|-----------|-----|
| `pfaz_modules/pfaz02_ai_training/overfitting_detector.py` | yeni | `analyze_training_metrics(...)` metodu eklendi | BUG-39 |

### Hardcoded Path
| Dosya | Satır | Değişiklik | Bug |
|-------|-------|-----------|-----|
| `pfaz_modules/pfaz07_ensemble/faz7_ensemble_pipeline.py` | - | Unix-spesifik hardcoded yol kaldırıldı; pathlib.Path kullanımı | BUG-20 |

### Dual R² Bağlam Geliştirmesi (Sprint 1'in devamı)
| Dosya | Değişiklik |
|-------|-----------|
| `pfaz_modules/pfaz04_unknown_predictions/single_nucleus_predictor.py` | Dual R² filtresi açıklamalı uyarı |
| `pfaz_modules/pfaz05_cross_model/cross_model_evaluator.py` | ValueError mesajına Dual R² bağlamı eklendi |
| `pfaz_modules/pfaz07_ensemble/pfaz7_complete_ensemble_pipeline.py` | Boş model havuzu için guard |
| `pfaz_modules/pfaz06_final_reporting/latex_generator.py` | N=75 ve Robust kaldırma notları |
| `pfaz_modules/pfaz08_visualization/master_report_visualizations_complete.py` | dataset_sizes default güncellendi |

---

## Adım Adım Uygulama (Tarihsel)

### Adım 1: BUG-02 ve BUG-03 — Fizik Sabitleri (2026-05-04)

`core_modules/constants.py` dosyasının başına ekle:

```python
# Bağıl atom kütlesi enerjisi (BUG-02 fix 2026-05-04)
HBAR_C = 197.3269804  # MeV * fm

# Woods-Saxon spin-yörünge parametreleri (BUG-03 fix 2026-05-04)
WOODS_SAXON_PARAMS = {
    'V0': 51.0,     # Potansiyel derinligi (MeV)
    'r0': 1.25,     # Yarıçap parametresi (fm)
    'a': 0.67,      # Yüzey difüzlüğü (fm)
    'V_so': 6.0,    # Spin-orbit potansiyel derinliği (MeV)
    'r_so': 1.25,   # Spin-orbit yarıçap parametresi (fm)
    'a_so': 0.67    # Spin-orbit yüzey difüzlüğü (fm)
}
```

### Adım 2: BUG-31 — NuclearBandAnalyzer Alias (2026-05-09)

`pfaz_modules/pfaz12_advanced_analytics/nuclear_band_analyzer.py` sonuna:

```python
# BUG-31 fix: __init__.py 'NuclearBandAnalyzer' adini bekliyor
NuclearBandAnalyzer = NuclearMomentBandAnalyzer
```

`pfaz_modules/pfaz12_advanced_analytics/__init__.py` içinde:

```python
try:
    from .nuclear_band_analyzer import NuclearBandAnalyzer
    NUCLEAR_BAND_ANALYZER_AVAILABLE = True
except ImportError:
    NuclearBandAnalyzer = None
    NUCLEAR_BAND_ANALYZER_AVAILABLE = False
```

### Adım 3: BUG-32 — Indent Hatalarını Sil (2026-05-09)

`automl_retraining_loop.py:537-539` ve `pfaz6_final_reporting.py:1264-1268`:
`return []` sonrası gereksiz 3-5 satırlık (`= None`, indent uyumsuz) blok silindi.
Bu satırlar muhtemelen önceki refactor'dan kalan dead code.

### Adım 4: BUG-38 — Monte Carlo K=1000 (2026-05-09)

`pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py`:

```python
DEFAULT_MC_CONFIG = {
    'n_bootstrap': 1000,         # eskisi: 100 (Efron & Tibshirani 1993)
    'n_samples_per_level': 1000, # eskisi: 100
    ...
}
```

**Not:** Sınıf default'ları (`BootstrapSimulator.__init__`, `NoiseSimulator.__init__`)
hala 100 idi — Sprint 5'te tamamlandı.

### Adım 5: BUG-39 — Overfit Detector Metod (2026-05-08)

`pfaz_modules/pfaz02_ai_training/overfitting_detector.py`'a `analyze_training_metrics(...)`
metodu eklendi. Train/Val/Test metriklerini alıp overfit/underfit skoru döndürür.

### Adım 6: BUG-20 — Hardcoded Unix Yolu (2026-05-09)

`pfaz_modules/pfaz07_ensemble/faz7_ensemble_pipeline.py`'da Unix-spesifik
hardcoded yol (`/tmp/...` gibi) `pathlib.Path` veya `Path.cwd()` ile değiştirildi.
Windows ve TRUBA Linux her ikisinde de çalışacak hale geldi.

### Adım 7: Dual R² Bağlam Mesajları

Sprint 1'de eklenen dual R² filtresi modelleri reddedebilir. Bu durumda
PFAZ 04/05/07'de "model bulunamadı" hatası yerine bağlamlı mesaj veriliyor:

```python
raise ValueError(
    f"Hiç model uygun değil: tüm modeller dual R² filtresine takıldı "
    f"(cv_R2<0 veya gap≥0.5). Bkz. Sprint 1 — Shang 2022, Utama 2016."
)
```

---

## Test ve Doğrulama

### Sprint 4 Sonu Test Durumu
- **py_compile:** Tüm değiştirilen dosyalar sözdizimsel geçerli ✓
- **Import test:** PFAZ 12 artık import ediliyor (BUG-31 fix) ✓
- **WS özellikleri:** HBAR_C tanımlı, hesaplama yapılabilir ✓
- **MC örnekleme:** K=1000 olduğu doğrulandı (DEFAULT_MC_CONFIG'de) ✓

### Bilinen Eksiklik (Sprint 5'e devredildi — Sprint 8'de tamamlandi)
- BUG-38'in **sinif default'lari** (sat. 194, 288) hala 100 idi
  → Sprint 5 belgesi "tamamlandi" dedi ama gercekte hala eksikti
  → **Sprint 8'de BUG-64 olarak tamamlandi (commit 2f1e594):**
    - `MCDropoutSimulator.__init__` n_samples=100 → **1000**
    - `FeatureDropoutSimulator.__init__` n_samples=500 → **1000**
    - Tum MC simulasyonlari artik K=1000 standardinda (Efron & Tibshirani 1993)

---

## Sprint 4 → Sprint 5 Geçişi

Sprint 4 bittiğinde **Inter-PFAZ veri akışı**nın **sistematik audit'i yapılmamıştı**.
PFAZ 02→03→08 arasında kolon adı (`R2_test` vs `Test_R2`) ve dosya adı
(`training_summary.xlsx` vs `training_results_summary.xlsx`) uyumsuzlukları
fark edilmemişti. Bu yüzden:

- PC error.md'de PFAZ 08 hala `pending` kaldı
- ANFISDatasetSelector belge "aktif" diyordu ama kod hala `deactivated`

**Sprint 5** bu eksikliği kapatmak için açıldı: Inter-PFAZ data flow audit
(KURAL 19) uygulandı, 5 yeni bug (BUG-42..46) tespit edildi ve çözüldü.

---

## Referanslar

- **Efron, B., & Tibshirani, R.J. (1993).** *An Introduction to the Bootstrap.*
  Chapman & Hall/CRC. (n_bootstrap≥1000 için akademik standart)
- **Shang, B., et al. (2022).** Dual R² filtresi metodolojisi
  (DOI: 10.1080/15140326.2023.2207326)
- **Utama, R., et al. (2016).** CV-train gap analizi
  (DOI: 10.1103/PhysRevC.93.014311)
- **v10 commit `3d61faa`** (2026-05-11) — Sprint 1-4 birleşik commit

---

## Tez Katkısı Notu

Sprint 4'ün tez §3.4'e doğrudan katkıları:
1. **Fizik sabitlerinin tam kapsamı** (HBAR_C, V_so) — Woods-Saxon ve spin-yörünge hesapları
2. **Monte Carlo K=1000 standardı** — Efron-Tibshirani'ye uygun belirsizlik analizi
3. **Dual R² mimari** — Sprint 1'in pipeline'a katmanlı uygulanışı

---

*Sprint 4 v1.0 | 2026-05-11 (retrospektif belge) | Kaynak: v10 commit 3d61faa + hpcv1 fix commit'leri*
