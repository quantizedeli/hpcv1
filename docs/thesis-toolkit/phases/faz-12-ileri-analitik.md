# PFAZ 12: İleri İstatistiksel Analitik

> **Belge Versiyonu:** v1.0
> **Analiz Tarihi:** 2026-05-04
> **Durum:** Kod hazir, FAILED (progress=0, 2026-03-24) -- import/calisma hatasi
> **Ana Sinif:** StatisticalTestingSuite + NuclearPatternAnalyzer + NuclearBandAnalyzer
> **Kapsam:** 7 dosya, ~4370 satir; 6 sinif

---

## 1. Genel Bakis

PFAZ 12, model karsilastirmasi icin hem frekansci (paired t-test, Wilcoxon, ANOVA, Friedman) hem de Bayesci (Bayes Factor, ROPE) istatistiksel testler uygular. Buna ek olarak nükleer veri örüntüsü (izotop zinciri siçramalari, küme analizi) ve duyarlillik analizi (Sobol, Tornado) iceren bir analitik suiti sunar.

**Tezdeki Rolu:** R2 degeri istatistiksel anlamliligini tanimaz; RF R2=0.97, XGB R2=0.96 -- ikisi arasinda anlamli fark var mi? Bu soruyu yanitsiz birakmak tez bulgularini zayiflatir. PFAZ 12 bu boşlugu doldurur.

### Sinif Katalogu

| Sinif | Dosya | Satir | Sorumluluk |
|-------|-------|-------|------------|
| StatisticalTestingSuite | statistical_testing_suite.py | 688 | 6 test + etki buyuklugu + coklu karsilastirma |
| AdvancedSensitivityAnalysis | advanced_sensitivity_analysis.py | 646 | Sobol / Morris / Tornado duyarlillik analizi |
| NuclearPatternAnalyzer | nuclear_pattern_analyzer.py | 789 | Izotop/izoton/izobar zinciri; siçrama; sihirli sayi KS testi |
| NuclearBandAnalyzer | nuclear_band_analyzer.py | 1174 | Deger bandi ve kutle bölgesi örüntü analizi |
| BootstrapConfidenceIntervals | bootstrap_confidence_intervals.py | 586 | R2/RMSE/MAE icin n=5000 bootstrap CI |
| BayesianModelComparison | bayesian_model_comparison.py | 450 | Bayes Factor, ROPE, Jeffreys yorumlama |

**Not:** ~~`NuclearBandAnalyzer` `__init__.py`'den export edilmiyor -- BUG-31~~
**DUZELTILDI 2026-05-09:** `nuclear_band_analyzer.py` sonuna `NuclearBandAnalyzer = NuclearMomentBandAnalyzer` alias eklendi. Standart import artik calisiyor.

---

## 2. Motivasyon

### Model Karsilastirmasi Neden Test Gerektirir?

N=267 cekirdeklik kucuk veri setinde:
- Bircok model R2 farki < 0.01 -- sansa bagli mi?
- RF ve XGBoost ayni veri bolunmesinde egitildi -- bagimli olcumler
- Paired t-test bagimli olcumler icin dogru test

**Friedman Test Kritikligi:** 10+ model, 848 dataset -- cok boyutlu karsilastirma yalnizca parametrik olmayan Friedman testi ile guvenilir.

**Nükleer Örüntü Analizi Motivasyonu:**
Modeller neden kimi çekirdekleri yanlis tahmin ediyor? Yanit izotop zinciri siçramalarinda gizli olabilir. PFAZ 12 bu örüntüleri veri ile ortaya cikiyor.

---

## 3. Baglam

### PFAZ Pipeline Konumu

Pipeline sırasi: `[1,2,3,4,5,7,9,**12**,13,6,8,10]` -- 8. sirada.

**Girisler:** PFAZ02 egitim metrikleri + PFAZ09 MC CI + aaa2.txt
**Cikiş:** outputs/advanced_analytics/ (Excel + PNG grafikleri)
**Downstream:** PFAZ13 (AutoML), PFAZ06 (Band_Analizi + istatistik sayfalarindan), PFAZ09 Analysis_5..15

---

## 4. Siniflar ve Metodlar

### 4.1 StatisticalTestingSuite

**Parametreler:** `alpha=0.05` (anlamlilik esigi)

**Testler:**

| Test | Metod | Kullanim | Etki Buyuklugu |
|------|-------|---------|----------------|
| Eslestirilmis t-testi | `paired_t_test()` | 2 model, ayni veri | Cohen's d |
| Wilcoxon Isaretli Sira | `wilcoxon_test()` | Parametrik-olmayan 2 model | Cliff's delta |
| Tek-yonlü ANOVA | `one_way_anova()` | 3+ model, normal dagilim | Eta-squared |
| Friedman Testi | `friedman_test()` | Parametrik-olmayan 3+ model | -- |
| Tukey HSD | `tukey_hsd_posthoc()` | ANOVA sonrasi pairwise | -- |
| Pairwise Wilcoxon | `pairwise_wilcoxon()` | Bonferroni/Holm duzeltme | Cliff's delta |

**Etki Buyuklugu Yorumlama:**

| Olcut | Kucuk | Orta | Buyuk |
|-------|-------|------|-------|
| Cohen's d | <0.5 | <0.8 | >=0.8 |
| Eta-squared | <0.06 | <0.14 | >=0.14 |
| Cliff's delta | <0.33 | <0.474 | >=0.474 |

**Gerceklesme (paired_t_test):**
```python
differences = scores_a - scores_b
statistic, p_value = scipy.stats.ttest_rel(scores_a, scores_b)
effect_size = cohens_d_paired(scores_a, scores_b)
ci = scipy.stats.t.interval(1 - alpha, len(diff) - 1, ...)
result = {'test': 'paired_t_test', 'p_value': ..., 'significant': ..., 'effect_size_cohens_d': ..., ...}
```

**Gerceklesme (wilcoxon_test):**
```python
statistic, p_value = scipy.stats.wilcoxon(scores_a, scores_b)
effect_size = cliffs_delta(scores_a, scores_b)
```

### 4.2 AdvancedSensitivityAnalysis

| Metod | Aciklama | Cikti |
|-------|---------|-------|
| `sobol_analysis()` | Varyans tabanli -- S1 (birinci dereceden), ST (toplam etki), S2 (ikinci dereceden) | SALib formatinda dict |
| `morris_analysis()` | Ekranlama yontemi -- mu, mu_star, sigma | Etki siralaması |
| `tornado_analysis()` | +/-%10 tek-seferinde degisim | Duyarlilik araliginda siralama |
| `plot_sobol_indices()` | S1/ST bar chart | PNG |
| `plot_tornado_diagram()` | Tornado diyagrami | PNG |

**Problem Tanimı (Sobol icin):**
```python
problem = {
    "num_vars": 3,
    "names": ["A", "Z", "SPIN"],
    "bounds": [[2, 209], [1, 83], [0, 7]],
}
```

### 4.3 NuclearPatternAnalyzer

**Parametreler:**
- `jump_sigma = 2.0` -- ani degisim esigi (|delta| > 2*sigma_zincir)
- `min_chain_len = 3` -- minimum zincir uzunlugu
- `MAGIC_NUMBERS = [2, 8, 20, 28, 50, 82, 126]`
- `NEAR_MAGIC_DIST = 3` -- +/-3 birim "yakin sihirli" sayilir

**6 Analiz (her hedef MM, QM, Beta_2 icin):**

| Analiz | Metod | Aciklama |
|--------|-------|---------|
| Kume Analizi | `_mean_cluster_analysis()` | +/-1sigma, +/-2sigma bantlarina gore gruplama |
| Izotop Zinciri | `_chain_analysis(mode='isotope')` | Z sabit, N degisiyor; sicrama tespiti |
| Izoton Zinciri | `_chain_analysis(mode='isotone')` | N sabit, Z degisiyor |
| Izobar Zinciri | `_chain_analysis(mode='isobar')` | A sabit, Z degisiyor |
| Sihirli Sayi | `_magic_number_analysis()` | KS testi + Mann-Whitney |
| Sicrama Ozellik | `_jump_feature_analysis()` | T-testi (sicrama vs normal) |

**Excel Sayfalarinın Isimleri (Turkce):**
Genel_Ozet, Target_Kume, Target_Izotop_Sicrama, Target_Izoton_Sicrama, Target_Izobar_Sicrama, Target_Izotop_ZincirStat, Target_Magic_Analiz, Target_Sicrama_Ozellik, Target_Sicrama_Cekirdek

### 4.4 NuclearBandAnalyzer

**Kullanim amaci:** MM ~ 4 olan tum cekirdekler ayni banta atanir. Bu banttaki cekirdeklerin ortak fiziksel ozelliklerini bulmak.

**Konfigürasyon:**
- `N_BANDS = 6` -- otomatik band sayisi (ceyrekler + alt/ust uclar)
- Kutle bolgeleri: Hafif (A<50), Orta (50<=A<100), Agir (A>=100)
- Baglantili ornek: Band uyeligi ile hangi ozellikler korelasyon gosteriyor?

**Excel Sayfalarinın Isimleri:**
Bant_Ozeti, Sicrama_Analizi, Capraz_Kutle, Korelasyon, Cekirdek_Detay, Aciklama

~~KRITIK: NuclearBandAnalyzer `__init__.py`'den export edilmiyor (BUG-31).~~
**DUZELTILDI 2026-05-09:** Alias eklendi; standart import ve dogrudan import her ikisi de calisiyor.

### 4.5 BootstrapConfidenceIntervals

**Kullanim:** Model metrikleri (R2, RMSE, MAE) icin n=5000 bootstrap orneklem ile %95 CI.

**Not:** Bu sinif PFAZ 06 da icin benzer bir islem yapiyor (PFAZ06'da da bootstrap CI var). Ancak PFAZ 12 surum model-bazli karsilastirmayi destekliyor.

### 4.6 BayesianModelComparison

**ROPE (Region of Practical Equivalence):** `rope_percentage=0.05` (etki buyuklugünun %5'i)

**Jeffreys Yorumlama Olcegi:**

| Bayes Factor | Guc |
|-------------|-----|
| > 100 | Kesin kanit |
| 30-100 | Cok guclu |
| 10-30 | Guclu |
| 3-10 | Onemli |
| 1-3 | Zayif |

---

## 5. Pipeline Entegrasyonu

### main.py (tahmini) Cagri

```python
# PFAZ 12 main.py:~1100 bolgesinde
from pfaz_modules.pfaz12_advanced_analytics import (
    StatisticalTestingSuite, AdvancedSensitivityAnalysis,
    NuclearPatternAnalyzer
)

suite = StatisticalTestingSuite(alpha=0.05)
results = suite.compare_models_comprehensive(scores_dict)  # PFAZ09 metrikleri
suite.export_to_excel(results, "outputs/advanced_analytics/pfaz12_statistical_tests.xlsx")

# NuclearPatternAnalyzer
analyzer = NuclearPatternAnalyzer(
    data_path='data/aaa2.txt',
    output_dir='outputs/advanced_analytics',
    jump_sigma=2.0, min_chain_len=3
)
analyzer.run_all()
```

---

## 6. Algoritmalar

### A-036: Paired t-test ile Model Karsilastirma

```
GIRIS: scores_A[n], scores_B[n] (ayni veri uzerinde)
CIKIS: {p_value, significant, cohens_d, ci_lower, ci_upper}

diff = scores_A - scores_B
t, p = scipy.stats.ttest_rel(scores_A, scores_B)
d = mean(diff) / std(diff)  # Cohen's d (eslestirilmis)
ci = t.interval(1-alpha, n-1, mean(diff), sem(diff))
```

**Gerceklesme:** statistical_testing_suite.py:87-144

### A-037: Friedman Testi (Cok Modelli Siralama)

```
GIRIS: {model_i: scores_i[n_datasets]} for i in 1..k
CIKIS: {F_statistic, p_value, significant, post_hoc_table}

# Siralamalara donustur
ranks = rank_scores_per_row(scores_matrix)
# Friedman istatistigi
chi2, p = scipy.stats.friedmanchisquare(*[ranks[:,i] for i in range(k)])
```

**Gerceklesme:** statistical_testing_suite.py:~380

### A-038: Izotop Zinciri Sicrama Tespiti

```
GIRIS: nuclei(Z, N, target), jump_sigma=2.0
CIKIS: sicrama_listesi = [{Z, N_from, N_to, delta, sigma_rank}]

FOR each Z (sabit):
    zincir = [(N, target) sorted by N]
    sigma_z = std(zincir.target)
    FOR adjacent (N_i, N_i+1):
        delta = |target(N_i+1) - target(N_i)|
        IF delta > jump_sigma * sigma_z:
            sicrama_listesi.append(...)
```

**Gerceklesme:** nuclear_pattern_analyzer.py:~200

### A-039: Sobol Varyans Analizi (SALib)

```
GIRIS: problem (num_vars, names, bounds), model_predict
CIKIS: {S1[k], ST[k], S2[k*k]} -- duyarlilik indeksleri

X = SALib.sample.saltelli(problem, N=512)
Y = [model_predict(x) for x in X]
Si = SALib.analyze.sobol.analyze(problem, Y)
```

**Gerceklesme:** advanced_sensitivity_analysis.py:~100

---

## 7. Formuller

### F-058: Cohen's d (Eslestirilmis Ornekler)

$$d = rac{ar{\Delta}}{	ext{std}(\Delta)}, \quad \Delta_i = A_i - B_i$$

Buyuk etki: |d| >= 0.8

### F-059: Cliff's Delta (Parametrik-Olmayan Etki Buyuklugu)

$$\delta = rac{|\{(i,j): A_i > B_j\}| - |\{(i,j): A_i < B_j\}|}{n_A \cdot n_B}$$

$\delta \in [-1, 1]$; buyuk etki: |delta| >= 0.474

### F-060: Eta-Squared (ANOVA Etki Buyuklugu)

$$\eta^2 = rac{SS_{between}}{SS_{total}}$$

$\eta^2 \geq 0.14$ = buyuk etki (Pierce vd., 2004)

### F-061: Sobol S1 Indeksi (Birinci Dereceden Duyarlilik)

$$S_i = rac{V_i}{V(Y)}, \quad V_i = V_{X_i}[E_{X_{\sim i}}(Y|X_i)]$$

---

## 8. Degiskenler ve Parametreler

| Parametre | Deger | Kaynak |
|-----------|-------|--------|
| alpha | 0.05 | StatisticalTestingSuite |
| n_bootstrap (CI) | 5000 | BootstrapConfidenceIntervals |
| rope_percentage | 0.05 (5%) | BayesianModelComparison |
| jump_sigma | 2.0 | NuclearPatternAnalyzer |
| min_chain_len | 3 | NuclearPatternAnalyzer |
| NEAR_MAGIC_DIST | 3 | NuclearPatternAnalyzer |
| N_BANDS | 6 | NuclearBandAnalyzer |
| Sobol N | 512 | AdvancedSensitivityAnalysis (SALib default) |
| Hedefler | MM, QM, Beta_2 | NuclearPatternAnalyzer |

---

## 9. Kisaltmalar

| Kisaltma | Acilim |
|----------|--------|
| STS | StatisticalTestingSuite |
| ASA | AdvancedSensitivityAnalysis |
| NPA | NuclearPatternAnalyzer |
| NBA | NuclearBandAnalyzer |
| BCI | BootstrapConfidenceIntervals |
| BMC | BayesianModelComparison |
| ROPE | Region of Practical Equivalence |
| KS | Kolmogorov-Smirnov test |

---

## 10. Uygulama Detaylari

### Opsiyonel Kutuphaneler

| Kutuphane | Kullanim | Yoksa |
|-----------|---------|-------|
| statsmodels | Tukey HSD, multipletests | Bazi testler devre disi |
| SALib | Sobol analizi | AdvancedSensitivityAnalysis kismi calismiyor |
| matplotlib/seaborn | Grafikler | Sessizce atlanir |
| pfaz06 ExcelStandardizer | Excel formatlama | Sessizce atlanir |

### Paralel Calisma

PFAZ12 testleri tek thread uzerinde calisuyor. Friedman testi ile cok modelli karsilastirmada girdi olusturma yavaslayabilir.

---

## 11. Hesaplama Karmasikligi

| Islem | Girdi | Karmasiklik |
|-------|-------|-------------|
| Paired t-test | n orneklem | O(n) |
| Friedman | k model x m dataset | O(k*m*log(k)) |
| Sobol analizi | N=512 orneklem | O(N*k*n_eval) -- yavas |
| Bootstrap CI (n=5000) | n orneklem | O(n*n_boot) |
| Izotop zinciri sicrama | N_nuclei=267 | O(N_nuclei^2 / Z) |

---

## 12. Dogrulama

**pfaz_status.json:** `failed, progress=0, 2026-03-24T17:18:15`

**Hata Analizi:** Progress=0 -- modül import sirasinda calisiyor. Muhtemel neden:
- statsmodels import hatasi veya
- scipy.special import sorunu veya
- Pipeline orkestrasyon sorunu (doğrudan cagri yanlıs)

**Gercek Cikti:** Mevcut degil -- PFAZ12 hic tamamlanmadi.

---

## 13. Sinirlamalar

**S-1 [KRITIK] Import Hatasi:** PFAZ12 progress=0 ile basladi -- modül import veya ilk baslangic adiminda hata. Pipeline durmadan raporlandigi icin kaynak belli degil.

**S-2 [ORTA] NuclearBandAnalyzer Eksik Export:** `__init__.py`'de yok; yalnizca dogrudan import calisuyor.

**S-3 [BILGI] Sobol N=512:** Kucuk veri setinde Sobol icin 512 orneklem yeterli; ancak n_vars arttikca dogruluk duser.

**S-4 [BILGI] NuclearPatternAnalyzer Beta_2 Hedefi:** Analiz MM, QM, Beta_2 uzerinde calisuyor; ancak aktif hedefler yalnizca MM ve QM. Beta_2 sonuclari tezde kullanilmayacak.

---

## 14. Sonuclar

1. **6 test kombinasyonu guclu:** Parametrik + parametrik-olmayan + Bayesci -- model karsilastirmasi her acidan destekleniyor.

2. **Nükleer örüntü analizi eşsiz:** Izotop zinciri siçrama analizi ML literaturunde nadir; bu tezin ozgun katkilarindan biri.

3. **PFAZ 12 FAILED kritik etki:** PFAZ06 Band_Analizi sayfasi, PFAZ09 Analysis_5..15, PFAZ08 ST12-A/B grafikleri bos kaliyor.

4. **NuclearBandAnalyzer kaybolan modul:** __init__ export hatasi nedeniyle PFAZ pipeline'inda cagrilmiyor olabilir.

---

## 15. Tezdeki Yeri

**Bolum 4.5 Istatistiksel Dogrulama:**
- Tablo: 'En iyi 5 modelin Friedman testi sonuclari (chi2, p, etki buyuklugu)'
- Paired t-test: 'RF vs XGBoost istatistiksel olarak anlamli farkli mi?'

**Bolum 5.1 Nükleer Örüntü Bulgulari:**
- Izotop zinciri siçrama haritasi (ST12-A)
- Sihirli sayi gerecisinde MM/QM dagilimi (ST12-B)
- 'Sihirli sayi cevresindeki cekirdekler tahmin guclukleri en yuksek gruptu'

**Metodoloji Katki:**
Isaret sirasi testi, etki buyuklugu ve ROPE kombinasyonu istatistiksel bulgularin yorumunu
'anlamli fark var/yok' otesine tasiyor -- bu kombinasyon nukleer fizik ML calismalarinda nadir.

---

## 16. Kaynaklar

1. Cohen (1988) — Statistical Power Analysis for the Behavioral Sciences (2nd ed.)
2. Wilcoxon (1945) — Individual Comparisons by Ranking Methods
3. Friedman (1937) — The Use of Ranks to Avoid the Assumption of Normality
4. Saltelli et al. (2010) — Variance Based Sensitivity Analysis of Model Output (SALib)
5. Jeffreys (1961) — Theory of Probability (3rd ed.) -- Bayes Factor yorumlama

---

## 17. Acik Sorular

1. **PFAZ12 neden failed?** Progress=0 -- neden hic baslamadi?
2. **NuclearBandAnalyzer kullaniliyor mu?** __init__ export yok; main.py nasil cagiriyor?
3. **Sobol S2 ikinci dereceden:** 3 degisken (A, Z, SPIN) yeterli mi -- gercekte 24+ ozellik var?
4. **PFAZ12 basarisiz -> tez istatistik bolumu?** BUG-02 fix + PFAZ12 yeniden calistirma planlaniyor mu?

---

## Ek: Moduller ve Bug Ozeti

| Modul | Satir | Durum |
|-------|-------|-------|
| statistical_testing_suite.py | 688 | Kod tamam |
| advanced_sensitivity_analysis.py | 646 | Kod tamam |
| nuclear_pattern_analyzer.py | 789 | Kod tamam |
| nuclear_band_analyzer.py | 1174 | Kod tamam ama __init__ export yok |
| bootstrap_confidence_intervals.py | 586 | Kod tamam |
| bayesian_model_comparison.py | 450 | Kod tamam |
| **TOPLAM** | **4370** | FAILED (progress=0) |

*faz-12-ileri-analitik.md v1.0 | 2026-05-04*
