# Faz Değerlendirme Notları
## Her Faz Belgesi Yazılmadan Önce Okunacak Kontrol Şablonu

> **Kullanım:** Yeni bir faz analizine başlamadan ÖNCE bu dosyayı oku.  
> **Amaç:** Aynı gözden kaçırmaları tekrarlamamak. Her başlık bir ders alınan hatayı temsil eder.  
> **Oluşturma:** 2026-05-03 | PFAZ 01 analizinden öğrenilenler

---

## BÖLÜM A: BAŞLAMADAN ÖNCE YAPILACAKLAR

### A1. İlgili Kaynak Dosyaları Oku — Tahmin Etme
Her faz için şu dosyaları OKU, varsayma:

```
1. Ana sınıf dosyası (örn. dataset_generation_pipeline_v2.py)
2. Yardımcı sınıflar (scaling_manager.py, sampling_manager.py, ...)
3. core_modules/constants.py  ← her fazda değişen sabitler burada
4. config.json  ← aktif parametreler burada
5. PFAZ_DEVELOPMENT_NOTES.md  ← en son değişiklikler burada
6. QA_WIRING_REPORT.md  ← neyin bağlı neyin bağlı olmadığı burada
```

### A2. "Aktif" ile "Tanımlı" Arasındaki Farkı Kontrol Et
Her parametre/hedef/metot için şu iki soruyu sor:
- **Tanımlı mı?** (kod veya config'de var)
- **Aktif mi?** (gerçekte çağrılıyor/kullanılıyor)

Örnek tuzak (PFAZ 01'den): 4 hedef tanımlı, 2 aktif.

---

## BÖLÜM B: VERİ SETİ ÜRETİM AĞACI

### B1. Tam Ağaç (PFAZ 01 çıktılarını kullanan tüm fazlar için geçerli)

```
aaa2.txt  (267 çekirdek, 12 ham sütun)
│
├─ DataLoader._clean_data()  [8 adım]
│   ├─ Boş satır kaldır
│   ├─ Tip dönüşümü (Z,N,A:int; MM,Q:float)
│   ├─ Fiziksel sınır: Z>0, N>0, A=Z+N
│   ├─ Hedef NaN → flag (silme)
│   ├─ isomer=1 → dışla
│   ├─ (Z,N) yinelenme → son kayıt tut
│   ├─ |MM|>15 μN veya |Q|>10 barn → uyarı
│   └─ spin=0 & MM≠0 → uyarı
│
├─ TheoreticalCalculationsManager  [7 modül, 44+ yeni sütun]
│   ├─ [1] SEMFCalculator → BE, T_v, T_s, T_c, T_a, δ, BE/A
│   ├─ [2] RadiusCalculator → R_nucl
│   ├─ [3] SeparationEnergy → S_n, S_p
│   ├─ [4] ShellModelFeatures → magic_character, Z_magic_dist, N_magic_dist
│   ├─ [5] DeformationCalc → Beta_2_estimated, Q0_intrinsic, spherical_index
│   ├─ [6] SchmidtCalc → mu_schmidt, Q_schmidt
│   └─ [7] WoodsSaxon/Nilsson → V_ws_center, epsilon_nilsson
│       ⚠ BUG: HBAR_C import hatası → bu modül çalışmıyor (sıfır değerler)
│
├─ QMFilterManager  [hedef bazlı filtre]
│   ├─ MM: MM_exp NaN → dışla | Q=0 hatalı filtreli (Bug 4)
│   └─ QM: Q_exp NaN → dışla | Q=0 HATALı FİLTRELENİYOR (kritik bug)
│
└─ FOR target IN [MM, QM]:           ← 2 aktif hedef
   └─ FOR size IN [75, 100, 150, 200, ALL]:   ← 5 boyut
      │   (ALL ≈ 197 geçerli örnek)
      ├─ SamplingManager.sample(size)
      └─ FOR scenario IN [S70*, S80]:  ← *size≤100 → yalnızca S70
         └─ FOR feat_set IN FEATURE_SETS[target]:
            │   (MM: ~15 set | QM: ~15 set | boyuta göre değişir)
            └─ FOR scaling IN [NoScaling, Standard, Robust, MinMax]:  ← 4 yöntem
               └─ FOR sampling IN [Random, Stratified, StratifiedMagic, StratifiedHybrid]:
                  │
                  ├─ ScalingManager.fit(train).transform(train/val/test)
                  │   ⚠ DİKKAT: Aşağıdaki özellikler ASLA ölçeklenmez:
                  │     A, Z, N, Nn, Np, SPIN, PARITY, magic_character
                  │
                  ├─ SamplingManager.split(scenario)
                  │   S70: %70/%15/%15 | S80: %80/%10/%10
                  │
                  ├─ → train.csv + val.csv + test.csv + metadata.json
                  │
                  └─ IF size IN [150, 200, ALL]:
                     ├─ AnomalyManager (IQR=3.0 + IsolationForest=0.08)
                     └─ → ..._NoAnomaly varyantı
```

### B2. Dataset Adlandırma Şeması
```
{HEDEF}_{BOYUT}_{SENARYO}_{ÖZELLIK_SET}_{ÖLÇEKLEME}_{ÖRNEKLEME}[_NoAnomaly]
```
Örnekler:
- `MM_ALL_S70_AZSMC_Standard_StratifiedHybrid`
- `QM_150_S80_ZB2EMC_Robust_StratifiedMagic_NoAnomaly`
- `MM_75_S70_AZN_NoScaling_Random`

---

## BÖLÜM C: ÖLÇEKLENDİRME — TAM BELGE

### C1. 4 Ölçekleme Yöntemi (scaling_manager.py'den)

| Yöntem | Formül | Ne zaman tercih? |
|--------|--------|-----------------|
| **NoScaling** | $x' = x$ | Tree modeller (RF, GBM, XGBoost) için |
| **Standard** | $x' = (x - \mu) / \sigma$ | Normal dağılım varsayımı, DNN/BNN için |
| **Robust** | $x' = (x - median) / IQR$ | Aykırı değer varlığında, kabuk kapanması çekirdekleri için |
| **MinMax** | $x' = (x - x_{min}) / (x_{max} - x_{min})$ | Sınırları anlamlı özellikler (β₂ ∈ [-0.6, 0.6]) için |

### C2. Asla Ölçeklenmeyen Özellikler (DISCRETE_FEATURES)
```python
['NUCLEUS', 'A', 'Z', 'N', 'Nn', 'Np',
 'SPIN', 'PARITY', 'magic_character',
 'magic_n', 'magic_p', 'magic_np']
```
**Neden?** Bu özellikler kategorik veya ayrık sayısal — ölçekleme anlamsız veya zararlı.  
`magic_character = 0.5` fiziksel olarak anlamsızdır.

### C3. Uygulama Sırası
```
TRAIN → Scaler.fit(train) → Scaler.transform(train) → train_scaled.csv
VAL   → Scaler.transform(val)  (FIT YOK, sadece transform)
TEST  → Scaler.transform(test) (FIT YOK, sadece transform)
```
**Kritik:** Scaler parametreleri (mean, std / median, IQR / min, max) yalnızca train setinden hesaplanır.  
Val ve test verileri bu parametrelerle dönüştürülür — fit edilmez.  
Bu, veri sızıntısını (data leakage) önler.

### C4. Metadata Kaydı
Her dataset için `scaler_metadata.json`:
```json
{
  "method": "Standard",
  "features_scaled": ["BE_total", "S_n_approx", ...],
  "features_excluded": ["A", "Z", "N", "SPIN", "PARITY", "magic_character", ...],
  "scaler_params": {"mean": [...], "std": [...]}
}
```

---

## BÖLÜM D: ÖZELLİK KISALTMALARl REFERANS TABLOSU

### D1. Tam Kısaltma Haritası (feature_combination_manager.py:FEATURE_ABBREV)

| Kısaltma | Gerçek Sütun | Açıklama |
|---------|-------------|---------|
| A | A | Kütle numarası |
| Z | Z | Proton sayısı |
| N | N | Nötron sayısı |
| S | SPIN | Nükleer spin J |
| PAR | PARITY | Parite (+1/-1) |
| MC | magic_character | Kabuk büyüsü skoru (0-1) |
| BEPA | BE_per_A | Nükleon başına bağlanma enerjisi |
| B2E | Beta_2_estimated | Tahmini kuadrupol deformasyon |
| ZMD | Z_magic_dist | Z'nin en yakın sihirli sayıya uzaklığı |
| NMD | N_magic_dist | N'nin en yakın sihirli sayıya uzaklığı |
| BEA | BE_asymmetry | Asimetri bağlanma enerjisi |
| ZV | Z_valence | Valens proton sayısı |
| NV | N_valence | Valens nötron sayısı |
| ZSG | Z_shell_gap | Proton kabuk açıklık enerjisi (MeV) |
| NSG | N_shell_gap | Nötron kabuk açıklık enerjisi (MeV) |
| BEP | BE_pairing | Çiftlenme enerjisi |
| SPHI | spherical_index | Küresellik indeksi (0-1) |
| CP | Q0_intrinsic | Kolektif/özüntrinsik kuadrupol |
| PF | P_FACTOR | P-faktör (parite faktörü) |
| BET | BE_total | Toplam bağlanma enerjisi |
| SN | S_n_approx | Nötron ayrılma enerjisi (yaklaşık) |
| SP | S_p_approx | Proton ayrılma enerjisi (yaklaşık) |
| NN | Nn | Valens nötron sayısı (aaa2.txt ham sütun) |
| NP | Np | Valens proton sayısı (aaa2.txt ham sütun) |

### D2. SHAP Önem Sıralamaları (feature_combination_manager.py:40-47)

**MM (Manyetik Moment):**
```
A(19.2%) > Z(17.5%) > S(12.8%) > MC(9.7%) > BEPA(8.3%) >
B2E(7.1%) > ZMD(5.4%) > N(4.9%) > BEP(4.2%) > NMD(3.1%) >
ZSG(2.7%) > SPHI(2.4%) > PAR(2.1%) > PF(1.8%)
```

**QM (Kuadrupol Moment):**
```
Z(21.5%) > B2E(18.3%) > A(15.7%) > MC(10.2%) > S(8.9%) >
BEA(6.4%) > ZV(5.1%) > NV(4.8%) > SPHI(4.3%) > CP(3.7%) >
ZMD(3.2%) > N(2.9%) > PAR(2.3%) > BEPA(2.1%)
```

**Beta_2 (Deformasyon):**
```
MC(22.1%) > ZMD(18.7%) > NMD(17.3%) > A(12.9%) > ZV(8.4%) >
NV(7.8%) > BEA(5.6%) > Z(3.9%) > N(3.4%) > CP(2.8%) >
S(2.3%) > BEPA(1.9%)
```

**Yorumlama:**
- MM için spin (S) üçüncü en önemli → tek-nükleon momentin spinle doğrudan bağlantısı
- QM için B2E (Beta_2_estimated) ikinci en önemli → deformasyon QM'yi doğrudan belirler
- Her iki hedef için MC (magic_character) ilk 4'te → kabuk kapanmasının kritik rolü
- Beta_2 için MC birinci sırada → deformasyonun kabuk yapısıyla bağı

### D3. Özellik Seti Kategorileri

| Kategori | Girdi Sayısı | ANFIS | Örnek Setler |
|----------|------------|-------|-------------|
| Common_3in | 3 | Evet (27 kural) | AZN, AZS, AZMC, AZBEPA, AZB2E |
| Common_4in | 4 | Evet (81 kural) | AZNS |
| MM_3in | 3 | Evet (27 kural) | ASMC, AMCBEPA |
| MM_4in | 4 | Evet (81 kural) | AZSMC, AZSBEPA, AZMCBEPA, AZSB2E |
| MM_5in | 5 | Evet (32 kural/2MF) | AZSMCBEPA, AZSMCB2E |
| QM_3in | 3 | Evet (27 kural) | ZB2EMC, B2EMCBEA |
| QM_4in | 4 | Evet (81 kural) | AZB2EMC, ZB2EMCS, AZB2EBEA |
| QM_5in | 5 | Evet (32 kural/2MF) | AZB2EMCS, AZB2EMCBEA |
| Beta2_* | 2-5 | Kısmi | MCZMNM, AZVNV, ... |
| NnNp_* | 3-5 | Kısmi | NNPMC, AZNNP, ... |

---

## BÖLÜM E: ÖRNEKLEMELERİN TAM LİSTESİ

### E1. 4 Örnekleme Yöntemi (sampling_manager.py'den)

| Yöntem | Mantık | Ne zaman kullan? |
|--------|--------|-----------------|
| **Random** | Basit rastgele örnekleme (seed=42) | Baseline; hızlı karşılaştırma |
| **Stratified** | A değerine göre kütle grubu stratifikasyonu | Kütle bölgesi dengeli dağılım için |
| **StratifiedMagic** | Test setinin %X'i sihirli çekirdeklerden | Kabuk kapanmasındaki model performansı için |
| **StratifiedHybrid** | A grubu + sihirli karakter birlikte | En dengeli, her iki yapıyı da temsil eder |

### E2. A Kütle Grupları (Stratified için)
```
light:        A < 40
medium_light: 40 ≤ A < 90
medium:       90 ≤ A < 140
medium_heavy: 140 ≤ A < 200
heavy:        200 ≤ A < 300
```
(constants.py:MASS_GROUPS'tan)

---

## BÖLÜM F: ANOMALİ TESPİT — TAM BELGE

| Parametre | Değer | Kaynak |
|-----------|-------|--------|
| IQR eşiği | 3.0 | constants.py:ANOMALY_THRESHOLDS['z_score']=3.5 (not: pipeline 3.0 kullanır) |
| IF contamination | 0.08 | constants.py:ANOMALY_THRESHOLDS['isolation_forest_contamination'] |
| İzotop zincirine sıçrama eşiği MM | 0.5 μN | constants.py:ANOMALY_THRESHOLDS['mm_jump'] |
| İzotop zincirine sıçrama eşiği QM | 0.3 barn | constants.py:ANOMALY_THRESHOLDS['q_jump'] |

**NoAnomaly koşulu:** Yalnızca size ∈ {150, 200, ALL} için üretilir.  
Boyut 75 ve 100'de zaten az veri var — anomali kaldırmak çok veri kaybettirir.

---

## BÖLÜM G: I/O KONFİGÜRASYONLARI

### G1. Tam Girdi/Çıktı Tablosu (io_config_manager.py'den)

| Konfigürasyon | Girdi | Çıktı | ANFIS | Kural (2MF) | Kural (3MF) |
|-------------|-------|-------|-------|------------|------------|
| 2In1Out | 2 | 1 | Evet | 4 | 9 |
| 3In1Out | 3 | 1 | Evet | 8 | 27 |
| 3In2Out | 3 | 2 (MM+QM) | Evet | 8 | 27 |
| 4In1Out | 4 | 1 | Evet | 16 | 81 |
| 5InAdv | 5-10 | 1 | **Hayır** (çok kural) | — | — |
| 10InAdv | 10-20 | 1 | **Hayır** | — | — |
| 20InAdv | 20-44 | 1 | **Hayır** | — | — |

---

## BÖLÜM H: BAĞIMLILIK ZİNCİRİ (Sonraki Fazlara Bağlantı)

### H1. metadata.json — Kritik Alanlar
```json
{
  "dataset_name": "...",
  "target": "MM",
  "feature_names": ["A", "Z", "S", "MC", ...],   ← PFAZ 02/09 bu listeyi okur
  "n_features": 4,                                 ← I/O konfigürasyonunu belirler
  "io_config": "4In1Out",                          ← PFAZ 03 ANFIS uygunluğunu kontrol eder
  "scaling_method": "Standard",                    ← PFAZ 04 inverse transform için kullanır
  "scaler_metadata_path": "..."                    ← Scaler parametreleri
}
```

### H2. Hangi Faz Neye Bağımlı
| Faz | metadata.json'dan | Kritik alan |
|-----|------------------|------------|
| PFAZ 02 | Evet | feature_names, n_features, target |
| PFAZ 03 | Evet | io_config (anfis_feasible=True için yalnızca 2In1Out-4In1Out) |
| PFAZ 04 | Evet | scaler_metadata_path (tahmin için inverse transform) |
| PFAZ 05 | Evet | dataset_name, model paketleri |
| PFAZ 09 | Evet | feature_names (Monte Carlo için doğru özellik seti) |

---

## BÖLÜM I: HATA AYIKLAMA KONTROL LİSTESİ

Program beklenmedik davranış gösteriyorsa kontrol sırası:

1. `pfaz_status.json` — hangi fazın hangi durumda olduğu
2. `logs/main_*.log` — son çalıştırmanın hata mesajları  
3. `outputs/pipeline_warnings.json` — birikmiş uyarılar
4. `QA_WIRING_REPORT.md` — hangi modülün bağlı olduğu
5. `PFAZ_DEVELOPMENT_NOTES.md` — son değişiklikler

---

*Faz Değerlendirme Notları v1.0 | 2026-05-03*  
*Güncelleme: Her faz analizinden sonra*


---

## BOLUM J: PFAZ 02 — ML Modelleri Hizli Referans

### J1. 6 Aktif Model ve Konfigurasyon Sayisi

| Model | Konfig | ID Aralik | Min Ornek | Ic Scaler | Ozel Kural |
|-------|--------|-----------|-----------|-----------|-----------|
| RF | 20 | RF_001-020 | 30 | Hayir | -- |
| XGBoost | 15 | XGB_021-035 | 30 | Hayir | -- |
| LightGBM | 1 (def.) | LGB_default | 30 | Hayir | -- |
| CatBoost | 1 (def.) | CAT_default | 30 | Hayir | -- |
| SVR | 1 (def.) | SVR_default | 30 | Evet (SS) | RBF C=10 |
| DNN | 15 | DNN_036-050 | 200 (is uretimi) | Evet (SS) | use_advanced_models=True |

### J2. Kritik Sabitleri

```
R2_MIN_SAVE_THRESHOLD = 0.5        # val_R2 < 0.5 -> PKL kaydedilmez
DNN divergence esigi: val_R2 < -2.0 -> DIVERGED
seed = 42 (sabit, parallel_ai_trainer.py:1363)
5-fold CV: n_jobs=1 (paralel mod aktifse deadlock onlemi)
```

### J3. Veri Sizintisi Onlemi (her fazda gecerli)

```
Cikarilan kolonlar: schmidt_moment, Q0_intrinsic, Beta_2_estimated
```

### J4. Overfitting Sinif Sistemi

| Sinif | Gap Aralik | Karar |
|------|-----------|-------|
| none | < 5% | Saglikli |
| mild | 5-10% | Kabul edilebilir |
| moderate | 10-20% | Izle |
| severe | 20-40% | Regularizasyon gerekli |
| extreme | >= 40% | Kullanilmamali |

---

## BOLUM K: PFAZ 03 — ANFIS Hizli Referans

### K1. 8 Konfigurasyon Ozeti

| CFG | Yontem | n_MF | MF Turu | Kural (3 giris) |
|-----|--------|------|---------|----------------|
| CFG001 | Grid | 2 | Gaussian | 8 |
| CFG002 | Grid | 2 | Bell (4. kuvvet) | 8 |
| CFG003 | Grid | 2 | Ucgen | 8 |
| CFG004 | Grid | 2 | Yamuk | 8 |
| CFG005 | Grid | 3 | Gaussian | 27 (adaptif olabilir) |
| CFG006 | SubClust | K-Means | Gaussian | radii=0.3 |
| CFG007 | SubClust | K-Means | Gaussian | radii=0.5 |
| CFG008 | SubClust | K-Means | Gaussian | radii=0.7 |

### K2. Adaptif n_mfs Formulu

```python
for mfs in range(requested_mfs, 1, -1):
    if mfs**n_inputs < max(4, n_train/3):
        return mfs   # Kural basi min 3 egitim ornegi
return 2             # Mutlak minimum
```

### K3. Hibrit Ogrenme Ozeti

```
Katman 4 (ardisil): LSE ridge -- kapalı form, alpha=0.01
Katman 1-2 (one): L-BFGS-B (CPU) veya LBFGS (GPU, opsiyonel)
max_iter=300, patience=30
```

### K4. SubClust Uyarisi

SubClust Python = KMeans (gercek subtractive clustering degil).
Radii, KMeans k'yi dogrudan etkilemez: k = min(n_rules, max(2, n_train//4))

---

## BOLUM L: PFAZ 04 — Bilinmeyen Cekirdek Tahmin Hizli Referans

### L1. Temel Formüller

```
Degradasyon = Val_R2 - Test_R2          (genelleme kaybi; yuksek = kotu)
GS = (Test_R2 / Val_R2) * 100           (genelleme puani; yuksek = iyi)
Consensus = mean(top-25 model tahminleri)
```

### L2. val_r2 Okuma Yapisi

```python
# metrics_{config_id}.json ic sozluk yapisi
val_r2 = m.get('val', {}).get('r2')    # DIKKAT: ic-ic sozluk
```

### L3. 7-Sayfali Excel Yapisi

| Sayfa | Icerik |
|-------|--------|
| All_Results | Tum model-dataset sonuclari |
| Best_Per_Dataset | Dataset x Target x Category bazinda en iyi |
| Degradation_Analysis | Genelleme kayiplari sirali |
| AI_vs_ANFIS | Karsilastirma |
| Pivot_By_Target | Hedef bazinda ozet |
| Pivot_By_ModelType | Model tipi bazinda ozet |
| Per_Nucleus_Predictions | Cekirdek bazinda y_true/y_pred/hata |

### L4. SingleNucleusPredictor — Minimum Giris

```
Yalnizca Z ve N yeterli. TheoreticalCalculationsManager ile 44+ ozellik turetilir.
5 giris formati: dict, .txt, aaa2.txt, .csv, .xlsx
ALL_TARGETS = ['MM', 'QM']
```

---

## BOLUM M: HER FAZ ICIN CIKTI INCELEME ZORUNLULUGU

Her faz belgesi bitmeden once su uclu kontrol zorunludur:

### M1. Durum Dogrulama

```
pfaz_status.json -> Status: completed/running/failed/pending?
Ilerleme yuzdesi?
```

### M2. Cikti Klasoru Inceleme

```
outputs/{faz_ciktisi}/ klasoru var mi?
Kac dosya var? Boyutlari mantikli mi?
PKL sayisi beklenen ile uyumlu mu?
```

### M3. Metrik Degerler

```
En iyi R2 degeri?
Ortalama R2 degeri?
Basan model orani?
```

Bu uc kontrol olmadan "Gercek Pipeline Ciktilari" bolumu YAZILAMAZ.

---

*Faz Degerlendirme Notlari v2.0 | 2026-05-03*
*Guncelleme: PFAZ 02/03/04 analizinden BOLUM J-M eklendi*


---

## PFAZ 05 Degerlendirme Notu (2026-05-04)

### Hata: pfaz_status.json 'completed' Yaniltici

PFAZ 05 icin pfaz_status.json 'completed=100%' gosteriyor ancak bu 'kod hazir' anlamina geliyor, 'pipeline calisti' degil. Gercek cikti dosyalari mevcut degil.

**Ders:** pfaz_status.json'un 'completed' etiketi her faz icin ayni anlama gelmiyor. PFAZ 01-04 gercekten calisti ve cikti uretti. PFAZ 05 ise kod tamamligi isareti.
Her fazda hem status.json HEM de outputs/ dizininin varligini kontrol etmek gerekiyor.

**Kural Guncelleme (KURAL 9 eki):**
pfaz_status.json 'completed' goruldugunde sadece status degil, fiziksel cikti dosyalarini da kontrol et. outputs/{faz_dizini}/ bos veya mevcut degilse faz 'bekleniyor' olarak isle.

### Bulunan Ilgili Cikti

ensemble_results/evaluation/comprehensive_report.json mevcut (PFAZ 07 Ensemble ciktisi):
- stacking_mlp R2: 0.9794 (en iyi)
- Ortalama R2: 0.9616
- 12 ensemble yontemi


---

## KURAL 16: Excel Icerigi = Kod Okuma (2026-05-04)

Faz belgesi yazarken cikti dosyalarinin ICERIGI de belgede yer almali:

- Her Excel sayfasi icin: baslik, sutun isimleri, satir sayisi, bicimleme ve NEDEN VAR sorusunun yaniti
- Gercek cikti yoksa: uretim kodundaki save_excel_report() / generate_excel_report() metodunu oku
- Sutun isimlerini varsayimla yazma -- kodu oku: Model_Type degil 'model_type' olabilir
- PKL_Saved, Status_Note gibi teknik sutunlar tez okuyucusu icin aciklanmali

**Uygulama:** Faz belgesi Bolum 4 (Girdi/Cikti) altinda Excel sayfalarini ayrintili tabloya donu.


---

## KURAL 17: Her Faz Sonrasinda Guncellenmesi Zorunlu 7 Belge (2026-05-04)

**Kural:** Her faz belge yazimi BITMEDEN asagidaki 7 dokuman guncellenmeden 'tamamlandi' denemez.
Bu kural her oturumda, her seferinde, istisnasiz uygulanir.

### 7 Zorunlu Guncelleme

| # | Dosya | Ne Eklenir |
|---|-------|------------|
| 1 | `pipeline-hatalari.md` | Yeni bulunan bug'lar (ID, oncelik, aciklama, fix) |
| 2 | `06-FIGURE-TABLE-CATALOG.md` | Yeni F-NNN (sekil), T-NNN (tablo), A-NNN (algoritma), S-NNN (sema) |
| 3 | `07-GLOSSARY-SYMBOLS.md` | Yeni kisaltmalar ve semboller |
| 4 | `faz-degerlendirme-notlari.md` | Bu dosyaya yeni ders/kural eklenir |
| 5 | `tez-yazim-not-defteri.md` | Tez icin anahtar argumanlar, acik sorular |
| 6 | `memory/project_context.md` | Teknik detaylar (siniflar, sabitler, Excel yapisi) |
| 7 | `memory/pipeline_bugs.md` | Bug sayisi ve yeni bug kayitlari |

### Neden Bu Kural Gerekli?

PFAZ 05 ve PFAZ 06 sonrasinda kullanici bu 7 belgeyi guncellememem nedeniyle iki kez
uyari vermek zorunda kaldi: "her seferinde her seferinde yaziyorum."
Bu kural o sorunu kokunden cozmelidir.

### Kontrol Mekanizmasi

Faz belgesi yazildiktan sonra, PFAZ'e gecmeden once bu 7 maddeyi tikle:
- [ ] pipeline-hatalari.md guncellendi
- [ ] 06-FIGURE-TABLE-CATALOG.md guncellendi
- [ ] 07-GLOSSARY-SYMBOLS.md guncellendi
- [ ] faz-degerlendirme-notlari.md guncellendi
- [ ] tez-yazim-not-defteri.md guncellendi
- [ ] memory/project_context.md guncellendi
- [ ] memory/pipeline_bugs.md guncellendi

---

## PFAZ 06 Degerlendirme Notu (2026-05-04)

### Pipeline Sira Surprizi

PFAZ 06, calisma sirasinda 6. degil 9. siradadir.
Gercek sira: [1, 2, 3, 4, 5, 7, 9, 12, 13, 6, 8, 10].
PFAZ 06 PFAZ 07/09/12/13'ten SONRA calisiyor.
Bu tasarim intentional: tum alt analizler bitmeden entegre rapor uretilemiyor.

**Ders:** Faz numarasi != calisma sirasi. Her faz belgesi icin pipeline_v2.py:PIPELINE_EXECUTION_ORDER kontrol et.

### PFAZ 12/13 Etkisi

PFAZ 12 (Istatistiksel Test) ve PFAZ 13 (AutoML) FAILED.
Sonuc: PFAZ 06 Excel'inde Band_Analizi ve AutoML_Karsilastirma sayfalari bos uretiliyor.
Bu, tezin istatistiksel guven bolumunu dogrudan etkiliyor.

**Ders:** Upstream faz basarisizliklari downstream ciktilari sessizce bos birakabilir.
Faz belgesi yazarken upstream bagimliliklarin durumunu pfaz_status.json'dan kontrol et.


---

## PFAZ 07 Degerlendirme Notu (2026-05-04)

### comprehensive_report.json -- Tek Hedef Sorusu

ensemble_results/evaluation/comprehensive_report.json mevcut ve 12 ensemble yontemi var.
Ancak JSON'da hangi hedefin (MM mi, QM mi, ikisi birden mi) sonuclari oldugu net degil.
Dosya timestamp 2026-04-02 -- PFAZ 02 tam tamamlanmadan uretilmis olabilir.

**Ders:** Gercek ensemble sonucu final PFAZ 02 tamamlandiktan sonra yeniden uretilmeli.
Mevcut R2=0.9794 gecici deger olarak tezde kullanilabilir ama final sonuc guncellenmeli.

### AdaBoost Anomali

R2=0.8282 ile en zayif sonuc 100 estimatorlu AdaBoost'tan geliyor. Bu tutarsizlik
kucuk orneklemde boosting'in aykiri cekirdeklere odaklanmasini destekler.


---

## PFAZ 08 Degerlendirme Notu (2026-05-04)

### Gercek Cikti Yok -- Ancak Farkli Neden

PFAZ 05 ve 06 gibi 'kod hazir ama cikti yok' kategorisinde.
Fark: PFAZ 08 ciktisi dinamik -- PFAZ06 Excel ve PFAZ09 CSV verisi olmadan calistirilamiyor.
Bu bir beklenti yonetimi sorunu, bug degil.

**Ders:** Bazı fazlar upstream veriyi bekliyor. pfaz_status.json 'completed' ama
cikti uretmek icin upstream bağımlılıkların da tamamlanmış olması gerekiyor.
PFAZ 02 bitince -> PFAZ 06 guncellenmesi -> PFAZ 08 calistirilmasi zinciri kurulmali.


---

## KURAL 18: VISUALIZATIONS_INDEX.md -- Yetkili Referans (2026-05-04)

PFAZ 08 belgesi ilk yaziminda VISUALIZATIONS_INDEX.md okunmadi.
Sonuclar: yanlis dizin yapisi, eksik grafik ID'leri (S70..S94), yanlis renk kodlari.

**Kural:** Her faz icin repo kokunde ilgili INDEX veya README dosyalari var mi kontrol et.
VISUALIZATIONS_INDEX.md, PFAZ_DEVELOPMENT_NOTES.md, PIPELINE_STATUS_REPORT.md,
QA_WIRING_REPORT.md -- bunlar kaynak koddan daha guncei olabilir.

**Kontrol Listesi Eki:**
Faz analizi baslamadan once: kaynak kod + pfaz_status.json + outputs/ + INDEX/README dosyalari.


---

## PFAZ 09: Monte Carlo Belirsizlik Analizi -- Degerlendirme Notu

**Analiz Tarihi:** 2026-05-04
**Kaynak Kod:** 5 dosya, 3505 satir (aaa2_control_group_complete_v4.py: 1046 + monte_carlo_simulation_system.py: 1259 + 3 yardimci dosya)
**Gercek Cikti:** Mevcut degil (PFAZ02 bekliyor)

### Guclu Yonler

1. **Iki Katmanli Mimari Akilli:** Katman 1 (Top-50, hizli ensemble CI) + Katman 2 (Top-10, 5 farkli MC teknigi) -- pratiklik ile derinligi dengeliyor.

2. **Per-Model Feature Set Tasarimi:** Her model kendi metadata.json'undaki ozellik setiyle tahmin yapiyor. Farkli dataset kombinasyonlarindan egitilen modellerin tahminlerini dogru birlestirebiliyor.

3. **Percentile CI Dogru Secim:** Normal dagilim varsayimi olmayan yuzdelik dilim CI, kucuk asimetrik veri setleri icin Bootstrap'tan daha saglam.

4. **5 Farkli Belirsizlik Kaynagi:** MCD (epiemik/model), Bootstrap (tahmin degiskenligi), Noise (giris duyarlilik), FeatureDrop (ozellik onem), EnsembleUncertainty (model anlasmamasi) -- cok boyutlu belirsizlik anatomisi.

### Zayif Yonler

1. **n_bootstrap=100 yetersiz:** Literatur standardi 1000+. CI bantlari guvenilir degil.
2. **Feature uyumsuzlugu sessiz:** Kac model atlandigi bilinmiyor -- Top-50 iddiasi sahte olabilir.
3. **MC Dropout DNN-only:** En ilginc Bayesci yaklasim yalnizca DNN icin gecerli.
4. **WS bug PFAZ09'u etkilyor:** BUG-02 zinciri.
5. **PFAZ12 FAILED:** 11 analiz sayfasi bos.

### Tespit Edilen Buglar

7 yeni bug (BUG-24..BUG-30) pipeline-hatalari.md'ye eklendi:
- BUG-24 [ORTA]: Bootstrap n=100 kucuk
- BUG-25 [ORTA]: Sessiz model atlama
- BUG-26 [DUSUK]: MC Dropout DNN-only
- BUG-27 [ORTA]: WS bug PFAZ09 turev etkisi
- BUG-28 [DUSUK]: Analysis_5..15 PFAZ12 bagimlisi
- BUG-29 [DUSUK]: n_jobs=8 hardcoded
- BUG-30 [DUSUK]: consensus_threshold target-specific degil

### Tez Acisi

PFAZ09, tezdeki en onemli metodolojik katkilardan birini saglayabilir: multi-source uncertainty
quantification. Ancak n_bootstrap=100 ve feature atlama sorunu giderilmeden CI guvenilir degil.
BUG-02 fix edilmeden WS ozellikleri dahil modellerin CI'si kirli kalir.

**Yeniden Calistirilma Onceligi:** PFAZ02 bittikten sonra + BUG-24 fix (n_bootstrap=1000) ile birlikte.


---

## PFAZ 12: Ileri Istatistiksel Analitik -- Degerlendirme Notu

**Analiz Tarihi:** 2026-05-04
**Durum:** FAILED (progress=0) -- import hatasi muhtemel
**Kod:** 7 dosya, 4370 satir; 6 sinif

### Guclu Yonler
1. Kapsamli test portfoyu: parametrik + parametrik-olmayan + Bayesci
2. NuclearPatternAnalyzer: izotop/izoton/izobar sicrama analizi -- teze eşsiz katki
3. Sobol analizi: ozellik duyarliligini varyans bazli olciyor
4. n=5000 bootstrap: CI'lar istatistiksel acidan saglam

### Zayif Yonler
1. NuclearBandAnalyzer __init__ export eksik (BUG-31) -- band analizi calısmıyor
2. Progress=0 -- hata kaynagi belirsiz
3. PFAZ12 basarisizligi: PFAZ06, PFAZ09, PFAZ08'i dogrudan etkiliyor

### Tespit Edilen Buglar
- BUG-31 [ORTA]: NuclearBandAnalyzer __init__ export eksik
- BUG-36 [BILGI]: PFAZ12 baslangic hatasi belirsiz

### Tez Acisi
PFAZ 12 calistirilabilirse tez istatistik bolumu cok daha guclu olur. BUG-31 fix: 3 satir kod. Baslatma hatasi: PFAZ12 isolation test gerekiyor.

---

## PFAZ 13: AutoML Yeniden Egitim -- Degerlendirme Notu

**Analiz Tarihi:** 2026-05-04
**Durum:** FAILED (progress=0) -- automl_retraining_loop.py:43 IndentationError
**Kod:** 9 dosya (+ __init__), ~5968 satir

### Guclu Yonler
1. Kategori bazli yeniden egitim stratejisi akilli: Poor->Medium->Good
2. Optuna TPE: Bayesian optimizasyon; 30 trialde makul sonuc
3. 7 model turu arama uzayi: RF, XGBoost, GBM, LGB, CatBoost, SVR, DNN -- kapsamli
4. ANFIS ve ozellik muhendisligi entegrasyonu (opsiyonel)

### Zayif Yonler
1. BUG-32 [KRITIK]: Tek satirlik SyntaxError tum modulu cokurtuyor
2. n_trials=30 kucuk (DNN icin ozellikle)
3. model_types default listesinde CB/SVR eksik
4. r2_threshold vs POOR_MAX dokumantasyon tutarsizligi

### Tespit Edilen Buglar
- BUG-32 [KRITIK]: IndentationError -- 1 satir silmekle duzeltilir
- BUG-33 [DUSUK]: n_trials=30 kucuk
- BUG-34 [DUSUK]: CB/SVR default eksik
- BUG-35 [BILGI]: r2_threshold dokumantasyon tutarsizligi

### Kritik Fix Plani
BUG-32 fix (5 dakika) -> PFAZ01-02 tamamlaninca PFAZ13 calistir -> n_trials=100 ile yeniden optimize et

---

## PFAZ 10: Tez Derleme (LaTeX Entegrasyonu) -- Degerlendirme Notu

**Tarih:** 2026-05-04
**Durum:** RUNNING (progress=50) -- kismi tamamlanma
**Kod Kalitesi:** YUksek (MasterThesisIntegration v5.0.0; try/except sarili modüller; fallback dizin cozumleme)

### Guclu Yonler

1. **Tam otomasyon**: Tum 13 fazdan veri toplayip LaTeX'e donusturen kapsamli pipeline
2. **Esnek mimari**: compile_pdf=False varsayilan -- pdflatex olmadan calisiyor
3. **PFAZ12+13 entegrasyonu**: v5.0.0 ile istatistiksel testler ve AutoML icin ozel bolumler (11+12) mevcut
4. **Booktabs LaTeX**: Excel tablolaini otomatik booktabs-style LaTeX'e donusturuyor
5. **Sembol + kisaltma listeleri**: Nukleer fizik, ML ve ANFIS icin kapsamli listeler hazir

### Zayif Yonler / Sinirlar

1. **progress=50**: Kismen calistı; hangi adimda durduğu belli degil
2. **PFAZ12+13 FAILED**: Bolum 11/12 placeholder kalabilir (BUG-31+32 sebebiyle)
3. **MC K=1000 tutarsizligi**: Tez metni ile kod uyumsuz (BUG-38); okuyucuyu yaniltir
4. **Metadata placeholder**: author/supervisor/university doldurulmamis
5. **ThesisOrchestrator (v2.0)**: Hardcoded Linux yolu; eski kod ancak hala yukleniyor (BUG-37)

### Tespit Edilen Buglar

- BUG-37 [DUSUK]: ThesisOrchestrator Linux yolu `/mnt/project` hardcoded
- BUG-38 [BILGI]: MC K=1000 tez/kod tutarsizligi

### Tez Acisinan Sonuc

PFAZ 10 altyapi olarak saglam: tum bolumler yazilmis, LaTeX yapisi olusmus. Ancak:
- BUG-32 (PFAZ13) ve BUG-31 (PFAZ12) duzeltilmeden Bolum 11/12 bos kalir
- Metadata guncellenmeli (yazar, danismanv universite)
- K=1000 vs n=100 tutarsizligi tez tesliminden once cozulmeli

---

## KURAL 19: Sprint Fix Kaydini Belgele (2026-05-04)

Her bug-fix sprint sonrasinda faz-degerlendirme-notlari.md'ye ekle:
- Hangi buglar duzeltildi
- Hangi fixler yeniden egitim gerektiriyor
- Hangi buglar "gecersiz" ilan edildi ve neden

Bu kural KURAL 17'nin uygulama uslubudur: 7 zorunlu belge guncellemesi sprint bazli yapilmalidir.

## Sprint 2026-05-04: Bug Fix Ozeti

**Toplam duzeltme:** 13 kod degisikligi, 10 dosyada.
**Gecersiz ilan:** 4 bug (BUG-01, 04, 12, 16 -- tasarim kararlari veya aktif degil).

**Yeniden egitim gerektiren fixler:**
- BUG-02 (HBAR_C) + BUG-03 (WS spin-orbit) -> PFAZ01 + PFAZ02 yeniden calistirma gerekli.
- Mevcut calisma WS features = 0/NaN ile devam ediyor; fix sonraki iterasyon icin.

**Hemen etkili fixler (yeniden egitim gerektirmez):**
- BUG-06: config.json model listesi duzeldi -> tez metodoloji bolumunde dogru model isimleri
- BUG-10/11: PFAZ04 degradasyon + GS hesabi duzeldi -> PFAZ04 yeniden calistir
- BUG-31: PFAZ12 NuclearBandAnalyzer export duzeldi -> PFAZ12 yeniden calistir
- BUG-32: PFAZ13 IndentationError duzeldi -> PFAZ13 yeniden calistir
- BUG-34: PFAZ13 model_types default duzeldi -> CB+SVR artik AutoML kapsaminada
- BUG-37: PFAZ10 project_dir='.' -> Windows'ta dogru calisir

**BNN/PINN Karari (BUG-06 kapsaminda):**
BNN ve PINN config'den cikarildi -- gercek aktif modeller artik dogru dokumante.
Bu modellerin eklenmesi PFAZ02 yeniden baslatma gerektirir ve kullanilinin kararina birakildi.

*Faz Degerlendirme Notlari v2.1 | 2026-05-04 | Sprint ozeti + KURAL 19 eklendi*

---

## BOLUM N: Log Analizi ve Sprint 2026-05-07/08 Bulgulari

**Tarih:** 2026-05-08
**Kaynak:** `old logs/main_20260430_184414.log.*` (eski PC, ~70 MB, ~6.5 milyon satir, ~7 gunluk calisma)
**Rapor:** `reports/old-log-analysis-2026-05-07.md`

### N1. Kritik Sayisal Bulgular

| Metrik | Deger |
|--------|-------|
| Toplam is | 446,400 (model egitim turu) |
| Tamamlanan | 241,890 / %54.2 |
| Tahmini toplam sure (eski PC) | ~12.7 gun (PFAZ2 tek basina) |
| En iyi config | QM_100_S70_B2EMCBEA_NoScaling_Stratified + XGBoost → val R2=0.84 |
| En kotu scaling | Robust — QM icin sistematik basarisizlik (R2<0) |

### N2. En Iyi Konfigurasyonlar (Log'dan)

Genel kural: **XGBoost > RF >= DNN** (nukleer moment tahmini icin)

- QM hedefinde en iyi: `B2EMCBEA` feature seti + NoScaling + Stratified sampling
- MM hedefinde: AZSMC feature seti + Standard scaling
- Feature set secimi target-bazli SHAP analizi ile yapilmali

### N3. Sistematik Basarisizliklar

| Durum | Etki | Karar |
|-------|------|-------|
| Robust scaling + QM | %100 R2<0 | KALDIRILDI (WARN-03) |
| N=75 dataset boyutu | DNN_MIN_SAMPLES=80 ihlali + CV fold basi ~12 ornek | KALDIRILDI |
| Nilsson ozellikleri | %34 NaN (268 cekirdekten 68'i) | KAPALI tutuldu |
| BNN/PINN modelleri | Desktop'ta cok yavas | KALDIRILDI (desktop icin) |

### N4. Duzeltilen Buglar (Bu Oturumda)

| Bug | Dosya | Aciklama |
|-----|-------|---------|
| BUG-39 | overfitting_detector.py | `analyze_training_metrics` metodu eksikti — eklendi |
| BUG-40 | automl_anfis_optimizer.py | `anfis_core.py` yok — dogru import gosterildi |
| BUG-41 | config_desktop.json | "Physics" feature set tanimsizdi — `null` yapildi |

### N5. Sprint Sonuclari

| Sprint | Konu | Sonuc |
|--------|------|-------|
| Sprint 1 | Cift R2 Filtresi | `parallel_ai_trainer.py` refactor: CV kayit oncesine, cv_R2>=0 + gap<0.5 |
| Sprint 2 | Config Senkronizasyonu | Robust + N=75 tum config'lerden kaldirildi; pfaz03 note eklendi |
| Sprint 3 | Belge Senkronizasyonu | Bu bolum + faz-01/02/03 belgeleri guncellendi |

### N6. Tez Icin Cikartilan Sonuclar

1. **Metodoloji §3.5 icin:** "Cift R2 filtresi Shang et al. (2022) metodolojisini temel alir;
   cv_R2 >= 0.0 kosuluyla asiri uyumu engelleyen guvenilir model secim kriteri olusturuldu."

2. **Metodoloji §3.2 icin:** "Robust scaling QM dagilminin asimetrik yapisiyla
   uyumsuzlugu saptandi (R2<0); yerine StandardScaler ve NoScaling kullanildi."

3. **Sinirlamalar icin:** "Nilsson tek-parcacik enerjileri yalnizca deforme
   cekirdeklerde anlamli (Beta_2 != 0); veri kumesinin %34'inde NaN — omitted."

*Faz Degerlendirme Notlari v2.2 | 2026-05-09 | BOLUM N eklendi (log analizi + sprint ozeti)*
