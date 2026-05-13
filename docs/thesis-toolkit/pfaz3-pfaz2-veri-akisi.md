# PFAZ3 ↔ PFAZ2 Veri Akışı

**Tarih:** 2026-05-13 (Sprint 10 ek denetim)
**Tetikleyici:** Kemal'in sorusu — "faz 3 PFAZ 2'nin hangi bilgilerini kullanıyor?"

## Kısa Cevap

PFAZ3, PFAZ2'nin **`training_summary.xlsx` dosyasından 5 sütun** okuyor ve bunlarla **datasetleri R²_test bazlı tier'lara ayırıp seçim yapıyor**.

## Detaylı Akış

```
┌─────────────────────────────────────────────────────────────────────┐
│ PFAZ2 (AI Training)                                                  │
│   Çıktı: outputs/trained_models/training_summary.xlsx                │
│                                                                       │
│   Yazılan satırlar (her: dataset × model_type × config_id):          │
│     - Model_Type     (RF, XGB, DNN, GBM, SVR, ...)                   │
│     - Config_ID      (RF_001, XGB_001, DNN_001, ...)                 │
│     - Dataset        (MM_N100_Normal_Basic_NoScaling_Random, ...)    │
│     - Target         (MM, QM, MM_QM, Beta_2)   ← BUG-74 ile eklendi  │
│     - Train_R2, Val_R2, Test_R2  ← Tier ayırımında kullanılan        │
│     - Train_RMSE, Val_RMSE, Test_RMSE                                │
│     - Train_MAE,  Val_MAE,  Test_MAE                                 │
│     - PKL_Saved, Status_Note, Training_Time_s, Error                 │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            │ ANFISDatasetSelector.load_ai_results()
                            │   - dosyayı okur, eski/yeni isim normalize eder
                            │   - Test_R2 → R2_test, Val_R2 → R2_val vs.
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ PFAZ3 (ANFIS Training) — ANFISDatasetSelector                        │
│                                                                       │
│   KULLANILAN SÜTUNLAR (sadece 5):                                    │
│     - Target      → tier filtresi (MM, QM ayrı analiz)               │
│     - Dataset     → çıkışta hangi dataset adlarının seçildiği        │
│     - R2_test     → tier sınırları için (üç katmanlı seçim)          │
│     - Model_Type  → istatistik için (her tier'da model dağılımı)     │
│     - Config_ID   → tracking, log                                    │
│                                                                       │
│   LAYERED SELECTION (select_method_1_layered):                       │
│     Top tier  (R2_test ≥ 0.90)             → Quota:  50 dataset      │
│     Mid tier  (0.80 ≤ R2_test < 0.90)      → Quota:  50 dataset      │
│     Low tier  (R2_test < 0.80)             → Quota: 100 dataset      │
│       └─ "ML başarısız → ANFIS rescue" hipotezi (Tez §3.4)           │
│                                                                       │
│   Adaptive quota redistribution: bir tier boş kalırsa diğerlerine    │
│   round-robin ile dağıtılır (toplam hep 200 hedefler).                │
│                                                                       │
│   Çıktı: outputs/anfis_models/selected_datasets/                     │
│     - selected_method1_layered.xlsx  (her target için 200 dataset)   │
│     - dataset_paths (PFAZ1 outputu) bu listeye göre filtrelenir      │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ANFIS eğitimi sadece seçilen 200 dataset üzerinde
                  (8 ANFIS konfigürasyonu × 200 dataset = 1600 koşu/target)
```

## Sütun Eşleştirme

PFAZ2 yeni adlandırmaya geçtiğinde (Sprint 5, BUG-17) selector eski isimlerle hâlâ uyumlu olsun diye `load_ai_results()` normalize ediyor:

| PFAZ2 yazar (yeni) | Selector kullanır (eski) |
|---------------------|--------------------------|
| `Test_R2`           | `R2_test`                |
| `Test_RMSE`         | `RMSE_test`              |
| `Test_MAE`          | `MAE_test`               |
| `Val_R2`            | `R2_val`                 |
| `Train_R2`          | `R2_train`               |
| `Target`            | `Target` (1:1)           |
| `Dataset`           | `Dataset` (1:1)          |
| `Model_Type`        | `Model_Type` (1:1)       |
| `Config_ID`         | `Config_ID` (1:1)        |

## KULLANILMAYAN PFAZ2 Sütunları

Selector aşağıdaki sütunlara **bakmıyor**:

- `PKL_Saved`, `Status_Note`  (PFAZ2 dual R² gate'i zaten temizlemiş satırları)
- `Training_Time_s`           (sadece tracking için PFAZ6'da görünür)
- `Error`                      (gate'ten geçmemiş satırlar zaten None döner)
- `Train_RMSE`, `Val_RMSE`, `Test_RMSE`, `..._MAE`  (selector sadece R²_test kullanıyor)

## BUG-74 Vakası

### Önce (Sprint 10 öncesi)

PFAZ2 satırlarda **`Target` sütunu yazmıyordu**. Dataset adından target çıkarılabiliyordu (`'MM' in name`) ama PFAZ2 bu çıkarımı kendisi yapıp summary'ye eklemiyordu.

Selector `results_df[results_df['Target'] == target]` filtresi yapıyor → `KeyError: 'Target'` → try/except içindeki `except Exception` yakalıyor → log'a `"ANFISDatasetSelector calismadi: 'Target'"` yazılıyor → **fallback: tüm datasetler kullanılıyor**.

### Etkisi

- Tezdeki "Top=50/Mid=50/Low=100 layered seçim" stratejisi (Sprint 5, Akademik Karar 1) **kod seviyesinde hiç uygulanmamış**
- "ML başarısız → ANFIS rescue" hipotezi (Low tier=100) **hiç test edilmemiş**
- PFAZ3 200 dataset yerine **tüm datasetleri** (yüzlerce) tarıyordu — ANFIS eğitim süresi ~3-5x uzun olabilir
- TRUBA'da bu fark çok büyük: 200 × 8 konfig = 1600 ANFIS koşusu yerine 500+ × 8 = 4000+ koşu

### Sprint 10'da Düzeltildi

```python
# parallel_ai_trainer.py:1693 (yeni)
def _target_from_dataset_name(name: str) -> str:
    if 'MM_QM' in name or 'MM-QM' in name: return 'MM_QM'
    if name.startswith('MM_') or '_MM_' in name: return 'MM'
    if name.startswith('QM_') or '_QM_' in name or '_Q_' in name: return 'QM'
    if 'Beta_2' in name or 'BETA_2' in name: return 'Beta_2'
    return 'UNKNOWN'

rows.append({
    ...
    'Target': _target_from_dataset_name(result.dataset_name),  # BUG-74 FIX
    ...
})
```

### Fonksiyonel Doğrulama

```
Önce (eski):  KeyError: 'Target' → fallback → tüm datasetler
Şimdi (yeni): Target sütunu var → Layered selection çalışır
              Top tier  R²≥0.90: N dataset seçilir
              Mid tier  0.80≤R²<0.90: N dataset seçilir  
              Low tier  R²<0.80: 100 dataset (rescue hipotezi)
```

## Tez Anlatısı için Kritik

Bu bug nedeniyle Sprint 5'te yapılan tüm PFAZ3 koşuları **tez stratejisinin aksine** tüm datasetleri kullanmış olabilir. Sprint 10 sonrası TRUBA koşusunda:

1. Layered selection gerçekten uygulanıyor mu? — log'larda `"Top layer (R2>=0.90): X datasets"` görünmeli
2. Low tier 100 datasette ANFIS gerçekten "rescue" yapıyor mu? — R²_ANFIS > R²_AI'de Low tier'da daha sık görülmeli
3. Top tier'da AI ve ANFIS yakın mı, ANFIS marjinal iyileştirme mi yapıyor?

Tez §3.4 "Adaptive Dataset Selection for ANFIS" bölümü için bu data **yeniden toplanmalı**.

---

*Sprint 10 ek denetim | PFAZ3 ↔ PFAZ2 sütun seviyesinde veri akışı | BUG-74 fix*
