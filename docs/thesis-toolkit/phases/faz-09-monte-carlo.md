# PFAZ 09: Monte Carlo Belirsizlik Analizi

> **Belge Versiyonu:** v1.0  
> **Analiz Tarihi:** 2026-05-04  
> **Durum:** Kod tamamlandi (2026-04-04), gercek cikti YOK (PFAZ02 bekliyor)  
> **Ana Siniflar:** AAA2ControlGroupAnalyzerComplete + MonteCarloSimulationSystem  
> **Kapsam:** 5 dosya, 3505 satir; 5 MC yontemi; 267 cekirdek; Top-50 model

---

## 1. Genel Bakis

PFAZ 09, tezin belirsizlik katmanini olusturur. Bir model R2=0.97 diyebilir; ama bu deger tek bir tahmin noktasini temsil eder. Monte Carlo analizi soruyor: 'Bu tahmin ne kadar guvenilir? Hangi cekirdekler icin tahminler tutarli, hangileri icin modeller anlasmıyor?' Bu sorular yanitsiz kalirsa, 'bilinmeyen cekirdekler icin tahmin' iddiasi zayif kalir.

### Ana Siniflar

| Sinif | Dosya | Satir | Sorumluluk |
|-------|-------|-------|------------|
| AAA2ControlGroupAnalyzerComplete | aaa2_control_group_complete_v4.py | 1046 | Ana orkestrator; top-50 model secim/tahmin/CI |
| MonteCarloSimulationSystem | monte_carlo_simulation_system.py | 1259 | 5 MC yontemi; top-10 model; grafik/Excel/JSON |
| AAA2DataQualityChecker | aaa2_quality_checker.py | 344 | Veri kalite kontrol |
| AdvancedAnalyticsComprehensive | advanced_analytics_comprehensive.py | 821 | Ileri istatistiksel analizler |

### MC Alt-Simulatorler (MonteCarloSimulationSystem icinde)

| Simulator | Satir | Yontem | N |
|-----------|-------|--------|---|
| MCDropoutSimulator | 124-184 | DNN inference sirasinda training=True (dropout aktif) | 100 ornek |
| BootstrapSimulator | 191-277 | Percentile CI; tahmin dagilimini bootstrap ile ornekle | n_bootstrap=100 |
| NoiseSimulator | 284-368 | Girise Gaussian gurultu ekle (5 seviye) | 100 ornek/seviye |
| FeatureDropoutSimulator | 375-464 | Ozellikleri rastgele maskele (3 olasilik) | 500 ornek |
| EnsembleUncertaintyAnalyzer | 471-542 | Model arasi std (inter-model anlasmama) | -- |

---

## 2. Motivasyon

### Neden Monte Carlo?

**1. Tek tahmin belirsizlik tasimaz:** R2=0.9794 (Stacking MLP) gozlemlenirken, bu deger egitim/test bolunmesinin sansina baglidir. 267 cekirdeklik kucuk veri setinde tek bir bolunmenin degiskenligi yuksektir. MC analizi bu degiskenligi olcer.

**2. Cekirdek bazinda guven degerlendirmesi:** Tum cekirdekler icin tahmin esit guvenilir degildir. Magic number gerecisindeki cekirdekler, agir/hafif uc cekirdekler, deformasyon gecis bolgelerindeki cekirdekler daha yuksek belirsizlik gosterir.

**3. Tez iddiasini somutlastirir:** 'Bilinmeyen cekirdekler icin guvenilir tahmin' iddiasi, her cekirdek icin 95% CI olmadan temelsizdir. PFAZ 09 bu CI'yi uretir.

**4. DNN ozel durum:** MC Dropout, DNN modellerinden Bayesci tahmin dagilimlari cikarmak icin klasik yontemdir (Gal & Ghahramani, 2016).

---

## 3. Baglam

### Pipeline Sirasi: PFAZ 09 = 5. SIRADA

Gercek yurekleme: [1,2,3,4,5,**7,9**,12,13,6,8,10] -- PFAZ 09, PFAZ 07'den hemen sonra.
PFAZ 06 ve PFAZ 08'den ONCE calisir. Bu onemlidir:
- PFAZ 06 (Final Raporlama), PFAZ 09 CI verilerini Excel'e yazar
- PFAZ 08 (Gorsellestirme) ikinci geciste MC9-A/B/C grafikleri uretir

### Onceki Fazlar

- **PFAZ 01:** AAA2_enriched_all_nuclei.csv (teorik feature'ler)
- **PFAZ 02:** trained_models/ (AI .pkl)
- **PFAZ 03:** anfis_models/ (ANFIS .pkl)
- **PFAZ 07:** ensemble_results/ (ensemble tahminleri; dogrudan kullanilmiyor ama referans)

### Sonraki Fazlar

- **PFAZ 06:** AAA2_Complete_MM/QM.xlsx CI sutunlarini THESIS Excel'e alir
- **PFAZ 08:** mc_summary JSON'dan MC9-A/B/C grafikleri uretir
- **PFAZ 12:** PFAZ 09 tahmin dagilimlari uzerinde istatistiksel testler yapabilir

---

## 4. Girdi / Cikti Spesifikasyonu

### Girisler

| Kaynak | Dosya | Metod |
|--------|-------|-------|
| PFAZ01 | outputs/pfaz01/AAA2_enriched_all_nuclei.csv | load_and_enrich_aaa2_data() |
| PFAZ02 | outputs/trained_models/ | select_top50_models() |
| PFAZ03 | outputs/anfis_models/ | select_top50_models() |
| Ham | data/aaa2.txt | load_and_enrich_aaa2_data() |
| Metadata | generated_datasets/{dataset}/metadata.json | feature_names per model |

### Ciktilar

```
outputs/pfaz09/
├── AAA2_Complete_MM.xlsx          (4 ana sayfa + 11 analiz yeri tutucu)
├── AAA2_Complete_QM.xlsx          (ayni yapi)
├── aaa2_enriched_with_theory.csv  (teorik feature'lerle zenginlestirilmis 267 cekirdek)
├── monte_carlo_analysis/
│   ├── MC_Analysis_MM_*.xlsx      (4 sayfa MC metrikleri)
│   ├── MC_Analysis_QM_*.xlsx
│   ├── visualizations/
│   │   ├── MM/
│   │   │   ├── 01_uncertainty_distribution.png
│   │   │   ├── 02_uncertainty_vs_A.png
│   │   │   ├── 11_3D_uncertainty_landscape.png
│   │   │   ├── 12_3D_model_agreement.png
│   │   │   └── 13_3D_noise_robustness.png
│   │   └── QM/  (ayni grafik seti)
│   └── summaries/
│       ├── mc_summary_MM.json
│       └── mc_summary_QM.json
└── data_quality/
    └── [AAA2DataQualityChecker ciktilari]
```

### AAA2_Complete_MM.xlsx Sayfa Yapisi (generate_comprehensive_excel, satir 758-904)

| Sayfa | Sutunlar | Icerigi Neden Var? |
|-------|----------|-------------------|
| Predictions | NUCLEUS, A, Z, N, Experimental_MM, Ensemble_Mean_Pred, Ensemble_Std_Pred, Residual, Abs_Residual, Best_Model_Type, Best_Model_Source, Best_Model_TestR2 | Cekirdek bazinda tahmin ozeti |
| Uncertainty | NUCLEUS, A, Z, N, Experimental_MM, Mean_Prediction, Std_Prediction, CI_Lower, CI_Upper, CI_Width, CV, Residual | 95% CI bilgisi; PFAZ 08 MC9-C grafiginin kaynagi |
| PerModel_Top25 | NUCLEUS, A, Z, N, Experimental_MM, + 25 model sutunu (AI_RF_R2=x, ANFIS_R2=y, ...) | Her modelin ayri tahminleri; anlasmama gostergesi |
| Model_Ranking | Rank, Source (AI/ANFIS), Model_Type, Dataset, Config_ID, Test_R2, N_Features | Tezde model secim metodolojisi tablosu |
| Analysis_5..15 | Yer tutucu pivot tablolar | Ileri analizler (PFAZ12/13 ile doldurulabilir) |

**ONEMLI:** Gercek cikti MEVCUT DEGIL -- PFAZ02 tamamlaninca uretilecek.

---

## 5. Yontem

### 5.1 Iki Katmanli Yapi

PFAZ 09 iki farkli MC katmani uygular:

**Katman 1 — AAA2ControlGroupAnalyzerComplete (Top-50):**
267 cekirdek icin tum top-50 modelin tahminleri alinir. Bu bir ensemble tahmin + belirsizlik hesabidir: 50 modelin ortalamasi Mean_Pred, standart sapmasi Std_Pred, percentile yontemiyle 95% CI hesaplanir.

**Katman 2 — MonteCarloSimulationSystem (Top-10 + 5 Teknik):**
En iyi 10 model uzerinde 5 farkli MC teknigi uygulanir: MC Dropout (DNN'ler), Bootstrap, Noise Sensitivity, Feature Dropout, Ensemble Uncertainty. Bu katman hangi belirsizlik kaynaginin en buyuk etkiye sahip oldugunu olcer.

### 5.2 Model Secimi

**Top-50 (Katman 1):** select_top50_models() (satir 555-671)
- trained_models/ dizini taranir; dataset prefix MM_ veya QM_ ile filtre
- Her model icin generated_datasets/{dataset}/metadata.json okunur (feature_names alınir)
- Test_R2 siralanir; en yuksek 50 model alinir
- AI ve ANFIS modelleri birlikte taranir

**Top-10 (Katman 2):** load_top10_models() (satir 613-716)
- trained_models/performance_summary_{target}.csv okunur
- R2 sirasiyla ilk 10 secilir
- DNN .h5, diger modeller .pkl

### 5.3 Per-Model Feature Set (Kritik Tasarim)

Her model farkli ozelliklere gore egitilmistir (PFAZ01: 848 farkli dataset). PFAZ09 tahmin sirasinda her modelin kendi ozellik setini kullanmasi zorunludur:

```python
# aaa2_control_group_complete_v4.py:686-693
feature_names = record['feature_names']  # metadata.json'dan
missing = [f for f in feature_names if f not in aaa2_df.columns]
if missing:
    logger.debug(f'Skip {config_id}: missing {missing}')
    continue
X = aaa2_df[feature_names].values
y_pred = model.predict(X)
```

Bu, daha az ozellikle egitilmis bir modelin daha fazla ozellik iceren AAA2 verisiyle yanlis tahmin yapmasini onler. Ancak feature eksikligi sessizce gecilir (BUG-24).

### 5.4 95% CI Hesaplama: Percentile Yontemi

Normal approximation kullanilmiyor; dogrudan percentile:

```python
# aaa2_control_group_complete_v4.py:216-234
ci_lower = np.percentile(predictions, 2.5, axis=0)
ci_upper = np.percentile(predictions, 97.5, axis=0)
```

Percentile yontemi dagilim varsayimi gerektirmez -- non-parametric. Kucuk N icin dikkatli olmak gerekir (n=50 percentile): 2.5 percentile = 1.25. satir ~ 1-2 ornek. CI dar olabilir (BUG-27).

---

## 6. Algoritmalar

### A-032: AAA2 Top-50 Ensemble Belirsizlik Hesabi

```
GIRIS: top50_models (R2 sirali), aaa2_df (267 cekirdek), feature_sets
CIKIS: mean_pred, std_pred, ci_lower, ci_upper (n_nuclei uzunlugunda)

predictions = [] (n_models x n_nuclei matris)
FOR her model in top50:
    features = model['feature_names']
    eksik = [f for f in features if f not in aaa2_df]
    IF eksik: atlat (sessiz)
    X = aaa2_df[features]
    y = model.predict(X)
    predictions.append(y)

predictions = np.array(predictions)   # (n_valid_models, n_nuclei)
mean_pred = predictions.mean(axis=0)
std_pred  = predictions.std(axis=0)
ci_lower  = np.percentile(predictions, 2.5, axis=0)
ci_upper  = np.percentile(predictions, 97.5, axis=0)
cv        = std_pred / (|mean_pred| + eps)   # Varyasyon katsayisi
```

**Gerceklesme:** aaa2_control_group_complete_v4.py:673-752

### A-033: Bootstrap CI (BootstrapSimulator)

```
GIRIS: model, X_test, y_test, n_bootstrap=100
CIKIS: ci_lower, ci_upper (per-sample)

bootstrap_preds = []
FOR i in 1..n_bootstrap:
    idx = rastgele_secim(n_test, yenileme_ile=True)
    X_boot, y_boot = X_test[idx], y_test[idx]
    model_copy = klonla(model); model_copy.fit(X_boot, y_boot)
    bootstrap_preds.append(model_copy.predict(X_test_full))

ci_lower = percentile(bootstrap_preds, 2.5, axis=0)
ci_upper = percentile(bootstrap_preds, 97.5, axis=0)
```

**Gerceklesme:** monte_carlo_simulation_system.py:191-277

### A-034: MC Dropout (MCDropoutSimulator)

```
GIRIS: dnn_model (TensorFlow), X, n_samples=100
CIKIS: mean_pred, std_pred (Bayesci yaklasim)

preds = []
FOR i in 1..n_samples:
    y = dnn_model(X, training=True)  # Dropout AKTIF
    preds.append(y)

mean_pred = mean(preds, axis=0)
std_pred  = std(preds, axis=0)
```

Gerceklesme: monte_carlo_simulation_system.py:124-184  
Not: Yalnizca TensorFlow DNN modelleri icin gecerli; RF/XGB gibi modeller atlaniyor.

### A-035: Teorik Feature Zenginlestirme

```
GIRIS: aaa2_df (12 ham sutun)
CIKIS: aaa2_df (12 + 14 = 26+ sutun)

# Woods-Saxon (4 feature):
WS_radius = 1.25 * A^(1/3)
WS_surface_thickness = 0.65
WS_fermi_energy = 33.0 * A^(2/3) / (1.25^2 * A)
WS_potential_depth = -51.0 * (1 + 0.4*(N-Z)/A)

# Nilsson (5 feature):
Beta_2_estimated = (input veya tahmini)
Nilsson_epsilon = 0.95 * Beta_2
Nilsson_omega = 41.0 / A^(1/3) * (1 + 0.31 * |Beta_2|)
# + 2 daha

# Shell Model (5 feature):
# Sihirli sayi etkileri, orbital aciklik enerjileri
```

**Gerceklesme:** aaa2_control_group_complete_v4.py:111-202 (TheoreticalFeaturesCalculator)

---

## 7. Formuller

### F-054: Coefficient of Variation (CV) -- Belirsizlik Indeksi

$$CV_i = \frac{\sigma_i}{|\bar{y}_i| + \varepsilon}$$

$i$: cekirdek indeksi; $\sigma_i$: model arasi std; $\bar{y}_i$: ensemble ortalama; $\varepsilon = 10^{-8}$ (sifir bolme). Yuksek CV -> modeller anlasamiyor -> belirsiz cekirdek.

### F-055: Percentile 95% CI

$$CI_{95\%} = [P_{2.5}(\hat{y}_{1..n}),\ P_{97.5}(\hat{y}_{1..n})]$$

$P_{2.5}$: tahmin dagiliminin 2.5. yuzdelik dilimi. Normal dagilim varsayimi yok.

### F-056: Noise Sensitivity

$$\hat{y}_{noisy} = f(X + \mathcal{N}(0, \sigma^2_k \cdot \text{std}(X)))$$

$\sigma_k \in \{0.01, 0.02, 0.05, 0.10, 0.20\}$. Her seviyede n=100 ornek.

### F-057: Feature Dropout

$$\hat{y}_{drop} = f(X \odot M), \quad M_{ij} \sim Bernoulli(1-p)$$

$p \in \{0.1, 0.2, 0.3\}$: her ozelligin silinme olasiligi. n=500 ornek.

---

## 8. Degiskenler ve Parametreler

| Parametre | Deger | Kaynak | Aciklama |
|-----------|-------|--------|----------|
| n_models (Katman1) | 50 | select_top50_models() | Top-50 AI+ANFIS modeli |
| n_models (Katman2) | 10 | load_top10_models() | Top-10 detayli MC |
| n_samples (MC Dropout) | 100 | DEFAULT_MC_CONFIG | DNN belirsizlik ornegi |
| n_bootstrap | 100 | DEFAULT_MC_CONFIG | Bootstrap CI ornegi |
| n_samples (Noise) | 100 | DEFAULT_MC_CONFIG | Gurultu seviyesi basi |
| noise_levels | [0.01,0.02,0.05,0.1,0.2] | DEFAULT_MC_CONFIG | Gurultu katsayilari |
| n_samples (FeatureDrop) | 500 | DEFAULT_MC_CONFIG | Feature maskeleme ornegi |
| dropout_probs | [0.1,0.2,0.3] | DEFAULT_MC_CONFIG | Feature silme olasiliklari |
| consensus_threshold | 0.1 | DEFAULT_MC_CONFIG | Anlasmama esigi |
| CI level | 95% | np.percentile(2.5, 97.5) | Guven araligi |
| WS r0 | 1.25 fm | TheoreticalFeaturesCalculator | Woods-Saxon yaricap sabiti |
| WS a | 0.65 fm | TheoreticalFeaturesCalculator | Yuzey kalinligi |
| WS V0 | -51.0 MeV | TheoreticalFeaturesCalculator | Potansiyel derinligi |
| Nilsson omega0 | 41.0 MeV | TheoreticalFeaturesCalculator | Harmonik osilatour frekansi |

---

## 9. Kisaltmalar ve Semboller

| Kisaltma | Acilim |
|----------|--------|
| ACGA | AAA2ControlGroupAnalyzerComplete |
| MCSS | MonteCarloSimulationSystem |
| MCD | MC Dropout (DNN Bayesci yaklasim) |
| BS | Bootstrap Simulator |
| NS | Noise Simulator |
| FDS | Feature Dropout Simulator |
| EUA | Ensemble Uncertainty Analyzer |
| CI_95 | %95 Guven Araligi |
| CV | Coefficient of Variation (Varyasyon Katsayisi) |
| ci_width | CI ust sinir - CI alt sinir |

| Sembol | Anlam | Birim |
|--------|-------|-------|
| sigma_i | i. cekirdek icin model arasi standart sapma | hedef birimi |
| CV_i | i. cekirdek varyasyon katsayisi | boyutsuz |
| P_2.5, P_97.5 | 2.5. ve 97.5. yuzdelik dilim | hedef birimi |

---

## 10. Uygulama Detaylari

### 10.1 main.py Entegrasyonu (satir 922-931)

```python
analyzer = AAA2ControlGroupAnalyzerComplete(
    pfaz01_output_path=str(pfaz_outputs[1] / 'AAA2_enriched_all_nuclei.csv'),
    aaa2_txt_path=aaa2_path,
    trained_models_dir=str(pfaz_outputs[2]),
    output_dir=str(pfaz_outputs[9])
)
results = analyzer.run_complete_pfaz9_pipeline(targets=['MM', 'QM'])
```

### 10.2 n_jobs=8 Paralel MC

DEFAULT_MC_CONFIG: `'parallel': {'enabled': True, 'n_jobs': 8}`. MC simulasyonlari 8 paralel is ile calisir -- hiz acisindan onemli, cunku 5 MC teknigi x 2 hedef x 10 model = 100 MC is birimidir.

### 10.3 Teorik Feature Zenginlestirme Sirasi

AAA2 verisi PFAZ01'den gelen baz featurelara ek olarak 14 teorik feature alir. Bu zenginlestirme PFAZ01 ile ayni hesaplamalar; fark: PFAZ01 egitim setlerini olusturdu, PFAZ09 bilinmeyen cekirdekler icin tahmin yapacak. WS featurelari BUG-02 (HBAR_C eksik) nedeniyle 0/NaN verecek -- bu PFAZ09 icin de gecerli.

---

## 11. Hesaplama Karmasikligi

| Islem | Karmasiklik | Pratik Sure |
|-------|-------------|-------------|
| Top-50 secimi | O(n_models log n) | Saniyeler |
| Ensemble tahmin (50 model x 267 cekirdek) | O(50 x 267 x n_features) | Dakikalar |
| Bootstrap (100 yeniden egitim) | O(100 x n_train x n_features) | ~30-60 dk |
| MC Dropout (100 forward pass) | O(100 x 267 x DNN_complexity) | Dakikalar |
| Noise (5 seviye x 100 ornek) | O(500 x 267) | Dakikalar |
| Feature Dropout (3 prob x 500) | O(1500 x 267) | Dakikalar |

---

## 12. Dogrulama ve Test

pfaz_status.json: `completed, progress: 100, 2026-04-04T23:45:55`

**Gercek Cikti:** outputs/pfaz09/ dizini MEVCUT DEGIL.
PFAZ 02 henuz tamamlanmamis (PC 3 gundur calisuyor) -- top-50 model secilemez.

**PFAZ08 Baglantisi:** MC9-A, MC9-B, MC9-C grafikleri (PFAZ08 ikinci gecis) sirasiyla AAA2_Complete_{target}.xlsx -- Uncertainty sayfasindaki Std_Prediction, CV ve CI_Width sutunlarindan besleniyor.

---

## 13. Sinirlamalar

**S-1 [KRITIK] WS Feature Bug Etkisi:**
PFAZ01 BUG-02 (HBAR_C eksik) PFAZ09'u da etkiliyor. WS ozelliklerini kullanan modeller 0/NaN feature degerleriyle calisacak. Ensemble CI'si bu modelleri iceriyorsa belirsizlik tahminleri hatalı olabilir.

**S-2 [ORTA] Percentile CI Kucuk N Sorunu:**
n_bootstrap=100 ile 2.5. percentile = 2-3 ornek dayanakli. Bu CI guvenilir degil; n=1000 tercih edilir. Ancak sure artisi var.

**S-3 [ORTA] Sessiz Feature Eksikligi:**
Model feature seti ile AAA2 dataframe uyusmadığında model sessizce atlaniyor. 50 modelden kac tanesi gercekte kullanilabildigi bilinmiyor.

**S-4 [BILGI] MC Dropout Sadece DNN:**
MCDropoutSimulator yalnizca TensorFlow DNN'ler icin gecerli. RF, XGB, ANFIS icin Bayesci belirsizlik bu yontemle hesaplanamaz.

**S-5 [BILGI] PFAZ 12 Bagimliligi:**
Analysis_5..15 sayfalar PFAZ12 istatistiksel test verisiyle doldurulabilir. PFAZ 12 FAILED oldugundan bu sayfalar bos kalacak.

---

## 14. Sonuclar

1. **Iki katmanli MC (Top-50 + Top-10):** Birincisi genis kapsam (tum cekirdekler icin CI), ikincisi derinlik (5 farkli belirsizlik kaynagi).

2. **Per-model feature set kritik:** Her model kendi ozellik setiyle tahmin yapiliyor -- bu tasarim PFAZ01 veri cesitliliginden tam faydalanir.

3. **Percentile CI teorik olarak saglikli:** Normal dagilim varsayimi yok; kucuk N'de hassasiyet dusuyor (n=100 yeterince buyuk degil).

4. **PFAZ 06 ve 08 icin kritik upstream:** PFAZ09 ciktilari olmadan PFAZ06 bazi Excel sayfalarini, PFAZ08 MC9-A/B/C grafikleri boş üretiyor.

---

## 15. Tezdeki Yeri

**Bolum 4.4 Belirsizlik Analizi:**
- CV > 0.3 olan cekirdeklerin listesi ve N-Z haritasi
- CI genisligi vs. tahmin degeri scatter (MC9-C)
- Yuksek belirsizlikli cekirdeklerin fiziksel aciklamasi

**Bolum 5.3 Tahmin Belirsizligi:**
- Bilinmeyen cekirdekler icin 95% CI tablosu
- Hangi bolgeler daha guvenilir?

**Metodoloji Katki Argumani:**
MC Dropout + Bootstrap + Noise + Feature Dropout kombinasyonu, belirsizlik kaynagini cok boyutlu olcmek icin literaturde az kullanilan bir yaklasim. Bu kombinasyon nükleer veri setleri icin teze methodolojik katki saglar.

---

## 16. Kaynaklar

1. Gal & Ghahramani (2016) — Dropout as a Bayesian Approximation, ICML
2. Efron & Tibshirani (1993) — An Introduction to the Bootstrap, Chapman & Hall
3. Lakshminarayanan et al. (2017) — Simple and Scalable Predictive Uncertainty, NIPS
4. Bohr & Mottelson (1975) — Nuclear Structure Vol.1 (WS ve Nilsson modelleri)
5. Boehnlein et al. (2022) — ML in Nuclear Physics, RMP

---

## 17. Acik Sorular

1. **Kac model gercekte yukleniyor?** Feature uyumsuzlugu nedeniyle sessizce atlanan model sayisi bilinmiyor. Bu oran CV guvenirligi icin kritik.

2. **n_bootstrap=100 yeterli mi?** Literaturde 1000+ onerilir. Zaman kisiti nedeniyle 100 mi secildi?

3. **WS feature bug PFAZ09'u etkiliyor mu?** WS ozelligini kullanan modeller atlanıyor mu, yoksa 0 deger ile calisuyor mu?

4. **MC9-A/B/C grafiklerinin verisi:** PFAZ08 ikinci gecisi hangi sutundan okuyacak? AAA2_Complete_MM.xlsx -- Uncertainty -- Std_Prediction (MC9-A), CV (MC9-B), CI_Width (MC9-C). Bu sutun adlari sabit mi?

5. **PFAZ12 yoksa Analysis_5..15 bos:** Tezdeki 'istatistiksel analiz' bolumleri PFAZ09 pivot verisi olmadan yazilabilir mi?

---

## Ek: Gercek Pipeline Ciktilari

**Mevcut:** Cikti yok (outputs/pfaz09/ mevcut degil)
**Kod durumu:** Tamamlandi (2026-04-04)
**Gecikme nedeni:** PFAZ02 hala calisıyor (PC aktif) -- top-50 model henuz hazir degil

*faz-09-monte-carlo.md v1.0 | 2026-05-04*
