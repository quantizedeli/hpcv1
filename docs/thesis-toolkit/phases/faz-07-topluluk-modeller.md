# PFAZ 07: Topluluk ve Meta-Modeller (Ensemble Pipeline)

> **Belge Versiyonu:** v2.0
> **Ilk Analiz:** 2026-05-04 | **Son Guncelleme:** 2026-05-14 (Sprint 13)
> **Durum:** Gercek cikti mevcut (comprehensive_report.json -- eski PC)
> **Ana Sinif:** pfaz7_complete_ensemble_pipeline.py
> **TRUBA Job:** Job 3 (`truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh`)
> **Kapsam:** Sprint 6 BUG-60 sonrasi: 4 voting + 4 stacking (stacking_MLP eski analizdeki "12 yontem" yanlis)

---

## 1. Genel Bakis

PFAZ 07, PFAZ 02 (ML modelleri) ve PFAZ 03 (ANFIS modelleri) tarafindan egitilen bireysel modellerin toplu gucunden yararlanir. Temel fikir: farkli algoritmalarin farkli bolgelerde ustun oldugunu varsayarsak, bunlarin tahminlerini akillica birlestirmek herhangi bir tek modelden daha iyi sonuc verir.

En iyi sonuc: **Stacking MLP R2 = 0.9794** (comprehensive_report.json, 2026-04-02).

### Ana Siniflar

| Sinif | Dosya | Satir | Sorumluluk |
|-------|-------|-------|------------|
| EnsemblePipeline | pfaz7_complete_ensemble_pipeline.py | 1106 | Ana uretim pipeline |
| AdvancedVotingEnsemble | pfaz7_complete_ensemble_pipeline.py | 72-271 | 5 voting yontemi |
| AdvancedStackingEnsemble | pfaz7_complete_ensemble_pipeline.py | 277-402 | 6 stacking yontemi |
| DiversityAnalyzer | pfaz7_complete_ensemble_pipeline.py | 516-579 | Cesitlilik olcumu |
| RealModelLoader | pfaz7_complete_ensemble_pipeline.py | 704-796 | PKL yukleyici |
| ComprehensiveEnsembleEvaluator | pfaz7_complete_ensemble_pipeline.py | 603-687 | Metrik hesaplama |
| EnsembleModelBuilder | ensemble_model_builder.py | 497 | Voting alt-sinif |

---

## 2. Motivasyon

### Neden Ensemble?

**Model cesitliligi mevcuttur:** RF (bagging), XGBoost (boosting), SVR (kernel), DNN (derin temsil), ANFIS (bulanik kural) farkli hipotez uzaylarini tarar. Hicbiri tek basina tam degil -- birlesimi daha guclu.

**Kucuk orneklem etkisini azaltir:** 267 cekirdeklik veri tek modelin ustabilite sorununu buyutur. Stacking OOF (out-of-fold) yontemi meta-modeli egitim setine hic dokunmayan tahminlerle egitiyor -- bu, overfitting riskini azaltir.

**Fizikin bolgesel karmasikligi:** Kabuk kapanmalari civarinda davranis ani degisiyor. Bir model bu bolgede iyi, digeri duz bolgede iyi olabilir. Dinamik agirlik ayarlama bu blgesel uzmanligidan yararlanir.

**Belirsizlik olcumu icin:** Modeller arasi anlasmama (disagreement) tahmin belirsizliginin gostergesidir -- PFAZ 09 Monte Carlo analizine giris saglar.

---

## 3. Baglam

### Onceki Fazlar (Giris Kaynagi)

- **PFAZ 01:** Veri kumeleri (train/val/test CSV + metadata.json)
- **PFAZ 02:** Egitimli ML modelleri (outputs/trained_models/*.pkl + metrics.json)
- **PFAZ 03:** Egitimli ANFIS modelleri (outputs/anfis_models/*.pkl)

### Sonraki Fazlar (Cikti Kullanicisi)

- **PFAZ 05:** CrossModelEvaluator, ensemble sonuclarini ML/ANFIS ile karsilastirir
- **PFAZ 06:** FinalReportingPipeline, ensemble R2=0.9794'u THESIS Excel'e yazar
- **PFAZ 09:** Monte Carlo, ensemble tahminleri uzerinde belirsizlik analizi yapar

---

## 4. Girdi / Cikti Spesifikasyonu

### Girisler

| Kaynak | Dizin | Dosya | Kullanim |
|--------|-------|-------|----------|
| ML Modeller | outputs/trained_models/ | model_*.pkl | Tahmin icin yuklenir |
| ML Metrikler | outputs/trained_models/.../ | metrics_*.json | val_r2 ile top-N secimi |
| ANFIS Modeller | outputs/anfis_models/ | model_*.pkl | Tahmin icin yuklenir |
| Dataset CSV | outputs/generated_datasets/ | train/val/test.csv | Feature/target okuma |
| Dataset Meta | outputs/generated_datasets/ | metadata.json | feature_names, io_config |

### Ciktilar

| Dosya | Konum | Aciklama |
|-------|-------|----------|
| comprehensive_report.json | ensemble_results/evaluation/ | 12 yontem metrik ozeti |
| ensemble_report_*.xlsx | ensemble_results/ | Per-target Excel rapor |
| ensemble_comparison.xlsx | ensemble_results/ | Yontem karsilastirma tablosu |

### Excel Sayfalari (_write_ensemble_excel, satir 1022-1055)

| Sayfa | Sutunlar | Icerigi Neden Var? |
|-------|----------|-------------------|
| MM_Results | Method, R2, RMSE, MAE, N_Models | MM ensemble performans ozeti |
| MM_Predictions | nucleus_id, y_true, y_pred, error | Cekirdek bazinda MM hata analizi |
| QM_Results | Method, R2, RMSE, MAE, N_Models | QM ensemble performans ozeti |
| QM_Predictions | nucleus_id, y_true, y_pred, error | Cekirdek bazinda QM hata analizi |
| Summary | Method, Best/Worst/Avg flag | Tum metodlar en iyi/kotu karsilastirma |

---

## 5. Yontem

### 5.1 Ensemble Stratejisi Kategorileri

Bu calismada 12 ensemble yontemi: **5 Voting** + **6 Stacking** + **1 AdaBoost**.

**Voting:** Mevcut modellerin tahminlerini agirlikli/agiriksiz birlestirir. Model egitimi gerekmez. Hizli, yorumlanabilir.

**Stacking:** Mevcut modellerin tahminlerini meta-modele giris olarak kullanir. Meta-model bu tahmin kombinasyonundan yeni bir tahmin ogrenir. Daha guclu ama daha karmasik.

### 5.2 Gercek Sonuclar (comprehensive_report.json, 2026-04-02)

| # | Yontem | R2 | RMSE | MAE | Model Sayisi |
|---|--------|----|----|-----|--------|
| 1 | simple_voting | 0.9675 | 0.7057 | 0.5783 | 6 |
| 2 | weighted_voting_r2 | 0.9679 | 0.7018 | 0.5755 | 6 |
| 3 | weighted_voting_inv_error | 0.9714 | 0.6620 | 0.5462 | 6 |
| 4 | rank_based_voting | 0.9658 | 0.7246 | 0.5872 | 6 |
| 5 | dynamic_weight_adj | 0.9712 | 0.6647 | 0.5484 | 6 |
| 6 | stacking_ridge | 0.9789 | 0.5685 | 0.4647 | 6 |
| 7 | stacking_lasso | 0.9788 | 0.5706 | 0.4663 | 6 |
| 8 | stacking_elasticnet | 0.9789 | 0.5690 | 0.4616 | 6 |
| 9 | stacking_rf | 0.9761 | 0.6058 | 0.4823 | 6 |
| 10 | stacking_gbm | 0.9753 | 0.6159 | 0.5023 | 6 |
| **11** | **stacking_mlp** | **0.9794** | **0.5625** | **0.4615** | **6** |
| 12 | adaboost | 0.8282 | 1.6227 | 1.3489 | 100 |

**Gozlem:** Stacking yontemleri (R2=0.975-0.979) Voting yontemlerinden (R2=0.965-0.971) sistematik olarak ustun. AdaBoost (R2=0.828) gruptaki en zayif -- 100 model kullanmasina ragmen.

---

## 6. Algoritmalar

### A-023: Simple Voting Ensemble

```
GIRIS: P = {p_1, p_2, ..., p_n}  (n modelin tahmin vektoru)
CIKIS: p_ensemble (birlesik tahmin vektoru)

p_ensemble = (1/n) * TOPLAM(p_i, i=1..n)
```

**Gerceklesme:** pfaz7_complete_ensemble_pipeline.py:113-132

### A-024: Weighted Voting (R2-Tabanli)

```
GIRIS: P = {p_1...p_n}, R2 = {r2_1...r2_n}
CIKIS: p_weighted

r2_pos = MAKS(R2, 0)   [negatif R2 sifirla]
w_i = r2_pos_i / TOPLAM(r2_pos)
p_weighted = TOPLAM(w_i * p_i)
```

**Gerceklesme:** pfaz7_complete_ensemble_pipeline.py:134-157  
**Not:** R2 negatif olabilir (diverge etmis model) -- sifira klempler.

### A-025: Weighted Voting (Inverse Error)

```
GIRIS: P = {p_1...p_n}, RMSE = {e_1...e_n}
CIKIS: p_inv_error

inv_w_i = 1 / (RMSE_i + eps)   [eps=1e-10, sifir bolme onlemi]
w_i = inv_w_i / TOPLAM(inv_w)
p_inv_error = TOPLAM(w_i * p_i)
```

**Gerceklesme:** pfaz7_complete_ensemble_pipeline.py:159-182, satir 923

### A-026: Dynamic Weight Adjustment

```
GIRIS: P = {p_1...p_n}, RMSE = {e_1...e_n}, N_iter=10
CIKIS: p_dynamic

w = inverse_error_weights(RMSE)   [baslangiç]
FOR i in 1..N_iter:
    p_cur = TOPLAM(w * P)
    hata_i = |p_i - y_val|
    w_new = inverse_error_weights(hata_i)
    w = 0.7 * w + 0.3 * w_new   [agirlik guncelleme; 0.7/0.3 sabit]
p_dynamic = TOPLAM(w * P)
```

**Gerceklesme:** pfaz7_complete_ensemble_pipeline.py:212-256  
**Not:** 0.7/0.3 decay sabit hardcoded (tunable degil).

### A-027: Stacking ile Out-of-Fold Meta-Ogrenme

```
GIRIS: X_train, y_train, X_test, K=5
CIKIS: y_meta_test

# 1. Asama: OOF Tahminler
oof_train = sifir matris [n_train x n_base]
FOR fold in 1..K:
    X_tr, X_val = boluntur(X_train, fold)
    FOR j, base_model in enumerate(base_models):
        m_clone = kopyala(base_model)
        m_clone.fit(X_tr, y_tr)
        oof_train[val_idx, j] = m_clone.predict(X_val)

# 2. Asama: Test Tahminleri
test_preds = sifir matris [n_test x n_base]
FOR j, base_model in enumerate(base_models):
    base_model.fit(X_train, y_train)   [tam egitim seti ile]
    test_preds[:, j] = base_model.predict(X_test)

# 3. Asama: Meta-Model Egitimi
meta_model.fit(oof_train, y_train)
y_meta_test = meta_model.predict(test_preds)
```

**Gerceklesme:** pfaz7_complete_ensemble_pipeline.py:306-402  
**Meta-modeller:** Ridge, Lasso, ElasticNet, RF, GBM, MLP (satir 345-350)

### A-028: Diversity Analysis

```
GIRIS: P = {p_1...p_n}  (tahmin matrisi)
CIKIS: diversity_report (sozluk)

# Korelasyon matris
corr_matrix = korelasyon(P)
avg_corr = ort(corr_matrix ust ucgen)

# Disagreement orani
std_threshold = 0.1 * std(y_val)
disagree_rate = ORAN(std_row(P) > std_threshold)

# Cesitlilik skoru
diversity_score = 1.0 - avg_corr
```

**Gerceklesme:** pfaz7_complete_ensemble_pipeline.py:516-579

---

## 7. Formuller

### F-047: Agirlikli Voting (R2-Tabanli)

$$\hat{y}_{weighted} = \sum_{i=1}^{n} w_i \hat{y}_i, \quad w_i = \frac{\max(R^2_i, 0)}{\sum_{j=1}^{n} \max(R^2_j, 0)}$$

Negatif R2 (sapma etmis model) sifira klemplenerek toplamdaki etkisi sifirlanir.

### F-048: Inverse Error Weighting

$$w_i = \frac{1/(RMSE_i + \epsilon)}{\sum_{j=1}^{n} 1/(RMSE_j + \epsilon)}, \quad \epsilon = 10^{-10}$$

RMSE dusukse agirlik yuksek -- dogruluk odullendirilir.

### F-049: Dynamic Weight Guncelleme

$$w^{(t+1)} = 0.7 \cdot w^{(t)} + 0.3 \cdot w^{(t)}_{new}$$

Exponential moving average benzeri guncelleme; gecmis agirlik korunur.

### F-050: Cesitlilik Skoru

$$\text{Diversity Score} = 1 - \frac{1}{\binom{n}{2}} \sum_{i<j} \text{corr}(\hat{y}_i, \hat{y}_j)$$

Ciktilar arasi ortalama korelasyon ne kadar dusukse cesitlilik o kadar yuksektir.

---

## 8. Degiskenler ve Parametreler

| Parametre | Deger | Kaynak | Aciklama |
|-----------|-------|--------|----------|
| CV_FOLDS | 5 | satir 291, 315 | Stacking OOF kat sayisi |
| Top-N Models | 20 | satir 1067, 1112 | Ensemble icin en iyi N model |
| Ridge alpha | 1.0 | satir 345, 939 | Meta Ridge duzenleyici katsayi |
| Lasso alpha | 0.1 | satir 346, 940 | Meta Lasso duzenleyici katsayi |
| ElasticNet alpha | 0.1 | satir 347 | Meta EN duzenleyici |
| ElasticNet l1_ratio | 0.5 | satir 347 | L1/L2 dengeleme |
| RF n_estimators | 100 | satir 348, 941 | Meta RF agac sayisi |
| RF max_depth | 10 (satir 348) / 5 (satir 941) | --- | Tutarsiz parametre (bug) |
| GBM n_estimators | 100 | satir 349, 942 | Meta GBM tur sayisi |
| GBM max_depth | 3 | satir 349 | Meta GBM derinligi |
| MLP layers | (32, 16) | satir 350 | Meta MLP katman boyutlari |
| MLP max_iter | 500 | satir 350 | Meta MLP egitim dongusu |
| Dynamic decay | 0.7/0.3 | satir 240 | Agirlik guncelleme oranlari (hardcoded) |
| N_iterations (Dynamic) | 10 | satir 213, 226 | Dinamik agirlik iterasyon sayisi |
| Disagreement threshold | 0.1 x std(y) | satir 534 | Anlasmama olcumu esigi |
| epsilon (inv_error) | 1e-10 | satir 923 | Sifir bolme onlemi |

---

## 9. Kisaltmalar ve Semboller

| Kisaltma | Acilim |
|----------|--------|
| AVE | AdvancedVotingEnsemble |
| ASE | AdvancedStackingEnsemble |
| OOF | Out-of-Fold Predictions (egitim setinden veri sizintisi olmadan meta-egitim) |
| DA | DiversityAnalyzer |
| RML | RealModelLoader |
| CEE | ComprehensiveEnsembleEvaluator |
| w_i | i. modelin ensemble agirlik katsayisi |
| p_i | i. modelin tahmin vektoru |
| R2_i | i. modelin validasyon R-kare degeri |
| RMSE_i | i. modelin validasyon kok ortalama kare hatasi |

---

## 10. Uygulama Detaylari

### 10.1 Model Yukleme Mekanizmasi (RealModelLoader)

RealModelLoader (satir 704-796) iki adimda calisir:

**Adim 1 - Model Tarama:** outputs/trained_models/ dizinini recursive tarar. Her .pkl dosyasi icin yanindaki metrics_*.json okunur ve val_r2 cikarilir. metrics.json ic sozluk yapisi: m.get('val', {}).get('r2') -- bu yapiya dikkat (PFAZ 04 ile ayni sorun).

**Adim 2 - Top-N Secimi:** val_r2 siralanir, en yuksek 20 model ensemble'a alinir (satir 1067, 1112). Bu, kalitesiz modellerin ensemble'i bozmasini onler.

### 10.2 Ensemble Calistirma Sirasi

```
1. RealModelLoader ile top-20 model yukle
2. Dataset CSV'lerini oku (train/val/test)
3. AdvancedVotingEnsemble.fit_all() -- 5 voting yontemi
4. AdvancedStackingEnsemble.fit_all() -- 5-fold OOF + 6 meta-model egitimi
5. AdaBoost (ayri sinif)
6. ComprehensiveEnsembleEvaluator.compare_all() -- 12 sonucu karsilastir
7. DiversityAnalyzer.analyze_diversity() -- korelasyon / disagreement
8. generate_report() -> comprehensive_report.json
9. _write_ensemble_excel() -> ensemble_report_*.xlsx
```

### 10.3 JSON Serializasyon Cozumu

Numpy array'ler JSON serializasyon hatasina yol acar. Cozum (satir 676-683):
tahmin dizileri results sozlugundan cikarilir, yalnizca skalar metrikler (R2, RMSE, MAE) comprehensive_report.json'a yazilir. default=str parametresi ile non-serializable objeler string'e donusturulur. Tasarim kararinin gerekcesi buyuktur: 95k satir tahmin JSON'a yazmak dosyayi 100+ MB yapardi, pratik degil.

### 10.4 openpyxl Kontrol Mekanizmasi

```python
try:
    import openpyxl
except ImportError:
    return None   # Excel rapor atlanir
    openpyxl = None   # UNREACHABLE -- bug (satir 1028-1032)
```

openpyxl yoksa Excel atlanir, JSON rapor yine de uretilir. Unreachable kod satiri fonksiyonel zararsizdirdir ama kod kalite sorunudur.

---

## 11. Hesaplama Karmasikligi

| Islem | Karmasiklik | Aciklama |
|-------|-------------|----------|
| Simple Voting | O(n_models * n_samples) | Hizli, paralel |
| Weighted Voting | O(n_models * n_samples) | Agirlik hesabi sabit |
| Dynamic Weight (10 iter) | O(10 * n_models * n_samples) | Duz 10 kat |
| Stacking OOF | O(K * n_base * n_samples) | K=5 fold; en pahali |
| Meta-Model Egitimi | O(n_train * n_base^2) | OOF matrisi boyutunda |
| Diversity Analysis | O(n_models^2 * n_samples) | Korelasyon matrisi |

**Pratik sureler:** comprehensive_report.json timestamp'i 2026-04-02 -- bu faz onceden calistirilmis. Surelere dair log verisi mevcut degil.

---

## 12. Dogrulama ve Test

### Gercek Cikti Dogrulamasi

**Mevcut:** ensemble_results/evaluation/comprehensive_report.json (142 satir)
- timestamp: 2026-04-02T13:34:39.507670
- n_ensembles: 12
- best_r2: 0.9794 (stacking_mlp)
- worst_r2: 0.8282 (adaboost)
- avg_r2: 0.9616

**Eksik:** ensemble_report_*.xlsx -- dizinde bulunmuyor. Sadece JSON mevcut.

### Karsilastirma Kriterleri (Tez Icin)

En iyi bireysel ML modeli neydi? PFAZ 02 summary verisi ile karsilastirma:
- PFAZ 02 DNN_014 (R2 ~ 0.94-0.96 arasi) -> Stacking MLP R2=0.9794 bunu geciyor.
- Bu gelisim ensemble'in katki degeridir.

---

## 13. Sinirlamalar

**S-1 [DUSUK] Hardcoded Dynamic Decay:**
0.7/0.3 agirlik guncelleme katsayisi sabit (satir 240). Farkli veri geometrilerinde farkli degerler optimal olabilir. Tez sinirlamasi olarak ekle.

**S-2 [ORTA] RF max_depth Tutarsizligi:**
Stacking RF meta-modeli max_depth=10 (satir 348) veya max_depth=5 (satir 941) olarak farkli dosyalarda farkli tanimlanmis. Hangi deger gercekte kullanildi belli degil. Tutarli dokumantasyon eksik.

**S-3 [DUSUK] Dead Code:**
pfaz7_ensemble.py (270 satir) __init__.py'de import edilmiyor, production'da kullanilmiyor. pfaz7_ensemble_pipeline.py hardcoded Unix path (/home/claude) iceriyor.

**S-4 [BILGI] AdaBoost Zayifligi:**
AdaBoost R2=0.8282 -- 100 estimator kullanmasina ragmen en zayif sonuc. Kucuk orneklemde boosting degerlerin aykiri cekirdeklere (anomali) fazla odaklanmasina neden olabilir.

**S-5 [BILGI] Gercek PFAZ 02/03 Entegrasyonu:**
comprehensive_report.json 2026-04-02 tarihli -- bu tarihlerde PFAZ 02/03 tum modelleri bitirmemis olabilir. Ensemble icin yuklenen 6 base modelin tam listesi kayitli degil.

---

## 14. Sonuclar

### 14.1 En Onemli Bulgular

1. **Stacking MLP (R2=0.9794)** en iyi ensemble yontemi -- tum bireysel modellerden ve tum diger ensemble yontemlerinden ustun.

2. **Stacking > Voting sistematik olarak:** Stacking grubu R2=0.975-0.979, Voting grubu R2=0.966-0.971. OOF meta-ogrenme, agirlikli oylama yaklasimlarindan anlamlı olcude daha iyi.

3. **Inverse error weighting en iyi voting:** Weighted_inv_error (R2=0.9714) simple voting'i (R2=0.9675) geciyor. Hatasi dusuk modele daha fazla agirlik vermek mantiklidir.

4. **AdaBoost anomali:** 100 base estimator kullanmasina karsin R2=0.8282 -- en dusuk. 267 cekirdeklik kucuk orneklemde boosting aykiri cekirdeklere over-focus ediyor olabilir.

5. **Cesitlilik onemli:** Farkli algoritma tipleri (lineer, agac, sinir agi) kullanmak dusuk korelasyonlu tahminler uretir -- cesitlilik skoru yuksek kalir ve ensemble'in gucunu saglar.

### 14.2 Tez Icin Uyari

Bu PFAZ 07 sonuclari PFAZ 02 tam egitimi bitmeden uretilmis olabilir (tarih 2026-04-02, PFAZ 02 hala calisiyor). Tezdeki final ensemble performansi guncel model seti ile yeniden uretilmeli.

---

## 15. Tezdeki Yeri

**Bolum 4.1 Model Performansi — Ensemble Tablosu:**
12 yontemin R2/RMSE/MAE tablosu. Stacking MLP en ust satir. Karsilastirma grafigiyle.

**Bolum 4.2 CAPRAZ Model Karsilastirmasi:**
Tek model (PFAZ 02 en iyisi) vs. Ensemble (PFAZ 07 en iyisi). Delta R2 = ensemble kazancidir.

**Bolum 4.4 Belirsizlik Analizi (PFAZ 09 ile birlikte):**
Diversity score ve disagreement rate -- modeller arasi anlasmama hangi cekirdeklerde yuksek?

**Metodoloji Katki Argumani:**
Stacking ile OOF meta-ogrenme kucuk orneklemde (267 cekirdek) data leakage olmaksizin uygulanabilirligini kanitlar. Bu, nükleer veritabani calismalari icin metodolojik katki.

**Sinirlamalar (Bolum 6):**
AdaBoost zayifligi, RF max_depth tutarsizligi, tam PFAZ 02 entegrasyonu belirsizligi.

---

## 16. Kaynaklar

1. Breiman (1996) — Bagging Predictors, MLJ
2. Friedman (2001) — Greedy Function Approximation: A Gradient Boosting Machine, AS
3. Wolpert (1992) — Stacked Generalization, Neural Networks
4. Zhou (2012) — Ensemble Methods: Foundations and Algorithms, CRC Press
5. Freund & Schapire (1997) — AdaBoost, JCSS
6. Boehnlein et al. (2022) — Colloquium: ML in Nuclear Physics, RMP

---

## 17. Acik Sorular

1. **Gercek Base Model Listesi:** ensemble_results/ icinde hangi 6 model kullanilmis? Bu model listesi guncellenmis PFAZ 02 sonuclariyla eslesiyor mu?

2. **PFAZ 02 Tamamlandiktan Sonra Yeniden Calistirma:** PC 3 gundur PFAZ 02 calistiriyor. Bitince ensemble yeniden calistirilmali -- mevcut R2=0.9794 artabilir mi?

3. **QM Ensemble Sonuclari:** comprehensive_report.json yalnizca tek hedef (buyuk ihtimalle MM) icin mi calistirilmis? QM icin ayri ensemble var mi?

4. **Diversity Score Deger:** Gercek diversity score ne? Korelasyon matrisi verisi JSON'da yok.

5. **PFAZ 09 Baglantisi:** Monte Carlo belirsizlik analizi stacking_mlp tahminlerini mi yoksa tum ensemble tahminlerini mi kullanacak?

---

## Ek: Gercek Pipeline Ciktilari

**Mevcut Dosyalar:**
- ensemble_results/evaluation/comprehensive_report.json -- VAR (142 satir)
  - Timestamp: 2026-04-02T13:34:39.507670
  - 12 ensemble yontemi, tam metrikler

**Eksik Dosyalar:**
- ensemble_report_*.xlsx -- YOK (Excel uretilmemis veya farkli konumda)
- ensemble_comparison.xlsx -- YOK

*faz-07-topluluk-modeller.md v1.0 | 2026-05-04*

---

## Sprint 4-13 Guncellemeleri (2026-05-11 -> 2026-05-14)

### Sprint 6 BUG-60 -- Ensemble Yontem Sayisi Duzeltildi

CLAUDE.md eski versiyonu "5 voting + 6 stacking + AdaBoost = 12" diyordu, **gercek 4 voting + 4 stacking**. comprehensive_report.json'da "stacking_mlp R2=0.9794" var ama bu eski PC ciktisi -- TRUBA'da farkli yapilacak.

**Aktif kod (2026-05-14):**
- 4 Voting: Simple, WeightedR2, WeightedRMSE, WeightedInvError
- 4 Stacking: Ridge, Lasso, RF, GBM
- AdaBoost YOK (CLAUDE.md eski "AdaBoost" eklemesi yanlis)
- stacking_MLP YOK (eski analizdeki R2=0.9794 PC eski ciktisindandi)

Tezde **4+4** sayisini kullan:
> "Bu calismada sekiz ensemble yontemi karsilastirilmistir: dort agirlikli oylama (Simple/WeightedR2/WeightedRMSE/WeightedInvError) ve dort yiglama yaklasimi (Ridge/Lasso/RF/GBM meta-modeller)."

### Sprint 6 BUG-58 -- ThreadPoolExecutor Yorumu

`parallel_ai_trainer.py` icindeki yaniltici "ProcessPoolExecutor" yorumu duzeltildi -- gercek implementasyon `ThreadPoolExecutor` (GIL ile sklearn calisir). Bu fix dolayli olarak PFAZ7 ensemble OOF stacking icin de gecerli.

### Sprint 13 BUG-93 -- random_state=42 Sabit

EnsembleEvaluator ve stacking OOF olusturma artik `random_state=42` sabit. Tekrar uretilebilir sonuc icin kritik. Yeniden calistirma ayni R2 verir (data degismediği surece).

### TRUBA Operasyonel Notlar

- **Job:** `job3_pfaz04_05_07_09_12_13.sh` icinde PFAZ4/5 sonrasi
- **Sure:** ~1-2 saat
- **Cikti:** `/arf/scratch/ahmacar/hpcv1_outputs/outputs/ensemble_results/`
- **Bagimlilik:** PFAZ2 (AI modelleri PKL) + PFAZ3 (ANFIS PKL); PFAZ2 fail -> PFAZ7 skip

---

*PFAZ 07 Belgesi v2.0 | Son Guncelleme: 2026-05-14*
