# 07 — Master Glossary: Kısaltmalar & Semboller

> ⚠️ **Bu dosya araştırma süresince DOLDURULACAK.** Her faz analizinde tespit edilen yeni kısaltma/sembol/birim buraya işlenir.

> **Tezdeki "Simgeler ve Kısaltmalar" listesinin master kaynağıdır.**

---

## İçindekiler

1. [Format Kuralları](#format-kuralları)
2. [Bölüm A: Kısaltmalar (Alfabetik)](#bölüm-a-kısaltmalar-alfabetik)
3. [Bölüm B: Matematiksel Semboller](#bölüm-b-matematiksel-semboller)
4. [Bölüm C: Birimler](#bölüm-c-birimler)
5. [Bölüm D: Domain Spesifik Terimler](#bölüm-d-domain-spesifik-terimler)
6. [Versiyonlama](#versiyonlama)

---

## Format Kuralları

### Kısaltma Girişi

```markdown
| Kısaltma | Tam Ad (TR) | Tam Ad (EN) | Faz | İlk Geçtiği Yer |
|----------|-------------|-------------|-----|-----------------|
| CNN | Konvolüsyonel Sinir Ağı | Convolutional Neural Network | 4 | faz-04.md §5.1 |
```

### Sembol Girişi

```markdown
| Sembol | Ad (TR) | Ad (EN) | Birim | Bağlam | İlk Geçtiği Yer |
|--------|---------|---------|-------|--------|-----------------|
| σ | Tesir kesiti | Cross-section | barn | Nükleer reaksiyon | faz-02.md §7 |
```

### Kurallar

- **Kısaltma:** İlk geçişte tam ad + parantez (örn. "Konvolüsyonel Sinir Ağı (CNN)")
- **Sembol:** İlk geçişte tanım (örn. "tesir kesiti $\sigma$")
- **Sıralama:** Alfabetik (Türkçe alfabeye göre — Ç, Ğ, İ, Ö, Ş, Ü)
- **Çelişki:** Aynı kısaltma iki anlamla geçerse, bağlamla ayır

---

## Bölüm A: Kısaltmalar (Alfabetik)

> **Doluluk:** ⏳ Faz analizleri ile dolar. Aşağıdaki başlangıç entry'leri bu projede sık geçeceği tahmin edilen terimler.

### Yapay Zeka & Makine Öğrenmesi

| Kısaltma | Tam Ad (TR) | Tam Ad (EN) | Faz | İlk Geçtiği Yer |
|----------|-------------|-------------|-----|-----------------|
| AE | Otokodlayıcı | Autoencoder | ⏳ | - |
| ANN | Yapay Sinir Ağı | Artificial Neural Network | ⏳ | - |
| AUC | Eğri Altı Alan | Area Under Curve | ⏳ | - |
| BCE | İkili Çapraz Entropi | Binary Cross-Entropy | ⏳ | - |
| CE | Çapraz Entropi | Cross-Entropy | ⏳ | - |
| CNN | Konvolüsyonel Sinir Ağı | Convolutional Neural Network | ⏳ | - |
| CV | Çapraz Doğrulama | Cross-Validation | ⏳ | - |
| DL | Derin Öğrenme | Deep Learning | ⏳ | - |
| DNN | Derin Sinir Ağı | Deep Neural Network | ⏳ | - |
| GAN | Çekişmeli Üretici Ağ | Generative Adversarial Network | ⏳ | - |
| GBM | Gradyan Artırımı Makinesi | Gradient Boosting Machine | ⏳ | - |
| GD | Gradyan İnişi | Gradient Descent | ⏳ | - |
| GRU | Geçitli Tekrar Birimi | Gated Recurrent Unit | ⏳ | - |
| KNN | K-En Yakın Komşu | K-Nearest Neighbors | ⏳ | - |
| LR | Öğrenme Oranı | Learning Rate | ⏳ | - |
| LSTM | Uzun-Kısa Süreli Bellek | Long Short-Term Memory | ⏳ | - |
| MAE | Ortalama Mutlak Hata | Mean Absolute Error | ⏳ | - |
| ML | Makine Öğrenmesi | Machine Learning | ⏳ | - |
| MLP | Çok Katmanlı Algılayıcı | Multi-Layer Perceptron | ⏳ | - |
| MSE | Ortalama Karesel Hata | Mean Squared Error | ⏳ | - |
| PCA | Temel Bileşen Analizi | Principal Component Analysis | ⏳ | - |
| ReLU | Doğrultulmuş Doğrusal Birim | Rectified Linear Unit | ⏳ | - |
| RF | Rastgele Orman | Random Forest | ⏳ | - |
| RL | Pekiştirmeli Öğrenme | Reinforcement Learning | ⏳ | - |
| RNN | Tekrarlayan Sinir Ağı | Recurrent Neural Network | ⏳ | - |
| ROC | Alıcı Çalışma Karakteristiği | Receiver Operating Characteristic | ⏳ | - |
| SGD | Stokastik Gradyan İnişi | Stochastic Gradient Descent | ⏳ | - |
| SVM | Destek Vektör Makinesi | Support Vector Machine | ⏳ | - |
| t-SNE | t-Dağılımlı Stokastik Komşu Yerleştirme | t-distributed Stochastic Neighbor Embedding | ⏳ | - |
| TL | Aktarım Öğrenmesi | Transfer Learning | ⏳ | - |
| UMAP | Üniform Manifold Yaklaşım ve Yansıtma | Uniform Manifold Approximation and Projection | ⏳ | - |
| VAE | Değişimsel Otokodlayıcı | Variational Autoencoder | ⏳ | - |
| YSA | Yapay Sinir Ağı | Artificial Neural Network | ⏳ | - |

### Bu Projeye Özgü (quantizedeli/v10)

| Kısaltma | Tam Ad (TR) | Tam Ad (EN) | Faz | İlk Geçtiği Yer |
|----------|-------------|-------------|-----|-----------------|
| ANFIS | Adaptif Ağ-Tabanlı Bulanık Çıkarım Sistemi | Adaptive Network-Based Fuzzy Inference System | 03 | faz-0 keşfi |
| BNN | Bayesian Sinir Ağı | Bayesian Neural Network | 02 | faz-0 keşfi |
| FCM | Bulanık C-Ortalamalar Kümeleme | Fuzzy C-Means Clustering | 03 | faz-0 keşfi |
| IQR | Çeyrekler Arası Aralık | Interquartile Range | 01 | faz-0 keşfi |
| MM | Manyetik Moment | Magnetic Moment | 01 | faz-0 keşfi |
| PFAZ | Proje Fazı (repo "pfaz_" ön eki) | Project Phase | tüm | faz-0 keşfi |
| PINN | Fizik-Bilgili Sinir Ağı | Physics-Informed Neural Network | 02 | faz-0 keşfi |
| QM | Kuadrupol Moment | Quadrupole Moment | 01 | faz-0 keşfi |
| S70 | 70/15/15 eğitim-doğrulama-test bölünmesi | 70/15/15 Train/Validation/Test Split | 01 | faz-0 keşfi |
| S80 | 80/10/10 eğitim-doğrulama-test bölünmesi | 80/10/10 Train/Validation/Test Split | 01 | faz-0 keşfi |
| SEMF | Yarı-Deneysel Kütle Formülü | Semi-Empirical Mass Formula (Bethe-Weizsäcker) | 01 | faz-0 keşfi |
| SHAP | Shapley Katkı Değeri | SHapley Additive exPlanations | 01 | faz-0 kesfi |
| BE | Baglanma Enerjisi | Binding Energy | 01 | faz-01 §7 (F-001) |
| WS | Woods-Saxon Potansiyeli | Woods-Saxon Potential | 01 | faz-01 §7 (F-016) |
| YSBF | Yari-Ampirik Sekli Baglanma Formulu | Semi-Empirical Mass Formula | 01 | faz-01 §7 (F-001) |
| IF | Yalitim Ormani | Isolation Forest | 01 | faz-01 §5.5 |

### Nükleer Fizik

| Kısaltma | Tam Ad (TR) | Tam Ad (EN) | Faz | İlk Geçtiği Yer |
|----------|-------------|-------------|-----|-----------------|
| ADC | Analog-Sayısal Dönüştürücü | Analog-to-Digital Converter | ⏳ | - |
| Bq | Becquerel | Becquerel | ⏳ | - |
| Ci | Curie | Curie | ⏳ | - |
| ENDF | Değerlendirilmiş Nükleer Veri Dosyası | Evaluated Nuclear Data File | ⏳ | - |
| FWHM | Tam Genişlik Yarı Yüksek | Full Width at Half Maximum | ⏳ | - |
| Gy | Gray | Gray | ⏳ | - |
| HPGe | Yüksek Saflıkta Germanyum | High-Purity Germanium | ⏳ | - |
| MCA | Çok Kanallı Analizör | Multi-Channel Analyzer | ⏳ | - |
| MCNP | Monte Carlo N-Parçacık | Monte Carlo N-Particle | ⏳ | - |
| NAA | Nötron Aktivasyon Analizi | Neutron Activation Analysis | ⏳ | - |
| NIST | Ulusal Standartlar ve Teknoloji Enstitüsü | National Institute of Standards and Technology | ⏳ | - |
| PMT | Foto Çoğaltıcı Tüp | Photomultiplier Tube | ⏳ | - |
| ROI | İlgi Bölgesi | Region of Interest | ⏳ | - |
| SCA | Tek Kanallı Analizör | Single-Channel Analyzer | ⏳ | - |
| Si(Li) | Lityum Sürüklenmiş Silikon | Lithium-Drifted Silicon | ⏳ | - |
| SNR | Sinyal-Gürültü Oranı | Signal-to-Noise Ratio | ⏳ | - |
| Sv | Sievert | Sievert | ⏳ | - |
| TALYS | TALYS Nükleer Reaksiyon Kodu | TALYS Nuclear Reaction Code | ⏳ | - |
| XRF | X-Işını Floresansı | X-Ray Fluorescence | ⏳ | - |

### Veri & Yazılım

| Kısaltma | Tam Ad (TR) | Tam Ad (EN) | Faz | İlk Geçtiği Yer |
|----------|-------------|-------------|-----|-----------------|
| API | Uygulama Programlama Arayüzü | Application Programming Interface | ⏳ | - |
| CSV | Virgülle Ayrılmış Değerler | Comma-Separated Values | ⏳ | - |
| FFT | Hızlı Fourier Dönüşümü | Fast Fourier Transform | ⏳ | - |
| GPU | Grafik İşlem Birimi | Graphics Processing Unit | ⏳ | - |
| HDF5 | Hiyerarşik Veri Formatı 5 | Hierarchical Data Format 5 | ⏳ | - |
| JSON | JavaScript Nesne Notasyonu | JavaScript Object Notation | ⏳ | - |
| RAM | Rastgele Erişimli Bellek | Random Access Memory | ⏳ | - |
| ROOT | (CERN ROOT veri analiz çatısı) | ROOT (CERN data analysis framework) | ⏳ | - |

---

## Bölüm B: Matematiksel Semboller

> **Doluluk:** ⏳ Her faz formülü taranınca güncellenir.

### Yunan Harfleri (Sık Kullanılan)

| Sembol | Ad | Bağlam | Birim | İlk Geçtiği Yer |
|--------|-----|--------|-------|-----------------|
| α | alfa | Öğrenme oranı, alfa parçacığı | - | ⏳ |
| β | beta | Beta parçacığı, regresyon katsayısı | - | ⏳ |
| γ | gamma | Gama radyasyonu, Lorentz çarpanı | - | ⏳ |
| δ | delta | Kronecker delta, küçük artım | - | ⏳ |
| ε | epsilon | Dedektör verimi, küçük sayı | dimensionless | ⏳ |
| η | eta | Verim, öğrenme oranı (alternatif) | - | ⏳ |
| θ | teta | Açı, model parametreleri | rad / - | ⏳ |
| λ | lambda | Bozunum sabiti, dalga boyu, regularization | s⁻¹ / m / - | ⏳ |
| μ | mü | Ortalama, atenüasyon katsayısı | - / cm⁻¹ | ⏳ |
| ν | nü | Frekans, Poisson oranı | Hz | ⏳ |
| π | pi | Sabit (3.14159...) | - | ⏳ |
| ρ | rho | Yoğunluk, korelasyon katsayısı | g/cm³ / - | ⏳ |
| σ | sigma | Standart sapma, tesir kesiti | - / barn | ⏳ |
| τ | tau | Zaman sabiti, ortalama ömür | s | ⏳ |
| φ | fi | Faz, akı (Φ ile karıştırma) | rad | ⏳ |
| Φ | Fi (büyük) | Akı (Flux) | n/cm²/s | ⏳ |
| χ² | ki-kare | Test istatistiği | - | ⏳ |
| ψ | psi | Dalga fonksiyonu | - | ⏳ |
| ω | omega | Açısal frekans, ağırlık | rad/s / - | ⏳ |

### Operatörler ve Genel

| Sembol | Anlam | Bağlam | İlk Geçtiği Yer |
|--------|-------|--------|-----------------|
| ∑ | Toplam | İstatistik | ⏳ |
| ∏ | Çarpım | Olasılık | ⏳ |
| ∫ | İntegral | Sürekli işlem | ⏳ |
| ∂ | Kısmi türev | Gradyan | ⏳ |
| ∇ | Nabla (gradyan) | Optimizasyon | ⏳ |
| ⊗ | Tensor çarpım | Lineer cebir | ⏳ |
| ‖·‖ | Norm | Vektör/matris | ⏳ |
| 𝔼 | Beklenti | Olasılık | ⏳ |
| ℙ | Olasılık ölçüsü | Olasılık | ⏳ |

### Domain-Spesifik Notation

| Sembol | Anlam | Faz | İlk Geçtiği Yer |
|--------|-------|-----|-----------------|
| T₁/₂ | Yarı ömür | ⏳ | - |
| dN/dt | Bozunum hızı | ⏳ | - |
| ΔE | Enerji aralığı | ⏳ | - |
| E_γ | Gama enerjisi | ⏳ | - |
| (n,γ) | Nötron yakalama reaksiyonu | ⏳ | - |
| ⟨x⟩ | x'in beklenti değeri | ⏳ | - |

### Bu Projeye Özgü Semboller (quantizedeli/v10)

| Sembol | Ad (TR) | Ad (EN) | Birim | Bağlam | İlk Geçtiği Yer |
|--------|---------|---------|-------|--------|-----------------|
| A | Kütle numarası | Mass number | boyutsuz | Çekirdek kimliği | aaa2.txt sütun, faz-0 |
| Z | Proton sayısı | Atomic number | boyutsuz | Çekirdek kimliği | aaa2.txt sütun, faz-0 |
| N | Nötron sayısı | Neutron number | boyutsuz | Çekirdek kimliği | aaa2.txt sütun, faz-0 |
| Nn | Valans nötron sayısı | Valence neutron number | boyutsuz | Shell model | aaa2.txt sütun, faz-0 |
| Np | Valans proton sayısı | Valence proton number | boyutsuz | Shell model | aaa2.txt sütun, faz-0 |
| β₂ | Kuadrupol deformasyon parametresi | Quadrupole deformation parameter | boyutsuz | Nilsson modeli | aaa2.txt (Beta_2), faz-0 |
| µ | Manyetik moment | Magnetic moment | µ_N (nükleer magneton) | Hedef değişken | aaa2.txt (MM), faz-0 |
| Q | Kuadrupol moment | Electric quadrupole moment | barn | Hedef değişken | aaa2.txt (QM), faz-0 |
| R² | Determinasyon katsayısı | Coefficient of determination | boyutsuz | Model performansı | config.json, faz-0 |
| B(A,Z) | Baglanma enerjisi | Binding energy | MeV | SEMF toplam (F-001) | faz-01 §7 |
| β₂ | Kuadrupol deformasyon | Quadrupole deformation parameter | boyutsuz | Nilsson, F-012 | faz-01 §7 |
| R₀ | Nukleer yaricap sabiti | Nuclear radius constant | fm | R = R₀·A^(1/3) (F-008) | faz-01 §7 |
| χ_magic | Sihirli karakter skoru | Magic character score | boyutsuz | Kabuk modeli (F-011) | faz-01 §7 |
| δ(A,Z) | SEMF eslenme terimi | SEMF pairing term | MeV | F-006 | faz-01 §7 |
| Δ | Eslenme acigi | Pairing gap | MeV | F-019 | faz-01 §7 |
| g_l, g_s | Yorunge/spin g-faktoru | Orbital/spin g-factor | boyutsuz | Schmidt momentleri (F-014) | faz-01 §7 |
| V₀ | WS potansiyel derinligi | WS potential depth | MeV | F-016 | faz-01 §7 |
| ℏω₀ | Nilsson osilatör frekansı | Nilsson oscillator frequency | MeV | F-017 | faz-01 §7 |
| Q₀ | Ozsel kuadrupol moment | Intrinsic quadrupole moment | fm² | F-013 | faz-01 §7 |
| κ, μ | Nilsson SO ve l² katsayilari | Nilsson spin-orbit and l² coefficients | boyutsuz | F-017 | faz-01 §7 |
| ℏc | Indirgenmus Planck x isik hizi | Reduced Planck constant × speed of light | MeV·fm | WS hesaplama (BUG-02 duzeltmesi) | constants.py HBAR_C=197.3269804 |
| V_so | WS spin-yorun potansiyelinin derinligi | WS spin-orbit potential depth | MeV | Spin-yorun terimi (BUG-03 duzeltmesi) | constants.py WOODS_SAXON_PARAMS |
| r_so | WS spin-yorun yaricap parametresi | WS spin-orbit radius parameter | fm | Spin-yorun terimi | constants.py WOODS_SAXON_PARAMS |
| a_so | WS spin-yorun difuzluk parametresi | WS spin-orbit diffuseness parameter | fm | Spin-yorun terimi | constants.py WOODS_SAXON_PARAMS |

---

## Bölüm C: Birimler

### SI Temel Birimleri

| Birim | Sembol | Ölçtüğü |
|-------|--------|---------|
| metre | m | Uzunluk |
| kilogram | kg | Kütle |
| saniye | s | Zaman |
| amper | A | Akım |
| kelvin | K | Sıcaklık |
| mol | mol | Madde miktarı |
| kandela | cd | Işık şiddeti |

### Türetilmiş ve Nükleer Birimler

| Birim | Sembol | Ölçtüğü | Tanım |
|-------|--------|---------|-------|
| Becquerel | Bq | Aktivite | 1 Bq = 1 bozunum/s |
| Curie | Ci | Aktivite | 1 Ci = 3.7×10¹⁰ Bq |
| Gray | Gy | Soğurulan doz | 1 Gy = 1 J/kg |
| Sievert | Sv | Doz eşdeğeri | 1 Sv = 1 J/kg (radyobiyolojik etki) |
| Rad | rad | Eski soğurulan doz | 1 rad = 0.01 Gy |
| Rem | rem | Eski doz eşdeğeri | 1 rem = 0.01 Sv |
| Roentgen | R | İyonizasyon | 2.58×10⁻⁴ C/kg |
| Elektronvolt | eV | Enerji | 1 eV = 1.602×10⁻¹⁹ J |
| Kiloelektronvolt | keV | Enerji | 10³ eV |
| Megaelektronvolt | MeV | Enerji | 10⁶ eV |
| Gigaelektronvolt | GeV | Enerji | 10⁹ eV |
| Atomik kütle birimi | u, amu | Kütle | 1 u = 1.66054×10⁻²⁷ kg |
| Barn | b | Tesir kesiti | 1 b = 10⁻²⁴ cm² |
| Milibarn | mb | Tesir kesiti | 10⁻³ b |
| Mikrobarn | μb | Tesir kesiti | 10⁻⁶ b |
| Sayım | counts | Tespit edilen olay | dimensionless |
| Sayım/saniye | cps | Sayım hızı | counts·s⁻¹ |

### ML/Veri Birimleri

| Birim | Sembol | Anlam |
|-------|--------|-------|
| Yüzde | % | Oran |
| dimensionless | - | Birimsiz |
| Adet | - | Sayı (örn: epoch sayısı) |
| Bayt | B | Veri büyüklüğü |
| Megabayt | MB | 10⁶ B |
| Gigabayt | GB | 10⁹ B |
| FLOP | flop | Floating-point operations |
| GFLOP | Gflop | 10⁹ FLOP |

---

## Bölüm D: Domain Spesifik Terimler

### Türkçe-İngilizce Terim Eşleştirmesi

#### Nükleer Fizik

| Türkçe | İngilizce | Notlar |
|--------|-----------|--------|
| Tesir kesiti | Cross-section | σ ile gösterilir |
| Yarı ömür | Half-life | T₁/₂ |
| Bozunum sabiti | Decay constant | λ |
| Aktivasyon analizi | Activation analysis | NAA özel |
| Gama spektroskopisi | Gamma spectroscopy | - |
| Pik fitleme | Peak fitting | Genelde Gaussian |
| Arka plan çıkarma | Background subtraction | - |
| Kalibrasyon eğrisi | Calibration curve | - |
| Compton sırtı | Compton edge | - |
| Tek-kaçışlı pik | Single-escape peak | - |
| Çift-kaçışlı pik | Double-escape peak | - |
| Geri saçılma piki | Backscatter peak | - |
| Toplama piki | Sum peak | Coincidence sum |
| Çekirdek izomerleri | Nuclear isomers | - |
| Reaksiyon kanalı | Reaction channel | - |

#### AI/ML

| Türkçe | İngilizce | Notlar |
|--------|-----------|--------|
| Aşırı uydurma | Overfitting | - |
| Yetersiz uydurma | Underfitting | - |
| Düzenlileştirme | Regularization | L1, L2 |
| Aktarım öğrenmesi | Transfer learning | - |
| Etiket dengesizliği | Class imbalance | - |
| Veri arttırma | Data augmentation | - |
| Yığın normalleştirmesi | Batch normalization | BN |
| Bırakma | Dropout | - |
| Erken durdurma | Early stopping | - |
| Çapraz doğrulama | Cross-validation | k-fold |
| Sözünü tutma kümesi | Hold-out set | Test set |
| İnce ayar | Fine-tuning | - |
| Dondurma | Freezing (layers) | - |
| Bilgi damıtma | Knowledge distillation | - |
| Etkinlik haritası | Activation map | - |
| Dikkat mekanizması | Attention mechanism | - |
| Konum kodlaması | Positional encoding | Transformer |

---

## Versiyonlama

```
v0.1 (2026-05-02) — Master glossary iskeleti
v0.2 — Faz 0 sonrası: domain terimleri tamamlandı
v0.3 — Faz 1 sonrası: yeni kısaltmalar
...
v1.0 — Tez "Simgeler ve Kısaltmalar" listesi tamamlandı
```

---

## Kullanım Örnekleri

### Yeni Kısaltma Eklenirken

```markdown
| ResNet | Artık (Residual) Sinir Ağı | Residual Network | 4 | faz-04.md §5.2 |
```

Faz dokümanında ilk geçişte:

> "Bu çalışmada Artık Sinir Ağı (Residual Network — ResNet) mimarisi kullanılmıştır."

### Yeni Sembol Eklenirken

```markdown
| ξ | ksi | Hata terimi | dimensionless | Regresyon | faz-06.md §7 (F-014) |
```

### Çakışma Durumu

Aynı kısaltma iki anlamda:

```markdown
| RF | Rastgele Orman | Random Forest | 6 | faz-06.md §5 |
| RF | Radyofrekans | Radio Frequency | 1 | faz-01.md §3 |
```

Bağlamla ayır, tezde ilk geçişte tam ad zorunlu.

---

*Master Glossary v0.4 | Son güncelleme: 2026-05-04 (Sprint: HBAR_C, SCALING_METHODS, BNN/PINN aciklama eklendi)*



## PFAZ 05 Kisaltmalar

| Kisaltma | Tam Ad | Aciklama |
|----------|--------|----------|
| CME | CrossModelEvaluator | Ana capraz model degerlendirme sinifi |
| CMP | CrossModelAnalysisPipeline | Pipeline orkestrator |
| BMS | BestModelSelector | Cok kriterli model secici |
| ICA | IsotopeChainAnalyzer | Izotop zinciri analiz sinifi |
| SDI | Sudden Change Index | Ani degisim indeksi; SDI = delta/sigma_zincir |
| common_nuclei | Ortak Cekirdek Altkumesi | Tum modellerin tahmin ettigi kesit |

## PFAZ 05 Semboller

| Sembol | Tanim | Birim |
|--------|-------|-------|
| S_agreement | Model uzlasma puani = 1/(1+sigma_error) | boyutsuz, (0,1] |
| sigma_error | Modeller arasi hata standart sapmasi | muN veya barn |
| SDI | Ani degisim indeksi = |delta_mu| / sigma_zincir | boyutsuz |
| Score_composite | BestModelSelector bilesite puani | boyutsuz, [0,1] |


## PFAZ 06 Kisaltmalar

| Kisaltma | Tam Ad | Aciklama |
|----------|--------|----------|
| FRP | FinalReportingPipeline | PFAZ 06 ana orkestrator sinifi |
| CER | ComprehensiveExcelReporter | Detayli ANFIS Excel rapor sinifi |
| ECG | ExcelChartGenerator | Gomulu grafik Excel uretici |
| ES | ExcelStandardizer | Standart Excel bicim context manager |
| LRG | LaTeXReportGenerator | Tez LaTeX/PDF uretici |
| BCI | BootstrapConfidenceIntervals | 5000-ornekli guven araligi |
| ASA | AdvancedSensitivityAnalysis | Tornado diyagrami uretici |

## PFAZ 06 Semboller

| Sembol | Tanim | Birim |
|--------|-------|-------|
| CI_95 | %95 Bootstrap guven araligi | Val_R2 birimi |
| delta_R2_p | Hiperparametre p icin duyarlilik araligi | R2 birimi |
| R2_FLOOR | Val_R2 < -10 filtre esigi | boyutsuz |


---

## PFAZ 07 Kisaltmalar

| Kisaltma | Acilim | Aciklama |
|----------|--------|---------|
| AVE | AdvancedVotingEnsemble | 5 voting yontemini uygulayan sinif |
| ASE | AdvancedStackingEnsemble | 6 stacking yontemini uygulayan sinif |
| OOF | Out-of-Fold Predictions | 5-fold CV ile data leakage olmaksizin meta-model egitim verisi |
| DA | DiversityAnalyzer | Model cesitliligi olcum sinifi |
| RML | RealModelLoader | PKL dosyalarindan model yukleme sinifi |
| CEE | ComprehensiveEnsembleEvaluator | Metrik hesaplama ve JSON rapor sinifi |

## PFAZ 07 Semboller

| Sembol | Anlam | Birim |
|--------|-------|-------|
| w_i | i. modelin ensemble agirlik katsayisi | boyutsuz [0,1] |
| p_i | i. modelin tahmin vektoru | hedef birimi |
| R2_i | i. modelin validasyon R-kare degeri | boyutsuz |
| RMSE_i | i. modelin validasyon kok ortalama kare hatasi | hedef birimi |
| Diversity_Score | 1 - ortalama cikti korelasyonu | boyutsuz [0,1] |
| K_stack | Stacking OOF kat sayisi | boyutsuz (=5) |


---

## PFAZ 08 Kisaltmalar

| Kisaltma | Acilim | Aciklama |
|----------|--------|---------|
| MVS | MasterVisualizationSystem | Ana entegrasyon sinifi (4531 satir) |
| TCG | ThesisChartGenerator | 300 DPI tez grafik uretici |
| SV | SHAPVisualizer | SHAP aciklanabilirlik grafikleri |
| AKV | AnomalyKernelVisualizer | Anomali ozellestirme grafikleri |
| RV | RobustnessVisualizer | Gurultu/perturbation grafikleri |
| MC9V | MonteCarlo9Visualizer | PFAZ09 belirsizlik grafikleri |
| SHAP | SHapley Additive exPlanations | Model karar aciklanabilirlik metodu |
| DPI | Dots Per Inch | Gorsel cozunurluk birimi |



---

## PFAZ 09 Kisaltmalar

| Kisaltma | Acilim | Aciklama |
|----------|--------|---------|
| ACGA | AAA2ControlGroupAnalyzerComplete | PFAZ09 ana orkestrator sinifi (1046 satir) |
| MCSS | MonteCarloSimulationSystem | 5 MC yontemini kapsayan sistem (1259 satir) |
| MCD | MC Dropout | DNN'lere ozgu Bayesci belirsizlik yaklasimi (Gal & Ghahramani, 2016) |
| BS9 | Bootstrap Simulator (PFAZ09) | Yeniden ornekleme tabanli CI hesabi; n=100 |
| NS | Noise Simulator | Girise Gaussian gurultu ekleyerek duyarlilik olcen simulator |
| FDS | Feature Dropout Simulator | Ozellikleri Bernoulli maskeyle rastgele silerek duyarlilik testi |
| EUA | Ensemble Uncertainty Analyzer | Model arasi std (inter-model anlasmama) olcum sinifi |
| TFC | TheoreticalFeaturesCalculator | WS+Nilsson+Shell model teorik ozellik hesaplama sinifi |
| ci_width | CI Genisligi | Guven araligi uzunlugu: P_97.5 - P_2.5 |

## PFAZ 09 Semboller

| Sembol | Tanim | Birim |
|--------|-------|-------|
| sigma_i | i. cekirdek icin model arasi standart sapma | hedef birimi (muN veya barn) |
| CV_i | i. cekirdek varyasyon katsayisi = sigma_i / (|y_bar| + eps) | boyutsuz |
| P_2.5, P_97.5 | Tahmin dagiliminin 2.5. ve 97.5. yuzdelik dilimleri | hedef birimi |
| n_boot | Bootstrap ornek sayisi | boyutsuz (=100; oneride 1000) |
| p_drop | Feature silme olasiligi | boyutsuz {0.1, 0.2, 0.3} |
| sigma_k | Noise seviyeleri = sigma_k * std(X) | oransal; sigma_k in {0.01, 0.02, 0.05, 0.10, 0.20} |



---

## PFAZ 12 Kisaltmalar

| Kisaltma | Acilim | Aciklama |
|----------|--------|---------|
| STS | StatisticalTestingSuite | 6 istatistiksel test + etki buyuklugu sinifi |
| ASA12 | AdvancedSensitivityAnalysis | Sobol/Morris/Tornado duyarlilik analizi |
| NPA | NuclearPatternAnalyzer | Izotop/izoton/izobar sicrama + sihirli sayi analizi |
| NBA | NuclearBandAnalyzer | Deger bandi + kutle bolgesi örüntü analizi (export eksik) |
| BCI12 | BootstrapConfidenceIntervals | n=5000 R2/RMSE/MAE guven araligi |
| BMC | BayesianModelComparison | Bayes Factor + ROPE testi |
| ROPE | Region of Practical Equivalence | Pratik esitlik bolgesi (BMC icin) |
| KS | Kolmogorov-Smirnov | Dagilim benzerlik testi (sihirli sayi analizi icin) |

## PFAZ 12 Semboller

| Sembol | Tanim | Birim |
|--------|-------|-------|
| d | Cohen's d etki buyuklugu (eslestirilmis) | boyutsuz |
| eta_sq | Eta-squared (ANOVA etki buyuklugu) | boyutsuz [0,1] |
| delta_cliff | Cliff's delta (parametrik olmayan etki buyuklugu) | boyutsuz [-1,1] |
| S1, ST | Sobol birinci derece ve toplam duyarlilik indeksleri | boyutsuz [0,1] |
| BF | Bayes Factor | boyutsuz |
| jump_sigma | Ani degisim esigi | sigma birimi |

---

## PFAZ 13 Kisaltmalar

| Kisaltma | Acilim | Aciklama |
|----------|--------|---------|
| AMRL | AutoMLRetrainingLoop | Ana AutoML dongu sinifi (1015 satir) |
| AO | AutoMLOptimizer | Optuna TPE hiperparametre optimizasyonu |
| ALRS | AutoMLLoggingReportingSystem | Trial-bazli detayli kayit sistemi |
| AFE | AutoMLFeatureEngineer | Polinomial + fizik esinli ozellik secimi |
| AAO | AutoMLANFISOptimizer | ANFIS konfigurasyon arama (PFAZ03 ile uyumlu) |
| TPE | Tree-structured Parzen Estimator | Optuna Bayesian sampler |
| MedianPruner | Median Pruner | Trial budama: medyan altindakileri budayan Optuna pruner |
| BKE | Backward Elimination | Geriye elemeli ozellik secim yontemi |

## PFAZ 13 Semboller

| Sembol | Tanim | Birim |
|--------|-------|-------|
| improvement | after_r2 - before_r2 (AutoML iyilesme) | R2 birimi (boyutsuz) |
| n_trials | Optuna trial sayisi (=30 default) | boyutsuz |
| n_per_category | Her kategoriden max dataset sayisi (=25) | boyutsuz |
| POOR_MAX | Poor kategori R2 siniri (=0.70) | boyutsuz |
| MEDIUM_MAX | Medium kategori R2 siniri (=0.90) | boyutsuz |

## PFAZ 10 Kisaltmalar

| Kisaltma | Acilim | Aciklama |
|----------|--------|----------|
| MTI | MasterThesisIntegration | PFAZ10 ana orkestrator sinifi (v5.0.0) |
| DCG | DetailedChapterGenerator | Metod + Bulgular bolumlerini LaTeX'e donusturucu |
| LTI | LaTeXIntegrator | Sekil/tablo LaTeX kodu + subfigure duzenleyici |
| TCS | ThesisCompilationSystem | Tez derleme sistemi (ThesisOrchestrator alternatifi) |
| TO | ThesisOrchestrator | Eski tez orkestratoru (v2.0; aktif degil) |
| VQA | VisualizationQA | PFAZ8 gorsel kalite kontrol modulu |

## PFAZ 10 Semboller

| Sembol | Tanim | Birim |
|--------|-------|-------|
| compile_pdf | PDF derleme bayragi (False=sadece LaTeX uret, True=pdflatex calistir) | bool |
| pfaz_outputs | {pfaz_id: Path} -- inject edilmis cikti dizin haritasi | dict |
| progress | pfaz_status.json ilerleme yuzdesi (=50 mevcut durum) | % |
