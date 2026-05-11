# 04 — Thesis Writing Guide (Akademik Yazım Rehberi)

> **Amaç:** Faz dokümanlarından tez bölümlerine geçişte tutarlı, akademik, savunulabilir yazım sağlamak.

> **Kapsam:** Türkçe PhD tezi, AI-destekli nükleer veri analizi alanı.

---

## İçindekiler

1. [Tez Yapı Şablonu](#tez-yapı-şablonu)
2. [Akademik Türkçe Stili](#akademik-türkçe-stili)
3. [Atıf Formatı](#atıf-formatı)
4. [Formül Yazım Kuralları](#formül-yazım-kuralları)
5. [Şekil & Tablo Standartları](#şekil--tablo-standartları)
6. [Nükleer Fizik Terminolojisi (TR-EN)](#nükleer-fizik-terminolojisi-tr-en)
7. [AI/ML Terminolojisi (TR-EN)](#aiml-terminolojisi-tr-en)
8. [Kaçınılacak Kalıplar](#kaçınılacak-kalıplar)
9. [Tezi humanizer ile Temizlerken Dikkat](#tezi-humanizer-ile-temizlerken-dikkat)
10. [Kalite Kontrol Listesi](#kalite-kontrol-listesi)

---

## Tez Yapı Şablonu

```
ÖZET (TR + EN)
ÖNSÖZ
İÇİNDEKİLER
ŞEKİLLER LİSTESİ
TABLOLAR LİSTESİ
SİMGELER VE KISALTMALAR

1. GİRİŞ
   1.1 Problem Tanımı
   1.2 Tezin Amacı
   1.3 Tezin Önemi ve Katkıları
   1.4 Tezin Düzeni

2. KURAMSAL ÇERÇEVE / LİTERATÜR ÖZETİ
   2.1 Nükleer Veri Analizi: Tarihsel Gelişim
   2.2 Yapay Zeka Yöntemlerinin Nükleer Alana Uygulamaları
   2.3 Mevcut Yaklaşımların Sınırlamaları

3. YÖNTEM (faz dokümanlarından derlenir)
   3.1 Genel Mimari (Sistemin Üst Düzey Tanımı)
   3.2 Faz 1: ...
   3.3 Faz 2: ...
   ...
   3.N Veri Akışı ve Entegrasyon

4. UYGULAMA ve DENEYSEL KURULUM
   4.1 Veri Kümesi
   4.2 Donanım ve Yazılım Ortamı
   4.3 Hiperparametreler ve Yapılandırma
   4.4 Değerlendirme Metrikleri

5. BULGULAR
   5.1 Faz Bazında Sonuçlar
   5.2 Karşılaştırmalı Analiz
   5.3 İstatistiksel Anlamlılık

6. TARTIŞMA
   6.1 Bulguların Yorumu
   6.2 Literatürle Karşılaştırma
   6.3 Sınırlamalar
   6.4 Tehditler ve Geçerlilik (Threats to Validity)

7. SONUÇ ve ÖNERİLER
   7.1 Tezin Özeti
   7.2 Bilimsel Katkılar
   7.3 Gelecek Çalışma Önerileri

KAYNAKÇA
EKLER
   EK A: Kod Repository Yapısı
   EK B: Hiperparametre Detayları
   EK C: Ek Şekil/Tablolar
   EK D: Sembol ve Kısaltma Sözlüğü
```

> **Not:** Üniversitenin tez şablonu varsa o esas alınır.

---

## Akademik Türkçe Stili

### 3. Tekil Şahıs Tercihi

✅ **"Önerilen yöntem ile veri seti normalize edilmiştir."**
❌ "Ben veri setini normalize ettim."

✅ **"Modelin doğrulama doğruluğu %92.4 olarak ölçülmüştür."**
❌ "Modelimi doğruladım, %92.4 çıktı."

### Pasif Yapı Kabul

✅ "Eğitim seti %80, doğrulama seti %20 oranında ayrılmıştır."
✅ "Hiperparametreler ızgara araması ile optimize edilmiştir."

### Kelime Tercihleri

| Tercih Edilen | Kaçınılan |
|---------------|-----------|
| gerçekleştirilmiştir | yapıldı |
| elde edilmiştir | bulduk |
| sunulmaktadır | gösteriyoruz |
| ortaya konulmuştur | çıkardık |
| önerilmektedir | öneriyoruz |
| tanımlanmaktadır | tanımlarız |

### Cümle Uzunluğu

- Ortalama: 15-25 kelime
- Çok uzun cümle bilimsel içeriği bulanıklaştırır
- Karmaşık matematiksel ifade öncesi: kısa giriş cümlesi

---

## Atıf Formatı

### Varsayılan: APA 7

```
Krane, K. S. (1988). Introductory nuclear physics. John Wiley & Sons.

Smith, J., & Doe, A. (2020). Deep learning for nuclear spectra. 
Nuclear Instruments and Methods A, 950, 162987.

Doe, A., Smith, J., Brown, K., & Lee, M. (2021). ...
```

**Metin içi:**
- Tek: `(Krane, 1988)`
- İki: `(Smith & Doe, 2020)`
- Üç+: `(Doe et al., 2021)`
- Sayfa: `(Krane, 1988, s. 142)`

### Alternatif: IEEE

```
[1] J. Smith and A. Doe, "Deep learning for nuclear spectra," 
    Nucl. Instrum. Methods A, vol. 950, p. 162987, 2020.
```

### BibTeX

```bibtex
@book{krane1988,
  author    = {Krane, Kenneth S.},
  title     = {Introductory Nuclear Physics},
  publisher = {John Wiley \& Sons},
  year      = {1988}
}

@article{smith2020dl,
  author  = {Smith, J. and Doe, A.},
  title   = {Deep learning for nuclear spectra},
  journal = {Nuclear Instruments and Methods A},
  volume  = {950},
  pages   = {162987},
  year    = {2020},
  doi     = {10.1016/j.nima.2019.162987}
}
```

---

## Formül Yazım Kuralları

### LaTeX Notasyonu

```latex
$E = mc^2$

$$
\sigma_{\text{abs}} = \frac{N_R}{N_T \cdot \Phi}
$$

\begin{equation}
\sigma_{\text{abs}} = \frac{N_R}{N_T \cdot \Phi}
\label{eq:abs-cross-section}
\end{equation}
```

### Değişken Tanımları

```
$$
\sigma_{\text{abs}} = \frac{N_R}{N_T \cdot \Phi}
$$

Burada:
- $\sigma_{\text{abs}}$: Absorbsiyon tesir kesiti (barn)
- $N_R$: Reaksiyon sayısı (adet)
- $N_T$: Hedef çekirdek sayısı (adet)
- $\Phi$: Akı (n/cm²/s)
```

### Sık Yapılan Hatalar

❌ Roman font değişken: `$\text{x}$` ✅ italic değişken: `$x$`
❌ İndis düz metin: `$x_max$` ✅ `$x_\text{max}$`
❌ Birim italic: `$10 km$` ✅ `$10 \, \text{km}$`
❌ Çarpım yıldız: `$a*b$` ✅ `$a \cdot b$`

---

## Şekil & Tablo Standartları

### Şekil

```
[Şekil]

Şekil 3.4: Önerilen evrişimsel sinir ağı mimarisi. Girdi katmanı 
1024-boyutlu enerji spektrumunu alır; üç evrişim bloğunu (Conv-BN-ReLU-MaxPool)
takiben tam-bağlı katman 32 sınıf çıktısı üretir.
```

**Kurallar:**
- Tüm şekiller numaralı
- Caption şekilden SONRA
- Atıf gerekirse: `(Smith ve Doe, 2020'den uyarlanmıştır)`

### Tablo

```
Tablo 4.2: Eğitim hiperparametreleri ve seçim aralıkları

| Parametre | Aralık | Seçilen | Kaynak |
|-----------|--------|---------|--------|
| Öğrenme oranı | [1e-5, 1e-2] | 1e-3 | Adam varsayılanı (Kingma & Ba, 2014) |
| Batch boyutu | [16, 128] | 32 | Bellek kısıtı |
| Epoch sayısı | [50, 200] | 100 | Erken durdurma ile |
```

**Kurallar:**
- Caption tablonun ÜSTÜNDE
- Sütun başlıkları kalın
- Birim sütun başlığında

### Türkçe Sayı Formatı

- Ondalık ayracı: virgül (`3,14`)
- Binlik ayracı: nokta (`1.000.000`)

> **Uluslararası dergi hedefi varsa:** Ondalık nokta (`3.14`).

---

## Nükleer Fizik Terminolojisi (TR-EN)

| Türkçe | İngilizce | Sembol | Birim |
|--------|-----------|--------|-------|
| Tesir kesiti | Cross-section | σ | barn (b) |
| Yarı ömür | Half-life | T₁/₂ | s, dk, sa, gün, yıl |
| Bozunum sabiti | Decay constant | λ | s⁻¹ |
| Aktivite | Activity | A | Bq |
| Becquerel | Becquerel | Bq | 1 bozunum/saniye |
| Curie | Curie | Ci | 3.7×10¹⁰ Bq |
| Akı | Flux | Φ | n/cm²/s |
| Enerji | Energy | E | eV, keV, MeV, GeV |
| Çok-kanallı analizör | Multi-channel analyzer | MCA | - |
| İlgi bölgesi | Region of Interest | ROI | - |
| Tam-genişlik yarı-yüksek | Full Width at Half Maximum | FWHM | keV |
| Çekirdek | Nucleus | - | - |
| Çekirdekçik | Nuclide | - | - |
| Aktivasyon analizi | Activation Analysis | NAA | - |
| Gama spektroskopisi | Gamma spectroscopy | - | - |
| Spektrum | Spectrum | - | counts vs energy |
| Sayım | Count | N | adet |
| Sayım hızı | Count rate | - | cps |
| Dedektör | Detector | - | - |
| Dedektör verimi | Detector efficiency | ε | dimensionless (0-1) |
| Pik | Peak | - | - |
| Pik fitleme | Peak fitting | - | (Gaussian) |
| Arka plan | Background | - | counts |
| Doğrusal zayıflama katsayısı | Linear attenuation coefficient | μ | cm⁻¹ |
| Kütle zayıflama katsayısı | Mass attenuation coefficient | μ/ρ | cm²/g |
| Soğurma | Absorption | - | - |
| Saçılma | Scattering | - | - |
| Compton saçılması | Compton scattering | - | - |
| Çift oluşumu | Pair production | - | - |
| Fotoelektrik etki | Photoelectric effect | - | - |
| Doz eşdeğeri | Equivalent dose | H | Sv |
| Soğurulan doz | Absorbed dose | D | Gy |
| İzotop | Isotope | - | - |
| Reaktör | Reactor | - | - |
| Nötron | Neutron | n | - |
| Termik nötron | Thermal neutron | - | E ≈ 0.025 eV |
| Hızlı nötron | Fast neutron | - | E > 1 MeV |
| Sintilasyon dedektörü | Scintillation detector | - | NaI(Tl), HPGe |
| Yarı iletken dedektör | Semiconductor detector | - | HPGe, Si(Li) |
| Yüksek-saflıkta germanyum | High-Purity Germanium | HPGe | - |

---

## AI/ML Terminolojisi (TR-EN)

| Türkçe | İngilizce | Kısaltma |
|--------|-----------|----------|
| Yapay sinir ağı | Artificial Neural Network | ANN, YSA |
| Konvolüsyonel sinir ağı | Convolutional Neural Network | CNN |
| Tekrarlayan sinir ağı | Recurrent Neural Network | RNN |
| Uzun-kısa süreli bellek | Long Short-Term Memory | LSTM |
| Geçitli tekrar birimi | Gated Recurrent Unit | GRU |
| Dönüştürücü | Transformer | - |
| Otokodlayıcı | Autoencoder | AE |
| Değişimsel otokodlayıcı | Variational Autoencoder | VAE |
| Çekişmeli üretici ağ | Generative Adversarial Network | GAN |
| Pekiştirmeli öğrenme | Reinforcement Learning | RL |
| Denetimli öğrenme | Supervised Learning | - |
| Denetimsiz öğrenme | Unsupervised Learning | - |
| Yarı-denetimli öğrenme | Semi-Supervised Learning | - |
| Aktarım öğrenmesi | Transfer Learning | - |
| Aşırı uydurma | Overfitting | - |
| Yetersiz uydurma | Underfitting | - |
| Düzenlileştirme | Regularization | - |
| Geri yayılım | Backpropagation | - |
| Gradyan inişi | Gradient Descent | GD, SGD, Adam |
| Aktivasyon fonksiyonu | Activation function | ReLU, sigmoid, tanh |
| Kayıp fonksiyonu | Loss function | - |
| Optimizatör | Optimizer | - |
| Çapraz doğrulama | Cross-validation | CV |
| Eğitim seti | Training set | - |
| Doğrulama seti | Validation set | - |
| Test seti | Test set | - |
| Karmaşıklık matrisi | Confusion matrix | - |
| Doğruluk | Accuracy | - |
| Kesinlik | Precision | - |
| Duyarlılık | Recall (Sensitivity) | - |
| F1-skoru | F1-score | - |
| Alıcı çalışma karakteristiği | Receiver Operating Characteristic | ROC |
| Eğri altı alan | Area Under Curve | AUC |
| Özellik mühendisliği | Feature engineering | - |
| Özellik çıkarımı | Feature extraction | - |
| Boyut indirgeme | Dimensionality reduction | PCA, t-SNE, UMAP |
| Temel bileşen analizi | Principal Component Analysis | PCA |
| Toplulukla öğrenme | Ensemble learning | - |
| Rastgele orman | Random Forest | RF |
| Gradyan artırımı | Gradient Boosting | XGBoost, LightGBM |
| Destek vektör makinesi | Support Vector Machine | SVM |
| K-en yakın komşu | K-Nearest Neighbors | KNN |
| Kümeleme | Clustering | K-means, DBSCAN |
| Yığın boyutu | Batch size | - |
| Çağ | Epoch | - |
| Erken durdurma | Early stopping | - |
| Hiperparametre | Hyperparameter | - |
| Izgara araması | Grid search | - |
| Sınıflandırma | Classification | - |
| Regresyon | Regression | - |
| Anomali tespiti | Anomaly detection | - |

---

## Kaçınılacak Kalıplar

### "AI Yazısı" Kalıpları

❌ "Çığır açan", "devrim yaratan"
❌ "Şüphesiz ki", "kesinlikle"
❌ "Evrim geçirmiş manzara"
❌ "Önemli bir rol oynar"
❌ "Sürekli artan ihtiyaç"
❌ "İlginç bir şekilde"

### Akademik Olmayan Tepki

❌ "Şaşırtıcı şekilde sonuçlar..."
❌ "Beklendiği gibi..."
❌ "Açıkça görülmektedir ki..."

### Belirsiz Niceleyiciler

❌ "Bazı çalışmalar gösterir ki..." → ✅ "Smith ve Doe (2020) ile Lee ve ark. (2021) ..."
❌ "Çoğu durumda" → ✅ "İncelenen 15 örnekten 12'sinde"
❌ "Genellikle" → ✅ "%73 oranında"

### Sahte Karşıtlık

❌ "Bu yöntem etkilidir, ancak ek araştırma gerektirir."
✅ "Bu yöntem 1024-boyutlu spektrumlarda %92 doğruluk sağlamaktadır;
   ancak 8192-boyutluya ölçeklendirildiğinde bellek tüketimi 8 GB'ı aşmaktadır."

---

## Tezi humanizer ile Temizlerken Dikkat

### ✅ humanizer Yapsın

- Em dash (—) aşırı kullanımı
- "kapsamlı bir şekilde", "etkili bir şekilde" gibi gereksiz takılar
- Chatbot artifaktları (varsa)
- Tireli kelime aşırı kullanımı
- Pohpohlama izleri
- 3'ler kuralı zorlaması

### ❌ humanizer DOKUNMASIN

- Akademik 3. tekil şahıs ("uygulanmıştır")
- Pasif yapı
- LaTeX formülleri
- Atıf yapıları `(Smith, 2020)`
- Teknik jargon (CNN, FWHM, ROI vs.)
- Bilimsel kesinlik ifadeleri (`%92.4 ± 0.3`)

### Uygulama Şekli

```
[Bölüm bölüm humanize et]

humanize this academic Turkish text. CRITICAL:
- Preserve all citations (Author, Year)
- Preserve all LaTeX formulas (between $)
- Preserve all numbers with units (%92.4, 1.5 MeV)
- Preserve passive constructions ("uygulanmıştır", "elde edilmiştir")
- Preserve technical terms (CNN, FWHM, ROI)
- Only remove: em-dash overuse, hedging filler, three-rule abuse,
  hyphenated word-pair overuse

[Yapıştır metin]
```

humanizer'ı sadece **danışmana göndermeden önce SON pass** olarak çalıştır.

---

## Kalite Kontrol Listesi

### Tez Bölümü Bittiğinde

- [ ] Tüm formüller LaTeX, numaralı, değişkenleri tanımlı
- [ ] Tüm şekil/tablolar caption'lı, numaralı, referans verilmiş
- [ ] Atıf formatı tutarlı (APA veya IEEE — karışık değil)
- [ ] Kaynakça'da olmayan atıf metinde yok, tersi de yok
- [ ] Kısaltma ilk geçişte tam ad
- [ ] Sembol ilk geçişte tanımlanmış
- [ ] "Muhtemelen", "genellikle" gibi belirsiz ifade yok
- [ ] Spekülatif iddia yok
- [ ] Türkçe yazım denetimi (Word + manuel)
- [ ] Mantık akışı düzgün
- [ ] Cümle uzunluğu ortalama 15-25 kelime
- [ ] Pasif yapı tutarlı
- [ ] Sayısal değerlerde birim
- [ ] Birim formatı tutarlı

### Tüm Tez

- [ ] İçindekiler güncel
- [ ] Şekiller listesi güncel
- [ ] Tablolar listesi güncel
- [ ] Simgeler ve kısaltmalar listesi güncel
- [ ] Sayfa numaraları doğru
- [ ] Kaynakça alfabetik (APA) veya numara sırası (IEEE)
- [ ] Cross-reference doğru
- [ ] Üniversite tez şablonu marjları
- [ ] PDF/A formatı (arşiv)
- [ ] Plagiarism check (Turnitin) yapıldı

---

## Pandoc İpuçları (Markdown → Tez PDF)

```bash
pandoc \
  -F pandoc-crossref \
  --citeproc \
  --csl=apa.csl \
  --bibliography=kaynakca.bib \
  --pdf-engine=xelatex \
  -V lang=tr \
  -V mainfont="Times New Roman" \
  -V geometry:margin=2.5cm \
  -V linestretch=1.5 \
  -o tez.pdf \
  thesis/00-icindekiler.md \
  thesis/01-giris.md \
  thesis/02-yontem.md \
  thesis/03-bulgular.md \
  thesis/04-tartisma.md \
  thesis/05-sonuc.md
```

---

*Thesis Writing Guide v1.0 | 2026-05-02*
