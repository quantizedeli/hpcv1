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
