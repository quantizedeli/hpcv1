# Ani Değişim Araştırması: Nükleer Kabuk Kapanmaları ve ML Etkileri

> **Konu:** Shell closure discontinuity — nükleer özelliklerin sihirli sayılarda ani değişimi  
> **Amaç:** Bu fenomeni tez dokümantasyonunda doğru ve derin belgelemek  
> **Tarih:** 2026-05-03

---

## 1. Fiziksel Temel

### 1.1 Sihirli Sayılar

Nükleer fizikteki sihirli sayılar (2, 8, 20, 28, 50, 82, 126) kabuk model teorisinin temel çıktısıdır. Bu sayılarda ya proton ya da nötron alt kabuğu tam olarak dolar. Fiziksel sonuçları:

- **Bağlanma enerjisi artışı:** Tam dolu kabuk daha kararlıdır → ΔBE aniden büyür
- **Nükleer yarıçap azalması:** Dolu kabuk kompakt yapı → kabuk kapanması sonrasında ani yarıçap artışı
- **Deformasyon sıfırlanması:** Kapalı kabuk çekirdekler küreseldir (β₂ ≈ 0), bir nükleon eklendikten sonra deformasyon başlar
- **Manyetik moment:** Schmidt değeri kapalı-kabuk+1 çekirdekte tam single-particle değerini gösterir
- **Kuadrupol moment:** Kapalı kabukta Q=0, açık kabukta Q≠0 (işaret değişimi olabilir)

### 1.2 Schmidt Değerlerinde Ani Değişim

Tek-nükleon yaklaşımında (Schmidt teoremi):

**Tek proton/nötron için:**
```
μ_Schmidt = g_l·(j-1/2) + g_s/2      (j = l + 1/2)
μ_Schmidt = g_l·(j+3/2) - g_s/2      (j = l - 1/2)
```

Kapalı kabuğun hemen üstüne bir nükleon eklendiğinde, bu nükleonun orbital değişir (l değişir) → Schmidt değeri **ani sıçrama** gösterir.

**Örnek:** ⁴⁰Ca (Z=20, N=20, çift-çift, μ=0) → ⁴¹Ca (Z=20, N=21) → N=21 nötronu f₇/₂ yörüngesine gider → μ ≠ 0 aniden.

### 1.3 Ani Değişimin Matematiksel İfadesi

Kapalı kabuk komşularında gözlenen empirik örüntü:

```
Δμ = μ(N=N_magic+1) - μ(N=N_magic) >> δμ_smooth
```

burada δμ_smooth normal çekirdek-çekirdek değişimidir. Bu sıçrama, interpolasyona dayalı ML modellerinin tahmin etmekte en çok zorlandığı bölgedir.

---

## 2. ML Modellerinde Sorun

### 2.1 Süreklilik Varsayımı

Standart ML algoritmaları (RF, GBM, XGBoost) yerel süreklilik varsayımına dayanır:
- Komşu örnekler benzer çıktılara sahiptir
- Kabuk kapanmalarında bu YANLIŞTIR

### 2.2 Eksik Özellik Problemi

Z ve N'in ham değerleriyle:
```
Z=82 → μ=... (Pb izotopları)  
Z=83 → μ=... (Bi izotopları, tamamen farklı)
```

Model, Z'nin 82 ile 83 arasındaki farkın neden bu kadar önemli olduğunu kendi başına öğrenemez.

### 2.3 Açık Özelliklerle Çözüm

Kodda tanımlanan üç özellik bu sorunu doğrudan ele alır:

```python
# magic_character: Z veya N sihirli ise 1, değilse 0
magic_character = 1 if (Z in MAGIC_NUMBERS or N in MAGIC_NUMBERS) else 0

# Z_magic_dist: Proton sayısının en yakın sihirli sayıya uzaklığı
Z_magic_dist = min(abs(Z - m) for m in MAGIC_NUMBERS)

# N_magic_dist: Nötron sayısının en yakın sihirli sayıya uzaklığı  
N_magic_dist = min(abs(N - m) for m in MAGIC_NUMBERS)
```

Bu özellikler modele şunu söyler: "Bu çekirdek bir kabuk kapanmasının yakınında, farklı davran."

---

## 3. SHAP Analizi Bağlantısı

Eğer SHAP değerleri hesaplanmışsa:
- magic_character yüksek SHAP önemi göstermeli (özellikle QM tahmini için)
- Z_magic_dist, N_magic_dist MM tahmininde önemli görünmeli
- Bu özellikler olmadan model kapalı-kabuk bölgesinde sistematik hata yapmalı

**Doğrulanması gereken:** PFAZ 05 veya PFAZ 12 çıktılarında kabuk kapanması bölgelerindeki hata analizi

---

## 4. Literatür Bağlamı

### Deneysel Kanıt
- Bohr & Mottelson (1975): Nuclear Structure Vol.2 — deformasyon ve kabuk etkileşimi
- Casten (1990): Nuclear Structure from a Simple Perspective — sihirli sayı etkileri
- Stone (2005): Table of Nuclear Magnetic Dipole Moments — geniş veri tabanı, ani değişimler açık

### ML Nükleer Fizik Literatürü
- Niu & Liang (2018): "Nuclear mass predictions based on Bayesian neural networks" — kabuk etkisinin ML'de modellenmesi
- Utama & Piekarewicz (2016): "Nuclear mass predictions..." — Bayesian yaklaşımda kabuk düzeltmeleri
- Dong et al. (2022): "Nuclear charge radii with machine learning" — benzer ani değişim problemi

---

## 5. Tezdeki Yeri

**§3.2 Özellik Mühendisliği** altında:
- Kabuk model özelliklerinin neden eklenmesi gerektiği → ani değişim argümanı
- magic_character, Z_magic_dist, N_magic_dist formülleri ile

**§4.x Sonuçlar** altında:
- Kabuk kapanması bölgelerinde model performansı analizi
- Bu özelliklerle vs. bu özellikler olmadan karşılaştırma (ablation study)

---

*Bu dosya araştırma notudur — tez metnine girecek kısımlar PFAZ 01 dokümantasyonuna taşınacak*
*Güncelleme: 2026-05-03*

---

## Sprint 4-13 Güncellemeleri (2026-05-11 → 2026-05-14)

### 6. NuclearBandAnalyzer Entegrasyonu (Sprint 4/11)

Sprint 4 BUG-31 fix sonrasi `NuclearBandAnalyzer = NuclearMomentBandAnalyzer` alias eklendi -- PFAZ12 deger bandi ve kutle bolgesi oruntu analizini calistirabiliyor. Bu, **ani degisim hipotezi** icin dogrudan ampirik dogrulama saglar:

- N veya Z sihirli sayinin (2,8,20,28,50,82,126) ±3 komsulugundaki cekirdekler ayri "band" olarak gruplanir
- Bu bandlar icindeki MM/QM dagilimi geri kalanlardan istatistiksel olarak farkli mi?
- KS test ve Mann-Whitney U test sonuclari `outputs/advanced_analytics/band_analysis/`'da

Sprint 11+12 BUG-80 ile PFAZ8'e Band_Analizi grafikleri (ST12-C/D turevi) entegre edildi.

### 7. PFAZ12 BootstrapCI Karsilastirmasi (Sprint 13 BUG-95/97)

Sprint 13 ile PFAZ12 artik magic_character=1 ve magic_character=0 alt gruplarda **Bootstrap CI ayri** raporluyor:
- Magic group R^2 [CI_lower, CI_upper]
- Non-magic group R^2 [CI_lower, CI_upper]
- Iki grup arasinda paired t-test p-value

Bu cikti, "magic_character ozelligi olmadan model kapanis bolgesinde sistematik hata yapiyor mu?" sorusunun ampirik testidir. Tez §4.3 (Model Karsilastirma) icin asagidaki cumle eklenebilir:

> "Kabuk kapanmasi cevresindeki cekirdekler (Z veya N sihirli sayilarin ±3 komsulugu) icin model performans (R^2) Bootstrap orneklem ile %95 CI'da [a, b] olarak hesaplanmis, diger cekirdekler icin [c, d] degerinde olcusulmustur. Paired t-test p-value [0.xx] istatistiksel anlamliligi gostermistir."

### 8. RobustnessTester Permutation Importance (Sprint 13 BUG-96)

Sprint 13 ile aktif edilen RobustnessTester (PFAZ2) her ozellik icin permutation importance ureriyor. Bu cikti **magic ozelliklerinin SHAP siralamasini empirik olarak dogrular**:

- magic_character, Z_magic_dist, N_magic_dist en yuksek importance siralamasinda olmali (MM ve QM icin)
- Ablation study gerekmez -- permutation importance ayni etkiyi olcuyor

Tez §3.2 (Ozellik Muhendisligi) icin direkt kullanilabilir veri.

### 9. Sprint 11+12 BandAnalyzer Yapilanma

`pfaz_modules/pfaz12_advanced_analytics/nuclear_band_analyzer.py` (1174 satir) artik PFAZ12'nin ana akisinda. PFAZ4 unknown_predictions Excel'ini explicit path ile alir (BUG-81 / Sprint 12).

### Tez §4.x Icin Ablation Study Onerisi (Acik)

`research/acik-sorular.md` S-002 ve §4.3'te bahsedilen ablation study (magic ozellikler cikarildiginda performans degisimi) icin uygulama plani:

1. PFAZ1 dataset varyantlarinda Basic+Magic vs Basic-NoMagic karsilastirmasi
2. PFAZ2 her iki seti egit (otomatik degil, manuel script)
3. R^2 farki ve sihirli bolge sistematik hatasi raporla

Bu, TRUBA sonrasi tez yazim asamasinda ele alinacak ayri bir is paketidir.

---

*Sprint 4-13 guncelleme: 2026-05-14*
