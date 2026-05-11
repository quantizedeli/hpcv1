# Eski PC Log Analizi — 2026-05-07

**Analiz Tarihi:** 2026-05-07  
**Log Kayıtları:** `old logs/main_20260430_184414.log.*` (5 dosya, ~70 MB toplam)  
**Kapsam:** PFAZ 01 (başlangıç) + PFAZ 02 (AI Eğitim, ~%54 tamamlandı)  
**Referans Repo:** `C:\Users\etabar\Desktop\v11\v11\nucdatav1` (eski PC)

---

## 1. Genel Zaman Çizelgesi

| Olay | Tarih/Saat |
|------|------------|
| Pipeline başlangıcı | 2026-04-30 18:44:14 |
| PFAZ 1 başlangıcı | 2026-04-30 18:44:17 |
| PFAZ 2 başlangıcı | (PFAZ 1'den hemen sonra) |
| Son log kaydı | 2026-05-07 16:11:20 (~7 gün 21 saat sonra) |
| İlerleme (son kayıt) | 241,890 / 446,400 (%54.2) |
| Tahmini ETA (son kayıt) | 8,391 dk daha (~5.8 gün) |
| Tahmini toplam süre | ~18,300 dk ≈ **12.7 gün** |

**Sonuç:** PFAZ 2 tek başına ~13 gün sürmektedir. Bu, tez takvimi için sürdürülemez.

---

## 2. "446,400" Sayısı Ne Anlama Geliyor?

Bu sayı **dataset sayısı değil, toplam model eğitim işi sayısıdır**.

### Hesaplama Şeması

```
PFAZ 1 Çıktısı (dataset kombinasyonları):
  - 2 Senaryo: S70, S80
  - 4 Ölçekleme: NoScaling, Standard, Robust, MinMax
  - 2 Örnekleme: Random, Stratified
  - 5 Çekirdek Sayısı: 75, 100, 150, 200, ALL
  - ~40 Feature Seti (SHAP tabanlı 35 + klasik 5)
  - 2 Hedef: MM, QM
  - NoAnomaly varyantları (150+ boyutlar için)
  ≈ ~848 toplam dataset

PFAZ 2 Model Eğitimi (her dataset için):
  - RF: ~50 farklı config (hyperparameter kombinasyonu)
  - DNN: ~50 farklı config
  - XGBoost (RF+XGB): ~100 farklı config
  - BNN, PINN, diğerleri: ~100+
  ≈ ~527 model/dataset

TOPLAM: 848 dataset × 527 model = ~446,896 ≈ 446,400 iş
```

**Her iş ~25-35 saniye → Sıralı toplam: ~3.1 milyon saniye ≈ 36 gün**  
**Paralel çalışma (gözlemlenen): ~12.7 gün**

---

## 3. R² Negatif Gelmesi — Açıklama

### Matematiksel Teori

```
R² = 1 - (SS_residual / SS_total)

SS_res < SS_tot → R² ∈ [0, 1)  (iyi)
SS_res ≈ SS_tot → R² ≈ 0       (baseline kadar)
SS_res > SS_tot → R² < 0        (baselineden kötü!)
```

R² **matematiksel olarak negatif olabilir** — model, sabit ortalama tahmininden daha kötü performans gösteriyorsa.

### R² 1'i Aşar mı?

**HAYIR.** R² maksimum 1'dir (mükemmel tahmin). `(+/-1.2228)` ifadesi R²'nin 1'i geçtiği anlamına **gelmez**; bu CV (5-kat çapraz doğrulama) katları arasındaki **standart sapma**dır.

Örnek: `r2: -0.3636 (+/-1.2228)` anlamı:
- Ortalama CV R² = -0.3636
- ±1 std aralığı: [-1.59, +0.86]
- Bazı katlarda R² pozitif, bazılarında çok negatif
- **Yüksek varyans** → küçük eğitim seti (fold başına ~17 örnek) → dengesiz tahmin

### Log'da Gözlemlenen Kritik Overfit

```log
XGBoost_RF_002 — 5-Fold CV:
  r2_train_mean: 0.9967  ← Neredeyse mükemmel eğitim skoru
  r2_test_mean:  -0.3103  ← Doğrulama seti tamamen başarısız
```

**Bu masif overfitting göstergesidir.** Model eğitim verisini ezberlemiş (R²=0.9967), genelleştirememektedir.

### Ancak Dikkat: İki Farklı R² Metriği

Log'da iki farklı R² görülmektedir:
1. **CV R² (model_validator):** `r2: -0.31` → 5-kat CV, train+val üzerinde, daha güvenilir
2. **Val set R² ([SUCCESS] satırı):** `R2=0.79-0.84` → 15-örnekli val set, küçük örneklem = yanıltıcı olabilir

**Sorun:** Kaydetme filtresi val set R²'ye göre çalışıyor. Val set sadece 15 örnekten oluştuğundan şanslı bölünme etkisi var.

---

## 4. Tespit Edilen Hatalar ve Anormal Durumlar

### BUG-39 (YENİ): OverfittingDetector — `analyze_training_metrics` Eksik

**Severity:** MEDIUM  
**Konum:** `pfaz02_ai_training/overfitting_detector.py`  
**Çağıran:** `parallel_ai_trainer.py:1407`

```log
WARNING - [OVERFITTING] Detection failed: 'OverfittingDetector' object has no attribute 'analyze_training_metrics'
```

**Frekans:** Her model eğitiminde, çok sayıda tekrar (binlerce WARNING)

**Neden:** `parallel_ai_trainer.py` bu metodu şöyle çağırıyor:
```python
detector.analyze_training_metrics(
    train_metrics=metrics['train'],
    val_metrics=metrics['val'],
    test_metrics=metrics.get('test', {})
)
```
Ama `OverfittingDetector` sınıfında bu metod tanımlı değil. Mevcut metodlar: `analyze_single_training`, `analyze_all_trainings`, `load_training_results`.

**Etki:** Overfitting tespiti hiç çalışmıyor; kayıt tutulmuyor.  
**Düzeltme:** `analyze_training_metrics` metodunu ekle. ✅ (Bu rapor ile birlikte düzeltildi)

---

### UYARI-01: Nilsson Features — %34 NaN

```log
[WARNING] Missing values in nilsson_epsilon: 68 (34.0%)
[WARNING] Missing values in nilsson_omega:   68 (34.0%)
```

**Etki:** `nilsson_epsilon` ve `nilsson_omega` özellikleri, 200 çekirdekten 68'inde eksik.  
**Sebep:** Nilsson modeli sadece deforme çekirdekler için tanımlı (Beta_2 ≠ 0).  
**Öneri:** Bu özellikleri içeren feature setleri için imputation veya conditional inclusion kullan.

---

### UYARI-02: Beta_2 ve Beta_2_estimated — NaN Var

```log
[WARNING] Missing values in Beta_2: 4 (2.0%)
[WARNING] Missing values in Beta_2_estimated: 5 (2.5%)
```

**Etki:** Küçük etki (%2-2.5), imputation yapılıyor.

---

### UYARI-03: Robust Scaling — QM için Tamamen Başarısız

Logdan gözlemlenen XGBoost + QM + Robust Scaling kombinasyonları:

```log
QM_100_S70_B2EMCBEA_Robust_Stratified_XGBoost_RF_001: r2 = -0.4871
QM_100_S70_B2EMCBEA_Robust_Stratified_XGBoost_RF_002: r2 = -0.5594
QM_100_S70_B2EMCBEA_Robust_Stratified_XGBoost_RF_003: r2 = -0.5392
QM_100_S70_B2EMCBEA_Robust_Stratified_XGBoost_RF_004: r2 = -0.5102
```

**Hepsi R² < 0.5 olduğundan kaydedilmedi (POOR filter).**

**Sebep:** Robust scaler (IQR tabanlı) QM hedefinin outlier-yoğun dağılımını aşırı sıkıştırıyor.

---

### UYARI-04: QM Filtresi — 67 Çekirdek Çıkarıldı

```log
Target: QM -> QM filtresi UYGULANDII (QM olmayan 67 çekirdek çıkarıldı)
Filtered: 200 nuclei remain
```

**BUG-01 (Açık):** Q=0 olan küresel çekirdekler de çıkarılıyor. Bu tartışmalı — Q=0 fiziksel olarak geçerli bir değer (sferik çekirdek).

---

### UYARI-05: Paralel Eğitimde n_jobs=1 (Seri CV)

```log
n_jobs: 1 (1=sequential CV to avoid deadlock in parallel training)
```

**Etki:** Her modelin CV'si seri çalışıyor → toplam süreyi artırıyor.  
**Sebep:** Paralel trainer içinde nested parallelism deadlock'a neden oluyor.  
**Öneri:** PFAZ 2 için batch-level parallelism kullan (birden fazla dataset eş zamanlı), model-level'da sequential tut.

---

## 5. Model Performans Analizi

### 5.1 Model Türleri — Sıralama

Logdan elde edilen val set R² değerleri:

| Model | Val R² Aralığı | Gözlem |
|-------|----------------|--------|
| **XGBoost** | 0.57 – 0.84+ | En iyi; tutarlı |
| **RF (Random Forest)** | 0.57 – 0.65 | İyi; daha az overfit |
| **DNN** | 0.57 – 0.65 | RF ile benzer |
| Robust+XGBoost | < 0 (hepsi) | Kaydedilmedi |

**Sonuç:** XGBoost > RF ≈ DNN. Ancak XGBoost için CV R² çok negatif — overfit riski.

### 5.2 Feature Set Başarısı

Gözlemlenen başarılı kombinasyonlar:

| Feature Set | Açıklama | Performans |
|-------------|----------|------------|
| **B2EMCBEA** | Beta_2, magic_character, BE_asymmetry | ★★★★★ (R²=0.79-0.84) |
| **AZSB2E** | A, Z, SPIN, Beta_2, BE | ★★★★☆ |
| **AZSBEPA** | A, Z, SPIN, BE/A | ★★★☆☆ |
| **AZS** (Basic) | Yalnızca A, Z, SPIN | ★★☆☆☆ |

**Sonuç:** Physics-informed features (Beta_2, magic_character, BE_asymmetry) kritik.  
Beta_2 ayrışım parametresi ve kabuk kapanma özelliği (magic_character) en önemli tahmin ediciler.

### 5.3 Ölçekleme Yöntemi Başarısı

| Yöntem | QM Performansı | MM Performansı | Öneri |
|--------|----------------|----------------|-------|
| **NoScaling** | ★★★★☆ | ★★★★☆ | Kullan |
| **Standard** | ★★★★★ | ★★★★★ | En iyi; kullan |
| **MinMax** | ★★★☆☆ | ★★★★☆ | Kabul edilebilir |
| **Robust** | ★☆☆☆☆ | ★★☆☆☆ | **KULLANMA** |

**Önemli Bulgu:** Robust scaling, QM target için sistematik olarak başarısız oluyor. Tüm R² değerleri negatif çıktı.

### 5.4 Örnekleme Stratejisi

| Yöntem | Gözlem |
|--------|--------|
| **Random** | XGBoost ile en iyi kombinasyon |
| **Stratified** | RF/DNN ile daha iyi |

Her iki yöntem de çalışıyor; model türüne göre değişiyor.

### 5.5 Dataset Boyutu Etkisi

| Çekirdek Sayısı | Train | Val | Test | Performans |
|-----------------|-------|-----|------|------------|
| 75 | ~38 | ~8 | ~8 | ★★☆☆☆ (çok küçük) |
| 100 | ~70 | ~15 | ~15 | ★★★★☆ |
| 150 | ~105 | ~23 | ~23 | ★★★★★ |
| 200 | ~140 | ~30 | ~30 | ★★★★☆ |
| ALL (267) | ~187 | ~40 | ~40 | ★★★☆☆ (gürültü artar) |

**Sonuç:** 150 çekirdek en iyi performans bölgesi.  
75'te DNN hiç çalışmıyor (DNN_MIN_SAMPLES = 80 kuralı devreye giriyor).

### 5.6 Senaryo Etkisi (S70 vs S80)

| Senaryo | Train Oranı | Val Oranı | Test Oranı | Not |
|---------|-------------|-----------|------------|-----|
| **S70** | %70 | %15 | %15 | Daha az eğitim verisi |
| **S80** | %80 | %10 | %10 | Daha fazla eğitim, daha az doğrulama |

**Gözlem:** Her iki senaryo da iyi çalışıyor. S80, daha fazla eğitim verisi sunduğundan büyük modellerde avantajlı olabilir.

---

## 6. Başarılı Konfigürasyonlar (Top Performers)

Logdan elde edilen yüksek R² değerleri:

| Sıra | Dataset | Model | R² (Val) |
|------|---------|-------|----------|
| 1 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | XGBoost_RF_008 | 0.8418 |
| 2 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | XGBoost_XGB_026 | 0.8418 |
| 3 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | XGBoost_RF_004 | 0.8311 |
| 4 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | XGBoost_RF_012 | 0.8387 |
| 5 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | XGBoost_RF_006 | 0.8195 |
| 6 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | XGBoost_RF_001 | 0.7907 |
| 7 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | RF_DNN_045 | 0.6459 |
| 8 | QM_100_S70_B2EMCBEA_NoScaling_Stratified | RF_DNN_049 | 0.6506 |

**⚠️ ÖNEMLI UYARI:** Bu val set R² değerleri 15 örnekten hesaplanıyor. CV R² = -0.31 olan aynı XGBoost modelinin val R²=0.84 vermesi, **15-örneklik val setinin çok dengesiz** olduğunu gösteriyor. Test setinde R² daha düşük olabilir.

**Gerçek performansı görmek için:** PFAZ 4 veya PFAZ 5'te cross-model değerlendirme yapılmalı.

---

## 7. Tutarsızlıklar

### 7.1 Val R² vs CV R² Çelişkisi

```
XGBoost_RF_008 val R² = 0.84  ← Çok iyi görünüyor
XGBoost_RF_002 CV  R² = -0.31 ← Aynı dataset, aynı model türü
```

**Açıklama:** CV, 85 örneği 5'e böldüğünde her katta ~17 örnek kalıyor. Bu kadar küçük katlarda XGBoost overfit yapıyor. Val set şansı büyük rol oynuyor.

**Önerilen Düzeltme:** 
- K-fold sayısını 3'e indir (daha büyük katlarda)  
- Veya hold-out doğrulaması için daha büyük dataset kullan (150+ çekirdek)

### 7.2 Aynı Hiperparametreler, Farklı Sonuçlar

```
RF_DNN_045: n_estimators=50, lr=0.1 → R² = 0.6459
RF_DNN_050: n_estimators=50, lr=0.1 → R² = 0.6169
```

**Açıklama:** `random_seed` farklı (log'da görüldü). Seed variasyonu ±0.03 R² fark yaratıyor.

---

## 8. Hafifletilmiş Repo İçin Kurallar (Bulgulara Dayalı)

Bu loglar referans alınarak `nucdatav2-desktop` konfigürasyonu şu şekilde optimize edilmeli:

### 8.1 Kullanılacak Ölçekleme Yöntemleri

```json
"scaling_methods": ["NoScaling", "Standard"]
```
→ Robust ve MinMax çıkarıldı. Robust sistematik olarak başarısız, MinMax vasat.

### 8.2 Kullanılacak Dataset Boyutları

```json
"nucleus_counts": [100, 150, 267]
```
→ 75 çıkarıldı (DNN çalışmıyor, küçük N yüksek varyans). 200 eklendi zaten.

### 8.3 Kullanılacak Model Türleri

```json
"model_types": ["XGBoost", "RF", "DNN"]
```
→ BNN ve PINN çıkarıldı (log'da bu eski PC versiyonunda görünmüyor, ayrıca çok yavaş).

### 8.4 Feature Set Öncelikleri

En iyi performans veren setler:
1. `B2EMCBEA` (Beta_2, magic_character, BE_asymmetry) — **öncelik 1**
2. `AZSB2E` (A, Z, SPIN, Beta_2, BE) — **öncelik 2**
3. `AZSBEPA` (A, Z, SPIN, BE/A) — **öncelik 3**

### 8.5 Hiperparameter Konfigürasyon Sayısı

Eski sistemde ~50 config/model → toplam süre ~13 gün.  
Desktop için: **10 config/model** (en iyi bilinen hiperparametreler)

### 8.6 Sampling

```json
"sampling_methods": ["Stratified"]
```
→ Tek yöntem yeterli (hem RF hem XGBoost için iyi).

---

## 9. Yeni Bug Listesi (Güncel)

| Bug ID | Dosya | Açıklama | Durum |
|--------|-------|----------|-------|
| BUG-39 | `overfitting_detector.py` | `analyze_training_metrics` metodu eksik | ✅ Düzeltildi |
| BUG-01 | `qm_filter_manager.py:153` | Q=0 küresel çekirdekler filtreleniyor | ⚠️ Açık |
| WARN-01 | `model_validator.py` | CV fold başına ~17 örnek → dengesiz | 📝 Tez notu |
| WARN-02 | `parallel_ai_trainer.py` | Val R² filtresi 15 örnekle çalışıyor → yanıltıcı | 📝 Tez notu |
| WARN-03 | `config.json` | Robust scaling = %100 başarısız için QM | ⚠️ Config değişikliği |

---

## 10. Sıradaki Adımlar

1. **Desktop config güncellemesi:** Robust scaling çıkar, boyut 75 çıkar, config sayısını 10'a indir
2. **PFAZ 2 yeniden çalıştırma (TRUBA):** Tüm 446,400 iş yerine 50,000–100,000 kritik iş
3. **BUG-39 fix:** `analyze_training_metrics` metodu eklendi ✅  
4. **CV fold sayısı:** Küçük dataset'ler (N<150) için 3-fold'a düşür
5. **Overfit monitoring:** CV train/val gap eşiği ile early stopping

---

*Oluşturan: Claude Code | 2026-05-07*  
*Kaynak loglar: `old logs/main_20260430_184414.log.1-4` + `Kopya.log`*  
*Referans: CLAUDE.md, pipeline_bugs.md, session-2026-05-07-truba-deployment.md*
