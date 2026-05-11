# PFAZ 03 -- ANFIS Egitimi
**Surum:** v1.0 | **Guncelleme:** 2026-05-03

---

## 1. Faz Karti

| Alan | Deger |
|------|-------|
| Faz No | PFAZ 03 |
| Ana Sinif | `ANFISParallelTrainerV2` |
| Modul | `pfaz_modules/pfaz03_anfis_training/` |
| Durum (2026-05-03) | completed 100% |
| Giris | PFAZ 01 ciktisi: train.csv / val.csv / test.csv |
| Cikti | `outputs/anfis_models/{dataset}/{config}/` |
| ANFIS Turu | Takagi-Sugeno 1. Dereceden (TakagiSugenoANFIS) |
| Konfigurasyon | 8 (CFG001-CFG008) |
| Paralel | ThreadPoolExecutor |
| MATLAB | Opsiyonel (Python fallback mevcut) |
| R2 Kayit Esigi | val_R2 >= 0.5 |
| Max Iterasyon | 300 |
| Erken Durma | patience=30 (val RMSE bazli) |
| Regularizasyon | L2 alpha=0.01 (ridge LSE) |

---

## 2. ANFIS Teorisi — Takagi-Sugeno Sistemi

ANFIS (Adaptive Neuro-Fuzzy Inference System), 1993'te Jang tarafindan onerilen ve
yapay sinir aglari ile bulanik mantigi birlestiren hibrit bir ogrenmeli sistemdir.
Bu projede kullanilan varyant: **Birinci Dereceden Takagi-Sugeno ANFIS**.

Temel fark: Sonuc (consequent) kismi sabit bir sayidan degil, girislerin dogrusal
kombinasyonundan olusur. Kural formu:

```
IF x1 is A1 AND x2 is A2 THEN f = p1*x1 + p2*x2 + q
```

Bu yaklasim, nükleer momentlerin A, Z, N gibi degiskenlerle
dogrusal olmayan ama yerel dogrusal iliskilerine son derece uygundur.

### 2.1 5-Katman Ag Mimarisi

```
Giris x = [x1, x2, ..., xn]
|
+-- Katman 1 (Fuzzifikasyon):
|     u_Ai(xi) = MF(xi; ci, si)  [Gaussian/Bell/Tri/Trap]
|
+-- Katman 2 (Kural Aktivasyonu):
|     w_r = PROD_i(u_Ai(xi))     [T-norm: carpim]
|
+-- Katman 3 (Normalizasyon):
|     w_hat_r = w_r / SUM_j(w_j)
|
+-- Katman 4 (Sonuc Hesaplama):
|     f_r = p_r0 + p_r1*x1 + ... + p_rn*xn
|     [LSE ile optimize - kapalı form]
|
+-- Katman 5 (Toplama/Cikis):
      y_hat = SUM_r(w_hat_r * f_r)
```

### 2.2 Uyelik Fonksiyon Formullleri

| Tur | Formul | Kod (anfis_parallel_trainer_v2.py) |
|-----|--------|----------------------------------|
| Gaussian | exp(-0.5 * ((x-c)/s)^2) | _gaussian: s clamped > 1e-6 |
| Bell (GenBell) | 1 / (1 + |((x-c)/s)|^4) | _bell: 4. kuvvet (standart: 2b) |
| Ucgen (Tri) | max(0, 1 - |x-c|/s) | _triangle: s clamped > 1e-6 |
| Yamuk (Trap) | min/max tabanli | _trapezoid: left/right egim |

NOT: Bell MF'de 4. kuvvet kullanilmistir (standart gbellmf: 2b kuvvet).
Bu, daha genis plato ve daha sert kenarl anlamına gelir.

---## 3. 8 Konfigurasyon Detaylari

*Kaynak: anfis_config_manager.py:72-145, ANFISConfigManager._initialize_configs()*

| ID | Isim | Yontem | n_MF | MF Turu | Radii | MATLAB Kodu |
|----|------|--------|------|---------|-------|-------------|
| CFG001 | Grid_2MF_Gauss | grid | 2 | gaussmf (Gaussian) | N/A | genfis1(tr, 2, 'gaussmf') |
| CFG002 | Grid_2MF_Bell | grid | 2 | gbellmf (GenBell) | N/A | genfis1(tr, 2, 'gbellmf') |
| CFG003 | Grid_2MF_Tri | grid | 2 | trimf (Ucgen) | N/A | genfis1(tr, 2, 'trimf') |
| CFG004 | Grid_2MF_Trap | grid | 2 | trapmf (Yamuk) | N/A | genfis1(tr, 2, 'trapmf') |
| CFG005 | Grid_3MF_Gauss | grid | 3 | gaussmf (Gaussian) | N/A | genfis1(tr, 3, 'gaussmf') |
| CFG006 | SubClust_R03 | subclust | K-Means | gaussmf | 0.3 | genfis2(tr(:,1:end-1), tr(:,end), 0.3) |
| CFG007 | SubClust_R05 | subclust | K-Means | gaussmf | 0.5 | genfis2(tr(:,1:end-1), tr(:,end), 0.5) |
| CFG008 | SubClust_R07 | subclust | K-Means | gaussmf | 0.7 | genfis2(tr(:,1:end-1), tr(:,end), 0.7) |

### 3.1 Grid Yontemi — Detaylar

Grid yonteminde her giris degiskeni icin n_MF adet uyelik fonksiyonu esit aralikla yerlestirilir:

```python
# _init_grid (anfis_parallel_trainer_v2.py:166-176)
centers[i] = np.linspace(lo, hi, n_mfs)              # Esit araliklarla merkez
spreads[i]  = (hi - lo) / (2 * n_mfs)                # Genislik: aralik/2n
```

Toplam kural sayisi: n_rules = n_mfs ^ n_inputs

| n_inputs | CFG001 n_mfs=2 | CFG005 n_mfs=3 |
|----------|---------------|---------------|
| 2 | 4 kural | 9 kural |
| 3 | 8 kural | 27 kural |
| 4 | 16 kural | 81 kural |
| 5 | 32 kural | 243 kural |

Bu kural sayısı patlaması CFG005'i adaptif n_mfs'e en cok maruz birakan konfigurasyon yapar.

### 3.2 SubClust Yontemi — Detaylar

SubClust yonteminde kural merkezleri KMeans ile belirlenir (gercek subtractive clustering
yerine KMeans tabanlı yaklasım):

```python
# _init_subclust (anfis_parallel_trainer_v2.py:179-190)
k = min(n_rules, max(2, len(X_norm) // 4))   # k: dataset boyutunun 1/4'u
km = KMeans(n_clusters=k, random_state=42, n_init=5)
km.fit(X_norm)
# Spread: En yakin kume merkezine ortalama yarim mesafe
spread_val = max(mean(nearest_distances) * 0.5, 0.1)
```

Radii parametresi dogrudan k'yi etkilemez — Python fallback gercek subtractive
clustering yerine KMeans kullanir. Radii farkli konfigurasyonlar arasinda teorik ayirim
icin saklanir.

### 3.3 Grid vs SubClust — Karsilastirma

| Kriter | Grid (CFG001-005) | SubClust (CFG006-008) |
|--------|-------------------|-----------------------|
| Kural merkezi | Veri dagilimından bağımsız | Veri kümelerinden turetilir |
| Kural sayısı | n_mfs^n_inputs (patlar) | n_train//4 (veriyle orantilı) |
| Yorumlanabilirlik | Yuksek (duzgun izgarа) | Dusuk (veri odaklı) |
| Kucuk veri seti | Asiri basit veya asiri karmasik | Adaptif |
| Overfitting riski | n_mfs artarken yukselir | Veri orantili, dustu |
| En iyi kullanim | Duzenli/ozgun veri | Kume yapili veri |

Nukleer veri seti icin: SubClust, kabukluluk (magic number) ve deformasyon (beta_2)
etrafinda dogal kume yapisi olustugunda genellikle daha iyi performans gosterir.

---## 4. Hibrit Ogrenme Algoritmasi

ANFIS'in gucu, parametrelerini iki farkli optimizasyon stratejisiyle ayri ayri ogrenebilmesinden gelir.

### 4.1 LSE: Ardisil Parametreler (Katman 4)

Verilen sabit one (premise) parametreler icin, sonuc parametreleri (p_r0..p_rn) kapalı
formda Ridge regresyon cozumu ile hesaplanir:

```
A[n, n_rules*(n_inputs+1)]  -- Agirlikli giris matrisi (her kural icin w_hat_r * [1, x])

(A^T A + alpha*I) * theta = A^T * y

theta = n_rules * (n_inputs+1) parametre vektoru
alpha = 0.01  (L2 ridge regularizasyon)

Cozum: np.linalg.solve() [normal denklem]
       np.linalg.lstsq()  [fallback: tekil matris durumunda]
```

LSE avantaji: One parametreleri sabitken, sonuc parametreleri GLOBAL optimuma erisilebilir.
Bu, iteratif gradient descent'in tuzaklarina dusmez.

### 4.2 Gradient: One Parametreler (Katmanlar 1-2)

MF merkezleri (c) ve genislikleri (s) gradient optimizasyonuyla ayarlanir:

```
# Scipy L-BFGS-B (CPU) — _gradient_scipy()
objective: v -> MSE(y, predict(X, unflatten(v)))
              [ic: LSE ile sonuc guncelleniyor her adimda]

v = concatenate([centers.ravel(), spreads.ravel()])

# PyTorch LBFGS (GPU) — _gradient_torch() [gpu_enabled=True ise]
# CPU fallback: _gradient_scipy()

use_gradient=True iff len(X_train) >= 10
```

Iki-kademe hibrit dongu:

```
1. LSE  -> sonuc optimum (sabit one'da)
2. LBFGS -> one'i guncelle (sabit sonucta gradient)
3. LSE  -> sonuc yeniden hesapla
4. ... max_iter=300 veya patience=30 adimda dur
```

Bu yaklasim, sadece gradient descent kullanimina gore genellikle daha hizli yakinsar.

### 4.3 Adaptif n_mfs — Kural Sayısı Guvenligi

Her egitim oncesinde, istenen n_mfs veri boyutuna gore kontrol edilir:

```python
# _adaptive_n_mfs (anfis_parallel_trainer_v2.py:81-89)
for mfs in range(requested_mfs, 1, -1):
    n_rules = mfs ** n_inputs
    if n_rules < max(4, n_train / 3):  # kural basi en az 3 ornek
        return mfs
return 2  # mutlak minimum
```

Kural: n_kural < n_train/3  (her kural icin en az 3 egitim ornegi)

| Ornek: n_train=60, n_inputs=3 | Deger |
|-------------------------------|-------|
| Esik: max(4, 60/3) | 20 |
| CFG001 mfs=2: n_rules=8 | 8 < 20 -> 2 MF kullan |
| CFG005 mfs=3: n_rules=27 | 27 >= 20 -> mfs'i azalt -> 2 MF kullan |

CFG005 (3 MF Gauss), kucuk veri kumelerinde otomatik olarak 2 MF'e duser.
Bu, kural patlamasından kaynaklanan overfitting riskini otomatik olarak azaltir.

---## 5. Veri Yukleme ve On-Isleme

### 5.1 Baslıksız CSV Formati

ANFIS trainer, PFAZ 01'in urettigi CSV dosyalarini okurken baslikları metadata.json'dan alir:

```python
# _load_split_csv (ANFISParallelTrainerV2)
# PFAZ01'den gelen CSV'ler basliksiz olabilir -> metadata.json okur
metadata = json.load(metadata_json_path)
feature_names = metadata['feature_names']  # PFAZ02 ile ayni liste
target_col = metadata['target']
```

### 5.2 Hedef Kolon Tespiti

_detect_target_cols() metodu, veri kumesinin hedefini metadata veya kolon adiyla tespit eder.

### 5.3 Aykırı Deger Tespiti ve Yeniden Egitim

Her egitim oncesinde IQR + z-skor cift filtresi uygulanir:

```
Adim 1: IQR filtresi (3x)  -->  Q1 - 3*IQR < y < Q3 + 3*IQR
Adim 2: z-skor filtresi    -->  |y - mean(y)| < 3 * std(y)

Kosul A: n_outlier > 0 VE keep_mask >= 0.90 (en az %90 korunuyor)
  -> Aykırı degerler cikarilir, model yeniden egitilir

Kosul B: keep_mask < 0.90 (cok fazla cikarma olacak)
  -> Yalnizca IQR filtresi uygulanir (z-skor devre disi)

Kosul C: Hicbir aykırı deger yok
  -> Dogrudan egitim (filtreleme yok)
```

Bu mekanizma, nukleer veri setindeki nadir outlier cekirdeklerin (orn. cok buyuk deformasyonlu
geciş bolgeleri) egitimi bozmasisini onler; ancak veri seti butunlugunu de korur.

### 5.4 Veri Sizintisi Onlemi

PFAZ 03, PFAZ 02 ile ayni veri sizintisi onlemini uygular.
schmidt_moment, Q0_intrinsic, Beta_2_estimated kolonlari train/val/test'ten cikarilir.
Bu islem PFAZ 01 tarafından zaten gerceklestirildigi icin PFAZ 03'te tekrar yapılmaz.

---

## 6. Gercek Pipeline Ciktilari

### 6.1 Durum (pfaz_status.json, 2026-05-03)

| Alan | Deger |
|------|-------|
| Durum | completed |
| Ilerleme | 100% |
| Aciklama | Onceki tam calisma tamamlandi |

PFAZ 03, onceki calisma turundan basarıyla tamamlanmistir.
Mevcut PFAZ 02 calistirma ile birlikte PFAZ 03 yeniden calistirilacaktir.

### 6.2 Cikti Dizin Yapisi

```
outputs/anfis_models/
  {dataset_name}/                  # ornek: MM_150_S70_Standard_Standard_Random
    {config_id}/                   # CFG001 | CFG002 | ... | CFG008
      model_{config_id}.pkl        # Egitilmis TakagiSugenoANFIS (val_R2>=0.5)
      metrics_{config_id}.json     # R2, MAE, RMSE, n_rules, adaptive_mfs
      completed.json               # Checkpoint

  anfis_training_summary.json      # Tum konfig sonuclari
  anfis_training_summary.xlsx      # Excel raporu
```

### 6.3 metrics_{config_id}.json Icerigi

```json
{
  "config_id": "CFG001",
  "config_name": "Grid_2MF_Gauss",
  "method": "grid", "mf_type": "gaussmf",
  "n_inputs": 3, "n_mfs_requested": 2, "n_mfs_used": 2,
  "n_rules": 8,
  "train_r2": 0.91, "val_r2": 0.87, "test_r2": 0.85,
  "train_mae": 0.31, "val_mae": 0.45,
  "n_iter": 187, "converged": true,
  "outliers_removed": 2, "filter_used": "iqr_zscore",
  "adaptive_mfs_triggered": false
}
```

---## 7. ANFIS ve ML Karsilastirmasi — Tez Icin Onem

PFAZ 03'un varliginin tez acısından iki temel gerekcesi var:

1. **Yorumlanabilirlik:** RF/DNN kara kutu iken ANFIS kural tabanli seffaf bir modeldir.
   'IF A is buyuk AND Z is orta THEN MM = 1.2*A - 0.3*Z + 0.5' gibi okunabilir
   kurallar, nükleer fizik literaturu ile dogrudan karsilastirilabilir.

2. **Fizik Bilgisi Entegrasyonu:** ANFIS'in fuzzy bolum parametreleri, fiziksel sinirlara
   uygun sekilde baslatilabilir. Ornegin, magic number cevresi icin ayri bir uyelik
   fonksiyonu tanimlamak dogal bir yoruma olanak verir.

Bu iki ozelligi nedeniyle ANFIS, derin ogrenme modellerinin yaninda metodolojik
denge ve yorumlanabilirlik amaciyla pipeline'a eklenmistir.

---

## 8. Bilinen Hatalar

| Oncelik | Konum | Davranis | Etki | Duzeltme |
|---------|-------|---------|------|---------|
| DUSUK | anfis_parallel_trainer_v2.py | SubClust KMeans kullanir (gercek subclust degil) | Radii parametresi etkisiz | Gerçek subtractive clustering implement et |
| DUSUK | _init_subclust | KMeans radii bağimsız k hesaplar | CFG006/007/008 cok benzer | k = f(radii, data_range) yap |
| DUSUK | _bell MF | 4. kuvvet (standart 2b degil) | Daha dik kenarlı bell | Dokümantasyon ile acikla |

---

## 9. Sonraki Fazlara Bagimlilik

| Faz | Hangi Ciktiyi Kullanir | Kritik Alan |
|-----|----------------------|-------------|
| PFAZ 06 (Raporlama) | anfis_training_summary.xlsx | Tum konfig metrikleri |
| PFAZ 07 (Ensemble) | PKL modeller (ANFIS dahil) | val_r2 ile siralama |
| PFAZ 08 (Gorsellestirme) | Metrik dosyalari | Karsilastirma grafikleri |
| PFAZ 10 (Tez) | Tum sonuclar | Metodoloji bolumu |

---

## 10. Kontrol Listesi

### Koddan Dogrulanan Parametreler

- [x] TakagiSugenoANFIS: max_iter=300, patience=30, alpha=0.01
- [x] 8 konfigurasyon: CFG001-005 grid, CFG006-008 subclust (anfis_config_manager.py:86-145)
- [x] Adaptif n_mfs: n_rules < max(4, n_train/3) (kod:81-89)
- [x] SubClust Python fallback: KMeans tabanlı (gercek subtractive degil)
- [x] Hibrit ogrenme: LSE (Katman 4) + L-BFGS-B/LBFGS (Katman 1-2)
- [x] R2_MIN_SAVE_THRESHOLD = 0.5 (kod:46)
- [x] Erken durma: val RMSE bazli, patience=30 adim

### Uretilen Ciktilar

- [ ] outputs/anfis_models/{dataset}/{config}/model_*.pkl
- [ ] outputs/anfis_models/anfis_training_summary.json
- [ ] outputs/anfis_models/anfis_training_summary.xlsx

### Ileri Faz Uyumlulugu

- [ ] PFAZ 06: anfis_training_summary.xlsx mevcut mu?
- [ ] PFAZ 07: ANFIS PKL'leri ensemble havuzuna dahil?
- [ ] feature_names metadata uyumu: PFAZ 02 ile ayni mi?

---

---

## 11. Çalışma Zamanı Davranışı — 2026-05-08 Keşifleri

### 11.1 ANFISDatasetSelector — AKTİF (2026-05-08)

`anfis_dataset_selector.py` içindeki `ANFISDatasetSelector` sınıfı PFAZ2 R² sonuçlarına
göre dataset seçimi yapar (Top ≥0.90 / Mid 0.80-0.90 / Low <0.80 katmanları).

**2026-05-08 itibarıyla aktif edildi.** `train_all_anfis_parallel` içinde `discover_datasets()`
hemen sonrasına entegre edildi. Kota: **Top=50, Mid=50, Low=100** (toplam 200/target).

Seçim stratejisi:
- Low kotası yüksek (100) → "ML başarısız → ANFIS dene" hipotezi test ediliyor
- `training_summary.xlsx` (PFAZ2 çıktısı) yoksa → fallback: tüm datasetler kullanılır
- Seçim sonucu `outputs/anfis_models/anfis_dataset_selection/` dizinine kaydedilir

Eğitim öncesi filtre `ANFIS_MAX_INPUTS = 5` (satır 1042) hâlâ geçerliliğini korur.
`TARGET_RECOMMENDED_SETS` içindeki tüm setlerin n_inputs ≤ 5 olduğu doğrulandı.

### 11.2 `configurations` Alanı Okunmuyor

`config.json` ve `config_desktop.json` içindeki `pfaz03_anfis_training.configurations`
listesi kod tarafından **hiç okunmuyor.** Gerçek davranış hardcoded `PILOT_IDS` kümesine dayanır:

```python
# anfis_parallel_trainer_v2.py:1171-1172
PILOT_IDS = {'CFG_Grid_2MF_Trap', 'CFG_Grid_2MF_Bell',
             'CFG_Grid_2MF_Gauss', 'CFG_Grid_2MF_Tri'}
```

3-phase pilot strategy (Wave 1: 4 PILOT config → Wave 2: ADVANCED configs) aktif olduğundan
config dosyasındaki liste yalnızca dokümantasyon amacıyla var. Kod değişikliği gerekmiyor.

### 11.3 Config Adlandırma Katmanları

| Katman | Adlandırma | Örnek |
|--------|------------|-------|
| `anfis_config_manager.py` | kısa isim | `Grid_2MF_Gauss` |
| `anfis_parallel_trainer_v2.py` PILOT_IDS | CFG_ önekli | `CFG_Grid_2MF_Gauss` |
| Çıktı dizini | uzun ID | `CFG001` |

`CFG_` öneki, `get_config_by_name()` lookup'ı için kasıtlı. Tutarsızlık değil, katmanlı yapı.

---

*PFAZ 03 Belgesi v1.2 | 2026-05-08 | Güncelleme: ANFISDatasetSelector AKTİF edildi (Top=50 Mid=50 Low=100), configurations alanı not, ANFIS_MAX_INPUTS keşifleri*