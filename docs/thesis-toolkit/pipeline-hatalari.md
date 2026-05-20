# Pipeline Hatalari ve Bug Takip Dosyasi

> **Proje:** Nuclear Physics AI Project v2.0.0  
> **Olusturulma:** 2026-05-03  
> **Kapsam:** PFAZ 01-04 kaynak kod analizi sonucu tespit edilen hatalar  
> **Format:** Oncelik | Konum | Etki | Fix Onerisi | Yeniden Egitim Gerekli mi?  
> **Kullanim:** Her faz belgesi kendi ilgili hatalari bu dosyadan referans alir.

---

## Oncelik Seviyeleri

| Simge | Seviye | Tanim |
|-------|--------|-------|
| [KRITIK] | Kritik | Veri kaybi veya yanlis sonuc; calisma tamamlanir ama yanlis iceriyor |
| [YUKSEK] | Yuksek | Onemli ozelligi tamamen etkisiz kiliyor; sessizce atlatiliyor |
| [ORTA] | Orta | Belirli kosullarda hata; detay kaybina neden oluyor |
| [DUSUK] | Dusuk | Kucuk tutarsizlik; sonuclari buyuk olcude etkilemiyor |
| [TASARIM] | Tasarim | Kod/dokumantasyon uyumsuzlugu; runtime hatasi degil |
| [BILGI] | Bilgi | Sinir notu; teknik borcu belgeler |

---

## Hata Ozet Tablosu

| ID | Oncelik | Faz | Dosya | Etki | Fix Durumu |
|----|---------|-----|-------|------|------------|
| BUG-01 | [KRITIK] | PFAZ 01 | qm_filter_manager.py:153 | Q=0 gecerli cekirdekler siliniyor | GECERSIZ -- Tasarim karari (Q=0 intentional) |
| BUG-02 | [YUKSEK] | PFAZ 01 | constants.py | WS ozellikleri tamamen 0/NaN | DUZELTILDI 2026-05-04 -- Yeniden egitim gerekli |
| BUG-03 | [ORTA] | PFAZ 01 | constants.py:WOODS_SAXON_PARAMS | V_so, r_so, a_so eksik | DUZELTILDI 2026-05-04 -- BUG-02 ile birlikte |
| BUG-04 | [DUSUK] | PFAZ 01 | pipeline_v2.py:1193 | data_file_mat key hatasi | GECERSIZ -- MAT formati kasitli kaldirildi |
| BUG-05 | [DUSUK] | PFAZ 02 | parallel_ai_trainer.py:1363 | seed=42 hardcoded | Bekliyor |
| BUG-06 | [TASARIM] | PFAZ 02 | config.json | Model listesi yaniltici | DUZELTILDI 2026-05-04 -- 6 dogru model eklendi |
| BUG-07 | [DUSUK] | PFAZ 03 | anfis_parallel_trainer_v2.py | SubClust KMeans fallback | Bekliyor (tez notu) |
| BUG-08 | [DUSUK] | PFAZ 03 | anfis_parallel_trainer_v2.py | Bell MF 4.kuv (standart 2b degil) | Bekliyor (tez notu) |
| BUG-09 | [BILGI] | PFAZ 03 | anfis_config_manager.py | MATLAB/Python esitsizligi | Dokumantasyon |
| BUG-10 | [ORTA] | PFAZ 04 | unknown_nuclei_predictor.py:~145 | val_r2 ic sozluk riski | DUZELTILDI 2026-05-04 |
| BUG-11 | [DUSUK] | PFAZ 04 | generalization_analyzer.py:96 | Negatif R2 icin GS=0 | DUZELTILDI 2026-05-04 |
| BUG-12 | [DUSUK] | PFAZ 04 | unknown_nuclei_predictor.py | MM_QM cok-cikis ANFIS yukleme | GECERSIZ -- MM_QM hedefi aktif degil |

---

## PFAZ 01 -- Veri Kumesi Uretimi

---

### BUG-01 [KRITIK] QM Filtre -- Gecerli Kuresel Cekirdekler Siliniyor

| Alan | Deger |
|------|-------|
| Dosya | `qm_filter_manager.py:153` |
| Sinif | `QMFilterManager._apply_qm_filter()` |
| Oncelik | [KRITIK] |
| Faz | PFAZ 01 |
| Tespit | 2026-05-02 kaynak kod analizi |

**Sorun:**  
`Q=0` olan cekirdekler gecersiz olarak filtreleniyor. Oysa spin J=0 olan cekirdeklerin elektrik kuadrupol momenti sifirdir; bu fiziksel olarak tutarlidir ve veri setine dahil edilmelidir.

**Etki:**  
- Cift-cift cekirdeklerin buyuk kismi (J=0, Q=0) QM veri setinden siliniyor.  
- QM egitim seti sistematik olarak tarafli hale geliyor (yalnizca Q != 0 ornekler).  
- RF/XGBoost/ANFIS modelleri Q=0 durumunu hic gormeden egitiliyor.  
- Mevcut calisma da bu hatali filtreyle uretilmis veri uzerinde.

**Mevcut Calisma Etkisi:** Sessizce atlatiliyor. Egitim tamamlanir, ama QM modelleri J=0 cekirdeklere yabancidir.

**Fix:**  
```python
# qm_filter_manager.py:153
# YANLIS:
if qm_value == 0:
    continue

# DOGRU: Yalnizca NaN'i filtrele, Q=0 gecerlidir
if pd.isna(qm_value):
    continue
```

**Yeniden Egitim Gerekli:** EVET -- QM modelleri fix sonrasi yeniden egitilmeli.

**Tez Notu:** Metodoloji bolumunde 'QM veri seti filtreleme kriterleri' altinda bu sinirlamayi belgelemek gerekir.

---

### BUG-02 [YUKSEK] Woods-Saxon HBAR_C Import Hatasi -- WS Ozellikleri Tamamen 0/NaN

| Alan | Deger |
|------|-------|
| Dosya | `woods_saxon.py:15` |
| Sinif | `WoodsSaxonCalculator.__init__()` |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 01 |
| Tespit | 2026-05-02 kaynak kod analizi |

**Sorun:**  
`constants.py` dosyasinda `HBAR_C` sabiti tanimlanmamis. `woods_saxon.py:15` bu sabiti import etmeye calisiyor ve `ImportError` aliyor. Ancak `try/except` blogu hatay sessizce yakalayip WS hesaplamalarini es geciyor.

**Etki:**  
- `WoodsSaxonCalculator` hicbir zaman basariyla olusturulmuyor.  
- Tum veri kumelerinde WS turevi ozellikler (V_ws, r_ws vb.) 0.0 veya NaN degeri aliyor.  
- Bu hata hicbir log'a yansimiyor.  
- Mevcut PC calismasinda (3+ gun) WS ozellikleri gecersiz -- sonuclar icsel tutarli ama WS bilgisi tamamen eksik.

**Mevcut Calisma Etkisi:** Sessizce devam ediyor. PC durdurulmamali; fix sonrasi yeniden calistirmak yeterli.

**Fix:**  
```python
# constants.py dosyasina su satiri ekle:
HBAR_C = 197.3269804  # MeV * fm (hbar*c, nükleer fizik birimi)
```

**Yeniden Egitim Gerekli:** EVET -- WS ozellikleri duzeltildikten sonra tum dataset uretimi ve model egitimi yenilenmelidir.

---

### BUG-03 [ORTA] Woods-Saxon Spin-Yorun Parametreleri Eksik

| Alan | Deger |
|------|-------|
| Dosya | `woods_saxon.py:73-75` |
| Sinif | `WoodsSaxonCalculator.compute_spin_orbit()` |
| Oncelik | [ORTA] |
| Faz | PFAZ 01 |
| Tespit | 2026-05-02 kaynak kod analizi |

**Sorun:**  
Spin-yorun potansiyeli parametreleri (`V_so`, `r_so`, `a_so`) tanimlanmamis veya varsayilan degerlere sahip degil. Bu parametreler olmadan spin-yorun hesaplamalari dogru sonuc uretemiyor.

**Etki:**  
- BUG-02 (HBAR_C eksik) nedeniyle WS hesaplamalari zaten calismiyor; bu hata simdilik tetiklenmiyor.  
- BUG-02 duzeltildiginde BUG-03 aktif hale gelecek ve spin-yorun ozellikleri yanlis hesaplanacak.

**Mevcut Calisma Etkisi:** BUG-02 maskeliyor; su an sessiz.

**Fix:**  
```python
# woods_saxon.py spin-orbit parametreleri ekle:
V_so = 6.0    # MeV -- spin-orbit derinligi (standart deger)
r_so = 1.25   # fm  -- spin-orbit yaricap parametresi
a_so = 0.67   # fm  -- spin-orbit yuzey yayilimi
```

**Yeniden Egitim Gerekli:** BUG-02 ile birlikte EVET.

---

### BUG-04 [DUSUK] Pipeline MAT Anahtar Hatasi -- Kaldirilmis Referans

| Alan | Deger |
|------|-------|
| Dosya | `pipeline_v2.py:1193` |
| Sinif | `DatasetGenerationPipelineV2._build_dataset_metadata()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 01 |
| Tespit | 2026-05-02 kaynak kod analizi |

**Sorun:**  
`data_file_mat` anahtari kodda referanslandiriliyor, ancak MAT egitim modu pipeline'dan kaldirilmis. Bu, metadata sozlugune erisimde `KeyError` olusturabilir.

**Etki:**  
- MAT egitimi cagrilmadigi surece sessiz.  
- Ileriki faz genislemelerinde veya debug sirasinda yaniltici hata mesaji.

**Fix:**  
```python
# pipeline_v2.py:1193 -- ya anahtari kaldir ya da None varsayili yap:
data_file_mat = metadata.get('data_file_mat', None)  # Kaldirildi, guvenli erisim
```

**Yeniden Egitim Gerekli:** HAYIR -- yalnizca guvenlik duzeltmesi.

---

## PFAZ 02 -- Yapay Zeka Egitimi

---

### BUG-05 [DUSUK] Seed Hardcoded -- Uretkenlik Kisitli

| Alan | Deger |
|------|-------|
| Dosya | `parallel_ai_trainer.py:1363` |
| Sinif | `ParallelAITrainer._set_random_seed()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 02 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
`seed=42` sabit kodlanmis. Kaynak yorumunda 'Currently hardcoded, should be in config' notu mevcut. Farkli seed denemeleri (istatistiksel guvenilirlik icin) manuel degisiklik gerektirir.

**Etki:**  
- Her calisma ayni rastgelelik dizisini uretir -- tekrarlanabilirlik iyi.  
- Ancak bootstrap belirsizlik analizi veya seed duyarliligi testi yapilamaz.

**Fix:**  
```python
# config.json'a ekle:
# "random_seed": 42

# parallel_ai_trainer.py:1363:
seed = self.config.get('random_seed', 42)  # config'den oku, fallback 42
```

**Yeniden Egitim Gerekli:** HAYIR -- mevcut ciktilar gecerli; config tasimasi isteye bagli.

---

### BUG-06 [TASARIM] config.json Model Listesi Yaniltici

| Alan | Deger |
|------|-------|
| Dosya | `config.json` (proje kok dizini) |
| Oncelik | [TASARIM] |
| Faz | PFAZ 02 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
config.json'daki model listesi: `['RF','GBM','XGBoost','DNN','BNN','PINN']`  
Gercekte aktif olan modeller: `RF, XGBoost, LightGBM, CatBoost, SVR, DNN`  
GBM, BNN, PINN config'de gorunuyor ancak `parallel_ai_trainer.py:1760-1776`'da
aktif olarak yuklenmiyorlar. LightGBM, CatBoost, SVR ise config'de gozukmuyor
ama kodda aktif.

**Etki:**  
- Proje dokumantasyonu hazirlanirken yanlis model sayisi/turu yazilabilir.  
- Tez metodoloji bolumunde hatali model listesi yer alabilir.  
- Runtime hatasi yok; yalnizca yaniltici dokumantasyon.

**Fix:**  
```json
// config.json model_types guncellenmeli:
"model_types": ["RF", "XGBoost", "LightGBM", "CatBoost", "SVR", "DNN"]
```

**Yeniden Egitim Gerekli:** HAYIR -- dokumantasyon duzeltmesi.

---

### SPRINT-1-IYILESTIRME Cift R2 Filtresi Uygulamaya Alindi [TAMAMLANDI 2026-05-08]

| Alan | Deger |
|------|-------|
| Dosya | `parallel_ai_trainer.py` + `config.json` + `config_desktop.json` |
| Sprint | Sprint 1 |
| Durum | UYGULAMAYA ALINDI |

**Degisiklik:**
- CV blogu model kaydinin ONCESINE tasindi (onceden SONRASINDAYDI)
- Yeni filtre: cv_R2 >= 0.0 (Shang et al. 2022) + gap < 0.6 (Utama et al. 2016)
- Adaptif fold sayisi: N<150 -> 3-fold, N>=150 -> 5-fold
- [DUAL_FILTER] log mesajlari: KABUL/RET gorulur
- config.json ve config_desktop.json: cv_r2_min_threshold=0.0, max_train_cv_gap=0.6 eklendi

**Yeniden Egitim Gerekli:** EVET -- mevcut kayitli modeller yeni filtreye tabi tutulmadi.

---

## PFAZ 03 -- ANFIS Egitimi

---

### BUG-07 [DUSUK] SubClust Python Gercek Subtractive Clustering Degil (KMeans Fallback)

| Alan | Deger |
|------|-------|
| Dosya | `anfis_parallel_trainer_v2.py` |
| Metod | `TakagiSugenoANFIS._init_subclust()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 03 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
ANFIS SubClust konfigurasyonlari (CFG006/007/008) MATLAB genfis2 (subtractive clustering) ile baslatilmasi icin tasarlanmis. Ancak Python implementasyonu KMeans kullanarak kume merkezlerini buluyor. Gercek subtractive clustering'de `radii` parametresi kume sayisini dogrudan etkiler; KMeans'de `k` manuel verilir.

**Etki:**  
- CFG006 (radii=0.3), CFG007 (radii=0.5), CFG008 (radii=0.7) arasindaki fark
  minimumdur -- hepsi benzer KMeans baslangic noktasiyla calisiyor.  
- Kume sayisi: `k = min(n_rules, max(2, n_train//4))` -- radii etkisiz.  
- SubClust konfigurasyonlarinin diferansiyasyonu gercek anlamda test edilemiyor.

**Mevcut Calisma Etkisi:** Modeller egitiliyor ve R2>=0.5 esigini geciyorsa kaydediliyor; sonuclar gecerli ama SubClust'in teorik avantaji realize edilemiyor.

**Fix Onerisi:**  
Gercek subtractive clustering Python implementasyonu ekle (skfuzzy.cluster.subtractive)
veya tezde sinirlamasi acikca belirt: 'Python implementasyonunda MATLAB genfis2 karsiligi
KMeans tabanli baslatma kullanilmistir; tam esitsizlik mevcuttur.'

**Yeniden Egitim Gerekli:** HAYIR -- gercek SubClust istenirse EVET (senaryo farki kucuk).

---

### BUG-08 [DUSUK] Bell MF 4. Kuvet Kulaniyor (Standart gbellmf 2b degil)

| Alan | Deger |
|------|-------|
| Dosya | `anfis_parallel_trainer_v2.py` |
| Metod | `TakagiSugenoANFIS._bell()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 03 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
Standart genellestirmis bell UF (gbellmf) formulü: `1 / (1 + |(x-c)/a|^(2b))`
Python implementasyonu: `1.0 / (1.0 + np.abs((x-c)/s)**4)` -- sabit 4. kuvet.
Bu, b=2 parametresini sabit kilip parametre esnekligini azaltiyor.

**Etki:**  
- Bell MF sekli standarttan farkli (daha dik kenarlar).  
- Egitim sirasinda b parametresi ogrenilemiyor.  
- Kucuk fark; tipik nukleer veri icin bell genisligi zaten s ile kontrol edilir.

**Fix Onerisi:**  
```python
# Parametrik b ekle (esnek bell):
def _bell(self, x, c, s, b=2.0):
    return 1.0 / (1.0 + np.abs((x - c) / (s + 1e-10)) ** (2 * b))
```

**Yeniden Egitim Gerekli:** HAYIR -- uygulama tercihi; tezde belgelenebilir.

---

### BUG-09 [BILGI] MATLAB genfis2 / Python KMeans Esitsizligi

| Alan | Deger |
|------|-------|
| Dosya | `anfis_config_manager.py` |
| Oncelik | [BILGI] |
| Faz | PFAZ 03 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
MATLAB CFG dosyalari `genfis2(tr, radii)` cagrilari iceriyor -- gercek subtractive clustering.
Python tarafinda bu cagri `KMeans(n_clusters=k)` ile karsilaniyor.
iki implementasyonun matematiksel sonuclari farkli; cross-platform reproducibility yok.

**Etki:**  
- MATLAB sonuclari Python sonuclariyla karsilastirilamiyor.  
- Tez karsilastirmasinda 'MATLAB vs Python ANFIS' yapilacaksa bu fark onemli.

**Tavsiye:**  
Tezde acikca belirt: 'Python implementasyonu MATLAB genfis2 ile tam esit degildir. Subtractive clustering yerine KMeans tabanli kume baslatma kullanilmistir. Bu durum BUG-07 ile ayni koktene sahiptir.'

---

## PFAZ 04 -- Bilinmeyen Cekirdek Tahminleri

---

### BUG-10 [ORTA] val_r2 Ic Sozluk Riski -- Degradasyon Kolonu Bos Kalabilir

| Alan | Deger |
|------|-------|
| Dosya | `unknown_nuclei_predictor.py:~145` |
| Sinif | `UnknownNucleiPredictor._load_ai_models_for_dataset()` |
| Oncelik | [ORTA] |
| Faz | PFAZ 04 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
PFAZ 04 val_r2'yi okurken ic-ic sozluk yapisi kullaniyor:
```python
val_r2 = m.get('val', {}).get('r2')  # ic sozluk bekleniyor
```
PFAZ 02 egitim ciktisinda metrics JSON flat (duz) yapi kullaniyorsa:
```python
# PFAZ 02 olasilik: {"val_r2": 0.85}  # flat
# PFAZ 04 bekliyor: {"val": {"r2": 0.85}}  # ic-ic
```
Bu uyumsuzlukta `val_r2 = None` donuyor; Degradasyon = `Val_R2 - None` = NaN.

**Etki:**  
- Degradasyon kolonu kismen veya tamamen bos kalabilir.  
- Generalization Score hesaplanamaz (GS = None / known_r2 = hata).  
- Excel raporunda Degradation_Analysis sayfasi eksik veri iceriyor.

**Dogrulama Yontemi:**  
```bash
# Bir PFAZ 02 cikti JSON'unu oku:
# outputs/trained_models/<dataset>/RF/RF_001/metrics.json
# Yapinin flat mi ic-ic mi oldugunu kontrol et
```

**Fix Onerisi:**  
```python
# Guvenli okuma (her iki yapiya da uyumlu):
if isinstance(m.get('val'), dict):
    val_r2 = m['val'].get('r2')
else:
    val_r2 = m.get('val_r2')  # flat yapi fallback
```

**Yeniden Egitim Gerekli:** HAYIR -- fix sonrasi PFAZ 04 yeniden calistirilmali.

---

### BUG-11 [DUSUK] Generalization Score Negatif R2 icin GS=0 Donuyor

| Alan | Deger |
|------|-------|
| Dosya | `generalization_analyzer.py:96` |
| Sinif | `GeneralizationAnalyzer.calculate_generalization_scores()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 04 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
```python
# generalization_analyzer.py:96
if known_r2 <= 0:
    gs = 0.0  # veya None
else:
    gs = (unknown_r2 / known_r2) * 100
```
Negatif R2 durumunda (model sabit tahmin ortalamadan bile kotu) GS=0 donuyor.
Ancak negatif R2, modelin tamamen basarisiz oldugunu gosteriyor; bu GS=0 ile ozetlenemez.

**Etki:**  
- Kotu modeller (R2 < 0) GS=0 ile iyi modeller (R2=0.0, GS=0) ile karistiriliyor.  
- Tablo yorumlamasi yaniltici: val_r2=0.01, test_r2=-0.5 -> GS=0; ama val_r2=0.0 da GS=0.

**Fix Onerisi:**  
```python
if known_r2 <= 0:
    gs = None  # GS tanimsiz -- yorumlanamaz durum
elif unknown_r2 < 0:
    gs = 0.0   # Model basarisiz; GS=0 kabul edilebilir
else:
    gs = (unknown_r2 / known_r2) * 100
```

**Yeniden Egitim Gerekli:** HAYIR -- analiz kodu duzeltmesi.

---

### BUG-12 [DUSUK] MM_QM Cok-Cikisli ANFIS Model Yukleme Farkliligi

| Alan | Deger |
|------|-------|
| Dosya | `unknown_nuclei_predictor.py` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 04 |
| Tespit | 2026-05-03 kaynak kod analizi |

**Sorun:**  
MM_QM cok-cikisli (2-output) ANFIS modelleri, tek-cikisli modellerden farkli yukleme
mantigina ihtiyac duyar. Mevcut `_load_anfis_models_for_dataset()` metodu bu ayrimi
her zaman dogru islemeyebilir.

**Etki:**  
- MM_QM ANFIS modelleri bilinmeyen cekirdek tahminlerinde kullanilamayabilir.  
- `TARGET_COLUMNS` mapping dogru ama model yukleme sonrasinda tahmin fonksiyonu
  2 cikis yerine 1 cikis bekliyorsa hata ortaya cikar.

**Tavsiye:**  
PFAZ 04 calisma loglarinda MM_QM modeli yukleme basarisi kontrol edilmeli.

**Yeniden Egitim Gerekli:** HAYIR -- yukleme mantigini duzelt.

---

## Fix Onceliklendirme Sirasi

Yeniden egitim oncesinde uygulanmasi gereken fix sirasi:

```
1. BUG-02 [YUKSEK] -- constants.py HBAR_C ekle (5 dakika, tek satir)
2. BUG-01 [KRITIK] -- qm_filter_manager.py Q=0 filtre duzelt (10 dakika)
3. BUG-03 [ORTA]   -- woods_saxon.py V_so, r_so, a_so ekle (BUG-02 sonrasi)
4. BUG-10 [ORTA]   -- PFAZ 04 val_r2 okuma uyumsuzlugu (dogrula + duzelt)
5. BUG-06 [TASARIM] -- config.json model listesi guncelle
6. BUG-04 [DUSUK]  -- pipeline_v2.py MAT key guvenli erisim
7. BUG-05 [DUSUK]  -- seed config'e tasi
8. BUG-11 [DUSUK]  -- GS None vs 0 ayrimi
9. BUG-07/08/09    -- ANFIS dokumantasyon + opsiyonel gercek SubClust
10. BUG-12 [DUSUK] -- MM_QM yukleme dogrulama
```

---

## Tez Sinirlamalar Bolumu Icin Ozet

Bu hatalar tezin 'Sinirlamalar' bolumunde asagidaki gibi sunulabilir:

1. **Veri Filtresi Tarafliligi (BUG-01):** QM veri seti, Q=0 olan kuresel cekirdekler
   yanlilikla dislanmistir. Bu durum, QM tahmin modellerinin kuresel cekirdeklerde
   sinirli performans gostermesine yol acabilir.

2. **Eksik Ozellik Grubu (BUG-02):** Woods-Saxon potansiyelinden turetilen ozellikler
   (V_ws, spin-orbit terimleri) mevcut calisma kapsaminda hesaplanamamistir.
   Bu ozellikler gelecek calismada dahil edilecektir.

3. **SubClust Yaklasimi (BUG-07/09):** ANFIS SubClust konfigurasyonlari icin Python
   implementasyonunda MATLAB genfis2 karsiligi KMeans tabanli baslatma
   kullanilmistir. Tam esdegerlik saglanamamistir.

---

*pipeline-hatalari.md v1.2 | 2026-05-04 | 18 bug, PFAZ 01-06 kapsami*

> **Genisletilmis Ozet -- BUG-13..BUG-38 Durumlari**
>
> | ID | Oncelik | Faz | Fix Durumu |
> |----|---------|-----|------------|
> | BUG-13 | [DUSUK] | PFAZ 05 | Bekliyor (tez notu) |
> | BUG-14 | [DUSUK] | PFAZ 05 | Bekliyor |
> | BUG-15 | [BILGI] | PFAZ 05 | Dokumantasyon |
> | BUG-16 | [ORTA] | PFAZ 06 | Bekliyor (PFAZ12/13 yeniden baslat) |
> | BUG-17 | [DUSUK] | PFAZ 06 | Bekliyor |
> | BUG-18 | [BILGI] | PFAZ 06 | Dokumantasyon |
> | BUG-19 | [ORTA] | PFAZ 07 | DUZELTILDI 2026-05-04 -- STACKING_RF_MAX_DEPTH=10 |
> | BUG-20 | [DUSUK] | PFAZ 07 | DUZELTILDI 2026-05-04 -- Unix path kaldirildi |
> | BUG-21 | [DUSUK] | PFAZ 08 | Bekliyor |
> | BUG-22 | [DUSUK] | PFAZ 08 | Bekliyor |
> | BUG-23 | [BILGI] | PFAZ 08 | Bekliyor |
> | BUG-24 | [ORTA] | PFAZ 09 | Bekliyor (config.json guncellenmeli) |
> | BUG-25 | [ORTA] | PFAZ 09 | Bekliyor |
> | BUG-26 | [DUSUK] | PFAZ 09 | Dokumantasyon |
> | BUG-27 | [ORTA] | PFAZ 09 | BUG-02 ile birlikte cozulur |
> | BUG-28 | [DUSUK] | PFAZ 09 | Bekliyor (PFAZ12 yeniden baslat) |
> | BUG-29 | [DUSUK] | PFAZ 09 | DUZELTILDI 2026-05-04 -- adaptive n_jobs |
> | BUG-30 | [DUSUK] | PFAZ 09 | DUZELTILDI 2026-05-04 -- MM/QM threshold notu |
> | BUG-31 | [ORTA] | PFAZ 12 | DUZELTILDI 2026-05-04 -- __init__.py export eklendi |
> | BUG-32 | [KRITIK] | PFAZ 13 | DUZELTILDI 2026-05-04 -- IndentationError kaldirildi |
> | BUG-33 | [DUSUK] | PFAZ 13 | Bekliyor |
> | BUG-34 | [DUSUK] | PFAZ 13 | DUZELTILDI 2026-05-04 -- cb+svr default listeye eklendi |
> | BUG-35 | [BILGI] | PFAZ 13 | Dokumantasyon |
> | BUG-36 | [BILGI] | PFAZ 12 | Bekliyor (import tani) |
> | BUG-37 | [DUSUK] | PFAZ 10 | DUZELTILDI 2026-05-04 -- project_dir='.' |
> | BUG-38 | [BILGI] | PFAZ 10 | Dokumantasyon (BUG-24 ile birlikte coz) |

## PFAZ 05 -- Capraz Model Analizi

---

### BUG-13 [DUSUK] CrossModelEvaluator R2 Tek Noktadan Yaklasim

| Alan | Deger |
|------|-------|
| Dosya | `cross_model_evaluator.py:204-210` |
| Metod | `CrossModelEvaluator._calculate_aggregate_performance()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 05 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**  
Cekirdek duzeyinde R2 hesaplamasinda tek noktadan yaklasim kullaniliyor:
```python
# cross_model_evaluator.py:204-210
r2_approx = 1 - (error / abs(target))**2  if abs(target) > 1e-6 else 0.0
```
Gercek R2, bircok ornekten hesaplanir. Tek-nokta yaklasimi agirlikli ortalama veya kucuk target degerleri (orn. MM ~ 0.1) icin yanlis sonuc verebilir.

**Etki:**  
- `mean_r2` cekirdek siniflandirmasinda (Good/Medium/Poor) kullaniliyor.  
- Kucuk hedef degerlerinde R2_approx yanlis hesaplanabilir.  
- MM gibi cok kucuk degerli (0.1-5 muN arasi) cekirdekler yanlis kategorize olabilir.

**Fix Onerisi:**  
Birden fazla model varyasyonu uzerinden gercek R2 hesabi yapilmali. Ya da siniflandirma yalnizca `mean_error` esigine dayandirip `mean_r2` kriter disi birakilmali.

**Yeniden Egitim Gerekli:** HAYIR -- analiz kodu duzeltmesi.

---

### BUG-14 [DUSUK] BestModelSelector Agirliklar Hardcoded

| Alan | Deger |
|------|-------|
| Dosya | `best_model_selector.py:59-73` |
| Sinif | `BestModelSelector.__init__()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 05 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**  
Composite score agirliklar varsayilan config icinde sabit tanimlanmis:
```python
# best_model_selector.py:59-73
'accuracy': 0.35,  'speed': 0.20,  'efficiency': 0.15,
'stability': 0.15, 'generalization': 0.15
```
Bu agirliklar genel ML uygulamalari icin tasarlanmis. Nukleer fizik tezi icin dogruluk agirliginin arttirilmasi (orn. 0.50) daha uygun olabilir.

**Etki:**  
- 'Best model' siralamasini dogrudan etkiler.  
- Yalnizca R2 bazli secimle farkli sonuclar uretebilir.  
- Sensitivity analizi yapilmadan 'en iyi model' iddiasi zayif kalir.

**Tez Notu:** Agirlik duyarlilik analizi yapilmali: accuracy=0.35 vs 0.50 durumunda sira listesi degisiyor mu? Bu, BestModelSelector dogrulugu icin onemli.

**Fix Onerisi:**  
```python
# config.json'a ekle:
"best_model_weights": {
  "accuracy": 0.50, "speed": 0.15, "efficiency": 0.10,
  "stability": 0.15, "generalization": 0.10
}  # Nukleer fizik icin dogruluk agirlikli
```

**Yeniden Egitim Gerekli:** HAYIR -- parametre duzeltmesi; analizi yeniden calistir.

---

### BUG-15 [BILGI] IsotopeChainAnalyzer SDI Esigi Sabit

| Alan | Deger |
|------|-------|
| Dosya | `isotope_chain_analyzer.py:41` |
| Sinif | `IsotopeChainAnalyzer` |
| Oncelik | [BILGI] |
| Faz | PFAZ 05 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**  
`SUDDEN_CHANGE_SIGMA = 1.5` tum hedefler (MM ve QM) icin ayni. Ancak MM ve QM farkli varyanslara sahip; MM icin 1.5 sigma ile flaglenen ani degisim QM icin gercekte kucuk bir sapma olabilir.

**Etki:**  
- MM ve QM icin farkli sayida ani degisim flaglenebilir; karsilastirma yaniltici.  
- Sihirli sayi korelasyon orani hedeften hedefe farkli gorulurse nedeni esik farki olabilir.

**Tavsiye:**  
Tezde 'her hedef kendi sigma esigi ile analiz edilmistir' gibi bir not eklenmeli veya hedef-bazli esik (MM_sigma=1.5, QM_sigma=2.0 gibi) denenebilir.

---

*pipeline-hatalari.md v1.1 | 2026-05-04 | +3 PFAZ 05 bug: BUG-13..BUG-15*

## PFAZ 06 -- Final Raporlama

---

### BUG-16 [ORTA] PFAZ 12/13 Basarisizligi -- 3 Excel Sayfasi Bos

| Alan | Deger |
|------|-------|
| Dosya | `pfaz6_final_reporting.py` |
| Oncelik | [ORTA] |
| Faz | PFAZ 06 |
| Tespit | 2026-05-04 kaynak kod + pfaz_status.json analizi |

**Sorun:**  
PFAZ 12 (Istatistiksel Analitik) ve PFAZ 13 (AutoML) pfaz_status.json'da 'failed' olarak isaretli. PFAZ 06 bu fazlarin ciktilarini okumaya calisir:
- `outputs/advanced_analytics/nuclear_band_analysis.xlsx` (PFAZ 12)
- `outputs/automl_results/automl_retraining_log.json` (PFAZ 13)

Dosyalar bulunamayinca `logger.warning()` + yer tutucu ('Veri Yok') yazilir.

**Etki:**  
THESIS_COMPLETE_RESULTS.xlsx icerisinde Band_Analizi, AutoML_Improvements, AutoML_BestParams, AutoML_Overview sayfalarinda gercek veri yerine yer tutucu.
Tezdeki bant analizi ve AutoML bolumu bos kalacak.

**Fix:**  PFAZ 12 ve 13 yeniden calistirilmali (PFAZ 01-02 tamamlaninca).

---

### BUG-17 [DUSUK] R2_FLOOR Filtresi -- Tum Modeller Kotu Ise Sayfa Bos

| Alan | Deger |
|------|-------|
| Dosya | `pfaz6_final_reporting.py:602` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 06 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**  
`_R2_FLOOR = -10.0` filtresi val_R2 < -10 modelleri atiyor. Teoride sapan modeller icin dogru. Ancak tum DNN modelleri val_R2 < -10 ise DNN_Models sayfasi tamamen bos kalir; bu hata kaynagiyla karistirabilir.

**Fix:**  
Bos sayfa kontrolu ekle; bos ise 'Bu konfigurasyonda gecerli model yok' not yaz.

---

### BUG-18 [BILGI] Pipeline Siralama Belgeleri Yaniltici

| Alan | Deger |
|------|-------|
| Dosya | `main.py` (pipeline sirasi), `phases/README.md` (belgeleme) |
| Oncelik | [BILGI] |
| Faz | PFAZ 06 |
| Tespit | 2026-05-04 main.py analizi |

**Sorun:**  
PFAZ 06 faz numarasi 6 olmasina ragmen gercek pipeline sirasinda 9. sirada: `[1,2,3,4,5,7,9,12,13,**6**,8,10]`. README ve faz dokumani bunu vurgulamali; tez okuyucusu 'neden PFAZ 07 bitmeden PFAZ 06 sonuclari yok?' diye sorabilir.

**Tavsiye:**  
Tez metodoloji bolumunde pipeline sirasini acikca goster.

---

*pipeline-hatalari.md v1.2 | 2026-05-04 | 18 bug, PFAZ 01-06 kapsami*

---

## PFAZ 07 -- Topluluk ve Meta-Modeller

### BUG-19 [ORTA] RF Meta-Model max_depth Tutarsizligi

**Dosya:** pfaz7_complete_ensemble_pipeline.py  
**Konum:** satir 348 vs satir 941  
**Sorun:** Stacking RF meta-modeli iki farkli yerde farkli max_depth degerleriyle tanimlanmis:
- satir 348: `RandomForestRegressor(n_estimators=100, max_depth=10)`
- satir 941: `RandomForestRegressor(n_estimators=100, max_depth=5)`  
**Etki:** Hangi deger gercekte kullanildigini soylemek guc. Sonuclar reproducibility sorununa sahip.  
**Fix:** max_depth degerini merkezi bir sabit ile tanimla (STACKING_RF_MAX_DEPTH = 10).

### BUG-20 [DUSUK] Dead Code Dosyalari

**Dosya:** pfaz7_ensemble.py (270 satir), faz7_ensemble_pipeline.py  
**Konum:** __init__.py -- pfaz7_ensemble.py import yok  
**Sorun 1:** EnsemblePipeline sinifi (pfaz7_ensemble.py) hic kullanilmiyor, import edilmiyor.  
**Sorun 2:** faz7_ensemble_pipeline.py satir 25: `sys.path.insert(0, '/home/claude')` -- Unix hardcoded path, Windows'ta ImportError.  
**Etki:** faz7_ensemble_pipeline.py Windows'ta calistirilirsa import hatasi verir.  
**Fix:** Dead code dosyalarini sil veya __init__.py'den kaldir.

---

## PFAZ 08 -- Gorsellestirme Sistemi

### BUG-21 [DUSUK] Sessiz Basarisizlik (Veri Eksikligi)
**Dosya:** pfaz8_thesis_charts.py:141-188
**Sorun:** `if self._aaa2 is not None` kosulu; veri yuklenemezse sessizce devam eder.
Grafik uretilmez ama hata mesaji da verilmez.
**Fix:** `else: logger.warning('aaa2 verisi yuklenemedi; grafik atlaniyor')` ekle.

### BUG-22 [DUSUK] SHAP Sessiz Atlama
**Dosya:** visualization_master_system.py (SHAP_AVAILABLE flag)
**Sorun:** SHAP kurulu degilse SHAP grafikleri sessizce atlanir. Tez aciklanabilirlik
bolumu eksik grafik riski tasir. Log mesaji var ama hata STATUS'u yok.
**Fix:** Calisma ozet raporuna 'SHAP_SKIPPED=True' bayragi yaz.

### BUG-23 [BILGI] DPI Tutarsizligi
**Dosya:** visualization_master_system.py vs supplemental_visualizer.py
**Sorun:** Tez grafikleri 300 DPI, supplemental grafikleri 150 DPI. Politika tutarsiz.
**Fix:** Tum grafikleri 300 DPI yapacak merkezi DPI sabiti tanimla.


## PFAZ 09 -- Monte Carlo Belirsizlik Analizi

### BUG-24 [ORTA] Bootstrap n=100 Kucuk -- CI Guvenilirligi Dusuk

| Alan | Deger |
|------|-------|
| Dosya | `monte_carlo_simulation_system.py:191-277` |
| Sinif | `BootstrapSimulator` |
| Oncelik | [ORTA] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
`n_bootstrap=100` ile 2.5. percentile yalnizca 2-3 ornege dayanir. Bootstrap literaturunde
minimum 1000 ornek onerilir (Efron & Tibshirani, 1993). n=100 ile CI intervallar
kararsiz; farkli kosmalar farkli CI uretir.

**Etki:**
- MC9-A/B/C grafikleri icin %95 CI bantlari guvenilir degil.
- Tez istatistiksel bolumunde hatasiz CI iddiasi zayif kalir.
- n=100 -> 2.5. percentile = 2-3 ornek -- cok kucuk.

**Fix:**
```python
# config.json guncelle:
"monte_carlo": {
  "n_bootstrap": 1000,  # 100 -> 1000 (literatur standardi)
  "n_mc_dropout": 100,  # Yeterli (DNN forward pass hizli)
  "n_noise": 100        # Yeterli
}
```
**Yeniden Egitim Gerekli:** HAYIR -- yalnizca PFAZ 09 yeniden calistirma.

---

### BUG-25 [ORTA] Feature Uyumsuzlugunda Sessiz Model Atlama

| Alan | Deger |
|------|-------|
| Dosya | `aaa2_control_group_complete_v4.py:~450` |
| Sinif | `AAA2ControlGroupAnalyzerComplete._load_models_with_metadata()` |
| Oncelik | [ORTA] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
Bir modelin ozellik seti (metadata.json) ile AAA2 dataframe'i uyusmadigi durumda
model `logger.warning()` ile sessizce atlanir. Kac modelin atlandigi bilinmiyor.
Top-50 iddiasi aslinda Top-N (N < 50) olabilir.

**Etki:**
- Ensemble CI, gercek 50 degil, az sayida model uzerinden hesaplanabilir.
- Model ranking gecersizlesir; 'Top-50 konsensus' iddiasi yaniltici.
- Log'a yaziliyor ama pipeline durmaz; kullanici fark etmeyebilir.

**Fix:**
```python
# Pipeline sonunda atlanma sayisini raporla:
logger.info(f"Yuklenen model: {loaded}/{total_candidates}; atlanma: {skipped}")
# Excel'e 'loaded_model_count' sutunu ekle
```
**Yeniden Egitim Gerekli:** HAYIR -- loglama iyilestirmesi.

---

### BUG-26 [DUSUK] MC Dropout Yalnizca DNN -- RF/XGB Belirsizlik Olculemez

| Alan | Deger |
|------|-------|
| Dosya | `monte_carlo_simulation_system.py:124-184` |
| Sinif | `MCDropoutSimulator` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
`MCDropoutSimulator` yalnizca TensorFlow DNN modelleri icin gecerli (`training=True`
ile forward pass). RF, XGBoost, CatBoost, SVR, ANFIS modelleri icin Bayesci
belirsizlik bu yontemle olculemez. `if not hasattr(model, 'predict_proba_mc'):
return None` ile sessizce atlanir.

**Etki:**
- Top-10 model icinde DNN olmayabilir (DNN egitim kisiti train_size < 200).
- DNN-icin iyi CI, diger modeller icin bos CI -- karsilastirma eksik.
- Tezde 'MC Dropout tum modellere uygulandi' yazilirsa yanlis.

**Tavsiye:**
Tezde acikca belirt: 'MC Dropout yalnizca TensorFlow DNN modelleri icin uygulanmistir;
diger model turleri Bootstrap ve Noise yontemleriyle degerlendirilmistir.'

**Yeniden Egitim Gerekli:** HAYIR -- dokumantasyon notu.

---

### BUG-27 [ORTA] WS Feature Bug PFAZ09'u Etkiliyor (BUG-02 Turev Etkisi)

| Alan | Deger |
|------|-------|
| Dosya | `aaa2_control_group_complete_v4.py:111-202` (TheoreticalFeaturesCalculator) |
| Oncelik | [ORTA] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-04 analizi |

**Sorun:**
BUG-02 (constants.py HBAR_C eksik) PFAZ01'i etkiler. PFAZ09 da ayni kodu cagirir:
`TheoreticalFeaturesCalculator.calculate_ws_features()` -> WS ozellikleri 0/NaN.
WS ozelliklerini kullanan modeller bu 0 degerler uzerinde tahmin yapacak.

**Etki:**
- WS-agirlikli modellerin MC CI'leri yanlis.
- Top-50 icinde WS ozellik kullanan modellerin tahminleri sistematik olarak hatali.
- BUG-02 duzeltilmeden PFAZ09 sonuclari gercek belirsizligi yansitmaz.

**Fix:** BUG-02 duzelt (constants.py'e HBAR_C ekle), sonra PFAZ01+PFAZ09 yeniden calistir.
**Yeniden Egitim Gerekli:** BUG-02 ile birlikte EVET.

---

### BUG-28 [DUSUK] Analysis_5..15 Sayfalari PFAZ12 Bagimlisi -- PFAZ12 FAILED

| Alan | Deger |
|------|-------|
| Dosya | `aaa2_control_group_complete_v4.py:~900` (Excel yazimi) |
| Oncelik | [DUSUK] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-04 pfaz_status.json + kaynak kod analizi |

**Sorun:**
Excel ciktisi Analysis_5..Analysis_15 sayfalarini istatistiksel testlerle doldurmak
icin PFAZ12 ciktilarindan veri bekliyor. PFAZ12 failed oldugundan bu 11 sayfa
yer tutucu veriyle kalir.

**Etki:**
- Tez istatistiksel analiz bolumu eksik kalir.
- PFAZ08 MC9-A grafikleri bu sayfalardan veri okuyorsa bos veya hata uretir.

**Fix:** PFAZ12 yeniden calistir (PFAZ01-02 tamamlaninca).
**Yeniden Egitim Gerekli:** HAYIR -- PFAZ12 yeniden calistirilmali.

---

### BUG-29 [DUSUK] n_jobs=8 Hardcoded -- Sistemin CPU Sayisina Uyarlanmiyor

| Alan | Deger |
|------|-------|
| Dosya | `monte_carlo_simulation_system.py` (DEFAULT_MC_CONFIG) |
| Oncelik | [DUSUK] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
`DEFAULT_MC_CONFIG: 'parallel': {'enabled': True, 'n_jobs': 8}` sabit tanimlanmis.
8'den az CPU'lu sistemlerde veya az RAM'li konfigurasyonlarda sorun cikabilir.

**Fix:**
```python
n_jobs = min(8, os.cpu_count() or 4)  # Sistemin cekirdek sayisina gore
```
**Yeniden Egitim Gerekli:** HAYIR -- konfigürasyon duzeltmesi.

---

### BUG-30 [DUSUK] Consensus Threshold 0.1 Hardcoded -- Hedef Spesifik Degil

| Alan | Deger |
|------|-------|
| Dosya | `aaa2_control_group_complete_v4.py` (DEFAULT_MC_CONFIG) |
| Oncelik | [DUSUK] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
`'consensus_threshold': 0.1` -- MM icin 0.1 muN fark anlamli, QM icin 0.1 barn
buyuk fark sayilir (QM tipik ~0.3-3.0 barn araliginda). Ayni esik her iki hedef icin
yaniltici.

**Etki:**
- MM anlasamama esigi QM icin cok gevs kalabilir veya tam tersi.
- 'Model anlasamadi' bayragi hedef bolgesiyle tutarsiz.

**Fix:**
```python
thresholds = {'MM': 0.05, 'QM': 0.20}  # Hedef spesifik esikler
```
**Yeniden Egitim Gerekli:** HAYIR -- parametre duzeltmesi.


## PFAZ 12 -- Ileri Istatistiksel Analitik

### BUG-31 [ORTA] NuclearBandAnalyzer Import Hatasi -- Sinif Adi Uyumsuzlugu

| Alan | Deger |
|------|-------|
| Dosya | `pfaz12_advanced_analytics/nuclear_band_analyzer.py` |
| Oncelik | [ORTA] |
| Faz | PFAZ 12 |
| Tespit | 2026-05-04 kaynak kod analizi |
| **Duzeltme** | **2026-05-09** |

**Gercek Sorun:**
`nuclear_band_analyzer.py` icindeki sinif adi `NuclearMomentBandAnalyzer` iken
`__init__.py` `NuclearBandAnalyzer` adini import etmeye calisiyordu.
`ImportError: cannot import name 'NuclearBandAnalyzer'` --> NUCLEAR_BAND_ANALYZER_AVAILABLE=False.

Ayrica `pfaz6_final_reporting.py:1267`'de ayni kalip IndentationError vardi (bu da fix edildi).

**Uygulanan Fix:**
```python
# nuclear_band_analyzer.py sonuna eklendi:
NuclearBandAnalyzer = NuclearMomentBandAnalyzer
```

**Dogrulama:** `from pfaz_modules.pfaz12_advanced_analytics import NuclearBandAnalyzer` --> OK, available=True.

**Yeniden Egitim Gerekli:** HAYIR -- modul duzeltmesi.

---

### BUG-36 [BILGI] PFAZ12 Import Hatasi -- Baslangic Noktasi Belirsiz

| Alan | Deger |
|------|-------|
| Dosya | pfaz_status.json: progress=0 |
| Oncelik | [BILGI] |
| Faz | PFAZ 12 |
| Tespit | 2026-05-04 pfaz_status.json analizi |

**Sorun:**
PFAZ12 progress=0 ile failed. Hata kaydi yok (test gunlugu kontrol edilmedi).
Muhtemel nedenler: statsmodels eksik, SALib eksik, pipeline cagri hatasi.

**Etki:**
Tum PFAZ12 analizleri (istatistiksel testler, örüntü analizi, duyarlilik) calismiyor.

**Tavsiye:**
`python main.py --pfaz 12 --mode run` ile yeniden calistirinca hata mesajini logla.

---

## PFAZ 13 -- AutoML Yeniden Egitim

### BUG-32 [KRITIK] automl_retraining_loop.py IndentationError -- Modul Import Edilemiyor

| Alan | Deger |
|------|-------|
| Dosya | `automl_retraining_loop.py:539` |
| Sinif | `AutoMLRetrainingLoop._run_anfis_for_category` |
| Oncelik | [KRITIK] |
| Faz | PFAZ 13 |
| Tespit | 2026-05-04 kaynak kod analizi |
| **Duzeltme** | **2026-05-09** |

**Gercek Sorun:**
`_run_anfis_for_category` metodunda satir 539 -- `return []` sonrasinda 3 gereksiz/hatali satir:
```python
            except ImportError:
                logger.warning("...")
                return []
            AutoMLANFISOptimizer = None   # satir 537 -- return sonrasi erisilemez, yanlis
            AutoMLANFISOptimizer = None   # satir 538 -- duplikat
                AutoMLANFISOptimizer = None  # satir 539 -- IndentationError!
```
Satir 539'daki fazla girintileme `IndentationError: unexpected indent` -- modul parse edilemiyor.

**Etki:**
- PFAZ 13 tamamiyla devre disi; AutoMLRetrainingLoop import edilemiyor.
- PFAZ06 AutoML sayfaları bos.

**Uygulanan Fix:** Satir 537-539 silindi (3 satir).

**Dogrulama:** `from pfaz_modules.pfaz13_automl.automl_retraining_loop import AutoMLRetrainingLoop` --> OK.

**Yeniden Egitim Gerekli:** HAYIR -- fix sonrasi PFAZ13 yeniden calistir.

---

### BUG-33 [DUSUK] n_trials=30 Kucuk -- Kompleks DNN Arama Uzayi Icin Yetersiz

| Alan | Deger |
|------|-------|
| Dosya | `automl_retraining_loop.py:254` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 13 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
DNN arama uzayi 6+ parametreye sahip (n_layers, hidden_units, dropout, lr, batch_size).
30 trial ile bu uzayi verimli tuzaklamak guc. Literatur 100+ trial oneriyor.

**Fix:**
```python
# config.json'a ekle:
"automl": {
  "n_trials_default": 100,  # RF/XGB/LGB
  "n_trials_dnn": 150       # DNN (daha buyuk arama uzayi)
}
```
**Yeniden Egitim Gerekli:** HAYIR -- n_trials arttirilirsa hesaplama maliyeti artar.

---

### BUG-34 [DUSUK] model_types Default Listesinde CatBoost/SVR Eksik

| Alan | Deger |
|------|-------|
| Dosya | `automl_retraining_loop.py:269` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 13 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
`model_types = model_types or ['rf', 'xgb', 'lgb']` -- CatBoost (cb) ve SVR eksik.
Oysa PFAZ02'de CatBoost ve SVR aktif olarak calistirildi; bu modellerin iyilestirilmesi PFAZ13'un kapsaminda olmali.

**Fix:**
```python
self.model_types = model_types or ['rf', 'xgb', 'lgb', 'cb', 'svr']
```
**Yeniden Egitim Gerekli:** HAYIR -- default degisiklik.

---

### BUG-35 [BILGI] r2_threshold vs POOR_MAX Tutarsizligi

| Alan | Deger |
|------|-------|
| Dosya | `automl_retraining_loop.py:252` vs `:242` |
| Oncelik | [BILGI] |
| Faz | PFAZ 13 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
README: `r2_threshold=0.80` (dusuk R2 esigi).
Kod: `POOR_MAX=0.70, MEDIUM_MAX=0.90, GOOD_MAX=0.95` -- kategori sinirlari.
`r2_threshold` parametresi backward compat icin tutuluyor ama gercekte kullanilmiyor.
README okuyucusu 0.80 alti modellerin optimize edildigini sanir; aslinda kategori bazli.

**Tavsiye:**
README ve dokümantasyonu guncelle; r2_threshold parametresini kaldir veya acikca 'deprecated' isaretine.

## PFAZ 10 -- Tez Derleme (LaTeX Entegrasyonu)

---

### BUG-37 [DUSUK] ThesisOrchestrator Linux Yolu Hardcoded

| Alan | Deger |
|------|-------|
| Dosya | `pfaz10_thesis_orchestrator.py:42` |
| Sinif | `ThesisOrchestrator.__init__()` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 10 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
```python
def __init__(self, thesis_dir='output/thesis', project_dir='/mnt/project'):
```
`project_dir` varsayilani `/mnt/project` -- Linux/Docker spesifik. Windows'ta bu yol mevcut degil.

**Etki:**
- Aktif sinif `MasterThesisIntegration` (v5.0.0) bu sorundan etkilenmiyor.
- Ancak `ThesisOrchestrator` (v2.0) dogrudan cagirilirsa yanlis dizin okunur, sessiz hata.

**Fix:**
```python
def __init__(self, thesis_dir='output/thesis', project_dir='.'):
    # veya: project_dir=str(Path.cwd())
```
**Yeniden Egitim Gerekli:** HAYIR.

---

### BUG-38 [BILGI] MC K=1000 Tez/Kod Tutarsizligi

| Alan | Deger |
|------|-------|
| Dosya | `pfaz10_master_integration.py` (_ch_methodology icinde) |
| Oncelik | [BILGI] |
| Faz | PFAZ 10 |
| Tespit | 2026-05-04 kaynak kod analizi |

**Sorun:**
`_ch_methodology()` bolumu tezde "K = 1000 Monte Carlo calistirmasi" yaziyor.
Gercekte PFAZ 09 kodu `n=100` kullanir (BUG-24 zaten bunu isaretledi).

**Etki:**
- Tez metni ile gercek implementasyon uyumsuz.
- Hakem veya okuyucu K=1000 beklentisiyle sonuclari degerlendirirse CI guvenilirligi fazla tahmin edilir.

**Tavsiye:**
Ya tez metnini `n=100` olarak duzelt (BUG-24 ile birlikte),
ya da BUG-24'u cozup PFAZ09'u gercekten `n=1000`'e yukselt.

---

## Sprint Ozeti -- 2026-05-04

**Sprint Kapsami:** BUG-01..BUG-38 (38 bug, PFAZ 01-13)
**Duzeltilen:** 13 kod degisikligi, 10 dosyada

### Duzeltilen Buglar (kod degisikligi yapildi)

| ID | Dosya | Degisiklik |
|----|-------|-----------|
| BUG-02 | `core_modules/constants.py` | HBAR_C = 197.3269804 MeV*fm eklendi |
| BUG-03 | `core_modules/constants.py` | WOODS_SAXON_PARAMS: V_so, r_so, a_so eklendi |
| BUG-06 | `repo/config.json` | model_types: [RF, XGBoost, LightGBM, CatBoost, SVR, DNN] |
| BUG-10 | `pfaz04/unknown_nuclei_predictor.py` | val_r2 flat/nested dual-format okuma |
| BUG-11 | `pfaz04/generalization_analyzer.py` | GS: known_r2<=0->None, unknown_r2<0->0.0 |
| BUG-19 | `pfaz07/pfaz7_complete_ensemble_pipeline.py` | STACKING_RF_MAX_DEPTH=10 sabiti |
| BUG-20 | `pfaz07/faz7_ensemble_pipeline.py` | sys.path.insert('/home/claude') kaldirildi |
| BUG-29 | `pfaz09/monte_carlo_simulation_system.py` | n_jobs: min(8, cpu_count() or 4) |
| BUG-30 | `pfaz09/monte_carlo_simulation_system.py` | consensus_threshold MM/QM notu eklendi |
| BUG-31 | `pfaz12/__init__.py` | NuclearBandAnalyzer + NuclearPatternAnalyzer export |
| BUG-32 | `pfaz13/automl_retraining_loop.py` | IndentationError (3 redundant satir silindi) |
| BUG-34 | `pfaz13/automl_retraining_loop.py` | model_types default: +cb, +svr |
| BUG-37 | `pfaz10/pfaz10_thesis_orchestrator.py` | project_dir: '/mnt/project' -> '.' |

### Gecersiz Buglar (hata degil, tasarim karari)

| ID | Neden Gecersiz |
|----|----------------|
| BUG-01 | Q=0 filtresi intentional: aaa2.txt'te olmayan cekirdekler hic kullanilmiyor |
| BUG-04 | MAT formati kasitli kaldirildi; .mat yerine .csv egitim yapiliyor |
| BUG-12 | MM_QM hedefi tanimli ama aktif degil; yalnizca MM ve QM calistirilmaktadir |

### Yeniden Baslatma Gerektiren Duzeltmeler

BUG-02 ve BUG-03 (HBAR_C + spin-orbit parametreleri) constants.py'de duzeltildi.
**Ancak:** Bu duzeltmelerin etkili olmasi icin PFAZ 01 veri uretimi ve PFAZ 02 egitimi
yeniden calistirilmalidir. Mevcut calisma WS ozellikleri 0/NaN ile devam etmektedir.

**Yeniden baslatma plani:**
1. Mevcut PFAZ 02 egitimi tamamlansin
2. PFAZ 01 yeniden calistir (constants.py guncel)
3. PFAZ 02 yeniden calistir (WS ozellikleriyle)
4. PFAZ 09, 12, 13 yeniden calistir

### BNN/PINN Karari (BUG-06 eki)

BNN (Bayesian Neural Network) ve PINN (Physics-Informed Neural Network) config'den cikarildi,
gercek aktif model listesi yazildi. Bu modellerin eklenmesi kullanicinin kararina birakildi:

- **BNN:** Bayesian belirsizlik tahminleri saglar; PFAZ09 MC Dropout'u zenginlestirir.
  Eklemek icin: TensorFlow Probability kurulumu + PFAZ02 yeniden baslatma gerekir.
- **PINN:** Fizik kisitlari loss fonksiyonuna entegre eder (SEMF/Schmidt terimleri).
  Eklemek icin: Ozel loss fonksiyonu yazimi + PFAZ02 yeniden baslatma gerekir.

*pipeline-hatalari.md v2.0 | 2026-05-04 | Sprint tamamlandi | 13 duzeltme, 3 gecersiz, 22 bekliyor*

---

## Sprint Ozeti — 2026-05-07/08 (Log Analizi + Config Temizligi)

**Sprint Kapsami:** BUG-39..41 (yeni buglar), WARN-03..05 (uyarilar), Sprint 1+2 kod iyilestirmeleri
**Duzeltilen:** 3 yeni bug, 2 yeni iyilestirme, config senkronizasyonu

### Yeni Duzeltilen Buglar (2026-05-07/08)

| ID | Dosya | Degisiklik | Tarih |
|----|-------|-----------|-------|
| BUG-39 | `pfaz02/overfitting_detector.py` | `analyze_training_metrics` metodu eksikti, eklendi | 2026-05-07 |
| BUG-40 | `pfaz13/automl_anfis_optimizer.py + retraining_loop.py` | `anfis_core.py` import yanlisti, duzeltildi | 2026-05-08 |
| BUG-41 | `nucdatav2-desktop/config_desktop.json` | "Physics" feature set tanimsizdi, kaldirildi | 2026-05-08 |

### Yeni Iyilestirmeler (Sprint 1+2)

| ID | Dosya | Degisiklik | Tarih |
|----|-------|-----------|-------|
| SPRINT-1 | `pfaz02/parallel_ai_trainer.py` | Cift R2 filtresi: cv_R2>=0.0 + gap<0.5 eklendi (Sprint 8: gap<0.6 revize edildi); CV kayit oncesine tasindi | 2026-05-08 |
| SPRINT-2 | `config.json + main.py + truba/desktop` | Robust scaling + N=75 tum config'lerden kaldirildi | 2026-05-09 |

### WARN-03: Robust Scaling QM Icin Basarisiz

| Alan | Deger |
|------|-------|
| Dosya | `config.json`, `config_desktop.json`, `nucdatav2-truba/config.json` |
| Oncelik | [CONFIG] |
| Tespit | 2026-05-07 eski PC log analizi |
| Durum | DUZELTILDI (Sprint 2, 2026-05-09) |

**Bulgu:** ~70 MB log analizi: Robust scaling + QM hedefi kombinasyonunda R2 sistematik olarak < 0.
IQR normallesirmesi simetrik olmayan QM dagilmiyla uyumsuz.

**Fix:** Tum config dosyalarindan `Robust` kaldirildi. Aktif: NoScaling, Standard, MinMax.

---

### WARN-04: CV Fold Basi Az Ornek (N<150)

| Alan | Deger |
|------|-------|
| Dosya | `pfaz02/model_validator.py` |
| Oncelik | [ANALIZ] |
| Durum | TEZ NOTU |

**Bulgu:** N=100 egitim setinde 5-fold CV → fold basi ~17 ornek.
17 ornek ile R2 tahmini yuksek varyansa sahip — val_R2 != cv_R2 bekleniyor.

**Tez notu:** Metodoloji bolumunde kucuk orneklem limitasyonu belirtilmeli.
**Sprint 1 cozumu:** N<150 icin 3-fold CV kullanilmaya baslandi (fold basi ~27 ornek).

---

### WARN-05: Val Set 15 Ornek — Yaniltici Yuksek R2

| Alan | Deger |
|------|-------|
| Dosya | `pfaz02/parallel_ai_trainer.py` |
| Oncelik | [ANALIZ] |
| Durum | UYGULAMAYA ALINDI (Sprint 1, 2026-05-08) |

**Bulgu:** S70 bolme ile 100 ornekli dataset → val set = 15 ornek.
15 ornek ile val_R2 yuksek varyans gosterir; train_R2=0.99 ama cv_R2=-0.31 olan modeller
POOR filtresini GECEBILIYORdu (val_R2=0.84 gorunuyordu).

**Fix (Sprint 1):** CV kayit oncesine tasindi; cv_R2 >= 0.0 AND gap < 0.6 zorunlu.

---

### BUG-39 [ORTA] OverfittingDetector — analyze_training_metrics Eksik

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz02_ai_training/overfitting_detector.py` |
| Oncelik | [ORTA] |
| Faz | PFAZ 02 |
| Tespit | 2026-05-07 orphan scan |
| Durum | DUZELTILDI 2026-05-07 |

**Sorun:** `overfitting_detector.py` icinde `analyze_training_metrics` metodu
tanimli degildi. `train_single_job` bu metodu cagiriyordu → `AttributeError`.

**Fix:** `analyze_training_metrics(train_metrics, val_metrics, test_metrics)` metodu eklendi.

**Yeniden Egitim Gerekli:** HAYIR — fonksiyon artik hata vermeden calisiyor.

---

### BUG-40 [YUKSEK] AutoML ANFIS — anfis_core Import Yanlisi

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz13_automl/automl_anfis_optimizer.py` + `automl_retraining_loop.py` |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 13 |
| Tespit | 2026-05-08 orphan scan |
| Durum | DUZELTILDI 2026-05-08 |

**Sorun:** `automl_anfis_optimizer.py` icinde `from pfaz_modules.pfaz03_anfis_training.anfis_core`
import ediyordu, ancak `anfis_core.py` dosyasi mevcut degil.
Dogru import: `anfis_parallel_trainer_v2.py` icindeki `TakagiSugenoANFIS` sinifi.

**Fix:** Import satiri `anfis_parallel_trainer_v2.TakagiSugenoANFIS` seklinde duzeltildi.

**Yeniden Egitim Gerekli:** HAYIR — PFAZ13 calismadan once bu fix gerekiyordu.

---

### BUG-41 [DUSUK] Desktop Config — "Physics" Feature Set Tanimsiz

| Alan | Deger |
|------|-------|
| Dosya | `nucdatav2-desktop/config_desktop.json` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 01/02 |
| Tespit | 2026-05-08 config incelemesi |
| Durum | DUZELTILDI 2026-05-08 |

**Sorun:** Desktop config `feature_sets` listesinde "Physics" string'i vardi.
`feature_set_builder.py` "Physics" adinda bir feature set tanimlamiyor (PFAZ01 import hatasi riski).

**Fix:** `feature_sets: null` olarak degistirildi — hedef-bazli otomatik set secimi (TARGET_RECOMMENDED_SETS).

---

## 2026-05-11 — Sprint 5: Inter-PFAZ Veri Akisi Audit Sonucu Yeni Bug'lar

QA tekrar denetimi sirasinda (commit cd25f42) **inter-PFAZ veri akisi** sistematik taranmis,
statik analiz ile yakalanmayan 5 yeni bug tespit edilmistir. Detay icin
`claude-hatalarim-ve-dersler.md` KURAL 19'a bakilabilir.

---

### BUG-42 [YUKSEK] PFAZ 08 model_comparison_dashboard -- Kolon Adi Uyumsuzlugu

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz08_visualization/model_comparison_dashboard.py` |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 08 |
| Tespit | 2026-05-11 inter-PFAZ data flow audit |
| Durum | **DUZELTILDI 2026-05-11 Sprint 5** |

**Sorun:**
PFAZ 02 `parallel_ai_trainer.py:1648` cikti Excel'inde kolon adlari `Train_R2`,
`Val_R2`, `Test_R2` (CamelCase) seklinde. Ancak PFAZ 08
`model_comparison_dashboard.py` 15+ farkli yerde `df['R2_test']`,
`df['RMSE_test']`, `df['MAE_test']` (snake_case) ariyor:

- Sat. 186: `'R2_test': ['mean', 'std', 'min', 'max', 'count']`
- Sat. 227-228: `df[df['Model'] == model1]['R2_test'].dropna()`
- Sat. 268, 275, 309, 334, 366, 374, 393, 418, 457, 489, 495, 519, 521, 543, 652

**Etki:** PFAZ 08 dashboard olusturulurken `KeyError: 'R2_test'` firlatir → tum
karsilastirma grafikleri uretilemez → `pc error.md` log'unda PFAZ 08 `pending`
kalir.

**Dogrulama komutu:**
```bash
grep -n "R2_test\|Test_R2" pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py
grep -cn "R2_test\|Test_R2" pfaz_modules/pfaz08_visualization/model_comparison_dashboard.py
```

**Fix:**
```python
# pfaz08/model_comparison_dashboard.py 15+ yerde:
# YANLIS:
df['R2_test']     -> df['Test_R2']
df['RMSE_test']   -> df['Test_RMSE']
df['MAE_test']    -> df['Test_MAE']
df['Training_Time']  -> df['Training_Time_s']
```

**Yeniden Egitim Gerekli:** HAYIR — yalnizca raporlama/gorsellestirme katmani.

**Tez Notu:** Bu bug `pc error.md` (2026-05-04 Elif K) log'unda PFAZ 08 pending
kalma sebebidir. Pipeline 13 fazdan 5'i sessizce eksik kalmis.

---

### BUG-43 [YUKSEK] main.py Flat Config Key'leri Cogu PFAZ'da Okumuyor

| Alan | Deger |
|------|-------|
| Dosya | `main.py` (run_pfaz_01, 03, 04, 05, 06, 07, 08, 09, 10, 12, 13) |
| Oncelik | [YUKSEK] |
| Faz | Tum PFAZ'lar |
| Tespit | 2026-05-11 config audit |
| Durum | **DUZELTILDI 2026-05-11 Sprint 5** |

**Sorun:**
`config.json` iki seviye config tutuyor:
- **Flat:** `pfaz01_dataset_generation`, `pfaz02_ai_training`, ..., `pfaz13_automl` (kullanicinin elle duzenledigi)
- **Nested:** `pfaz_config[1]`, `pfaz_config[2]`, ..., `pfaz_config[13]` (varsayilan, kod tarafindan)

`main.py:554` icinde **yalnizca PFAZ 02** her ikisini birden okuyor:
```python
_pfaz02_cfg = self.config.get('pfaz02_ai_training', {})
config = self.config['pfaz_config'][pfaz_id]
```

Diger PFAZ'lar (PFAZ 01, 03-13) yalnizca nested okuyor:
```python
config = self.config['pfaz_config'][pfaz_id]
```

**Etki:** Kullanici `config.json`'da `pfaz03_anfis_training.matlab_engine.enabled =
true` yapsa bile, main.py default `use_matlab: false` ile gider. Ayni durum GPU
ayari, n_workers, dataset_sizes, vb. icin de gecerli.

**Ozelikle TRUBA'ya kritik:** TRUBA icin yapilan tum config ozellestirmeleri (GPU off,
n_workers=16, MATLAB on) sessizce **ignore** edilir.

**Dogrulama komutu:**
```bash
grep -n "self\.config\.get('pfaz0\|self\.config\['pfaz_config'\]" main.py | head -20
```

**Fix:** main.py'ye `_get_pfaz_config(pfaz_id)` helper ekle:
```python
def _get_pfaz_config(self, pfaz_id: int) -> Dict:
    """Hem nested hem flat config'i birlestirir; flat oncelikli."""
    flat_keys = {
        1: 'pfaz01_dataset_generation', 2: 'pfaz02_ai_training',
        3: 'pfaz03_anfis_training', 4: 'pfaz04_unknown_predictions',
        5: 'pfaz05_cross_model_analysis', 6: 'pfaz06_final_reporting',
        7: 'pfaz07_ensemble', 8: 'pfaz08_visualization',
        9: 'pfaz09_aaa2_monte_carlo', 10: 'pfaz10_thesis_compilation',
        11: 'pfaz11_production_deployment', 12: 'pfaz12_advanced_analytics',
        13: 'pfaz13_automl'
    }
    nested = self.config.get('pfaz_config', {}).get(pfaz_id, {})
    flat = self.config.get(flat_keys.get(pfaz_id, ''), {})
    return {**nested, **flat}  # flat oncelikli
```

Tum `run_pfaz_*` fonksiyonlarinda `config = self._get_pfaz_config(pfaz_id)` kullanilir.

**Yeniden Egitim Gerekli:** Cogu durumda HAYIR (default'larla zaten gitmis). Ama
GPU/MATLAB/dataset_sizes degisiklikleri yapilmissa bu fix sonrasi tekrar calistirmak
faydali.

---

### BUG-44 [ORTA] Dataset Sizes -- `267` int vs `'ALL'` str Uyumsuzlugu

| Alan | Deger |
|------|-------|
| Dosya | `config.json` (pfaz01_dataset_generation.dataset_sizes) + `pfaz_modules/pfaz01_dataset_generation/dataset_generation_pipeline_v2.py:154` |
| Oncelik | [ORTA] |
| Faz | PFAZ 01 |
| Tespit | 2026-05-11 type consistency check |
| Durum | **DUZELTILDI 2026-05-11 Sprint 5** |

**Sorun:**
`config.json`:
```json
"dataset_sizes": [100, 150, 200, 267]
```

`dataset_generation_pipeline_v2.py:154`:
```python
self.NOANOMALY_SIZES: set = {150, 200, 'ALL'}
```

`267` integer iken NOANOMALY_SIZES set'inde `'ALL'` string var. Set kontrolu
`267 in {150, 200, 'ALL'}` -> `False` doner.

**Etki:** NoAnomaly varyantlari yalnizca 150 ve 200 boyutlari icin uretilir; 267
(ALL) boyutu icin uretilmez. Tezde "tum boyutlar icin NoAnomaly varyanti var" iddiasi
gerceklesmiyor.

**Dogrulama komutu:**
```bash
grep -n "NOANOMALY_SIZES\|'ALL'\|267" pfaz_modules/pfaz01_dataset_generation/dataset_generation_pipeline_v2.py
python3 -c "import json; c=json.load(open('config.json')); print(c['pfaz01_dataset_generation']['dataset_sizes'])"
```

**Fix:**
Iki secenek (ikisi de uygulanabilir):

A) Kodda esdegerlik garanti et:
```python
ALL_SIZES = {267, 'ALL'}
self.NOANOMALY_SIZES: set = {150, 200, 267, 'ALL'}  # her iki temsil de
```

B) Config'i kodla hizala:
```json
"dataset_sizes": [100, 150, 200, "ALL"]   // string olarak
```

**Onerilen:** A — kod tarafinda esdegerlik kur (kullanicinin int yazimini bozma).

**Yeniden Egitim Gerekli:** EVET — NoAnomaly varyantlari eksik uretildiyse 267 icin
PFAZ 01 yeniden calistirilmali.

---

### BUG-45 [ORTA] ANFISDatasetSelector -- Kod ile Belge Uyumsuzlugu (Drift)

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py:1427-1428` |
| Oncelik | [ORTA] |
| Faz | PFAZ 03 |
| Tespit | 2026-05-11 kod-belge tutarlilik kontrolu |
| Durum | **DUZELTILDI 2026-05-11 Sprint 5** |

**Sorun:**
`docs/thesis-toolkit/phases/faz-03-anfis-egitimi.md` belgesi:
> "11.1 ANFISDatasetSelector -- AKTIF (2026-05-08)
> `train_all_anfis_parallel` icinde `discover_datasets()` hemen sonrasina entegre
> edildi. Kota: Top=50, Mid=50, Low=100 (toplam 200/target)."

Kodda gercek durum:
```python
# anfis_parallel_trainer_v2.py:1427-1428
# ANFISDatasetSelector: deactivated - ANFIS 3-phase strategy covers all datasets
logger.info("[INFO] ANFISDatasetSelector: deactivated (3-phase pilot strategy active)")
```

**Etki:** Belgenin iddia ettigi tabakali secim aslinda **devre disi**. PFAZ 03 tum
848 dataset uzerinde calismaya devam ediyor. Belge ileri donuk niyeti not almis ama
kod hicbir zaman aktive edilmemis. Bu klasik KURAL 18 vakasi.

**Dogrulama komutu:**
```bash
grep -n "ANFISDatasetSelector\|deactivated" pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py
```

**Fix:**
```python
# anfis_parallel_trainer_v2.py:1427-1428 yerine:
try:
    from .anfis_dataset_selector import ANFISDatasetSelector
    selector = ANFISDatasetSelector(
        ai_results_dir=str(self.output_dir.parent / 'trained_models'),
        output_dir=str(self.output_dir / 'selected_datasets')
    )
    selector.load_ai_results()
    selections = selector.select_both_methods(
        targets=['MM', 'QM'],
        n_datasets=200,
        n_top_quota=50, n_mid_quota=50, n_low_quota=100
    )
    # selections kullanilarak dataset listesi filtrele
    logger.info(f"[OK] ANFISDatasetSelector aktif: {sum(len(v['method1']) for v in selections.values())} dataset secildi")
except FileNotFoundError:
    logger.warning("[WARN] PFAZ 02 ciktisi bulunamadi, tum datasetler kullanilacak (fallback)")
except Exception as e:
    logger.warning(f"[WARN] Selector calismadi: {e}; tum datasetler kullanilacak")
```

**Tez Notu:** Tier kotalari (Top=50, Mid=50, Low=100) **akademik olarak savunulabilir**:
Low tier kotasinin yuksek (100) olmasi "ML basarisiz olan dataset'lerde ANFIS
performansi" hipotezini test etmek icindir. Detay: `tez-yazim-not-defteri.md`
Sprint 5 bolumu.

**Yeniden Egitim Gerekli:** EVET — PFAZ 03 yeniden calistirilmali.

---

### BUG-46 [YUKSEK] Training Summary -- Uc Farkli Dosya Adi Aranıyor

| Alan | Deger |
|------|-------|
| Dosyalar | PFAZ 02 yaziyor; PFAZ 03 selector ariyor; PFAZ 08 visualizer ariyor |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 02 -> PFAZ 03 -> PFAZ 08 |
| Tespit | 2026-05-11 inter-PFAZ file flow audit |
| Durum | **DUZELTILDI 2026-05-11 Sprint 5** |

**Sorun:**
Uc PFAZ ucu de farkli dosya adi kullaniyor:

| PFAZ | Islem | Dosya Adi | Konum |
|------|-------|-----------|-------|
| 02 (yazar) | Excel | `training_results_summary.xlsx` | `parallel_ai_trainer.py:1657` |
| 02 (yazar) | JSON | `training_summary.json` | `parallel_ai_trainer.py:1582` |
| 03 (selector okur) | Excel | `training_summary.xlsx` (yok!) | `anfis_dataset_selector.py:66` |
| 08 (viz okur) | Excel | `training_summary.xlsx` veya `ai_training_summary.xlsx` | `visualization_master_system.py:4340-4342` |
| 10 (thesis okur) | JSON | `training_summary.json` (var) | `pfaz10_content_generator.py:66` |

**Etki:**
- PFAZ 03 selector aktif edilirse (BUG-45 fix sonrasi) `FileNotFoundError` firlatir
- PFAZ 08 viz "summary bulunamadi -- atlaniyor" warning'i basar ve baska bir cikti
  uretmez
- PFAZ 10 sadece JSON okudugu icin etkilenmez

**Dogrulama komutu:**
```bash
grep -rn "training_summary\|training_results_summary" --include="*.py" pfaz_modules/
```

**Fix:**
PFAZ 02'de **iki dosya** yaz (yeni isim + eski isim, geri uyumluluk):

```python
# pfaz02/parallel_ai_trainer.py:1655-1664
if rows:
    df = pd.DataFrame(rows)
    excel_files = [
        self.output_dir / 'training_results_summary.xlsx',  # legacy
        self.output_dir / 'training_summary.xlsx',          # canonical
    ]
    for excel_file in excel_files:
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='All_Results', index=False)
            for mtype in df['Model_Type'].unique():
                sub = df[df['Model_Type'] == mtype]
                sheet = mtype[:31]
                sub.to_excel(writer, sheet_name=sheet, index=False)
    logger.info(f"[OK] Excel ozet raporu: training_summary.xlsx + training_results_summary.xlsx")
```

Selector tarafinda (`anfis_dataset_selector.py:66`) da fallback ekle:
```python
if summary_file is None:
    candidates = [
        self.ai_results_dir / 'training_summary.xlsx',
        self.ai_results_dir / 'training_results_summary.xlsx',  # fallback
    ]
    summary_file = next((p for p in candidates if p.exists()), candidates[0])
```

**Yeniden Egitim Gerekli:** HAYIR — yalnizca raporlama dosya adi. Ancak BUG-45
selector aktive edilince bu fix yapilmadan PFAZ 03 baslayamaz.

---

### BUG-38 (TAMAMLAMA) [DUSUK] MonteCarlo Sinif Default'lari -- 100 Hala

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py:194, 288` |
| Oncelik | [DUSUK] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-11 KURAL 18 dogrulamasi |
| Durum | YARIM duzeltildi 2026-05-09; Sprint 5'te tamamlanacak |

**Sorun:**
2026-05-09 Sprint 4'te `DEFAULT_MC_CONFIG`'de `n_bootstrap` ve `n_samples_per_level`
100'den 1000'e cikartildi (Efron & Tibshirani 1993). Ancak sinif tanimlarinda
default parametre degerleri **hala 100**:

```python
# sat. 194: class Bootstrap:
def __init__(self, n_bootstrap: int = 100, stratified: bool = True):

# sat. 288: class Sensitivity:
def __init__(self, ..., n_samples_per_level: int = 100, ...):
```

**Etki:** `MonteCarloSimulationSystem(config=DEFAULT_MC_CONFIG)` cagrildiginda 1000
kullanilir (config dict gecer). Ama dogrudan `Bootstrap()` veya `Sensitivity()`
cagrilirsa 100 default ile baslar. Pipeline icinde her ikisi de mevcut.

**Dogrulama komutu:**
```bash
grep -n "n_bootstrap.*=\|n_samples_per_level.*=" pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py
```

**Fix:**
```python
# sat. 194:
def __init__(self, n_bootstrap: int = 1000, stratified: bool = True):

# sat. 288:
def __init__(self, ..., n_samples_per_level: int = 1000, ...):
```

**Yeniden Egitim Gerekli:** HAYIR (config dict ile cagrilmissa zaten 1000); EVET
(dogrudan sinif cagrilmissa).

---

*Sprint 5 raporu sonu | 5 yeni bug (BUG-42 ... BUG-46) + BUG-38 tamamlama | Toplam: 8 yeni audit kalemi*

---

## 2026-05-12 -- Sprint 6: 8 Kategori Kapsamli Tarama

8 paralel sub-agent ile 165+ Python dosyasi taranmis; 15 yeni bug (BUG-47...BUG-61) tespit edilmistir.
Kategoriler: Hardcoded Path, Optional Import, Excel Sheet Name, n_jobs Nested Parallelism,
Silent Exception, Encoding, Memory Leak, Doc vs Artifact.

### Ozet Tablo

| ID | Oncelik | Kategori | Faz | Fix Durumu |
|----|---------|----------|-----|------------|
| BUG-47 | [TRUBA-CRITICAL] | Hardcoded Path | analysis_modules | **DUZELTILDI 2026-05-12** |
| BUG-48 | [TRUBA-CRITICAL] | Hardcoded Path | visualization_modules | **DUZELTILDI 2026-05-12** |
| BUG-49 | [YUKSEK] | Optional Import | PFAZ 02 | **DUZELTILDI 2026-05-12** |
| BUG-50 | [ORTA] | Optional Import | PFAZ 09 | **DUZELTILDI 2026-05-12** |
| BUG-51 | [YUKSEK] | Excel Sheet Name | PFAZ 06/08 | **DUZELTILDI 2026-05-12** |
| BUG-52 | [ORTA] | Excel Sheet Name | PFAZ 06 | **DUZELTILDI 2026-05-12** |
| BUG-53 | [KRITIK] | Memory Leak | PFAZ 02/13 | **DUZELTILDI 2026-05-12** |
| BUG-54 | [ORTA] | Memory Leak | PFAZ 02 | **DUZELTILDI 2026-05-12** |
| BUG-55 | [YUKSEK] | Silent Exception | PFAZ 04 | **DUZELTILDI 2026-05-12** |
| BUG-56 | [YUKSEK] | Silent Exception | PFAZ 06 | **DUZELTILDI 2026-05-12** |
| BUG-57 | [KRITIK] | Silent Exception | PFAZ 13 | **DUZELTILDI 2026-05-12** |
| BUG-58 | [ORTA] | n_jobs Parallelism | PFAZ 02 | **DUZELTILDI 2026-05-12** |
| BUG-59 | [TASARIM] | Doc vs Artifact | PFAZ 06 | **DUZELTILDI 2026-05-12** |
| BUG-60 | [TASARIM] | Doc vs Artifact | PFAZ 07 | **DUZELTILDI 2026-05-12** |
| BUG-61 | [TASARIM] | Doc vs Artifact | PFAZ 10 | **DUZELTILDI 2026-05-12** |

**Not:** Encoding (Kategori 10) temiz cikti -- 0 bug. n_jobs=-1 hardcoded YOK; _inner_n_jobs() dogru kullaniliyor.

---

### BUG-47 [TRUBA-CRITICAL] Hardcoded /home/claude sys.path -- real_data_integration_manager

| Alan | Deger |
|------|-------|
| Dosya | `analysis_modules/real_data_integration_manager.py:28-29` |
| Oncelik | [TRUBA-CRITICAL] |
| Tespit | 2026-05-12 Sprint 6 path taramasi |

**Sorun:**
```python
sys.path.insert(0, '/home/claude')           # sat. 28 -- Claude.ai artifact ortami
sys.path.insert(0, '/mnt/user-data/outputs') # sat. 29 -- Claude.ai artifact mount point
```
Bu iki satir modul seviyesinde (her import aninda) calisiyor. `/home/claude` TRUBA'da mevcut degil.
`from ensemble_model_builder import EnsembleModelBuilder` bu path'e bagimli.

**Etki:** Bu modul import edildiginde `ImportError` riski. TRUBA'da her pipeline calistirmasinda crash.

**Fix:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# /mnt/user-data/outputs satiri tamamen kaldirilmali
```

**Yeniden Egitim Gerekli:** HAYIR -- import duzeltmesi.

---

### BUG-48 [TRUBA-CRITICAL] Hardcoded /mnt/user-data/outputs sys.path -- visualization_integration

| Alan | Deger |
|------|-------|
| Dosya | `visualization_modules/visualization_integration.py:31` |
| Oncelik | [TRUBA-CRITICAL] |
| Tespit | 2026-05-12 Sprint 6 path taramasi |

**Sorun:**
```python
sys.path.insert(0, '/mnt/user-data/outputs')  # sat. 31
```
Bu modul `reports_visualization_integration.py:205`'den try/except icinde import ediliyor;
tam crash olmaz ama gorsellestime tamamen devre disi kalir.

**Etki:** PFAZ 08 TRUBA'da gorsellestime ciktisi uretemiyor; tez sekilleri eksik.

**Fix:** Satir 31 kaldirilmali; importlar tam package path ile yapilmali.

**Yeniden Egitim Gerekli:** HAYIR.

---

### BUG-49 [YUKSEK] torch Hard Import -- advanced_models_extended.py

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz02_ai_training/advanced_models_extended.py:16-20` |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 02 |
| Tespit | 2026-05-12 Sprint 6 optional import taramasi |

**Sorun:**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
```
5 torch import korumasiz (try/except yok, TORCH_AVAILABLE flag yok). Oysa ayni PFAZ'in
`advanced_models.py:15-28` dosyasi tam dogru patterni kullaniyor.

**Karsilastirma -- Dogru Pattern:**
```python
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    TORCH_AVAILABLE = False
```

**Etki:** TRUBA'da PyTorch kurulu degilse import aninda `ModuleNotFoundError`. PFAZ 02 baslamiyor.

**Fix:** `advanced_models_extended.py:16-31` araligini try/except + TORCH_AVAILABLE ile sar.

**Yeniden Egitim Gerekli:** HAYIR -- import duzeltmesi.

---

### BUG-50 [ORTA] tqdm Hard Import -- pfaz09 (2 dosya)

| Alan | Deger |
|------|-------|
| Dosyalar | `pfaz_modules/pfaz09_aaa2_monte_carlo/aaa2_control_group_complete_v4.py:29` |
|          | `pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py:31` |
| Oncelik | [ORTA] |
| Faz | PFAZ 09 |
| Tespit | 2026-05-12 Sprint 6 optional import taramasi |

**Sorun:**
```python
from tqdm import tqdm   # korumasiz
```
Her iki dosyada da try/except yok, TQDM_AVAILABLE flag yok.

**Fix (her iki dosya):**
```python
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    tqdm = None
    TQDM_AVAILABLE = False
```
Kullanim noktalarinda: `if TQDM_AVAILABLE: iterator = tqdm(items) else: iterator = items`

**Yeniden Egitim Gerekli:** HAYIR.

---

### BUG-51 [YUKSEK] Excel Sheet Name Uyumsuzlugu -- Robustness_CV_Results vs Robustness_CV

| Alan | Deger |
|------|-------|
| Yazan | `pfaz_modules/pfaz06_final_reporting/pfaz6_final_reporting.py:746` |
| Okuyan | `pfaz_modules/pfaz08_visualization/visualization_master_system.py:1492` |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 06 -> PFAZ 08 |
| Tespit | 2026-05-12 Sprint 6 sheet name taramasi |

**Sorun:**
- PFAZ 06 yazar: `sheet_name='Robustness_CV'`
- PFAZ 08 okur: `sheet_name='Robustness_CV_Results'`

Sheet adi uyumsuzlugu. PFAZ 08 bu sheet'i bulamazsa sessizce None doner; robustness grafikleri uretilmez.

**Fix:** PFAZ 08 okuma kismini `sheet_name='Robustness_CV'` olarak guncelle:
```python
# visualization_master_system.py:1492
df = pd.read_excel(excel_path, sheet_name='Robustness_CV')  # 'Results' kaldirildi
```

**Yeniden Egitim Gerekli:** HAYIR -- yalnizca gorsellestime kodu.

---

### BUG-52 [ORTA] Dinamik Sheet Name -- Truncation Eksik (comprehensive_excel_reporter.py)

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz06_final_reporting/comprehensive_excel_reporter.py:210, 223` |
| Oncelik | [ORTA] |
| Faz | PFAZ 06 |
| Tespit | 2026-05-12 Sprint 6 sheet name taramasi |

**Sorun:**
```python
sheet_name = f'{target}_Sonuclar'     # sat. 210 -- [:31] yok
sheet_name = f'{config_id}_Detay'     # sat. 223 -- [:31] yok
```
Mevcut data degerleriyle 31 siniri asilmiyor. Ancak beklenmedik data gelirse openpyxl crash eder.

**Fix:**
```python
sheet_name = f'{target}_Sonuclar'[:31]
sheet_name = f'{config_id}_Detay'[:31]
```

**Yeniden Egitim Gerekli:** HAYIR.

---

### BUG-53 [KRITIK] TF Memory Leak -- Optuna Trial Dongulerinde clear_session Eksik

| Alan | Deger |
|------|-------|
| Dosyalar | `pfaz_modules/pfaz02_ai_training/hyperparameter_tuner.py:423, 436` |
|          | `pfaz_modules/pfaz13_automl/automl_optimizer.py:289` |
|          | `pfaz_modules/pfaz13_automl/automl_hyperparameter_optimizer.py:276` |
| Oncelik | [KRITIK] |
| Faz | PFAZ 02, 13 |
| Tespit | 2026-05-12 Sprint 6 memory leak taramasi |

**Sorun:**
Optuna her trial'da yeni Keras modeli olusturuyor ve `model.fit()` cagiriyor. Her fit sonrasinda
`tf.keras.backend.clear_session()` cagrilmiyor. 30+ trial x n_datasets GPU VRAM birikmesi.

Karsilastirma: `parallel_ai_trainer.py:1468-1483` dogru patterni kullaniyor (projede tek yer).

**Etki:** TRUBA'da GPU bellek tukenirse `ResourceExhaustedError`; PFAZ 02/13 ortasinda durur.

**Fix (her uc dosyada _train_dnn metoduna finally blogu ekle):**
```python
try:
    history = model.fit(...)
finally:
    try:
        import tensorflow as tf
        tf.keras.backend.clear_session()
    except Exception:
        pass
    import gc
    gc.collect()
```

**Yeniden Egitim Gerekli:** HAYIR -- temizlik kod iyilestirmesi.

---

### BUG-54 [ORTA] TF Memory Leak -- model_trainer.py Eski Trainer

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz02_ai_training/model_trainer.py:489` |
| Oncelik | [ORTA] |
| Faz | PFAZ 02 |
| Tespit | 2026-05-12 Sprint 6 memory leak taramasi |

**Sorun:**
`DNNTrainer.train()` icinde `model.fit()` cagrisinda finally blogu ve clear_session yok.
Bu eski trainer dogrudan cagrilirsa (main pipeline disinda) TF grafikleri birikir.

**Fix:** BUG-53 ile ayni pattern -- finally + clear_session ekle.

**Yeniden Egitim Gerekli:** HAYIR.

---

### BUG-55 [YUKSEK] Silent Exception -- PFAZ 04 Model Yukleme Koru

| Alan | Deger |
|------|-------|
| Dosyalar | `pfaz_modules/pfaz04_unknown_predictions/unknown_nuclei_predictor.py:149, 190, 240` |
|          | `pfaz_modules/pfaz04_unknown_predictions/single_nucleus_predictor.py:423, 455, 485` |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 04 |
| Tespit | 2026-05-12 Sprint 6 silent exception taramasi |

**Sorun:**
```python
except Exception:
    pass   # metrics_*.json okuma hatasi sessiz
except Exception:
    return {'r2': None, 'rmse': None, 'mae': None}  # metrik hesaplama sessiz
except Exception:
    continue  # model tarama dongusunde sessiz atla
```
Model yukleme, metrik okuma, ve CI hesaplamasi hatalari hic loglanmiyor.
Top-25 konsensus listesi eksik model iceriyor ama sebep bilinmiyor.

**Fix (her noktada):**
```python
except Exception as e:
    get_tracker().warn(f"[PFAZ04] Model scan/metric read failed: {e}", category="WARNING")
    continue  # veya return None
```

**Yeniden Egitim Gerekli:** HAYIR -- loglama iyilestirmesi.

---

### BUG-56 [YUKSEK] Silent Exception -- PFAZ 06 Rapor JSON Okumalari

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz06_final_reporting/pfaz6_final_reporting.py:375, 406, 470, 532, 1415` |
| Oncelik | [YUKSEK] |
| Faz | PFAZ 06 |
| Tespit | 2026-05-12 Sprint 6 silent exception taramasi |

**Sorun:**
```python
except Exception:
    continue  # AI metrics_*.json okuma hatasi
except Exception:
    pass      # CV results JSON okuma
except Exception:
    continue  # ANFIS metrics_*.json okuma
except Exception:
    pass      # robustness CV JSON
except Exception:
    pass      # Excel sheet yazma hatasi
```
Excel raporunda eksik satirlar/sayfalar olustugunda kullanici hic fark etmez.

**Fix:** Her bloga `get_tracker().warn(f"[PFAZ06] {dosya_adi} read failed: {e}", ...)` ekle.

**Yeniden Egitim Gerekli:** HAYIR.

---

### BUG-57 [KRITIK] Silent Exception -- PFAZ 13 AutoML Dataset Yukleme

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz13_automl/automl_retraining_loop.py:211, 305, 758` |
| Oncelik | [KRITIK] |
| Faz | PFAZ 13 |
| Tespit | 2026-05-12 Sprint 6 silent exception taramasi |

**Sorun:**
```python
except Exception:
    pass  # veri yukleme hatasi
except Exception:
    pass  # config.json okuma hatasi
except Exception:
    pass  # bos rapor JSON yazma hatasi
```
AutoML dongusu calismiyor ama hata izi birakmadan None donuyor. PFAZ 13 gibi
gorunuyor ama hicbir model optimize edilmiyor.

**Fix:**
```python
except Exception as e:
    get_tracker().warn(f"[PFAZ13] Dataset load/config read failed: {e}", category="ERROR")
```

**Yeniden Egitim Gerekli:** HAYIR -- loglama; sonrasinda PFAZ 13 yeniden calistir.

---

### BUG-58 [ORTA] ProcessPoolExecutor -- _PFAZ_PARALLEL_ACTIVE Flag Eksik

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz02_ai_training/model_trainer.py:607` |
| Sinif | `ParallelTrainer.train_all_parallel()` |
| Oncelik | [ORTA] |
| Faz | PFAZ 02 |
| Tespit | 2026-05-12 Sprint 6 n_jobs taramasi |

**Sorun:**
`ProcessPoolExecutor` kullanilirken oncesinde `os.environ['_PFAZ_PARALLEL_ACTIVE'] = '1'` set edilmiyor.
`_inner_n_jobs()` bu flag olmadan -1 dondurur; child process'lerde RF/XGB'de nested parallelism riski.
Not: ProcessPoolExecutor child process'leri fork sonrasi env'yi inherit etmeyebilir.

**Fix onerileri (ikisi de gecerli):**
- A) ProcessPoolExecutor -> ThreadPoolExecutor degistir (env shared olur)
- B) ProcessPool initializer fonksiyonu ile flag set et

**Yeniden Egitim Gerekli:** HAYIR -- parallelism kodu degisikligi.

---

### BUG-59 [TASARIM] PFAZ 6 Sheet Sayisi -- Her Iki CLAUDE.md Yanlis

| Alan | Deger |
|------|-------|
| Dosyalar | `CLAUDE.md` (kok), `docs/thesis-toolkit/CLAUDE.md` |
| Oncelik | [TASARIM] |
| Faz | PFAZ 06 |
| Tespit | 2026-05-12 Sprint 6 doc vs artifact taramasi |

**Sorun:**
- Kok CLAUDE.md: "18-sheet Excel" -- YANLIS
- docs/thesis-toolkit/CLAUDE.md: "29-sheet Excel workbook" -- YANLIS
- `pfaz6_final_reporting.py` gercekte **22-29 sheet** uretiyor (konfigurasyona gore degisken).
- Eski `comprehensive_excel_reporter.py` 18 sheet uretiyor (ancak ana rapor bu dosya degil).

**Fix:** Her iki CLAUDE.md'yi "22-29 sheet (konfigurasyona gore)" seklinde guncelle.

---

### BUG-60 [TASARIM] PFAZ 7 Stacking Sayisi Yanlis Belgelenmis

| Alan | Deger |
|------|-------|
| Dosya | `docs/thesis-toolkit/CLAUDE.md` |
| Oncelik | [TASARIM] |
| Faz | PFAZ 07 |
| Tespit | 2026-05-12 Sprint 6 doc vs artifact taramasi |

**Sorun:**
CLAUDE.md: "5 voting + 6 stacking + AdaBoost"
Gercek `EnsemblePipeline._run_stacking()`: **4 meta-model** (Ridge, Lasso, RF, GBM).
MLP ve ElasticNet yalnizca `stacking_meta_learner.py`'de tanimli, ana pipeline'da cagrilmiyor.

**Fix:** Dokumantasyonu "5 voting + 4 stacking + AdaBoost" seklinde guncelle.

---

### BUG-61 [TASARIM] Kok CLAUDE.md PFAZ 10 Bolum Sayisi Yanlis

| Alan | Deger |
|------|-------|
| Dosya | `CLAUDE.md` (kok) |
| Oncelik | [TASARIM] |
| Faz | PFAZ 10 |
| Tespit | 2026-05-12 Sprint 6 doc vs artifact taramasi |

**Sorun:**
- Kok CLAUDE.md: "11 chapters + 2 appendices" -- YANLIS (eski v2.0)
- docs/thesis-toolkit/CLAUDE.md: "14 chapters + 4 appendices" -- DOGRU
- `pfaz10_master_integration.py:394-418`: 14 ana bolum (01-14) + 4 ek (A-D)

**Fix:** Kok CLAUDE.md'yi "14 chapters + 4 appendices" olarak guncelle.

---

*Sprint 6 raporu sonu | 15 yeni bug (BUG-47...BUG-61) | 2 TRUBA-CRITICAL, 3 KRITIK, 4 YUKSEK, 4 ORTA, 3 TASARIM | Encoding: 0 bug (temiz) | n_jobs: hardcoded -1 YOK*
---

## 2026-05-12 -- Sprint 8: Sprint 1/2/4 Eksik Uygulamalar

Sprint 1/2/4 belgede "TAMAMLANDI" yaziyordu ancak kod gerçegi farkliydi (KURAL 18).
Claude Code analizi bu üç eksikligi tespit etti.

### BUG-62 [KRITIK] CV Gate Kodda Yoktu -- parallel_ai_trainer.py

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py |
| Sprint | Sprint 1 (belge), Sprint 8 (gercek fix) |
| Durum | **DUZELTILDI 2026-05-12** |

**Sorun:** Sprint 1 belgesi "cv_R2 >= 0.0 + gap < 0.5 gate eklendi" diyordu.
Gercekte: constructor bu parametreleri kabul etmiyordu (imzada yoktu).
main.py parametreleri geciriyordu ama constructor sessizce görmezden geliyordu.
Pipeline tum modelleri kaydediyordu -- gate hic calismiyor.

**Fix:** Constructor imzasina 5 parametre eklendi. DUAL_FILTER blogu kayit
oncesine tasindi. Adaptif fold (N<150 -> 3-fold, N>=150 -> 5-fold) aktif.
max_train_cv_gap: 0.6 (Sprint 8 karari: kucuk N icin 0.5 yanlis alarm).

---

### BUG-63 [DUSUK] _configurations_note config'e Eklenmemis -- Sprint 2

| Alan | Deger |
|------|-------|
| Dosya | config.json pfaz03_anfis_training |
| Sprint | Sprint 2 (belge), Sprint 8 (gercek fix) |
| Durum | **DUZELTILDI 2026-05-12** |

**Sorun:** Sprint 2 belgesi _configurations_note ekleneceği yazyordu. Eklenmemis.

**Fix:** config.json pfaz03_anfis_training altina _configurations_note eklendi.

---

### BUG-64 [ORTA] MC Sinif Default'lari 100/500 Kalmis -- Sprint 4 BUG-38 Eksik

| Alan | Deger |
|------|-------|
| Dosyalar | monte_carlo_simulation_system.py: MCDropoutSimulator.__init__ (sat 132), FeatureDropoutSimulator.__init__ (sat 386) |
| Sprint | Sprint 4 (belge), Sprint 8 (gercek fix) |
| Durum | **DUZELTILDI 2026-05-12** |

**Sorun:** Sprint 4/BUG-38 DEFAULT_MC_CONFIG'u 1000'e cikardi ama sinif __init__
default'lari (MCDropoutSimulator: 100, FeatureDropoutSimulator: 500) guncellenmedi.

**Fix:** MCDropoutSimulator.__init__ n_samples=100->1000, FeatureDropoutSimulator n_samples=500->1000.

---

*Sprint 8 raporu | 3 eksik fix (BUG-62/63/64) + Dual R2 bağlam mesajlari*

---

# Sprint 10 — TRUBA QA Raporu Düzeltmeleri (2026-05-13)

Kemal'in `nucdatav2-truba` lokal kopyasında çıkardığı statik QA raporu (`sprint6-scan-results` branch) 7 bulgu listeledi; Claude bağımsız doğrulama yaparken 3 ek kritik bulgu ekledi. BUG-65..72 bu sprintte düzeltildi.

**Bu sprintin temel dersi:** PFAZ-arası kod standardı (örn. headerless CSV + metadata.json okuma) bir fazda değiştirildiğinde diğer fazlar bu standarda göre tek tek kontrol edilmeli. Sprint 1-8'de PFAZ2 headerless CSV okuma yapmıştı ama PFAZ13'e aynı pattern hiç taşınmamıştı — sonuç: PFAZ13 sessizce her zaman boş AutoML üretiyordu.

---

### BUG-65 [KRITIK] PFAZ13 Dataset Path Yanlis

| Alan | Deger |
|------|-------|
| Dosya | main.py:1305 |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** PFAZ13 PFAZ2 metrics dosyasından dataset bulurken `metrics_file.parent.parent.parent` kullanıyor. Bu `trained_models/{dataset}` dizinine gider ama `train.csv`/`val.csv` `generated_datasets/{dataset}/` altında. Path yanlış -> `train.csv` bulunamadı uyarısı -> her target için `continue` -> AutoML hiç çalışmaz, `automl_summary.json` boş, ama PFAZ13 `status='completed'` döner.

**Fix:**
```python
trained_ds_dir = metrics_file.parent.parent.parent
ds_dir = self.pfaz_outputs[1] / trained_ds_dir.name  # generated_datasets/{name}
```

**Tetikleyici kaynak:** Kemal'in TRUBA QA raporu Bulgu 1.

---

### BUG-66 [KRITIK] PFAZ13 Metadata-Aware CSV Okuma Yok

| Alan | Deger |
|------|-------|
| Dosya | main.py:1336 (eski) -> 1336+ (yeni) |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun (raporun atladığı):** BUG-65 düzeltilse bile PFAZ13 hâlâ çöker. PFAZ1 (`dataset_generation_pipeline_v2.py:1108`) headerless CSV yazıyor — sadece sayılar, sütun adları `metadata.json`'da. PFAZ2 bunu doğru okuyor: `pd.read_csv(file_path, header=None, names=_col_names)`. **PFAZ13** ise default `pd.read_csv(train_csv)` (header=0) kullanıyor → ilk veri satırını başlık zanneder → `target_col_map['MM'] = 'MAGNETIC MOMENT [µ]'` kolonunu hiç bulamaz → `continue` → her target skip.

**Fix:** PFAZ2 ile aynı pattern — `metadata.json` oku, `header=None, names=feat+tgt` ile load et. Geriye dönük uyumluluk için metadata yoksa eski header'lı format kullanılır.

**Fonksiyonel doğrulama (Sprint 10 patch):**
```
ESKI yontem 'MAGNETIC MOMENT [µ]' bulundu: False  <- bozuk
YENI yontem 'MAGNETIC MOMENT [µ]' bulundu: True   <- duzeltildi
```

**Ders:** KURAL 18 — kod ≠ doc varsayımı. PFAZ2 headerless+metadata pattern'i Sprint 1-8 boyunca standart oldu ama PFAZ13 hiç bu standarda göre güncellenmedi. PFAZ-arası okuma yöntemleri tutarlılığı **her sprint sonunda taranmalı.**

---

### BUG-67 [ORTA] PFAZ13 Bos AutoML Sessizce 'completed' Donerdi

| Alan | Deger |
|------|-------|
| Dosya | main.py:1470 (eski) |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** BUG-65/66 nedeniyle `automl_results` her zaman boş kalsa bile PFAZ13 `status='completed'` döndürürdü. Slurm/sacct başarılı görür, PFAZ6 final raporu AutoML bölümünü geçtiğini sanır.

**Fix:** Açık status kodları:
- `best_by_target` boş -> `status='skipped_no_pfaz2_results'`
- `automl_results` boş ama `best_by_target` dolu -> `status='skipped_no_datasets'`
- Aksi halde `status='completed'`

Ek alanlar: `n_best_by_target`, `n_automl_results` — raporlamada görünür hale geldi.

---

### BUG-68 [KRITIK] Job 3 ve Job 4 Hatalari `exit 0` ile Gizliyordu

| Alan | Deger |
|------|-------|
| Dosyalar | truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh:75, job4_pfaz06_08_10.sh:84 |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** Job 1 ve Job 2 doğru exit code döndürüyordu (`exit $EXIT_CODE`), ama Job 3 ve Job 4 fazlardan biri fail olsa bile **koşulsuz `exit 0`** ile bitiyordu. README "Job 3 bittikten sonra Job 4'u gönder" diyor — kullanıcı `sacct` veya mail'e güveniyor → "TAMAMLANDI" görür → Job 4'ü başlatır → eksik PFAZ13 sonucu ile final rapor üretilir.

**Ek not:** `EC=$?` `tee` pipe yüzünden Python'un değil tee'nin exit code'unu yakalıyordu. Fix `${PIPESTATUS[0]}` kullanır.

**Fix:**
```bash
FAIL=0
for PFAZ in ...; do
    python3 -u main.py --pfaz $PFAZ 2>&1 | tee "..."
    EC=${PIPESTATUS[0]}
    if [ $EC -ne 0 ]; then FAIL=1; fi
done
exit $FAIL
```

---

### BUG-69 [ORTA] `run_complete_pipeline.py` Eski Layout Import'lari

| Alan | Deger |
|------|-------|
| Dosya | run_complete_pipeline.py:154-241 |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** (deprecated guard) |

**Sorun:** `from dataset_generation.dataset_generator import ...`, `from ai_training.model_trainer import ...` gibi import'lar — bu top-level klasörler artık yok. Gerçek layout `pfaz_modules/pfaz0X_*/`. TRUBA'da yanlışlıkla çalıştırılırsa ilk import'ta çöker; iş yükü ve job zaman kaybı.

**Fix:** Modül başına deprecated banner ve `sys.exit(2)` guard. Tarihsel kayıt için eski kod alta korundu ama erişilemiyor. Kullan: `python3 -u main.py --run-all`.

---

### BUG-70 [KRITIK] HPC_MODE'da Desktop Worker Limitleri Aktif Kaliyordu

| Alan | Deger |
|------|-------|
| Dosya | utils/gpu_manager.py:181-199 |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun (raporun yetersiz tartıştığı):** Rapor "config notu güncellenmeli" dedi ama gerçek sorun farklı. TRUBA orfoz partition `#SBATCH -c 110` ayırıyor (BUG-25). Kod ise:
```python
return max(4, min(16, n // 3))  # AI mode
return max(4, min(20, n - 2))   # ANFIS mode
```
110-cpu node'da: AI worker = `min(16, 110//3) = 16`, ANFIS worker = `min(20, 108) = 20`. **Ayrılan kaynağın %14'ü kullanılır.** PFAZ2 koşusu ~7x daha uzun sürer → TRUBA'nın 3-gün limitini aşma riski.

`HPC_MODE=1` env değişkeni tüm Slurm scriptlerinde set ediliyor ama `gpu_manager.py` bunu hiç kontrol etmiyordu.

**Fix:** `HPC_MODE=1` ise tüm modlar için `max(4, n - 2)` döner (2 cekirdek IO icin). Desktop limitleri korundu (geriye dönük uyumluluk).

| Mode | Desktop (32 cpu) | HPC (110 cpu) önce | HPC (110 cpu) sonra |
|------|------------------|--------------------|---------------------|
| ai | 10 | 16 | **108** |
| anfis | 20 | 20 | **108** |
| mc | 16 | 16 | **108** |

**Ders:** HPC_MODE flag'i tüm kaynak hesaplayan yerlerde kontrol edilmeli, sadece env karşılaştırma değil davranışsal etki.

---

### BUG-71 [ORTA] `config.json` Top-Level `data_file` Eksik

| Alan | Deger |
|------|-------|
| Dosya | config.json |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** `main.py:479` `self.config.get('data_file', 'aaa2.txt')` çağırıyor — top-level alanı arıyor. Config'de bu alan yoktu → default `'aaa2.txt'` (root) kullanılırdı. Ama TRUBA job pre-check `data/aaa2.txt` arıyor. İki path farklı yerde → asimetri. Yerel repoda hem root hem `data/` altında dosya var, TRUBA'ya transfer sırasında sadece biri giderse PFAZ1 kırılır.

**Fix:** `"data_file": "data/aaa2.txt"` top-level eklendi. Hem job pre-check hem Python kodu aynı dosyayı arar.

---

### BUG-72 [DUSUK] Config n_workers Notu Yaniltici

| Alan | Deger |
|------|-------|
| Dosya | config.json (PFAZ2 + PFAZ3 parallel_training._note) |
| Sprint | Sprint 10 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** Eski not "orfoz 110 CPU max, 10 OS icin bırakıldi -> 100 worker" diyordu ama kod bu sayıyı okumuyordu (BUG-70 nedeniyle 16 worker kullanılırdı). Belge ile davranış uyuşmazlığı.

**Fix:** Not güncellendi — BUG-70 fix bağlamı eklendi: HPC_MODE=1 ise `GPUManager.optimal_workers()` n-2 worker döner.

---

*Sprint 10 raporu | TRUBA QA bulguları + 3 ek bulgu (BUG-65..72)*

---

### BUG-74 [YUKSEK] PFAZ2 'Target' Sutunu Yazmiyor -- Selector Calismaz, Layered Secim Sessizce Atlanir

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py:1690 (rows.append) |
| Sprint | Sprint 10 (ek denetim) |
| Durum | **DUZELTILDI 2026-05-13** |

**Tetikleyici:** Kemal'in sorusu "faz 3 PFAZ 2'nin hangi bilgilerini kullaniyor?" sonrasi sutun seviyesinde veri akisi denetimi.

**Sorun:** PFAZ2 `training_summary.xlsx`'e su sutunlari yaziyordu:
```
Model_Type, Config_ID, Dataset, PKL_Saved, Status_Note,
Train_R2, Train_RMSE, Train_MAE, Val_R2, Val_RMSE, Val_MAE,
Test_R2, Test_RMSE, Test_MAE, Training_Time_s, Error
```

PFAZ2 her satirin target'ini biliyordu (`train_single_job` sat. 285-304 dataset adina gore cikariyor) ama summary'ye **YAZMIYORDU**.

PFAZ3 ANFISDatasetSelector ise:
```python
target_df = self.results_df[self.results_df['Target'] == target]
```
ile filtre yapiyordu -> `KeyError: 'Target'` -> try/except Exception ile yakalanip log:
```
[WARNING] ANFISDatasetSelector calismadi: 'Target'; tum datasetler kullanilacak (fallback)
```

**Gercek davranis:** Tezde §3.4'te yazili "Top=50/Mid=50/Low=100 Layered Selection" stratejisi **kod seviyesinde hicbir zaman uygulanmamis**. PFAZ3 200 dataset yerine TUM datasetleri tariyor -> ~3-5x daha uzun ANFIS egitim suresi.

**Tez icin kritik:** "ML basarisiz -> ANFIS rescue" hipotezi (Low tier=100) hic test edilmemis. Sprint 5 §"Akademik Karar 1" bu hipotezi bu sprintin tasarim karari olarak konumlandiriyordu ama veri seviyesinde dogrulama yok.

**Fix:** `_target_from_dataset_name()` helper eklendi (PFAZ2 mevcut dataset-adi cikarim mantigini kullanir), `rows.append({...})` sozlugune `'Target': _target_from_dataset_name(result.dataset_name)` eklendi.

**Fonksiyonel dogrulama:**
```
Once (BUG-74): KeyError: 'Target' -> fallback -> tum datasetler
Sonra (fix):   Target sutunu var -> Layered selection calisir
               Top tier  R2>=0.90 -> Quota 50
               Mid tier  0.80<=R2<0.90 -> Quota 50
               Low tier  R2<0.80 -> Quota 100 (rescue hipotezi)
```

**Sprint 10 sonrasi yapilmasi gereken:** TRUBA'da PFAZ2 + PFAZ3 yeniden kosulmali. Log'larda `"Top layer (R2>=0.90): X datasets"` mesaji gorunmeli. Eski kosulardan elde edilen ANFIS sonuclari (Sprint 5 oncesi) tez stratejisini yansitmaz.

**Iliskili bug'lar:** BUG-17 (Sprint 5, sutun isimlendirme) -- ayni dosya cevresinde, ama BUG-74 farkli sutunu (`Target`) etkiliyordu.

---

*Sprint 10 ek denetim | PFAZ3-PFAZ2 sutun seviyesinde veri akisi analizi*

---

# Sprint 12 — Cikti Tamligi + TRUBA 2025-12-15 Kural Guncellemesi (2026-05-13)

Kemal'in iki talebi Sprint 12'yi tetikledi:
1. "Sprint 11 sonrasi her sey kusursuz mu?" -- 44 sibling-inference noktasi denetlendi, 36 kirilgan tespit, kategori C noktalari fix edildi.
2. TRUBA 2025-12-15 ekran goruntusu: "orfoz kuyruguna gonderilecek islerde node basina 56/112 ve katlarinda cekirdek talep edilmelidir."

Bu sprintin amaci: TRUBA'da tezdeki ciktilarin (xlsx, png, html) EKSIKSIZ uretilmesi + yeni TRUBA kuralina uyum.

---

### BUG-79 [ORTA] PFAZ3 Robustness CSV Path -- self.datasets_dir Kullanmıyordu

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py |
| Sprint | Sprint 12 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** PFAZ3 robustness analizi dataset CSV ararken `self.output_dir.parent / 'generated_datasets'` sibling-inference yapiyordu. `self.datasets_dir` constructor'da set ediliyor ama burada kullanilmiyordu.

**Fix:** Explicit > sibling-inference fallback. `_cand_list` once `self.datasets_dir / _rc.dataset_name`'i dener.

---

### BUG-80 [YUKSEK] PFAZ8 Helper-Based Path Resolution

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz08_visualization/visualization_master_system.py |
| Sprint | Sprint 12 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** PFAZ8'de **22 farkli yerde** sibling-inference (output_dir.parent / 'X') kullaniliyordu. Her sub-method ayri ayni pattern'i tekrarliyordu -- log dosyalari, training_summary, AAA2_enriched, anfis summary, final_report araniyordu.

**Risk:** Cikti yapisi degisirse PFAZ8 grafiklerinin yarisi uretilmez. Ozellikle:
- LogAnalyticsVisualizationsComplete: TRUBA'da loglar `outputs/logs/` altinda, eski kod scratch root'unda ararken bulamazdi -> log grafigi eksik.
- MasterReportVisualizationsComplete: 'final_report' adinda bir klasor PIPELINE'da YOK (PFAZ6 'reports/' kullanir). Eski kod hep miss -> master report grafigi hic uretilmezdi.

**Fix:** 
1. Constructor'a 6 parametre eklendi: `reports_dir`, `trained_models_dir`, `anfis_models_dir`, `datasets_dir`, `log_dir`, `project_root`.
2. 5 generic helper method: `_resolve_path`, `_find_reports_dir`, `_find_trained_models_dir`, `_find_anfis_models_dir`, `_find_datasets_dir`, `_find_log_dir`.
3. Tum sub-method'lar bu helper'lari kullanir -- explicit > fallback.
4. main.py PFAZ8 cagrisinda 6 path explicit aktarilir.

**Etki:** PFAZ8'in **9 visualization modulu** artik TRUBA'da eksiksiz cikti uretir:
- robustness, shap, anomaly, master_report, predictions, model_comparison, training_metrics, optimization, features
- + interactive_html, log_analytics_complete, master_report_complete, model_comparison_dashboard, shap_analysis, anomaly_visualizations

---

### BUG-81 [ORTA] PFAZ12 BandAnalyzer rglob -- Yanlis Path + Performans

| Alan | Deger |
|------|-------|
| Dosya | main.py + pfaz_modules/pfaz12_advanced_analytics/nuclear_band_analyzer.py |
| Sprint | Sprint 12 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** NuclearMomentBandAnalyzer PFAZ4 ciktisini ararken `self.output_dir.parent.parent` ve `self.output_dir.parent.parent.parent` tabanlarindan `rglob` yapiyordu. TRUBA'da:
- `output_dir.parent.parent = /arf/scratch/ahmacar` (proje disi)
- `output_dir.parent.parent.parent = /arf/scratch` (tum scratch alani)

Yanlis path'ler taraniyordu -- yavas + diger projelerin dosyalarini tarama riski.

**Fix:** 
- Constructor'a `pfaz4_excel_path: str = None` parametresi.
- Targeted fallback: sibling `unknown_predictions/` klasoru (PFAZ4 cikti).
- main.py'de explicit `pfaz4_pred_xlsx = self.pfaz_outputs[4] / 'AAA2_Original_vs_Predictions.xlsx'` aktarilir.

**Etki:** Band analyzer artik PFAZ4 cikti dosyasini DOGRU yerde arar. Tezdeki `Tahmin_Dogrulugu` sheet'i eksiksiz uretilir.

---

### BUG-82 [ORTA] PFAZ6 cross_model/unknown/datasets Sibling-Inference

| Alan | Deger |
|------|-------|
| Dosya | main.py + pfaz_modules/pfaz06_final_reporting/pfaz6_final_reporting.py |
| Sprint | Sprint 12 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** PFAZ6 constructor'da `base = self.output_dir.parent` ile 3 path turetiyordu: `cross_model_dir`, `unknown_dir`, `datasets_dir`. main.py bunlari aktarmiyordu -- sibling-inference.

**Fix:** Constructor parametreleri eklendi (`cross_model_dir`, `unknown_dir`, `datasets_dir`). main.py PFAZ6 cagrisinda explicit aktarir.

**Etki:** PFAZ6 final reportta PFAZ5 (cross_model_analysis) ve PFAZ4 (unknown_predictions) verisi eksiksiz dahil edilir.

---

### BUG-83 [ORTA] PFAZ6 pfaz9 Fallback YANLIS Klasor Adlari Ariyordu

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz06_final_reporting/pfaz6_final_reporting.py:1336 |
| Sprint | Sprint 12 |
| Durum | **DUZELTILDI 2026-05-13** |

**Sorun:** PFAZ6 `pfaz9_output_dir` None ise fallback sibling-inference ile arardi -- aradigi klasor adlari `pfaz9_output`, `aaa2_control_group`, `pfaz9`. **AMA gercek PFAZ9 cikti klasoru `aaa2_results`** (pfaz_outputs[9] = 'aaa2_results').

main.py:991 `reporter.pfaz9_output_dir = str(self.pfaz_outputs[9])` aktariyor -- explicit oldugu surece fallback tetiklenmez. Ama eger main.py disindan cagrilirsa MC summary sheet'i bos kalir.

**Fix:** Fallback hedefi `aaa2_results` ile baslar. Eski hatali adlar (pfaz9_output, aaa2_control_group) geriye donuk uyumluluk icin korundu.

**Etki:** PFAZ6 MC Uncertainty summary sheet'i ne main.py'den ne de baska bir entry point'ten cagrilsa eksik kalmaz.

---

### BUG-84 [KRITIK] TRUBA 2025-12-15 Kurali -- orfoz -c 56/112 Katlari Zorunlu

| Alan | Deger |
|------|-------|
| Dosya | truba/slurm_jobs/*.sh + config.json + utils/gpu_manager.py + truba/slurm_jobs/README.md |
| Sprint | Sprint 12 |
| Durum | **DUZELTILDI 2026-05-13** |

**Tetikleyici:** Kemal'in TRUBA login ekran goruntusu (2026-05-13):
> "Yeni depolama sistemine gecis tamamlanmistir. Bu gecis ile birlikte orfoz kuyruguna gonderilecek islerde node basina 56/112 ve katlarinda cekirdek, hamsi kuyrugunda ise node basina 56 ve katlarinda cekirdek talep edilmelidir."

**Sorun:** Tum 4 Slurm job script `#SBATCH -c 110` kullaniyordu. **Bu yeni kuralla iş kabul edilmez.**

**Fix:** Tum 4 job script `#SBATCH -c 112` yapildi (56'nin kati, tek node).

| Parametre | Eski | Yeni |
|-----------|------|------|
| #SBATCH -c | 110 | **112** |
| Worker (HPC_MODE n-2) | 108 | **110** |
| Config notu | "110-cpu node" | "112-cpu node" |
| README Max CPU | 110 | 112 (56 veya 112 katlari) |

**Etki:**
- Worker sayisi 108 -> 110 (yine paralel hizlanma korundu, hatta 2 worker fazla)
- Job submit reddedilmeyecek
- 56-cpu single socket alternatifi: kucuk testler icin gelecekte kullanilabilir

**Not:** BUG-70 (Sprint 10) fix'i ile `gpu_manager.py` `HPC_MODE=1` ise `n - 2` worker doner. 112 cpu node'da -> 110 worker. Sonraki Sprint 12 calismasinda gerek kalmazsa, simdilik bu yapi optimum.

---

*Sprint 12 raporu | Cikti tamligi + TRUBA kural guncellemesi (BUG-79..84) | 6 fix*

---

## Sprint 13 — Codex Audit + Tez Plani (BUG-85..99) | 2026-05-14

*15 fix: Codex audit bulgulari (4), Claude ek bulgulari (11), dead-code notlari (2)*

---

### BUG-85 [KRITIK] Job 1/2 + truba_slurm_job.sh `$?` tee Exit Yakalamiyordu

| Alan | Deger |
|------|-------|
| Dosya | truba/slurm_jobs/job1_pfaz01.sh, job2_pfaz02_03.sh, truba_slurm_job.sh |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Kaynak:** Codex audit bulgusu #1.

**Sorun:** `python3 main.py ... | tee log.txt; EXIT_CODE=$?` -- Bash'te `$?` pipeline'in **son komutunun** ciktisini doner. Son komut `tee` oldugundan, python fail etse bile `tee` basarili ise `EXIT_CODE=0` olur. Slurm `afterok` zinciri devam eder, eksik veriyle sonraki job baslar.

**Fix:** `EXIT_CODE=${PIPESTATUS[0]}` -- pipeline'in **ilk** komutunu (python) yakalar.

**Not:** Job3/Job4 Sprint 10'da duzeltilmisti. Job1/Job2/tek-parca script kaçmisti.

---

### BUG-86 [KRITIK] `--run-all` HPC Modda Faz Hatalarini Yutuyordu

| Alan | Deger |
|------|-------|
| Dosya | main.py: run_all_pfaz, main() |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Kaynak:** Codex audit bulgusu #2.

**Sorun:** `run_all_pfaz` HPC modda exception yakalayip `logger.warning` yaziyordu, sonra devam ediyordu. En sonda `return results` -- process exit 0. Slurm `afterok` zinciri devam eder, eksik modelleri bilen job baslar, PDF eksik uretilir.

**Fix:** `failed_phases` listesi eklendi. Sonunda `failed_phases` doluysa `RuntimeError` raise edilir. `main()` disindaki `except Exception: sys.exit(1)` bu RuntimeError'u yakalar -> Slurm non-zero exit gorur.

---

### BUG-87 [YUKSEK] `--check-deps` optuna/lightgbm Kontrolu Yapmiyor

| Alan | Deger |
|------|-------|
| Dosya | main.py: AutoInstaller.REQUIRED_PACKAGES |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Kaynak:** Codex audit bulgusu #3.

**Sorun:** `REQUIRED_PACKAGES` 13 temel paketi kontrol ediyordu. `optuna` ve `lightgbm` eksik -- PFAZ13 `optuna` olmadan sessizce `skipped` donuyordu. Kullanici `--check-deps` calistirip "tamam" goruyordu ama PFAZ13 hic calismiyor.

**Fix:** `optuna` ve `lightgbm` `REQUIRED_PACKAGES`'a eklendi. `catboost` `OPTIONAL_PACKAGES`'a tasindi (TRUBA modulunde yok, egitimde kullanilmiyor).

---

### BUG-88 [YUKSEK] PFAZ13 `skipped` Durumu Slurm'a Hata Olarak Iletilmiyordu

| Alan | Deger |
|------|-------|
| Dosya | main.py: run_pfaz_13, config.json: system.strict_truba |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Kaynak:** Codex audit bulgusu #4.

**Sorun:** PFAZ13 `optuna` yoksa veya dataset bulunamazsa `status='skipped'` donup `completed` isaretleniyordu. Slurm job exit 0 aliyordu. PFAZ6 final raporu AutoML bolumunu eksik aliyordu.

**Fix:** `config.json`'a `system.strict_truba: true` eklendi. HPC modda `skipped` durumunda `RuntimeError` raise edilir -> `sys.exit(1)` -> Slurm FAIL. Test ortaminda `strict_truba: false` yapilabilir.

---

### BUG-89 [ORTA] Slurm Job Script'lerinde Hardcoded Dizinler

| Alan | Deger |
|------|-------|
| Dosya | truba/slurm_jobs/job1..4.sh |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** `PROJECT_DIR="/arf/home/ahmacar/hpcv1"` ve `OUTPUT_DIR="/arf/scratch/ahmacar/hpcv1_outputs"` hardcoded. Farkli scratch dizini veya kullanici icin her job script elle duzenlenmesi gerekiyordu.

**Fix:** `${PROJECT_DIR:-/arf/home/ahmacar/hpcv1}` env override pattern. `export PROJECT_DIR=/baska/yol` ile override edilebilir.

---

### BUG-90 [ORTA] submit_all.sh Reset Talimatı Yoktu

| Alan | Deger |
|------|-------|
| Dosya | truba/slurm_jobs/submit_all.sh |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** Yeniden baslatmadan once hangi dizinlerin silinmesi, hangilerinin korunmasi gerektigine dair talimat yoktu. Eski `pfaz_status.json` ile yeni calistirma cakisiyordu.

**Fix:** Script basina reset notu eklendi: `pfaz_*/` sil, `pfaz_status.json` sil, `generated_datasets/` koru (PFAZ1 tekrar costurma). `squeue` kontrolu hatirlatan satir eklendi.

---

### BUG-91 [KRITIK] Job 2: PFAZ2 Fail → PFAZ3 Yine de Calisiyordu

| Alan | Deger |
|------|-------|
| Dosya | truba/slurm_jobs/job2_pfaz02_03.sh |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** PFAZ2 (AI egitim) basarisiz olsa bile PFAZ3 (ANFIS egitim) basliyordu. PFAZ3 PFAZ2 ciktilarini okur -- eksik model listesiyle ANFIS dataset secimi anlamsiz.

**Fix:** `if [ "$EXIT_PFAZ2" -ne 0 ]; then exit "$EXIT_PFAZ2"; fi` -- PFAZ2 fail ederse job erken cikiyor.

---

### BUG-92 [DUSUK] config.json'da Aktif Model Listesi Belirtilmemisti

| Alan | Deger |
|------|-------|
| Dosya | config.json: pfaz02_ai_training._models_active_note |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** LightGBM/CatBoost/SVR'in neden egitimde olmadigi belirtilmemisti.

**Fix:** `_models_active_note` eklendi: RF+XGBoost+DNN aktif, LightGBM/CatBoost/SVR pasif ve neden.

---

### BUG-93 [ORTA] PFAZ13 Trial-Level Detay Excel'i Uretilmiyordu

| Alan | Deger |
|------|-------|
| Dosya | main.py: run_pfaz_13, pfaz6_final_reporting.py |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** PFAZ13 her model icin JSON kaydediyordu ama tum deneme detayi tek bir Excel'de yoktu. PFAZ6 final raporu da bu verileri gostermiyordu.

**Fix:** `automl_trials_details.xlsx` (3 sheet: Best_Params, Trials_Detail, Convergence) PFAZ13 sonunda uretilir. PFAZ6'ya `AutoML_Trial_Details` sheet eklendi.

---

### BUG-94 [ORTA] PFAZ9 Monte Carlo Alt Siniflari random_state Almiyordu

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** `MCDropoutSimulator`, `BootstrapSimulator`, `NoiseSimulator`, `FeatureDropoutSimulator` constructor'lari `random_state` parametresi almiyordu. TRUBA'da her kosulusta farkli MC sonuclari uretiliyordu -- reproducibility yok.

**Fix:** 4 sinifa `random_state: int = 42` parametresi + `np.random.seed(random_state)` eklendi.

---

### BUG-95 [ORTA] PFAZ9 joblib.load Hatalari debug Seviyesinde Kaliyordu

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz09_aaa2_monte_carlo/aaa2_control_group_complete_v4.py |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** `joblib.load` exception'lari `logger.debug` ile susturuluyordu. Bozuk/eksik pkl dosyalari sessizce atlandi. Hata ayiklamasi cok zordu.

**Fix:** `logger.warning` seviyesine tasinandi. `failed_models` listesi eklendi. Sonda ozet log: `{N}/{toplam} model yuklenemedi: [config_id listesi]`.

---

### BUG-96 [YUKSEK] PFAZ2 RobustnessTester Dead Code'du

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py, model_validator.py |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun:** `RobustnessTester` sinifi (noise/outlier/perturbation testleri) `model_validator.py`'de yazilmisti ama `run_model_validation` onu hic cagirmiyordu. Tez icin kritik robustness analizi eksikti.

**Fix:** `run_model_validation`'a `X_test`/`y_test` parametresi eklendi. CV sonrasi 3 test calistirilir (noise_sensitivity, outlier_sensitivity, feature_perturbation). `robustness_summary.xlsx` tum modeller icin ozet Excel. Her model icin ayri PNG + JSON.

**Sure etkisi:** Model basina ~8-10 dakika ek sure. Toplam PFAZ2 sure etkisi beklenen aralikta.

---

### BUG-97 [YUKSEK] PFAZ12 BootstrapCI Dead Code + ANFIS Verisi Kullanilmiyordu

| Alan | Deger |
|------|-------|
| Dosya | main.py: run_pfaz_12, pfaz12/bootstrap_confidence_intervals.py |
| Sprint | Sprint 13 |
| Durum | **DUZELTILDI 2026-05-14** |

**Sorun (1):** `BootstrapConfidenceIntervals` sinifi yazilmisti ama `run_pfaz_12`'de hic import edilmemisti.

**Sorun (2):** `run_pfaz_12` sadece PFAZ2 (AI modeller) verisi kullaniyordu. PFAZ3 (ANFIS) `anfis_training_results.xlsx` hic okunmuyordu. Tezin ana sorusu -- "ANFIS istatistiksel olarak AI'dan anlamli mi farkli?" -- cevaplanamiyordu.

**Fix:**
- PFAZ3 `anfis_training_results.xlsx`'ten `Val_R2` skorlari okunur, `model_scores['ANFIS']` olarak eklenir.
- Tum modeller (RF, XGBoost, DNN, ANFIS) icin Bootstrap CI hesaplanir (10.000 resample, %95 CI).
- En iyi AI modeli vs ANFIS bootstrap karsilastirmasi: p-value + CI + significant flag.
- `bootstrap_ci_results.xlsx` (Summary, Model_Performance, Model_Comparison) + `bootstrap_distribution.png`.
- ANFIS skorlari `scores_dict`'e eklendiginden mevcut ANOVA/Wilcoxon testleri de ANFIS'i kapsıyor.

**Sure etkisi:** ~2-5 dakika. numpy/scipy only, SALib gerektirmez.

---

### BUG-98 [DUSUK] PFAZ12 AdvancedSensitivityAnalysis Dead Code (Future Work)

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz12_advanced_analytics/advanced_sensitivity_analysis.py |
| Sprint | Sprint 13 |
| Durum | **DEAD CODE NOTE EKLENDI** |

**Karar:** AKTIVE EDILMEDI. Sobol/Morris SALib gerektirir (TRUBA'da yok), saatlerce surebilir. Tez kapsaminda "future work" olarak isaretlendi. Dosya basina DEAD_CODE_NOTE eklendi.

---

### BUG-99 [DUSUK] PFAZ5 OptimizerComparisonReporter Dead Code (Future Work)

| Alan | Deger |
|------|-------|
| Dosya | pfaz_modules/pfaz05_cross_model/optimizer_comparison_reporter.py |
| Sprint | Sprint 13 |
| Durum | **DEAD CODE NOTE EKLENDI** |

**Karar:** AKTIVE EDILMEDI. PFAZ5 MASTER_CROSS_MODEL_REPORT'ta kismen kapsaniyor. Zaman darligi. Dosya basina DEAD_CODE_NOTE eklendi.

---

*Sprint 13 raporu | Codex audit + Tez plani (BUG-85..99) | 15 fix/not | 2026-05-14*

---

# Sprint 15 -- TRUBA Kriz Yonetimi (BUG-101..110)

**Tarih:** 2026-05-19/20
**Baglam:** TRUBA Job2 2x timeout sonrasi tam denetim. 61283 metrics dosyasi + kalite haritasi analizi sonrasi 10 yeni bug tespit edildi. Numara atlamasi: BUG-100 memory'de rezerve, cakisma riski icin BUG-101'den baslandi (KURAL 6).

### BUG-101 [KRITIK] PFAZ2 Resume: Kalite Filtresine Takilan Modeller Checkpoint Yazmiyor

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py` |
| Satirlar | 1346, 1368, 1423, 1438 (4 success=False return + 1530 exception) |
| Sprint | Sprint 15 |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:** `train_single_job` icinde model bir kalite filtresinden gecemezse (DIVERGED, val_R2<0.5 POOR, dual-R2 cv RET, dual-R2 gap RET) sadece `metrics_*.json` yazip donuyor; `.pkl` DE `completed.json` DE yazmiyor. Resume mekanizmasi (1242 + 1281. satir) yalniz `.pkl`/`completed.json` arar. Sonuc: reddedilen her model her resume'da sifirdan tekrar egitilir.

**Kanit:** TRUBA Job2 5779758: METRICS=61283, PKL=6615, COMPLETED.json=5731. Yaklasik 54668 model reddedilip checkpoint yazmamis. Job2 iki kere timeout oldu; aynı 54668 model her seferinde tekrar egitildi.

**Fix:** `_save_checkpoint(out_dir, ...)` helper eklendi; 4 kalite-red return yoluna cagri kondu. Exception yolu (1530) checkpoint yazmaz -- geçici hata olabilir, tekrar denensin (B kararı).

**Tezsel etki:** Resume davranisi belgeli olarak tutarli. Tez §3.5'te "deterministik kalite filtresi + checkpoint" akisi anlatilir.

---

### BUG-102 [KRITIK] ANFIS Resume Ayni Pattern -- Reddedilen Modeller Checkpoint Yazmiyor

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py` |
| Satirlar | 858, 871 (success=False return) + 1263, 1292 (resume check) |
| Sprint | Sprint 15 |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:** BUG-101 ile birebir ayni pattern. ANFIS reddedilen modeller `.pkl` yazmiyor. ANFIS henuz TRUBA'da basariyla calismadi (PFAZ2 timeout zincirinde bekledi), bu yuzden gercek etki gozlemlenmedi -- ama calistirildiginda BUG-101 ile ayni patlamayi yapacakti.

**Fix:** Ayni `_save_checkpoint` pattern'i ANFIS trainer'da uygulandi.

---

### BUG-103 [YUKSEK] Model Tipi x Config Caprazi -- Dizin Yapisi Tutarsiz

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py:create_training_jobs` |
| Sprint | Sprint 15 |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:** `train_all_models_parallel` `model_types` listesini (RF/XGB/LGB/CB/SVR/DNN) tum 50 config ile capraz cogaltiyor. Sonuc: `trained_models/<dataset>/SVR/RF_018/metrics_RF_018.json` gibi tutarsiz dizinler -- klasor "SVR", config "RF_018". Is hacmi beklenenin 6 kati: 6 model tipi x 50 config = 300 is/dataset.

**Kanit:** TRUBA cikti dizininde gercek ornek:
```
QM_150_S70_AZNNP_MinMax_Stratified/SVR/RF_018/metrics_RF_018.json
MM_150_S80_AZSBEPA_MinMax_Stratified_NoAnomaly/LightGBM/XGB_027/metrics_XGB_027.json
```

**Fix:** `create_training_jobs` icinde config['id'] prefix'i (`RF_`, `XGB_`, `DNN_`) ile `model_type` eslesmesi zorunlu kilindi. Eslesme yoksa is olusturulmuyor.

---

### BUG-104 [YUKSEK] model_types Listesi config.json'dan Okunmiyor -- LightGBM/CatBoost/SVR Otomatik Dahil

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py:1857-1867` |
| Sprint | Sprint 15 |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:** Kod su sekilde model tipi ekliyor:
```python
model_types = ['RF']
if XGBOOST_AVAILABLE:   model_types.append('XGBoost')
if LIGHTGBM_AVAILABLE:  model_types.append('LightGBM')
if CATBOOST_AVAILABLE:  model_types.append('CatBoost')
model_types.append('SVR')  # her zaman
if TF_AVAILABLE and self.use_advanced_models:
    model_types.append('DNN')
```
TRUBA'da bu kutuphaneler kuruluysa otomatik egitiliyorlar. Memory'de "BUG-92: LightGBM/CatBoost/SVR egitime DAHIL DEGIL" notu vardi -- bu sadece KULLANICI NIYETIYDI, kod hala bunlari ekliyordu. KURAL 31 (SSoT) ihlali: config.json model listesi vs kod davranisi farkli.

**Fix:** `config.json`'a `pfaz02.model_types` listesi eklendi; kod once config'i okuyor, kutuphane kuruluysa ve config'te listeleniyorsa modeli ekliyor. Config tek kaynak (SSoT).

**KURAL 38 dogdu:** "Memory'deki niyet != kod davranisi" -- BUG-104'un birebir ders kaynagi.

---

### BUG-105 [ORTA] PFAZ5 `faz5_complete_cross_model.py` -- Ölü Kod (Eski API)

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz05_cross_model/faz5_complete_cross_model.py:432` |
| Sprint | Sprint 15 |
| Durum | **DEAD_CODE_NOTE EKLENDI 2026-05-20** |

**Sorun:** Bu modul `self.ai_models = ['RandomForest', 'GradientBoosting', 'XGBoost', 'DNN', 'BNN', 'PINN']` listesi ve `ai_dir / model_name / target_predictions.csv` yolu ariyor -- bu eski API. Gercek PFAZ2 cikti yapisi `trained_models/<dataset>/<model_type>/<config_id>/`. Modul caligmaz, hicbir yerde import edilmiyor.

**Karar:** AKTIVE EDILMEDI. Gercek PFAZ5 `faz5_cross_model_analysis.py` uzerinden calisiyor. Dosya basina DEAD_CODE_NOTE eklendi (BUG-98/99 patterni).

---

### BUG-106 [ORTA] PFAZ8 Visualization Hardcoded Model Listeleri

| Alan | Deger |
|------|-------|
| Dosyalar | `pfaz_modules/pfaz08_visualization/visualization_system.py:222,251`, `model_comparison_dashboard.py:667`, `pfaz8_thesis_charts.py:53` (MODEL_COLORS), `visualization_master_system.py:1585,1698,1768,2212,2930,2999,3043` |
| Sprint | Sprint 15 |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:** Hardcoded `models = ['XGBoost', 'RF', 'GBM', 'DNN', 'ANFIS-M1', 'ANFIS-M2']` veya `colors = {'RF': '#2196F3', 'XGBoost': '#4CAF50', 'DNN': '#FF9800'}` Sprint 15'te DNN cikarilinca bazi gorseller bos DNN sutunu/bar gosteriyor (crash yok ama kalite dusuk).

**Fix:** `models = sorted(df['Model_Type'].unique())` ve `colors = generate_colors(model_list)` -- veri dinamik okunuyor. MODEL_COLORS dict'i `.get(model, default)` ile defansif olusturuluyor.

---

### BUG-107 [DUSUK] Slurm Sure Limiti Tutarsiz (Belge vs Script)

| Alan | Deger |
|------|-------|
| Dosyalar | `truba/slurm_jobs/job2_pfaz02_03.sh`, `docs/thesis-toolkit/sprints/sprint-13-final.md`, memory |
| Sprint | Sprint 15 |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:** Memory'de "job2 3 gun" notu vardi, scriptte `--time=1-00:00:00` (1 gun). Tutarsizlik. Sprint 15 sonrasi is hacmi 360k->36k'ya dustugu icin 1 gun fazlasiyla yetiyor; ancak belge senkronizasyonu zorunlu.

**Fix:** Belgelerde "Job2 sure: 1 gun (Sprint 15 sonrasi ~1 saat gercek)" yazildi; scriptte degisiklik yok.

---

### BUG-108 [YUKSEK] PFAZ9 Monte Carlo ANFIS Yolu Yanlis -- Hicbir ANFIS Modeli Yuklenemiyor

| Alan | Deger |
|------|-------|
| Dosya | `pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py:684` |
| Sprint | Sprint 15 |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:** Kod su yolu ariyor:
```python
model_path = self.models_dir / 'ANFIS' / model_id / 'model.mat'
```
Gercek ANFIS kayit yapisi (KURAL 32 ile dogrulandi):
- Dizin: `trained_anfis_models/<dataset>/<config_id>/`
- Dosyalar: `model_{cfg_id}.pkl` (joblib), `{name}_workspace.mat`, `{name}_fis.mat`, `metrics_{cfg_id}.json`

`model.mat` diye bir dosya UCRETLI YOK. PFAZ9 ANFIS Monte Carlo simulasyonu calismiyor. ANFIS hicbir zaman tam calismadigi icin (PFAZ2 timeout) fark edilmemis.

**Fix:** Yol PFAZ4 ile ayni pattern'e cevrildi:
```python
model_path = self.anfis_models_dir / dataset_name / config_id / f'model_{config_id}.pkl'
model = joblib.load(model_path)
```

---

### BUG-109 [DOKUMANTE EDILDI -- KASITLI TASARIM KARARI] PFAZ2/3 -> PFAZ12 Ters Bagimliik

| Alan | Deger |
|------|-------|
| Dosyalar | `parallel_ai_trainer.py:2019`, `anfis_parallel_trainer_v2.py:1609` -> `from pfaz_modules.pfaz12_advanced_analytics.nuclear_pattern_analyzer` |
| Sprint | Sprint 15 (tespit) / **Sprint 16 (dokumante: tasarim karari)** |
| Durum | **DOKUMANTE EDILDI 2026-05-20 (kod yorum eklendi, refactor yapilmadi)** |

**Sorun:** Alt-faz (PFAZ2/3) ust-faza (PFAZ12) bagimli. Memory'deki "BUG-65/66/74 pattern" ile ayni mimari risk gibi gorunur.

**Sprint 16 ANALIZ SONUCU (KASITLI TASARIM KARARI):** Bu bir BUG degil, bilincli mimari karar:
1. NuclearPatternAnalyzer egitim SONRASI cagrilir (predict-time, not train-time)
2. Lazy import (try/except icinde, fonksiyon icinde) -- runtime'da modul yoksa PFAZ2/3 calismaya devam eder
3. PFAZ12 kategorisi "ileri analitik"; PFAZ2/3 "egitim". Sinifi PFAZ2'ye tasimak kategori karistirmaktan kacinmak icin yapilmadi
4. Mevcut kosulda kod calisiyor, davranissal bir sorun yok

**Fix (Sprint 16):** Iki import noktasina aciklayici yorum eklendi (kasitli tasarim karari, refactor not). Kod davranisi degismedi.

**Tez-sonrasi opsiyonel iyilestirme:** NuclearPatternAnalyzer cagrisini main.py'ye tasimak (PFAZ2 sonrasi callback). Bu Sprint 18+ icin not edildi -- tezin akademik iddialarini etkilemez.

---

### BUG-110 [DUZELTILDI Sprint 16] PFAZ6 <-> PFAZ12 Soft Circular Import

| Alan | Deger |
|------|-------|
| Dosyalar | `utils/excel_standardizer.py` (yeni canonical), `pfaz_modules/pfaz06_final_reporting/excel_standardizer.py` (stub), `pfaz_modules/pfaz12_advanced_analytics/nuclear_band_analyzer.py:60`, `pfaz_modules/pfaz12_advanced_analytics/nuclear_pattern_analyzer.py:66`, `utils/warning_tracker.py:233`, `pfaz_modules/pfaz06_final_reporting/__init__.py` |
| Sprint | Sprint 15 (tespit) / **Sprint 16 (DUZELTILDI)** |
| Durum | **DUZELTILDI 2026-05-20** |

**Sorun:**
- ESKI: `pfaz06_final_reporting/pfaz6_final_reporting.py` -> `pfaz12.bootstrap_confidence_intervals` (lazy)
- ESKI: `pfaz12_advanced_analytics/nuclear_band_analyzer.py:60` -> `pfaz06.excel_standardizer` (modul-ustu try/except)
- DAIRE: PFAZ6 -> PFAZ12 ve PFAZ12 -> PFAZ6

Lazy import sayesinde su an patlamiyor ama tehlikeli. Yarin biri lazy'i modul-ustune cekerse circular import hatasi.

**Fix (Sprint 16, KAPSAMLI QA ile dogrulandi):**

1. **`utils/excel_standardizer.py` yeni CANONICAL kaynak** -- ExcelStandardizer'in tam kodu (468 satir) buraya tasindi
2. **`pfaz_modules/pfaz06_final_reporting/excel_standardizer.py` stub haline geldi** -- sadece `from utils.excel_standardizer import *` yapar (backward compat)
3. **PFAZ12 modulleri (`nuclear_band_analyzer.py`, `nuclear_pattern_analyzer.py`)** artik direkt `utils/`'den import ediyor
4. **`utils/warning_tracker.py`** (BUG-110 KAPSAMLI QA ile bulundu, 4. kullanici!) artik in-package `utils/excel_standardizer` import ediyor
5. **`utils/__init__.py`** ExcelStandardizer'i top-level re-export ediyor (`from utils import ExcelStandardizer`)
6. **`pfaz_modules/pfaz06_final_reporting/__init__.py`** stub uzerinden re-export (backward compat korundu)

**Yapisal sonuc:**
- ONCEKI: PFAZ12 -> PFAZ6 (1 yon) + PFAZ6 -> PFAZ12 (3 yer) = DONGU
- SONRA: PFAZ12 -> utils (1 yon) + PFAZ6 -> PFAZ12 (3 yer) = TEK YONLU, DONGU YOK
- Grep dogrulamasi: `grep "from pfaz_modules.pfaz06" pfaz12/*.py` -> 0 sonuc

**Test sonuclari (Sprint 16 KURAL 42 KAPSAMLI QA):**
- Sentaks: 8 dosya OK
- Real import: 4 yol calisir (utils canonical, utils paketinden, PFAZ6 stub, PFAZ6 paketten) -- hepsi ayni sinifi donduruyor
- Fonksiyonel: gercek Excel dosyasi yazildi (5709 bytes, 1 sayfa)
- Regression: Sprint 15 helper'lari yerinde

---

*Sprint 15 raporu | TRUBA kriz yonetimi (BUG-101..110) | 8 fix + 2 ertelendi | 2026-05-20*

*Sprint 16 raporu | SON SPRINT -- BUG-109 dokumante, BUG-110 fix, KURAL 41-42 | 2026-05-20*
