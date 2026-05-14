# PFAZ 04 -- Bilinmeyen Cekirdek Tahminleri
**Surum:** v2.0 | **Ilk Tarih:** 2026-05-03 | **Son Guncelleme:** 2026-05-14 (Sprint 13)
**TRUBA Job:** Job 3 (`truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh`, 18 saat limit)

---

## 1. Faz Karti

| Alan | Deger |
|------|-------|
| Faz No | PFAZ 04 |
| Durum (2026-05-03) | completed 100% |
| Modul | `pfaz_modules/pfaz04_unknown_predictions/` |
| Ana Sinif | `UnknownNucleiPredictor` |
| Ek Siniflar | `SingleNucleusPredictor`, `GeneralizationAnalyzer` |
| Giris (AI) | `outputs/trained_models/{dataset}/{model}/{config}/model_*.pkl` |
| Giris (ANFIS) | `outputs/anfis_models/{dataset}/{config}/model_*.pkl` |
| Giris (veri) | `outputs/generated_datasets/{dataset}/test.csv` |
| Cikti | `outputs/unknown_predictions/` |
| Excel | `Unknown_Nuclei_Results.xlsx` (7 sayfa) |

---

## 2. Amac ve Bilimsel Motivasyon

PFAZ 04, tezin temel bilimsel iddiasini test eden fazdir:
**Egitim setinde olmayan cekirdekleri tahmin edebilir miyiz?**

Geleneksel ML degerlenirmesinde test seti, egitimde kullanilmayan ornekleri icerir.
Nükleer fizik perspektifinden bu, sinirli deneysel veriyle hic olculmemis cekirdeklerin
momentlerini tahmin etme kapasitesini olcmek anlamina gelir.

### Iki Asamali Degerlendirme

**Asama 1: Sistematik Test** (UnknownNucleiPredictor)
Tum datasets x tum modeller kombinasyonunda test.csv uzerinde tahmin yap.
val_R2 (bilinen, egitim setine yakin) ile test_R2 (bilinmeyen) arasindaki farki olc.
Bu fark = Degradasyon = Genelleme kaybi.

**Asama 2: Tekil Cekirdek** (SingleNucleusPredictor)
Kullanici Z ve N vererek herhangi bir cekirdek icin anlik tahmin alabilir.
Yalnizca Z ve N yeterli; diger 44 ozellik TheoreticalCalculationsManager ile otomatik uretilir.
En iyi Top-25 model oy birligi (consensus) tahmin uretir.

### Kavramsal Cerceve

```
PFAZ 01: train / val / test ayirimi yapti
                 |
                 +-> test.csv = 'bilinmeyen cekirdekler'
                              (egitimde hic kullanilmadi)
                              (bu PFAZ 04'e girer)
```

Test seti orani: S70 scenariosunda %15 (~40 cekirdek); S80'de %10 (~27 cekirdek).

---

## 3. Mimari Genel Bakis

```
PFAZ 04 Bile?enleri
|
+-- UnknownNucleiPredictor.predict_unknown_nuclei()
|     Tum dataset x model kombinasyonlari
|     test.csv -> R2/RMSE/MAE + Degradasyon
|     7-sayfali Excel raporu
|     GeneralizationAnalyzer entegrasyonu
|
+-- SingleNucleusPredictor.predict_from_dict() / .predict_from_file()
|     Tek/liste cekirdek tahmini
|     Feature enrichment: TheoreticalCalculationsManager
|     Top-25 model consensus
|     Excel + JSON + grafik
|
+-- GeneralizationAnalyzer.calculate_generalization_scores()
      GS = (Test_R2 / Val_R2) * 100
      Genelleme siralaması
      Excel raporu: generalization_analysis/
```

---## 4. UnknownNucleiPredictor — Ana Akis

### 4.1 Calisma Prensibi

```python
# predict_unknown_nuclei() — unknown_nuclei_predictor.py:243
for dataset_dir in datasets_with_test_csv:      # Tum dataset klasorleri
    test_df = pd.read_csv(test.csv)
    X_test  = test_df[feature_cols].values
    nuclei  = test_df['NUCLEUS'].tolist()

    for m_info in ai_models:                     # Her AI modeli
        y_pred = model.predict(X_test)
        metrics = calc(y_true, y_pred)            # R2, RMSE, MAE
        degradation = val_r2 - test_r2            # Genelleme kaybi

    for m_info in anfis_models:                  # Her ANFIS modeli
        # Ayni akis

generate_excel_report()                          # 7 sayfa
GeneralizationAnalyzer()                         # GS hesapla
```

### 4.2 Hedef Kolon Haritalamasi

| Hedef Kodu | CSV Kolon Adı |
|-----------|--------------|
| MM | `MAGNETIC MOMENT [µ]` |
| QM | `QUADRUPOLE MOMENT [Q]` |
| Beta_2 | `Beta_2` |
| MM_QM | Her iki kolon (liste) |

*Kaynak: TARGET_COLUMNS dict, unknown_nuclei_predictor.py:57*

### 4.3 Cikti Veri Yapisi — all_results Listesi

Her model x dataset x target kombinasyonu icin bir kayit:

| Alan | Icerik |
|------|--------|
| Dataset | Veri kumesi adi |
| Target | Hedef kolon |
| Model_Category | AI veya ANFIS |
| Model_Type | RF / XGBoost / SVR / DNN / LightGBM / CatBoost / ANFIS |
| Config_ID | RF_001 / XGB_021 / CFG001 vb. |
| Train_R2 | Egitim R2 (metrics JSON'dan) |
| Val_R2 (Known) | Dogrulama R2 (bilinen cekirdekler) |
| Test_R2 (Unknown) | Test R2 (bilinmeyen cekirdekler) |
| Degradation | Val_R2 - Test_R2 (genelleme kaybi) |
| Test_RMSE | Test seti RMSE |
| Test_MAE | Test seti MAE |
| N_Test | Test ornegi sayisi |

### 4.4 7-Sayfali Excel Raporu

| Sayfa | Icerik | Siralamakriteri |
|-------|--------|----------------|
| All_Results | Tum model-dataset sonuclari | - |
| Best_Per_Dataset | Dataset x Target x Category bazinda en iyi | Test_R2 desc |
| Degradation_Analysis | Genelleme kayiplari | Degradation desc |
| AI_vs_ANFIS | AI ile ANFIS karsilastirmasi | - |
| Pivot_By_Target | Hedef bazinda ortalama Test_R2 | - |
| Pivot_By_ModelType | Model tipi bazinda ortalama Test_R2 | - |
| Per_Nucleus_Predictions | Cekirdek bazinda y_true/y_pred/hata | - |

R2 renk kodlamasi: >= 0.9 = yesil; 0.7-0.9 = sari; < 0.7 = kirmizi

---## 5. SingleNucleusPredictor — Tekil Cekirdek Tahmini

### 5.1 Desteklenen Giris Formatlari

| Format | Aciklama | Ornek |
|--------|----------|-------|
| Dict | Sozluk: {'Z':26,'N':30,'SPIN':0,'PARITY':1} | predict_from_dict() |
| pred_input.txt | Bosluk ayrimli satir: '26 30 0.0 1' | predict_from_file() |
| aaa2.txt | Orijinal veri dosyasi formati | predict_from_file() |
| .csv | Z,N,SPIN,PARITY sutunlu CSV | predict_from_file() |
| .xlsx | Ayni sutun yapisiyla Excel | predict_from_file() |

*Kaynak: single_nucleus_predictor.py:6-48, GIRIS FORMATI yorumu*
*Minimum gereksinim: Yalnizca Z ve N yeterli (SPIN/PARITY opsiyonel)*

### 5.2 Ozellik Zenginlestirme (Feature Enrichment)

Kullanicidan yalnizca Z ve N alindiktan sonra eksik ozellikler otomatik hesaplanir:

```python
# _enrich_features() — single_nucleus_predictor.py:284
if 'A' not in df.columns:
    df['A'] = df['Z'] + df['N']           # A = Z + N

# TheoreticalCalculationsManager ile:
# SEMF -> BE_per_A, BE_per_nucleon, pairing_delta
# Woods-Saxon -> V_ws, level_energies
# Nilsson -> deformation_beta2
# Schmidt -> schmidt_moment (bilgi amacli, egitimde kullanilmaz)
# Kabuk modeli -> magic_character, Z_magic_dist, N_magic_dist
```

Basarisiz olursa orijinal DataFrame dondurulur (0-fill ile devam).

### 5.3 Consensus Mekanizmasi

Her hedef icin Top-25 modelden tahmin toplanir:

```
target_preds = {model_id: y_pred_array, ...}  # Top-25 model
consensus    = mean(all model predictions)     # Aritmetik ortalama
n_models     = len(non-NaN predictions)        # Gecerli tahmin sayisi
```

Cikti sozlugu yapisi (her cekirdek icin):

```json
{
  "nucleus": "Fe-56",
  "MM": {
    "RF_RF_001_MM_150_S70_..._": 0.09,
    "XGBoost_XGB_021_..._": 0.12,
    "...",
    "consensus": 0.093,
    "n_models": 23
  },
  "QM": { "consensus": 0.0, "n_models": 20 }
}
```

### 5.4 SingleNucleusPredictor Ciktilari

| Cikti | Format | Icerik |
|-------|--------|--------|
| Excel | .xlsx | Her hedef icin model siralaması + consensus |
| JSON | .json | Tam tahmin sozlugu + summary stats |
| Grafik | PNG | Her hedef icin model tahmin dagilimi, consensus cizgisi |

---

## 6. GeneralizationAnalyzer

### 6.1 Genelleme Puani (GS) Formulü

```
GS = (Test_R2 / Val_R2) * 100
```

GS yorumlama:

| GS Aralik | Anlam |
|-----------|-------|
| >= 95% | Mukemmel genelleme |
| 85-95% | Iyi genelleme |
| 70-85% | Kabul edilebilir |
| 50-70% | Zayif genelleme |
| < 50% | Aşıri uyum (kotu) |

*Kaynak: generalization_analyzer.py:68-99*
*NOT: Val_R2 <= 0 ise GS = 0 (bolme hatasi onlemi)*

### 6.2 GeneralizationAnalyzer Cikti

Output: `unknown_predictions/generalization_analysis/`
- Genelleme puanlari Excel raporu
- Model siralaması (GS'ye gore)
- Istatistiksel ozet

---## 7. Gercek Pipeline Ciktilari

### 7.1 Durum (pfaz_status.json, 2026-05-03)

| Alan | Deger |
|------|-------|
| Durum | completed 100% |
| Not | Onceki tamamlanmis calisma turundan |

### 7.2 Cikti Dizin Yapisi

```
outputs/unknown_predictions/
  Unknown_Nuclei_Results.xlsx        # 7-sayfali ana rapor
  all_results.csv                    # CSV yedek (openpyxl yoksa)
  generalization_analysis/           # GeneralizationAnalyzer cikti
    generalization_scores.xlsx

outputs/single_nucleus_predictions/  # SingleNucleusPredictor cikti
  single_nucleus_results.xlsx
  single_nucleus_results.json
  plots/                             # PNG grafikleri
    MM_predictions.png
    QM_predictions.png
```

### 7.3 Ornek all_results Kaydi

```json
{
  "Dataset": "MM_150_S70_Standard_Standard_Random",
  "Target": "MAGNETIC MOMENT [u]",
  "Model_Category": "AI",
  "Model_Type": "RF",
  "Config_ID": "RF_001",
  "Train_R2": 0.97,
  "Val_R2 (Known)": 0.89,
  "Test_R2 (Unknown)": 0.84,
  "Degradation (Val-Test)": 0.05,
  "Test_RMSE": 0.48,
  "Test_MAE": 0.36,
  "N_Test": 23
}

```

### 7.4 Tez Icin Kritik Metrikler

PFAZ 04, tezin 'Bulgular' bolumunun temel veri kaynagindir:

| Metrik | Tez Bolumu | Anlami |
|--------|-----------|--------|
| Test_R2 (Unknown) | 4.2 Capraz Model Karsilastirmasi | Gercek genelleme performansi |
| Degradation | 4.2 | Train overfitting gostergesi |
| Generalization Score | 4.1 | Best_Per_Dataset tablosu |
| Per-nucleus hata | 5.1 Tahmin Metodolojisi | Spesifik cekirdek analizleri |
| Consensus degeri | 5.2 Model Uyumu | Top-25 model anlasmasi |

---

## 8. Model Yuklemede Dikkat Edilecekler

**Model yolu yapisi (unknown_nuclei_predictor.py:128):**

```
AI:    trained_models/{dataset}/{model_type}/{config}/model_*.pkl
ANFIS: anfis_models/{dataset}/{config}/model_*.pkl
```

**Metriklerin okunmasi:**

```python
# val_r2 okuma (kod:139-148)
metrics_file = pkl.parent / f'metrics_{config_id}.json'
val_r2 = m.get('val', {}).get('r2')   # ic ic sozluk: {'val': {'r2': 0.89}}
```

*NOT: PFAZ 02 metrics JSON'u {'val': {'r2': ...}} yapisinda, PFAZ 03 metrics JSON'u
da ayni yapıyı kullanmalidir. Yapı uyumsuzlugu val_r2=None sonuclari.*

**Cok-cikisli ANFIS (MM_QM hedefi):**

```python
# _predict_with_model (kod:206-217)
if isinstance(model, list):  # Multi-output ANFIS: model listesi
    preds = [m.predict(X) for m in model]
    return np.column_stack(preds)
```

---## 9. Tez Icin Tartisma Noktlari

**Degradasyon Analizi:**
Bazi modellerin val_R2 >> test_R2 gostermesi, test setindeki cekirdeklerin
training distribution'dan uzakligini yansitir. Nukleer fizik baginlaminda bu:
- Magic number cevresindeki cekirdekler (kuresel degil deformasyonlu) -> daha zor tahmin
- Cok agir veya cok hafif cekirdekler -> az egitim ornegi
- Gecis bolgeleri -> discontinuous behavior

Bu analiz, hangi nükleer bolgelerin tahmininin daha zor oldugunu ortaya koyar ve
tezin 'Sinirlamalar' bolumu icin kritik veriler saglar.

**Consensus Guclu/Zayif:**
Top-25 model yuksek consensus (dusuk std) -> guvenilir tahmin
Yuksek std -> modeller anlasamiyor -> bu cekirdek belirsiz/zorlu

---

## 10. Bilinen Hatalar

| Oncelik | Konum | Davranis | Duzeltme |
|---------|-------|---------|---------|
| ORTA | unknown_nuclei_predictor.py:145 | val_r2 = m.get('val',{}).get('r2') -- ic sozluk yapisi PFAZ02 ile uyumlu olmayabilir | Metriklerin JSON yapisini standardize et |
| DUSUK | generalization_analyzer.py:96 | GS = 0 if val_r2 <= 0 (negatif R2 durumu) | Negatif R2 icin farkli GS formulü |
| DUSUK | single_nucleus_predictor.py | MM_QM multi-output ANFIS model listesi | Tek-cikisli ve cok-cikisli model yuku farkli |

---

## 11. Sonraki Fazlara Bagimlilik

| Faz | Hangi Ciktiyi Kullanir | Kritik Alan |
|-----|----------------------|-------------|
| PFAZ 05 (Capraz Model) | unknown_predictions sonuclari | Test_R2, Degradation |
| PFAZ 06 (Raporlama) | Unknown_Nuclei_Results.xlsx | 7 sayfa tum veriler |
| PFAZ 07 (Ensemble) | Test seti tahminleri | Ensemble validation icin |
| PFAZ 08 (Gorsellestirme) | Per-nucleus sonuclari | Cekirdek haritası, hata dagilimi |
| PFAZ 10 (Tez) | Tum metrikler | Bulgular bolumu |

---

## 12. Kontrol Listesi

### Koddan Dogrulanan

- [x] Test seti = 'bilinmeyen' cekirdekler (val seti 'bilinen') — kod:9
- [x] 7-sayfali Excel: All_Results, Best_Per_Dataset, Degradation_Analysis, AI_vs_ANFIS, 2xPivot, Per_Nucleus (kod:460-508)
- [x] GS formulu: (Test_R2/Val_R2)*100 (kod:96)
- [x] SingleNucleusPredictor: yalnizca Z ve N yeterli; TheoreticalCalculationsManager ile zenginlestirme (kod:284)
- [x] Top-25 model consensus: mean(non-NaN tahminler) (kod:240)
- [x] R2 renk kodlamasi: >=0.9 yesil (kod:568)
- [x] ALL_TARGETS = ['MM', 'QM'] (tek hedef degil, cift hedef) (single_nucleus_predictor.py:65)

### Uretilen Ciktilar

- [ ] outputs/unknown_predictions/Unknown_Nuclei_Results.xlsx
- [ ] outputs/unknown_predictions/generalization_analysis/
- [ ] outputs/single_nucleus_predictions/ (ayrica, kullanici talebi ile)

### Tez Baglaminda

- [ ] Degradasyon tablosu Bulgular bolumune hazir mi?
- [ ] Hangi model tipleri en iyi generalise ediyor?
- [ ] Hangi nükleer bolgeler tahmin icin zorlayici?
- [ ] Consensus std dagilimi belirsizlik analizi icin yeterli mi?

---

*PFAZ 04 Belgesi v1.0 | 2026-05-03 | Kaynak: unknown_nuclei_predictor.py + single_nucleus_predictor.py + generalization_analyzer.py*
### Unknown_Nuclei_Results.xlsx -- Gercek Sayfa Yapisi (Kaynak Koddan)

**Kaynak:** `unknown_nuclei_predictor.py:447-600`

| Sayfa | Baslik | Sutunlar | Bicimleme | Neden Var? |
|-------|--------|---------|----------|-----------|
| All_Results | Tum Model Tahminleri | Dataset, Target, Model_Type, Model_Category, Test_R2(Unknown), per-nucleus verisi | R2 renk: Yesil(>=0.9), Acik Yesil(>=0.7), Sari(>=0.5), Pembe(>=0), Kirmizi(<0); AutoFilter | Hangi model, hangi veri kumesinde, hangi cekirdegi ne kadar dogru tahmin ediyor? |
| Best_Per_Dataset | Dataset x Target x Model icin en iyi R2 | Dataset, Target, Model_Category, Best_Test_R2 | En iyi sonucu vurgular | Konfigurasyon bazinda kazanan modeli hizlica bulmak |
| Degradation_Analysis | Val_R2 - Test_R2 farki (azalan sirali) | Degradation, Val_R2, Test_R2 | Degradation'a gore azalan siralama | Hangi modeller overfitting yapti? Yuksek Degradation = dusuk genelleme |
| AI_vs_ANFIS | AI ve ANFIS en iyi sonuclari | Dataset, Target, AI_Best_R2, ANFIS_Best_R2 | Karsilastirmali iki sutun | Hangi yaklasim (ML vs ANFIS) hangi veri kumesinde kazaniyor? |
| Pivot_By_Target | Hedef x Model Kategori ortalama R2 | Index: Target; Sutunlar: RF, GBM, XGB, DNN, BNN, PINN | Pivot tablo; ortalama Test_R2 | Hangi hedef (MM vs QM) hangi model tipiyle daha iyi tahmin edilebiliyor? |
| Pivot_By_ModelType | Model tipi bazinda ortalama R2 | Index: Model_Type | Pivot tablo | Model tipi bazinda genel performans ozeti |
| Per_Nucleus_Predictions | Cekirdek bazinda top-N tahminler | Nucleus, Z, N, A, Target, Model_Name, Prediction, Experimental, Error, 95%CI_Lower, 95%CI_Upper | En spesifik; cekirdek adina gore filtrelenebilir | Belirli bir cekirdek icin hangi model ne tahmin etti? Belirsizlik araligi? |

**Bicimleme:**
- Baslik: Koyu mavi (#1F4E79) zemin, beyaz kalin yazi, ortalanmis
- Freeze panes: baslik satirinda
- AutoFilter: tum sutunlarda
- Sutun genisligi: otomatik, max 40 karakter

---

## Sprint 4-13 Guncellemeleri (2026-05-11 -> 2026-05-14)

### Sprint 7 BUG-55 -- Silent Exception Temizlendi

`unknown_nuclei_predictor.py` ve `single_nucleus_predictor.py` model yukleme yerlerinde 2x silent `except: pass` kalibi `logger.warning(...)` ile degistirildi. Top-25 konsensus listesinde eksik model varsa artik nedeni TRUBA loglarinda gozukur. Tezde "model havuzu ayrintilari" §4.x bolumunde bu warning'lerden ozet cikarilabilir.

### Sprint 10 BUG-65..74 -- Inter-PFAZ Akis Standardi

PFAZ04 girdi format kontrolü:
- PFAZ02/03 metrics JSON yapisi: `{'metrics': {'val': {'r2': ...}, 'test': {'r2': ...}}}` ic sozluk yapisi sutun seviyesinde dogrulandi (BUG-73)
- Tek seviyeli `{'val_r2': ...}` fallback hala destekleniyor (BUG-74)

### Sprint 13 BUG-93 -- MC random_state=42

`SingleNucleusPredictor` Top-25 consensus hesabinda bootstrap CI uretimi artik deterministik:
- `random_state=42` sabit (eski versiyon her cagrida farkliydi)
- Tekrar uretilebilir 95% CI

### Sprint 13 PFAZ2 fail/skip Etkisi

PFAZ2 PRE-CONDITION zayifladi:
- PFAZ2 'failed' veya 'skipped' ise PFAZ4 da sessizce skip edilir
- Sebep: model havuzu bos -- consensus anlamsiz
- main.py'de `_check_upstream_failure(4)` ile

### TRUBA Operasyonel Notlar

- **Job:** `job3_pfaz04_05_07_09_12_13.sh` icindeki ilk PFAZ
- **Sure:** ~30-60 dakika
- **Cikti:** `/arf/scratch/ahmacar/hpcv1_outputs/outputs/unknown_predictions/`

---

*PFAZ 04 Belgesi v2.0 | Son Guncelleme: 2026-05-14*
