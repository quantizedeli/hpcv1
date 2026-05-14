# ML/AI Model Seçim Gerekçeleri — PFAZ 02 ve 03

> **Amaç:** Her modelin bu problemde neden kullanıldığını akademik olarak belgelemek  
> **Tarih:** 2026-05-03

---

## Problemin Özellikleri

Veri kümesi karakteristikleri model seçimini doğrudan etkiler:
- **Küçük veri:** 267 çekirdek (maksimum 197 eğitim örneği S70'de)
- **Yüksek boyut:** 44+ özellik, çok sayısı korele
- **Fizik kısıtları:** SEMF ve Schmidt teorisi bilinen ilişkiler sağlar
- **Ayrık yapı:** Sihirli sayı efektleri — sürekli değil, ayrık değişim noktaları
- **Gürültülü ölçüm:** Deneysel MM/QM'ler ~%5-15 belirsizlik içerebilir

Bu özellikler model seçimini aşağıdaki gibi yönlendirir.

---

## 1. Random Forest (RF)

**Seçim gerekçesi:**
RF, küçük boyutlu veri kümelerinde güvenilir bir temel (baseline) sağlar. 267 çekirdeklik veriyle ağaç tabanlı yöntemler sinir ağlarına göre daha iyi genelleme yapar — her alt ağaç farklı bir bootstrap örneği kullanır ve bu durum veri kıtlığını dolaylı olarak telafi eder.

**Teknik avantajlar:**
- Yüksek korele özelliklerle başa çıkar (rassal özellik seçimi ile)
- Hiperparametre hassasiyeti düşük — küçük veriyle güvenli
- Özellik önemi (SHAP için altyapı) doğrudan çıkarılabilir
- Aşırı uyum (overfit) riski düşük — bootstrap ağaçların varyansını dengeler

**Sınırlamalar:**
- Doğrusal olmayan ilişkileri öğrenir ama ekstrapolasyon yapamaz
- Deneysel verisi olmayan çekirdekler için (PFAZ 04) güvenilirlik azalır

---

## 2. Gradient Boosting (GBM / LightGBM)

**Seçim gerekçesi:**
Sıralı hata düzeltme mekanizması, nükleer moment verisindeki sistematik sapmaları (özellikle Schmidt değerinden sapma) iteratif olarak giderme kapasitesi sağlar. Nükleer enerji modellemesi literatüründe GBM tabanlı yöntemler başarılı sonuçlar vermiştir (Zhang et al., 2017; Gao et al., 2021).

**Teknik avantajlar:**
- Rezidüel (artık) hata üzerine eğitim → sistematik hatalar azalır
- L1/L2 regularizasyon → overfit kontrolü
- LightGBM'in leaf-wise büyümesi küçük veriyle verimli

---

## 3. XGBoost

**Seçim gerekçesi:**
GBM'in genelleştirilmiş bir versiyonu olarak XGBoost, nukleer fizik ML çalışmalarında standart başvuru modelidir. Spesifik regularizasyon (α, λ, γ) parametreleri küçük veri kümelerinde kritik olan overfit kontrolü sağlar.

**Teknik avantajlar:**
- Tree pruning: gereksiz dallarda büyüme durur — 267 örnekle kritik
- Column subsampling: korele özelliklerde GBM'e göre daha sağlam
- Bilgi eksikliği (missing value) doğal işleme
- Geniş hiperparametre optimizasyon literatürü

---

## 4. Derin Sinir Ağı (DNN: 128-64-32)

**Seçim gerekçesi:**
Nükleer momentlerin hesaplanması Z, N, A arasındaki karmaşık çok-yönlü etkileşimleri gerektirir. Tek katmanlı modeller bu etkileşimleri yakalayamaz. 128-64-32 mimarisi, 267 örnek için parametre/veri oranını makul tutar.

**Mimari tercihi 128-64-32:**
- Toplam parametre ≈ 12,000 (giriş boyutuna göre değişir)
- 267 eğitim örneği için parametre/örnek oranı ~45 → kabul edilebilir
- Üç gizli katman: doğrusal olmayan ilişkilerin yeterli temsili
- Dropout + BatchNorm → overfit kontrolü

**256-128-64 yerine neden?**
~50,000 parametre / 267 örnek = ~187 → ciddi overfit riski.

---

## 5. Bayesian Sinir Ağı (BNN)

**Seçim gerekçesi:**
Deneysel verisi olmayan çekirdeklerin tahmininde belirsizlik tahmini zorunludur. BNN, ağırlıklara olasılık dağılımı atayarak tahmin belirsizliğini doğrudan çıkarır. Bu, PFAZ 04 (bilinmeyen çekirdek tahminleri) için metodolojik bütünlük sağlar.

**Tezdeki katkı:**
"Model X, çekirdek Y için μ = A ± B μ_N öngörüyor" ifadesi, B (belirsizlik) olmadan bilimsel olarak eksiktir. BNN bu gereksinimi karşılar.

---

## 6. Fizik Bilgili Sinir Ağı (PINN, physics_weight=0.5)

**Seçim gerekçesi:**
267 çekirdeğin bir kısmında deneysel MM ve QM aynı anda mevcut değildir. Veri boşluklarını kapatmak ve model tahminlerini fizik kısıtlarıyla uyumlu tutmak için PINN tercih edilmiştir.

**physics_weight=0.5 tercihi:**
```
Toplam kayıp = 0.5 × MSE(veri) + 0.5 × MSE(fizik_kısıtı)
```
- weight → 1.0: model sadece SEMF'i taklit eder → veri öğrenimi azalır
- weight → 0.0: standart DNN, fizik avantajı kaybolur
- 0.5: denge noktası — literatürde nükleer PINN çalışmalarında yaygın değer

**Fizik kısıtı içeriği:**
SEMF bağlanma enerjisi tahmini ile bağlanma enerjisi özelliği arasındaki uyumluluk.

---

## 7. ANFIS (Adaptif Nöro-Fuzzy Çıkarım Sistemi)

**Seçim gerekçesi:**
Nükleer bölgeler (hafif/ağır, sihirli/sihirli olmayan, deforme/küresel) doğası gereği bulanık sınırlara sahiptir. ANFIS, bu fizik bilgisini yorumlanabilir Eğer-O zaman kurallarına çevirir ve veri üzerinde optimize eder.

**8 konfigürasyon seçimi:**
```
2 üyelik fonksiyonu × 2 kümeleme yöntemi × 2 kalite seviyesi = 8
Gauss2MF/Gauss3MF × Grid/SubClust × standart konfigürasyonlar
```

- **Gauss üyelik fonksiyonu:** Nükleer özellikler sürekli ve pürüzsüz değişir → Gauss geçişi fiziksel
- **Grid partition:** Uniform ızgara → özellik uzayını eşit örnekler
- **Subtractive clustering:** Veri yoğunluğuna dayalı → az örnek bölgelerine uyumlu

---

## Özet Tablo

| Model | Temel Neden | Küçük Veri | Belirsizlik | Fizik Bilgisi |
|-------|-------------|-----------|------------|--------------|
| RF | Güvenilir baseline, özellik önemi | +++ | - | - |
| GBM | Sistematik hata düzeltimi | ++ | - | - |
| XGBoost | Regularize gradient boosting | ++ | - | - |
| DNN | Çok-yönlü etkileşimler | + | - | - |
| BNN | Belirsizlik tahmini (PFAZ 04 için zorunlu) | + | +++ | - |
| PINN | Fizik kısıtlı öğrenme | + | - | +++ |
| ANFIS | Yorumlanabilir bulanık kurallar | ++ | - | ++ |

---

*Araştırma notu — 2026-05-03*
