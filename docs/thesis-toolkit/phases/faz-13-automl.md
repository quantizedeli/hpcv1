# PFAZ 13: AutoML Yeniden Egitim Dongusu

> **Belge Versiyonu:** v2.0
> **Ilk Analiz:** 2026-05-04 | **Son Guncelleme:** 2026-05-14 (Sprint 13)
> **Durum:** ~~FAILED~~ DUZELTILDI (BUG-32 Sprint 4); TRUBA cikti bekleniyor
> **Ana Sinif:** AutoMLRetrainingLoop + AutoMLOptimizer
> **TRUBA Job:** Job 3 (`truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh`)
> **Kapsam:** 9 dosya (+ __init__), ~5968 satir

---

## 1. Genel Bakis

PFAZ 13, PFAZ 02'den dusen R2 skorlu modelleri tespit ederek Optuna TPE ile otomatik hiperparametre optimizasyonu uygular. Sadece kotu modelleri optimize etmekle kalmaz; Good/Medium/Poor kategorilerine gore sistematik bir yeniden egitim stratejisi izler ve ANFIS ile ozellik muhendisligini opsiyonel modul olarak entegre eder.

**Tezdeki Rolu:** 'Model R2=0.75 aldiysa, acaba daha iyi hiperparametrelerle ne kadar iyilesebilirdi?' sorusunu yanit verir. Tez metodoloji acikligini saglar: sistem yalnizca egitim yapmakla kalmaz, kendini otomatik optimize eder.

### Sinif Katalogu

| Sinif | Dosya | Satir | Sorumluluk |
|-------|-------|-------|------------|
| AutoMLRetrainingLoop | automl_retraining_loop.py | 1015 | Ana dongü; kategori tespiti; yeniden egitim; Excel |
| AutoMLOptimizer | automl_optimizer.py | 475 | Optuna TPE; 7 model turu; arama uzayi tanımlari |
| AutoMLLoggingReportingSystem | automl_logging_reporting_system.py | 1021 | Trial-bazli loglama; detayli JSON kayit |
| AutoMLFeatureEngineer | automl_feature_engineer.py | 767 | Polinomial + fizik esinli ozellik secimi |
| AutoMLANFISOptimizer | automl_anfis_optimizer.py | 741 | ANFIS konfigurasyon arama (6-8 konfigürasyon) |
| AutoMLVisualizer | automl_visualizer.py | 698 | Optuna grafikleri (parametre onem, trial gecmisi) |
| AutoMLHyperparameterOptimizer | automl_hyperparameter_optimizer.py | 557 | Eski surum (backward-compat alias) |
| feature_engineering_extended.py | -- | 609 | Gelismis ozellik muhendisligi yardimcilari |

~~KRITIK BUG (BUG-32): `automl_retraining_loop.py:43` SyntaxError -- indentation hatasi.~~
**DUZELTILDI 2026-05-09:** Gercek hata satir 539'daydı (dokumanda yanlis yazilmis). `_run_anfis_for_category` icinde `return []` sonrasi 3 hatali/tekrar satir silindi. Modul artik import edilebiliyor.

---

## 2. Motivasyon

### Neden AutoML?

PFAZ 02'de 50 konfigürasyon sabit hiperparametrelerle denendi. Ancak:
- RF max_depth=10 mu yoksa 20 mi daha iyi? Bunun yamitini grid search verir ama pahali.
- DNN learning_rate=0.001 mi 0.0001 mi? Optuna Bayesian optimizasyon ile verimli bulur.
- 848 dataset x 50 konfigürasyon = 42,400 model. Bunlarin R2<0.80 olanlarini cikar, Optuna ile iyilestir.

**Teorik Arka Plan:**
Optuna TPE (Tree-structured Parzen Estimator), gözlemlenen trial sonuçlarından bir olasilik modeli kurarak gelecekteki denemeleri yonlendirir. Rastgele aramaya gore 3-5x daha verimli.

### Kategori Stratejisi

| Kategori | R2 Araligi | Eylem |
|----------|-----------|-------|
| Poor | R2 < 0.70 | Mutlaka optimize et (n_per_category=25) |
| Medium | 0.70 <= R2 < 0.90 | Dene (n_per_category=25) |
| Good | 0.90 <= R2 < 0.95 | Seçici optimize et (n_per_category=25) |
| Excellent | R2 >= 0.95 | En dusuk skoru seç (iyilesme potansiyeli) |

---

## 3. Baglam

### PFAZ Pipeline Konumu

Pipeline sırasi: `[1,2,3,4,5,7,9,12,**13**,6,8,10]` -- 9. sirada.

**Girisler:** PFAZ02 trained_models/ (metrics JSON) + PFAZ01 generated_datasets/ (train/val CSV)
**Cikis:** outputs/automl_results/ (Excel + JSON + opsiyonel grafik)
**Downstream:** PFAZ06 (AutoML_Improvements + AutoML_BestParams sayfalarindan)

---

## 4. Calisma Akisi (AutoMLRetrainingLoop.run())

```
ADIM 1: find_low_scoring_candidates()
  -> trained_models/ altindaki tum metrics_*.json dosyalarini tara
  -> val_r2 < r2_threshold (0.80) VEYA kategori siralamasina gore sec
  -> Liste: [(target, dataset_name, model_type, original_r2, kategori)]

ADIM 2: Her aday icin _retrain_one():
  -> PFAZ1 CSV'lerini yükle (train.csv, val.csv)
  -> AutoMLOptimizer(X_train, y_train, X_val, y_val, model_type).optimize(n_trials=30)
  -> Iyilestirme kaydi: {before_r2, after_r2, improvement, best_params}

ADIM 3: _save_results():
  -> automl_retraining_log.json -- tam kayit listesi
  -> automl_improvement_report.xlsx -- 3 sayfa

ADIM 4: Opsiyonel (try/except ile):
  -> AutoMLFeatureEngineer (en cok iyilesen dataset icin)
  -> AutoMLANFISOptimizer (en kotu dataset icin ANFIS konfigürasyon arama)
  -> AutoMLVisualizer (Optuna grafikleri)
  -> Deneysel veri (aaa2.txt) karsilastirmasi
```

**Gerceklesme:** automl_retraining_loop.py:224-400 (AutoMLRetrainingLoop sinifi)

---

## 5. AutoMLOptimizer -- Arama Uzaylari

**Yapılandirma:** Optuna TPE sampler + MedianPruner; maximize R²; n_trials=30 (default)

| Model | Arama Uzayi |
|-------|------------|
| RF | n_estimators(50-500), max_depth(3-20), min_samples_split(2-10), max_features(auto/sqrt/log2) |
| XGBoost | n_estimators, max_depth(2-8), learning_rate, subsample, colsample_bytree, reg_alpha/lambda |
| GBM | n_estimators, max_depth, learning_rate, subsample |
| LightGBM | n_estimators, num_leaves, learning_rate, subsample, colsample_bytree, reg_alpha/lambda, min_child_samples |
| CatBoost | iterations, depth, learning_rate, l2_leaf_reg |
| SVR | C, epsilon, kernel(rbf/linear/poly), gamma |
| DNN | n_layers(2-4), hidden_units(32-256), dropout(0-0.5), learning_rate, batch_size, epochs=80 |

**DNN Ozel Davranis:**
- Huber loss (outlier'lara dayanikli)
- Y-olcekleme: StandardScaler (inverse_transform tahmin sonrasi)
- EarlyStopping: patience=10
- R2 < -2.0 ceza puan -> trial prune edilir

**Gerceklesme:** automl_optimizer.py:38-475 (AutoMLOptimizer sinifi)

---

## 6. AutoMLFeatureEngineer

Ozellik secimine ek olarak yeni ozellikler uretir:
- Polinomial kombinasyonlar (derece 2)
- Fizik esinli ozellikler: log_A, A^(1/3), N*Z/A, (N-Z)^2/A^2
- Geriye eliminasyon (backward elimination) ile ozellik secimi
- Cikti: yeni train/val CSV + secilen ozellik listesi

**Gerceklesme:** automl_feature_engineer.py:767 satir

---

## 7. Excel Ciktisi: automl_improvement_report.xlsx

| Sayfa | Icerik |
|-------|--------|
| Summary | Target, Dataset, Model, Once_R2, Sonra_R2, Iyilesme, En_Iyi_Params, Sure |
| Best_Params | Uzun format -- her (target, dataset, model, param, deger) satiri |
| Overview | Toplam_yeniden_egitilen, Iyilestirilen, Ortalama_Iyilesme, Max_Iyilesme, Esik |

**Ek JSON:**
- `automl_retraining_log.json` -- tam kayit listesi
- `automl_summary.json` -- ozet metrikler

---

## 8. Algoritmalar

### A-040: AutoML Kategori Tespiti

```
GIRIS: models_dir (PFAZ02 ciktisi), r2_threshold
CIKIS: candidates_list (target, dataset, model_type, r2, kategori)

metrics_files = glob(models_dir, "metrics_*.json")
FOR each metrics_file:
    r2 = json.load(mf).get('val_r2', None)
    IF r2 is None: skip
    IF r2 < POOR_MAX (0.70): kategori = "Poor"
    ELIF r2 < MEDIUM_MAX (0.90): kategori = "Medium"
    ELIF r2 < GOOD_MAX (0.95): kategori = "Good"
    ELSE: kategori = "Excellent"
categorized[kategori].append((...)

FOR her kategori:
    candidates.extend(sorted_by_r2_asc[:n_per_category])
```

**Gerceklesme:** automl_retraining_loop.py:~310

### A-041: Optuna TPE Optimizasyonu

```
GIRIS: X_train, y_train, X_val, y_val, model_type, n_trials
CIKIS: best_params, best_r2

study = optuna.create_study(
    direction="maximize",
    sampler=TPESampler(seed=42),
    pruner=MedianPruner(n_startup_trials=5)
)
study.optimize(objective, n_trials=n_trials, n_jobs=1)

# objective(trial):
#   params = _suggest_XX_params(trial)
#   model = _train_model(params)
#   r2 = r2_score(y_val, model.predict(X_val))
#   RETURN r2 (maximize)
```

**Gerceklesme:** automl_optimizer.py:68-150

---

## 9. Formuller

### F-062: Optuna TPE Posterior (basitlestirilmis)

$$p(y | x) = egin{cases} l(x) & y < y^* \ g(x) & y \geq y^* \end{cases}$$

$y^*$: yuzdelik dilim esigi (quantile); $l$: iyi sonuclarin KDE; $g$: kotu sonuclarin KDE.
Sonraki deneme $l(x)/g(x)$'i maximize eder.

### F-063: Iyilesme Orani

$$	ext{improvement} = 	ext{after\_r2} - 	ext{before\_r2}$$

### F-064: DNN Huber Loss

$$L_\delta(y, \hat{y}) = egin{cases} rac{1}{2}(y-\hat{y})^2 & |y-\hat{y}| \leq \delta \ \delta|y-\hat{y}| - rac{\delta^2}{2} & |y-\hat{y}| > \delta \end{cases}$$

$\delta = 1.0$ (varsayilan). Buyuk hatalarda L2'den daha dayanikli.

---

## 10. Degiskenler ve Parametreler

| Parametre | Deger | Sinif |
|-----------|-------|-------|
| r2_threshold | 0.80 | AutoMLRetrainingLoop (backward compat) |
| POOR_MAX | 0.70 | AutoMLRetrainingLoop |
| MEDIUM_MAX | 0.90 | AutoMLRetrainingLoop |
| GOOD_MAX | 0.95 | AutoMLRetrainingLoop |
| n_per_category | 25 | AutoMLRetrainingLoop |
| n_trials | 30 | AutoMLRetrainingLoop |
| model_types | ['rf', 'xgb', 'lgb'] | AutoMLRetrainingLoop |
| max_retrain | 0 (sinirsiz) | AutoMLRetrainingLoop |
| DNN epochs | 80 | AutoMLOptimizer |
| DNN patience | 10 | AutoMLOptimizer |
| DNN R2 ceza esigi | -2.0 | AutoMLOptimizer |
| Optuna quantile | 0.25 | TPESampler default |

---

## 11. Kisaltmalar

| Kisaltma | Acilim |
|----------|--------|
| AMRL | AutoMLRetrainingLoop |
| AO | AutoMLOptimizer |
| ALRS | AutoMLLoggingReportingSystem |
| AFE | AutoMLFeatureEngineer |
| AAO | AutoMLANFISOptimizer |
| TPE | Tree-structured Parzen Estimator (Optuna sampler) |
| MedianPruner | Medyan altindaki triallari prune eden Optuna pruner |
| KDE | Kernel Density Estimation (TPE icinde) |
| BKE | Backward Elimination (ozellik secim yontemi) |

---

## 12. Uygulama Detaylari

### Opsiyonel Kutuphaneler

| Kutuphane | Kullanim | Yoksa |
|-----------|---------|-------|
| optuna | Tum AutoML | AUTOML_OPTIMIZER_AVAILABLE = False; pipeline devam eder |
| openpyxl | Excel rapor | OPENPYXL_AVAILABLE = False; JSON rapor uretilir |
| matplotlib | Optuna grafikleri | Sessizce atlanir |
| lightgbm | LGB modeli | Bu model turu atlanir |
| catboost | CatBoost modeli | Bu model turu atlanir |

### ANFIS AutoML

AutoMLANFISOptimizer, PFAZ03 ANFIS konfigürasyonlarini Optuna ile arar:
- Arama uzayi: MF türü, n_mfs, max_iter, alpha (L2 reg), radii (SubClust)
- Giris: en kotu performansli dataset
- Cikis: ANFIS konfigürasyon onerisi

---

## 13. Dogrulama ve Test

**pfaz_status.json:** `failed, progress=0, 2026-03-24T17:18:33`

~~KRITIK: SyntaxError Tespiti~~ **DUZELTILDI 2026-05-09**

Gercek hata satir 41-43'te degil, `_run_anfis_for_category` metodunda satir 537-539'daydı.
`return []` sonrasındaki 3 tekrar/hatali satir silindi. Modul artik import ediliyor.

**Dogrulama:** `from pfaz_modules.pfaz13_automl.automl_retraining_loop import AutoMLRetrainingLoop` -- OK

**Gercek Cikti:** Henuz uretilmedi -- PFAZ02 bittikten sonra PFAZ13 calistir.

---

## 14. Sinirlamalar

**S-1 [KRITIK] SyntaxError:** automl_retraining_loop.py:43 -- IndentationError. 1 satir silmekle duzeltilir.

**S-2 [ORTA] n_trials=30 Dusuk:** Literatur TPE icin 100+ trial onerir. 30 trial ile kompleks arama uzayinda (DNN 6+ parametre) kureseli arama yetersiz.

**S-3 [DUSUK] model_types=['rf','xgb','lgb']:** CatBoost ve SVR default'ta yok; ancak PFAZ02'de aktif. Iyilestirme CatBoost/SVR icin yapilmiyor.

**S-4 [BILGI] Backward Compatibility:** README'de r2_threshold=0.80 parametresi var, kod icinde kullanilmiyor; POOR_MAX/MEDIUM_MAX/GOOD_MAX kategori sinirlari gercek mantigi belirliyor.

**S-5 [BILGI] PFAZ12 Bagimliligi:** PFAZ12 basarisiz oldugundan PFAZ13 istatistiksel test sonuclarina gore optimize etme yapilmayor -- bu entegrasyon eksik.

---

## 15. Sonuclar

1. **AutoML Stratejisi Akilli:** Kategori bazinda yeniden egitim, yalnizca kotu modellere odaklanmayi saglıyor.

2. **Optuna TPE Dogru Secim:** Bayesian hiperparametre optimizasyonu buyuk arama uzaylarinda grid search/random'dan ust.

3. **SyntaxError Kolay Cozum:** automl_retraining_loop.py:43 tek satir silme ile duzeltilir; ardından PFAZ01-02 tamamlaninca PFAZ13 calistirilabilir.

4. **PFAZ06 Etkisi:** PFAZ13 basarisiz -> PFAZ06 Excel'de AutoML_Improvements + AutoML_BestParams sayfaları bos.

---

## 16. Tezdeki Yeri

**Bolum 4.6 AutoML Yeniden Egitim:**
- Tablo: 'R2 < 0.80 olan modellerin Optuna sonrasi iyilesme ozeti'
- Grafik: AM13-A (Optuna optimizasyon sureci -- trial R2 gelisimi, AM13-C dan)
- Grafik: AM13-D (Iyilesme oncesi/sonrasi karsilastirmasi)

**Metodoloji Katki Argumani:**
'Sistem, kendi ciktisini degerlendirir ve dusen modelleri otomatik olarak yeniden optimize eder. Bu kendi-kendini iyilestirme dongusu, tek-seferlik egitim yaklasimlarindan ustundur.'

**Sinirlamalar Bolumu:**
'PFAZ 13 import hatasi (SyntaxError) nedeniyle calistirilamamistir. Bu hata duzeltildiginde n_trials=30 yerine 100+ kullanilmasi onerilmektedir.'

---

## 17. Kaynaklar

1. Bergstra & Bengio (2012) — Random Search for Hyper-Parameter Optimization, JMLR
2. Akiba et al. (2019) — Optuna: A Next-generation Hyperparameter Optimization Framework, KDD
3. Snoek et al. (2012) — Practical Bayesian Optimization of Machine Learning Algorithms, NIPS
4. Bergstra et al. (2011) — Algorithms for Hyper-Parameter Optimization (TPE teorisi)

---

## 18. Acik Sorular

1. **BUG-32 ne zaman duzeltilecek?** Tek satirlik fix; PFAZ01-02 tamamlaninca PFAZ13 calisabilir.
2. **n_trials=30 yeterli mi?** DNN 6+ parametre ile 30 trial kucuk -- arttirilmali mi?
3. **Excellent kategori stratejisi mantikli mi?** En dusuk Excellent R2 seçilmek üstün model gönderir; amac ne?
4. **ANFIS AutoML entegrasyonu?** PFAZ03 ile uyumlu mu yoksa standalone mi calisuyor?

---

## Ek: Bug Ozeti

| ID | Oncelik | Sorun |
|----|---------|-------|
| BUG-32 | [KRITIK] | automl_retraining_loop.py:43 IndentationError -- import hata |
| BUG-33 | [DUSUK] | n_trials=30 kucuk (onerilen 100+) |
| BUG-34 | [DUSUK] | model_types default CB/SVR eksik |
| BUG-35 | [BILGI] | r2_threshold vs POOR_MAX tutarsizligi (dokumantasyon) |

*faz-13-automl.md v1.0 | 2026-05-04*

---

## Sprint 4-13 Guncellemeleri (2026-05-11 -> 2026-05-14)

### Sprint 4 BUG-32 -- IndentationError Fix (KRITIK)

Onceki durum: `automl_retraining_loop.py:539` `return []` sonrasi 3 satir hatali indent + tekrar; PFAZ13 hicbir zaman import edilemiyordu.

Sprint 4 fix (2026-05-09):
- Hatali 3 satir silindi
- pfaz06 ayni kalip da duzeltildi (1267. satir)
- Smoke test 8/8 PASS

PFAZ13 artik import edilebiliyor ve calistirilabiliyor.

### Sprint 6 BUG-53 -- Optuna TF Memory Leak Guard (KRITIK)

`hyperparameter_tuner.py` + `automl_optimizer.py` + `automl_hyperparameter_optimizer.py` Optuna trial dongularinde TF `clear_session()` eksikti. 30+ trial x n_datasets boyunca GPU VRAM birikiyordu -- TRUBA'da `ResourceExhaustedError` riski yuksekti.

Sprint 7 fix (BUG-53):
```python
try:
    # Optuna trial logic
finally:
    tf.keras.backend.clear_session()
    gc.collect()
```

### Sprint 6 BUG-57 -- Silent Exception Temizlendi

`automl_retraining_loop.py:211, 305, 758` 3 yerde dataset yukleme ve config okuma hatalari sessizce yutuluyordu. PFAZ13 hicbir iz birakmazken calismis gozukuyordu. Sprint 7 fix ile `logger.warning(...)` eklendi.

### Sprint 13 BUG-87 -- optuna + lightgbm REQUIRED_PACKAGES

`main.py:REQUIRED_PACKAGES` listesine eklendi -- artik opsiyonel degil. TRUBA strict_truba modunda eksiklik RuntimeError verir.

### Sprint 13 BUG-88 -- strict_truba Mode

`config.json` icinde `strict_truba=true` ayari eklendi:
- PFAZ13 skipped olursa RuntimeError (eski versiyon sessiz devam)
- TRUBA'da AutoML eksik tez verir -- bu durum artik onlenir

### Sprint 13 BUG-98 -- automl_trials_details.xlsx (YENI)

`automl_improvement_report.xlsx` yaninda yeni Excel dosyasi uretilir:

| Sayfa | Icerik |
|-------|--------|
| Summary | Toplam trial, basarili/prune ozet, model tipi bazinda |
| All_Trials | Her trial: param degerleri, R2, duration_s, prune_status |
| Convergence | Best-so-far R2 progress (Optuna learning curve) |

Tez §4.6 (AutoML Optimizasyonu) icin **Convergence sayfasinin grafigi** dogrudan kullanilabilir. AM13-A grafigi olarak PFAZ8'e besleniyor.

### Sprint 13 KURAL 33 -- Cross-Layer Failure Chain

PFAZ13 skip -> Slurm afterok chain etkisi:

```
Python: PFAZ13 skip (strict_truba=true) -> RuntimeError -> sys.exit(1)
Bash:   $? = 1 -> ${PIPESTATUS[0]} = 1 (Sprint 13 BUG-85)
Slurm:  Job 3 exit 1 -> Job 4 afterok asla calismaz
```

Bu zincir Sprint 13'te `_check_upstream_failure` + PIPESTATUS fix ile dogrulandi.

### TRUBA Operasyonel Notlar

- **Job:** `job3_pfaz04_05_07_09_12_13.sh` icinde PFAZ12 sonrasi
- **Sure:** ~3-5 saat (n_per_category=25 * n_trials=30 = 750 trial/kategori)
- **Cikti:** `/arf/scratch/ahmacar/hpcv1_outputs/outputs/automl_results/`
- **Bagimlilik:** PFAZ2 (AI metrics summary)
- **Memory:** TF clear_session() guard (BUG-53)

---

*PFAZ 13 Belgesi v2.0 | Son Guncelleme: 2026-05-14*
