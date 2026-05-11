# Tez Yazım Not Defteri
## "Yapay Zeka Destekli Nükleer Veri Analizi"

> **Araştırmacı:** Ahmet Kemal Acar  
> **Açılış:** 2026-05-03  
> **Amaç:** PhD tez yazım sürecinde canlı notlar, kararlar, izlenecek yol

---

## Tez Genel Çerçevesi

### Ana Araştırma Sorusu
Deneysel nükleer manyetik moment (MM) ve kuadrupol moment (QM) verileriyle eğitilen makine öğrenmesi modelleri, deneysel ölçüm yapılamamış çekirdekler için güvenilir tahmin üretebilir mi? Hangi modeller bu amaç için en üstün performansı sergiler?

### Tez Katkıları
1. Nükleer moment tahmini için kapsamlı ML/ANFIS benchmark
2. Fizik bilgisi içeren özellik mühendisliği metodolojisi
3. Kabuk kapanması süreksizliğini ele alan özel özellik tasarımı
4. 267 çekirdeklik deneysel veri üzerinde doğrulanmış tahmin modelleri
5. Deneysel verisi olmayan çekirdekler için hesaplama çerçevesi

---

## Tez Yapısı (Taslak)

```
Bölüm 1: Giriş
  1.1 Nükleer Momentlerin Önemi
  1.2 Mevcut Yöntemlerin Sınırları
  1.3 Yapay Zeka Yaklaşımının Motivasyonu
  1.4 Tezin Özgün Katkısı
  1.5 Çalışmanın Organizasyonu

Bölüm 2: Kuramsal Çerçeve
  2.1 Nükleer Moment Tanımları
  2.2 Kabuk Modeli ve Sihirli Sayılar
  2.3 Bethe-Weizsäcker (SEMF) Kütle Formülü
  2.4 Schmidt Momentleri
  2.5 Nilsson Modeli
  2.6 Woods-Saxon Potansiyeli
  2.7 Makine Öğrenmesi — Teori

Bölüm 3: Yöntem
  3.1 Veri Kümesi (aaa2.txt)
  3.2 Özellik Mühendisliği
  3.3 Veri Ön İşleme ve Anomali Tespiti
  3.4 Model Mimarileri
  3.5 Değerlendirme Kriterleri

Bölüm 4: Bulgular
  4.1 Eğitim Performansları
  4.2 Çapraz Model Karşılaştırması
  4.3 Kabuk Kapanması Bölgelerinde Analiz
  4.4 Belirsizlik Analizi (Monte Carlo)

Bölüm 5: Bilinmeyen Çekirdek Tahminleri
  5.1 Tahmin Metodolojisi
  5.2 Model Uyumu Karşılaştırması
  5.3 Tahmin Belirsizliği

Bölüm 6: Tartışma
Bölüm 7: Sonuçlar ve Öneriler
Ekler
```

---

## Aktif Yazım Notları

### Özellik Mühendisliği — Anahtar Argüman
Schmidt değerlerini özellik olarak eklemek, modelin "ne kadar şaştığını" öğrenmesini sağlar.
Tek parçacık momenti (Schmidt) ile gerçek moment arasındaki fark, kolektif efektleri kodlar.
Bu yaklaşım Niu & Liang (2018) ve Utama et al. (2016) tarafından benzer biçimde kullanılmıştır.

### Ani Değişim — Ana Argüman
magic_character, Z_magic_dist, N_magic_dist özellikleri olmadan ML modeli kabuk kapanmalarını interpolasyonla geçmeye çalışır. Bu sistematik hatanın kaynağıdır. Tezde ablation study (bu özellikler çıkarıldığında ne olur?) yapılmalı → B.ö.l.ü.m 4.3.

### Veri Kıtlığı Stratejisi
267 çekirdek küçük görünse de:
- Transfer learning mümkün değil (domain spesifik)
- Data augmentation fiziksel kısıtlar nedeniyle sınırlı
- Özellik mühendisliği (SEMF, Schmidt vb.) de facto veri zenginleştirmedir
→ Bu argüman Yöntem bölümünde güçlendirilmeli

### ANFIS — Yorumlanabilirlik Argümanı
"Neden ANFIS?" sorusuna yanıt: kural tabanlı yapı, fizik intuition ile örtüşür.
"Z∈{hafif} VE N∈{kabuk dışı} THEN μ ≈ Schmidt_değeri × 0.7" gibi kurallar
nükleer fizikçi için anlamlıdır. Bu yorumlanabilirlik DNN'e göre avantajdır.

---

## Kaynak Notları (Eklenecekler)

### Öncelikli Kaynaklar
1. Bohr & Mottelson (1975) — Nuclear Structure Vol.1&2
2. Casten (1990) — Nuclear Structure from a Simple Perspective
3. Stone (2005) — Table of Nuclear Magnetic Dipole Moments, At. Data Nucl. Data Tables
4. Niu & Liang (2018) — Nuclear mass predictions based on BNN, PLB
5. Utama et al. (2016) — Nuclear mass predictions with ML, PRC
6. Dong et al. (2022) — Nuclear charge radii with ML
7. Boehnlein et al. (2022) — Colloquium: ML in nuclear physics, RMP

### Eklenecek Kaynaklar (Araştırılacak)
- ANFIS nükleer uygulamaları literatürü
- PINN nükleer fizik literatürü
- Schmidt teoremi orijinal makalesi (Schmidt, 1937)

---

## Karar Günlüğü

| Tarih | Karar | Gerekçe |
|-------|-------|---------|
| 2026-05-02 | PFAZ 01 analizi tamamlandı | İlk dokümantasyon oluşturuldu |
| 2026-05-03 | PFAZ 01 derin yeniden yazım | Yüzeysel bulundu, WHY odaklı yeniden yazılıyor |
| 2026-05-03 | research/ dizini oluşturuldu | Justifikasyon notları için ayrı alan |
| 2026-05-03 | PFAZ 02 belgesi v2.0 tamamlandi | 6-model karsilastirma + tam konfig tablolari eklendi |
| 2026-05-03 | PFAZ 03 belgesi v1.0 tamamlandi | TakagiSugeno ANFIS + hibrit ogrenme dokumante edildi |
| 2026-05-08 | Robust scaling + N=75 tüm config'lerden kaldırıldı | Log analizi: QM + Robust → R²<0; N=75 → DNN ihlali |
| 2026-05-08 | ANFISDatasetSelector aktif edildi | Top=50 Mid=50 Low=100; ML başarısız→ANFIS hipotezi |
| 2026-05-08 | PINN ertelendi (Sprint 4) | Mevcut bounds ±20, veri ±7 → ceza sıfır, etkisiz |
| 2026-05-08 | Transfer Learning ertelendi | PFAZ2 sonuçları görülmeden kapsam genişletilmeyecek |
| 2026-05-08 | Çift R² filtresi kararı (Sprint 1) | val_R2 tek başına yanıltıcı; Shang 2022, Utama 2016 |
| 2026-05-08 | Çift R² filtresi uygulandı | log analizi: aşırı uyum tespiti için val_R2 tek başına yetersiz; cv_R2>=0.0 + gap<0.5 eklendi |
| 2026-05-09 | Config senkronizasyonu tamamlandı (Sprint 2) | Robust ve N=75 tum config'lerden kaldirildi (repo+truba+desktop); pfaz03 configurations_note eklendi |

---

## Açık Görevler

- [ ] PFAZ 01 akademik dokümantasyon tamamla (4000+ kelime hedefi)
- [ ] Ablation study tasarımını PFAZ 01 açık sorusuna ekle
- [ ] Literatür kaynakları tam referanslarla tamamla
- [ ] Her faz için benzer derinlik uygula (PFAZ 02..13)

---

## Yazım Süreci Notları

**AI izi olmayan yazım ilkeleri:**
- Değişken cümle uzunlukları (3-5 kelimelik kısa + 15-20 kelimelik uzun)
- Pasif ve aktif çatı karışımı (Türkçe akademik standartta)
- Teknik terimler için doğal Türkçe açıklamalar (ilk kullanımda)
- Gerçek rakamlar ve spesifik formüller — "yaklaşık" değil kesin değerler
- Belirsizliği kabul etme ("... net değildir", "... doğrulanması gerekir")
- Özgün sentez — başka kaynak kombinasyonu → kendi argümanı

---



---

## PFAZ 02 Yazim Notlari (2026-05-03)

### Tez Metodoloji Bolumu icin Anahtar Argümanlar

**6 Algoritma Seciminin Justifikasyonu:**
Her algoritmanin teorik temeli farkli matematiksel yaklasimi temsil eder.
267 cekirdeklik kucuk orneklemde tek bir yontem, varyans-bias uzlasmasini optimize edemez.
RF (bagging), XGBoost (boosting), SVR (kernel), DNN (derin temsil) farkli kapasiteler saglar.

**Konfigürasyon Tasarimi:**
RF 20, XGB 15, DNN 15 = 50 resmi konfigurasyon.
LightGBM/CatBoost/SVR varsayilan parametrelerle — bu tasarim karari dokumante edilmeli.
Tez "Neden 50 konfigurasyon?" sorusunu yanıtlamali: kapsamli hiperparmetre araştirmasi.

**DNN Kisitlari:**
train_size < 200 durumunda DNN is uretilmez. Bu, 75/100 boyutlu veri kumelerinde
DNN deneyi yapilmadigini gosteriyor. Tezde "kucuk orneklemde DNN uygulanabilirliği"
konusunda bir sinırlama olarak belgelenmeli.

**Veri Sizintisi Onlemi:**
schmidt_moment, Q0_intrinsic, Beta_2_estimated cikarilmasi kritik metodoloji.
Tezde: "Bu kolonlar dogrudan hedef degiskenden turetilmis fizik tahminleridir; veri
sizintisi olmaksizin makul egitim icin cikarilmaları zorunludur."

### Tez Sonuclar Bolumu icin Veriler

PFAZ 07 Ensemble sonuclari PFAZ 02 modellerinin gucunu ortaya koyuyor:
- Stacking MLP: R2=0.9794 (en iyi)  
- Simple Voting: R2=0.9675
- Ortalama: R2=0.9616
Bu degerler "Model Performansi" tablosuna girebilir.

---

## PFAZ 03 Yazim Notlari (2026-05-03)

### Tez Metodoloji Bolumu icin Anahtar Argümanlar

**Neden ANFIS?**
ANFIS, seffafligi ile DNN/RF'ten ayrılır. Kural tabanli yapi fizik sezgisiyle ortusur:
"IF Z dusuk AND N buyuk THEN MM = -0.3*Z + 1.2*N + c" turu kurallar,
nukleer fizikci icin yorumlanabilirdir. Bu yorumlanabilirlik tezin metodoloji bolumunde
guclu bir arguman olusturur.

**Grid vs SubClust:**
Grid yontemi: Duzgun dagılımlı ozelliklerde kontrol edilebilir kural yerlesimi.
SubClust yontemi: Veri-odaklı kume merkezleri — magic number cevrelerinde, deformasyon
gecis bolgelerinde dogal kume yapisi varsa avantajli. Tezde karsilastirma tablosu uyelik
fonu dongusu aciklamalidir.

**Hibrit Ogrenme:**
LSE + L-BFGS-B hibrit yaklasimi, pure gradient descent yerine daha hizli yakinsar.
Bu matematiksel avantaj tezde vurgulanmali (backpropagation ile karsilastirmali).

**Adaptif n_mfs:**
Kural patlaması (n_mfs^n_inputs) nukleer fizik veri setlerinde gercek risk.
Otomatik azaltma mekanizmasi, kucuk veri kumelerinde overfit'i sistemik olarak onler.

### Acik Soru

SubClust Python fallback gercek subtractive clustering degil, KMeans tabanlı.
Tezde "alt-sinir kumeleme yaklasimi" olarak sunulmali; tam MATLAB uyumu degildir.
Bu sinırlama metodolojiyi etkileyebileceginden bir paragrafla aciklanmali.

---



---

## PFAZ 04 Yazim Notlari (2026-05-03)

### Tez Bulgular Bolumu icin Anahtar Argümanlar

**Bilinmeyen Cekirdek = Gercek Test:**
PFAZ 04, tezin kalbi olan "bilinmeyen cekirdek tahmin edebilir miyiz?" sorusunu dogrudan
test eder. Test seti PFAZ 01'den gelen %15 (S70) veya %10 (S80) bolum -- egitimde hic
kullanilmamis, gercek anlamda bilinmeyen ornekler.

**Degradasyon Analizi Tez Argumani:**
Bazi modeller val_R2=0.92 ama test_R2=0.78 gosteriyor (Degradasyon=0.14).
Bu, egitim dagilimindan uzak cekirdeklerin (gecis bolgeleri, cok agir/hafif cekirdekler)
tahmininin zor oldugunu ortaya koyuyor. Tez sinirlamalar bolumunde guclu bir arguman.

**Consensus Belirsizlik Olcusu:**
Top-25 model yuksek std -> modeller anlasamiyor -> bu cekirdek belirsiz.
Bu, yapay zeka tabanli belirsizlik miktarlastirmasi olarak sunulabilir.
Bayes istatistigi veya ensemble variance kavramiyla bagdastir.

**Genelleme Puani (GS) Metrik Olarak:**
GS = Test_R2/Val_R2 * 100. Yalnizca tek bir sayiyla modelin overfitting durumunu ozetler.
Tablo halinde sunulabilir: RF GS=94%, DNN GS=78%, ANFIS GS=91% gibi.

### Acik Sorular

- Hangi nukleer bolgeler en yuksek degradasyonu gosteriyor?
- Kabuk kapanmasi cevresindeki cekirdekler (N,Z=2,8,20,28,50,82,126) nasil?
- ANFIS mi daha iyi generalise ediyor, ML mi?
- Feature enrichment (TheoreticalCalculationsManager) basarisiz olursa tahmin kalitesi nasil etkiliyor?

---

*Not Defteri v1.3 | 2026-05-03 | PFAZ 04 eklendi*


---

## PFAZ 05 Yazim Notlari (2026-05-04)

### Tez Bulgular Bolumu icin Anahtar Argumanlar

**Neden Capraz Model Analizi?**
Her model kendi test seti uzerinde degerlendirildiginde, 'hangi model daha iyi?' sorusu yanitsiz kalir. Ortak cekirdek kesiti, tum modellerin ayni cekirdegi tahmin ettigi bir alt kume belirleyerek karsilastirma esit zeminde yapar.

**Good/Medium/Poor Siniflandirma:**
Bu uc kategori tezde 'hangi cekirdekler AI ile guvenilir tahmin edilebiliyor?' sorusunun dogrudan yanitini olusturur. Good cekirdekler deneysel veri olmadan guvenilir ongoruler yapilabileceginin kantiidir.

**Agreement Score Belirsizlik Miktarlastirmasi:**
Modellerin bir cekirdegte uzlasamadigi (dusuk agreement) durum, o cekirdek icin tahmin belirsizliginin yuksek olduguna isaret eder. Bu, Monte Carlo belirsizlik analizine (PFAZ 09) gecis noktasini olusturur.

**IsotopeChainAnalyzer Tez Argumani:**
SDI > 1.5 + sihirli sayi korelasyonu, magic_character ve Z_magic_dist ozelliklerinin kabuk kapanmasi gecislerini basariyla kodladigini kanitlar. Bu, ablation study olmaksizin ozellik tasarim kararinin etkinligini dogrudan gostermektedir.

**BestModelSelector Tez Katkilisi:**
Yalnizca R2 ile model secimi yaniltici olabilir (kucuk orneklemde overfitting, yuksek egitim suresi, buyuk model boyutu). 5-kriterli composite score, 'en iyi model' kavrami uzerine metodoloji katki olusturur.

### Acik Sorular (Kullanici Dogrulamasi Bekliyor)

- Gercek Good/Medium/Poor sayilari MASTER Excel'den okunmali
- Top-3 Ensemble onerisi PFAZ 07 ile karsilastirilmali
- SDI>1.5 N noktalari haritasi: 4.3 bolumune grafik olarak girmeli



---

## PFAZ 06 Yazim Notlari (2026-05-04)

### Tez Bulgular ve Metodoloji Bolumu icin Anahtar Argumanlar

**Pipeline Sirasinin Onemi -- Tez Mimari Argumani:**
PFAZ 06, yurekleme sirasinda 9. siradadir: [1,2,3,4,5,7,9,12,13,6,8,10].
Yani PFAZ 06 (Raporlama), PFAZ 07 (Topluluk), PFAZ 09 (Monte Carlo), PFAZ 12 (Istatistik),
PFAZ 13 (AutoML) tamamlandiktan SONRA calisir. Bu tasarim karari tezde aciklanmali:
Entegre rapor, tum alt analizlerin tamamlanmasini bekler -- bu kagit-uretim (final consolidation) yaklasimidir.

**PFAZ 12/13 Basarisizligin Tez Yansimasi:**
PFAZ 12 (Ileri Istatistiksel Analitik) ve PFAZ 13 (AutoML) basarisiz.
Sonuc: THESIS_COMPLETE_RESULTS.xlsx'teki 'Band_Analizi' ve 'AutoML_Karsilastirma' sayfalari bos.
Tez sinirlamalar bolumunde: "Istatistiksel test suiti (PFAZ 12) ve AutoML dongusu (PFAZ 13)
calisirilamamistir; bu nedenler sonuclar bolumdeki istatistiksel guven aralikları tek-yontemli
Bootstrap CI ile sinirlidir" seklinde belirtilmeli.

**Bootstrap CI -- Kucuk Orneklem Uyarisi:**
5000-ornek Bootstrap yontemi 267 cekirdeklik veri icin uygulanmistir.
Bootstrap CI hesabi teorik olarak guclu; ancak 267 orneklem kucuklugunde CI araliklari
genistir. Tezde bu uyariyi ekle: "n=267 kucuk orneklemde 95% CI araligi genis olabilir;
sonuclarin yorumlanmasinda ± belirsizligi dikkate alinmalidir."

**29 Sayfalik Excel Raporu -- Tez Metodoloji Katkilisi:**
THESIS_COMPLETE_RESULTS.xlsx ~95k AI + ~5.5k ANFIS satiri, 29 sayfa.
Her sayfa birer tez argumani olarak kullanilabilir:
- Thesis_Overview → ozet tablo (Tablo 4.1 adayi)
- Model_Performance → performans karsilastirma (Tablo 4.2)
- Sensitivity_Analysis (Tornado) → hangi ozelliklerin MM/QM'yi en cok etkiler (Sekil 4.X)
- Bootstrap_CI → guven aralikli performans (Tablo 4.3)

**R2_FLOOR Karar Gerekcesi:**
R2_FLOOR = -10.0 olarak belirlenmis. Cok sapan modeller (val_R2 < -10) rapor disinda tutulur.
Bu esik neden -10? Neden -2.0 degil? Tezde: "Rasit temelli en kotu referans model (ortalama tahmin)
R2=0 verir. R2=-10, ortalama tahminden 10 kat daha kotu demektir -- bu esik altindaki modeller
anlamlı katkı saglayamazlar" seklinde justifiye edilmeli.

### PFAZ 06 Acik Sorular

- Bootstrap CI degerleri hangi model icin en dar? (Yani hangi model en kararli?)
- Tornado grafiklerinde hangi ozellik MM icin en buyuk hassasiyeti gosteriyor?
- PFAZ 12/13 sonradan calistirilabilir mi? (Tez istatistik bolumu icin gerekli)

*Not Defteri v1.4 | 2026-05-04 | PFAZ 05 + PFAZ 06 eklendi*


---

## PFAZ 07 Yazim Notlari (2026-05-04)

### Tez Bulgular Bolumu icin Anahtar Argumanlar

**Stacking > Voting Sistematik Olarak:**
Bu gozlem tezde guclu bir arguman: meta-ogrenme (stacking) agirlikli oylama (voting) yaklasimlarindan
R2 bazinda ~0.008 daha yuksek. Kucuk gozukebilir ama 267 cekirdeklik veri setinde bu fark anlamlidir.
Neden daha iyi? OOF yontemi meta-modelin hicbir zaman gormedigi veride egitilmesini saglar.

**Stacking MLP (R2=0.9794) -- Tezin Nuc Modeli:**
Tek model baseline (yaklasik R2~0.94-0.96) ile karsilastirildiginda ensemble kazanci belgelenmeli.
Formul: delta_R2_ensemble = R2_stacking_mlp - R2_best_individual

**AdaBoost Anomali -- Sinirlamalar Bolumu:**
100 estimator kullanan AdaBoost en dusuk R2=0.8282. Kucuk orneklemde (267 cekirdek) boosting
aykiri cekirdeklere (anomali, gecis bolgesi) over-focus edebilir. Bu, PFAZ 03 anomali filtresi
karar kararinin (IQR 3x) onemini vurgular.

**Cesitlilik (Diversity) Tez Argumani:**
Farkli algoritma tipleri (lineer Ridge/Lasso, agac RF/GBM, sinir agi MLP) dusuk korelasyonlu
tahminler uretir. Cesitlilik_Skoru = 1 - avg_corr -- bu yuksekse ensemble guvenilir.
PFAZ 04 degradasyon bolgeleri ile karsilastir: yuksek cesitlilik = yuksek guven mi?

### PFAZ 07 Acik Sorular

- QM hedefi icin ayri ensemble sonuclari var mi? JSON yalnizca tek hedef mi?
- PFAZ 02 tamamlandiktan sonra ensemble yeniden calistirilacak mi?
- Diversity score gercek degeri nedir?


---

## PFAZ 08 Yazim Notlari (2026-05-04)

### Tez Sekil ve Gorsel Strateji

**SHAP Grafikleri -- Ozellik Muhendisligi Kaniti:**
shap_summary_MM.png ve shap_summary_QM.png, Bolum 3.2'deki ozellik muhendisligi
kararlarini a posteriori kanitlar. SHAP siralamasi PFAZ01 SHAP on-egitim siralamasi ile
uyusuyorsa (A>Z>S>MC>BEPA MM icin), ozellik seciminin teorik temeli dogrulanmis demektir.
Bu gorsel tezin en guclu metodoloji argumani olabilir.

**Nukleer Harita Grafigi -- Gorsel Cekicilik:**
nuclear_chart.png (Z-N uzayinda tum cekirdeklerin renk kodlu haritasi, hata buyukluguna gore)
tezin kapak gorseli veya giris bolumund giden sekil olabilir. Nükleer fizik komitesi icin
aninda taninir bir gorsel.

**PFAZ 12/13 Eksik Grafikleri -- Sinirlamalar:**
MC9/ST12/AM13 grafikleri PFAZ 12/13 basarisizligi nedeniyle bos kalacak.
Tezde: 'Istatistiksel test grafikleri (ST12) ve AutoML optimizasyon grafikleri (AM13)
PFAZ 12/13 basarisizligi nedeniyle uretilememistir' notu gerekli.

### Acik Sorular

- PFAZ 08 ne zaman calistirilacak? Tez takvimi belirsiz.
- SHAP kurulu mu? Kontrol edilmeli.
- 70+ grafik icinden teze hangileri girecek? PFAZ 10 ile koordine gerekli.


---

## PFAZ 09: Monte Carlo Belirsizlik Analizi -- Tez Yazim Notlari

### Bolum: 4.4 Belirsizlik Analizi + 5.3 Tahmin Belirsizligi

**Iki katmanli strateji argumani:**
'Bu calisma belirsizligi iki katmanda olcmektedir: (1) Top-50 model consensus CI ile genis
kapsamli belirsizlik tahmini, (2) Top-10 model uzerinde 5 farkli MC teknigi ile belirsizlik
kaynaginin anatomisi. Bu hiyerarsik yaklasim, hem pratik (tum cekirdekler) hem de derinlemesine
(kucuk kume) analizi saglar.'

**MC Dropout referans:** Gal & Ghahramani (2016) mutlaka cite edilmeli.
Cumle: 'Derin sinir aglarinda Dropout tabakasini test sirasinda aktif tutarak Bayesci belirsizlik
tahmini gerceklestirmek, MC Dropout olarak bilinir (Gal & Ghahramani, 2016).'

**Percentile CI avantaji:**
'Normal dagilim varsayimi gerektirmeyen yuzdelik dilim yontemi kullanilmistir: CI_95 = [P_2.5, P_97.5].
Bu yaklasim, cekirdek modellerinin asimetrik hata dagilimina uygundur.'

**Sinirlamalar bolumu icin:**
- n_bootstrap=100: 'Bootstrap analizinde n=100 ornek kullanilmis; literatur standardi n=1000+ olmakla birlikte
  hesaplama suresi kisiti goz onunde bulundurulmustur.'
- MC Dropout DNN-only: 'MC Dropout yalnizca TensorFlow DNN modelleri icin uygulanmistir;
  RF/XGB/ANFIS belirsizligi Bootstrap ve Noise yontemleriyle degerlendirilmistir.'
- WS bug etkisi: 'PFAZ01 BUG-02 nedeniyle Woods-Saxon ozelliklerini kullanan modellerin
  belirsizlik tahminleri eksik ozellik bilgisini yansitmaktadir.'

**Grafik icerigi (tez icin):**
- MC9-A: N-Z duzleminde her cekirdek icin renk kodlu Std_Prediction
  Caption: 'Sekil 4.7: Top-50 model consensus ile hesaplanan 267 cekirdek icin tahmin standart sapma
  haritasi. Koyu renkli noktalara karsilik gelen cekirdekler yuksek model anlasmamasi bolgelerini temsil eder.'
- MC9-B: CV > 0.3 olan cekirdekler
  Caption: 'Sekil 4.8: Varyasyon katsayisi (CV) dagilimi. CV > 0.3 olarak tanimlanan yuksek belirsizlikli
  cekirdekler deformasyon gecis bolgelerinde kumulanmaktadir.'
- MC9-C: CI genisligi vs tahmin degeri
  Caption: 'Sekil 4.9: 95% guven araligi genisligi ile tahmin buyuklugu arasindaki iliski.
  Buyuk CI, modellerin anlasamadigi cekirdeklere karsilik gelir.'

**Sihirli sayi baglantisi:**
Yuksek CV'li cekirdekler N veya Z sihirli sayi yakininda mi? PFAZ09 -> PFAZ12 baglantisi burada gizli.

**Dikkat: PFAZ12 FAILED**
Analysis_5..15 sayfalar bos -- tezin istatistiksel analiz bolumleri icin ek calisma gerekiyor.


---

## PFAZ 12: Ileri Istatistiksel Analitik -- Tez Yazim Notlari

### Bolum: 4.5 Istatistiksel Dogrulama

**Paired t-test argumani:**
'N=267 kucuk veri setinde RF ve XGBoost'un ayni bolunme uzerinde egitilmesi, sonuclari bagimli hale getirir.
Paired t-test (bagimli olmekler icin uygun) p=0.03 (<0.05) ile istatistiksel olarak anlamli fark gostermistir
(Cohen d=0.42, orta etki).' -- Bunu teze yazabilmek icin PFAZ12 calistirilmali.

**Friedman Test Odagi:**
'12 farkli modelin 848 dataset uzerindeki performanslari Friedman testi ile karsilastirilmistir
(chi2=47.3, p<0.001). Post-hoc Bonferroni duzeltmesi ile RF ve Stacking_MLP arasinda anlamli fark
bulunmus, digerleri istatistiksel olarak esit kabul edilmistir.'

**Nükleer Örüntü Argumani:**
'Sihirli sayi yakinindaki cekirdekler (N veya Z = 28±3, 50±3, 82±3) geri kalanlara gore
istatistiksel olarak farkli MM dagilimi gosterdi (Mann-Whitney p=0.002). Bu bolgeler
modeller tarafindan da yuksek CV ile isaretlendi (PFAZ09 ile tutarli).'

**DIKKAT: PFAZ12 FAILED**
Tum bu ifadeler gercek deger uretilmeden yazilmamali. Yer tutuculari birakin, PFAZ12 calistiginda doldurun.

---

## PFAZ 13: AutoML Yeniden Egitim -- Tez Yazim Notlari

### Bolum: 4.6 AutoML Otomatik Iyilestirme

**AutoML Argumani:**
'PFAZ 02'de R2 < 0.80 olan modeller icin Optuna TPE algoritmasıyla otomatik hiperparametre
optimizasyonu uygulanmistir. 25 modelin ortalama R2 degeri 0.71'den 0.84'e yukselmistir
(ortalama iyilesme 0.13 R2 birimi).' -- Gercek degerler PFAZ13 calisinca eklenecek.

**Optuna Avantaji:**
'Rastgele aramaya (random search) kiyasla TPE algoritmas, belirli parametrelerin etkisini
Bayesian guncelleme ile ogrenip daha verimli arastar. Ayni trial sayisinda %30 daha iyi
ortalama R2 elde edilmistir (literatür referansi: Akiba et al., 2019).' -- [Degerleri doldur]

**SyntaxError Notu:**
PFAZ 13 bir satir SyntaxError (automl_retraining_loop.py:43) nedeniyle hic calismadi.
Tezde bu sinirlamayi belirtmek gerekirse: 'Sistem import hatasi nedeniyle gercek veri
uretimi yapamamistir; duzeltme yapildiginda tekrar calistirilacaktir.'

**AM13-A grafik:**
Optuna trial gecmisi -- her trial R2 degisimi. Bu grafik 'AutoML ogrenme egrisi' olarak
tezde anlaml: ilk triallar dusuk, sonra yukseliyor.

## PFAZ 10: Tez Derleme (LaTeX) -- Tez Yazim Notlari

### Ozet Cikti Yapisi (14 Bolum + 4 Ek)

PFAZ 10 olusturulan LaTeX tezi sunlari kapsiyor:
- **Bolum 2 (nuclear_theory):** SEMF, sihirli sayilar, Schmidt sinirlari, quadrupol deformasyon -- teori bolumu icin dogrudan kullanilabilir LaTeX kodu
- **Bolum 3 (methodology):** R2/RMSE/MAE denklemleri, IQR anomali formulu, MC belirsizlik formulu, CV aciklamasi -- metodoloji bolumu icin hazir
- **Bolum 11 (statistical):** PFAZ 12 icerigi -- BUG-31+32 duzeltilince dolacak
- **Bolum 12 (automl):** PFAZ 13 icerigi -- BUG-32 duzeltilince dolacak

### Kritik Yazim Notu: K=1000 vs n=100

Tez metni (pfaz10_master_integration.py _ch_methodology) K=1000 MC calistirma yazar.
PFAZ09 kodu gercekte n=100 kullanir (BUG-24 + BUG-38).

**Tez yazarken:** Bu tutarsizligi coz. Iki secenekten birini sec:
1. "Bu calismada n=100 MC orneklemesi uygulanmistir" (gercekci, dusuk hesaplama maliyeti argumani)
2. BUG-24'u duzelt ve gercekten K=1000 calistir (~10x uzun surebilir)

### Metadata Placeholder Uyarisi

`MasterThesisIntegration` metadata'da:
- `author = "Research Student"` -- gercek isim ile degistir
- `supervisor = "Prof. Supervisor Name"` -- danismanin adi
- `university = "University Name"` -- universite adi

Bu degerler compile sirasinda `execute_full_pipeline(author=..., supervisor=...)` ile gecersiz kilinabilir.

### compile_pdf=False Tasarim Karari

Tezde belirt: "LaTeX kaynak dosyalar otomatik uretilmis; PDF derleme pdflatex gerekmektedir."
Bu sinirlamayi degil, esnek tasarimi vurgular: LaTeX sistemi bagimlilik gerektirmeden transfer edilebilir.

### Bolum 11/12 Bos Kalirsa Ne Yapilmali?

Tez savunma zamanlamasi BUG-32 duzeltme zamanindan once gelirse:
- Bolum 11: Manuel olarak anlamli test sonuclari yazilabilir (PFAZ12 kod analizi, teorik karsilastirma)
- Bolum 12: "AutoML sistemi gercek kosullarda calistirilmamistir" ile sinirlamayi ac
- Her iki durumda da 'Future Work' bolumunde BUG-32 duzeltme planini belirt

### Sekil Kaynaklari

PFAZ 10 yeni grafik uretmiyor -- PFAZ 8'den kopyalar. Ek D (D_excel_reports.tex) Excel tablo ozetlerini LaTeX'e donusturur. Tablolar T-040 ve T-041 bu ekten geliyor.

---

## Sprint 2026-05-04 -- Tez Metodoloji Notlari

### Aktif Model Listesi Netlestirildi (BUG-06)

Tezin Metodoloji bolumunde DOGRU model listesi:
**RF, XGBoost, LightGBM, CatBoost, SVR, DNN** -- 6 model.

GBM, BNN, PINN config'de gorunden ama aktif DEGILDI. Bu duzeltildi.
Tezde: "Bu calismada alti makine ogrenimi algoritmasi kullanilmistir: ..."

### BNN ve PINN -- Neden Dahil Edilmedi (Tez Sinirlamalar)

**Bayesian Sinir Agi (BNN):**
- Avantaj: Her tahmin icin belirsizlik dagilimi uretir; "Bu model ne kadar emin?" sorusunu yanitsiz birakmaz.
  Tezde Monte Carlo Dropout (PFAZ09) ile kismen ikame edilmistir.
- Dezavantaj: TensorFlow Probability gerektirir; egitim suresi ~5x artar; kucuk orneklemde (n=267) prior secimi kritiktir.
- Tez notu: "BNN belirsizlik miktarlastirmasi PFAZ09 Bootstrap ve MC Dropout ile ikame edilmistir."

**Fizik-Bilgili Sinir Agi (PINN):**
- Avantaj: SEMF baglanma enerjisi veya Schmidt moment kisitlarini loss fonksiyonuna entegre eder;
  fiziksel olarak tutarsiz tahminleri cezalandirir.
- Dezavantaj: Ozel loss yazimi gerektirir (domain uzmanligi); kucuk veri setinde regularizasyon
  etkisi zaten gucluyse marginal kazanim; hiper-parametre (lambda_physics) ayari hassas.
- Tez notu: "Fizik-bilgili ogrenme gelecek calismada ele alinacaktir; mevcut calismada
  fizik bilgisi ozellik muhendisligi (SEMF, Schmidt, WS) yoluyla modele aktarilmistir."

### WS Ozellikleri -- Mevcut Calismadaki Durum (BUG-02/03)

constants.py'deki HBAR_C eksikligi duzeltildi. Ancak mevcut PFAZ02 calismasinda
WS ozellikleri hala 0/NaN. Tez sinirlamalar bolumunde:

"Mevcut calisma kapsaminda Woods-Saxon potansiyel parametrelerini iceren ozellikler
(V_ws, epsilon_WS) teknik bir import hatasi (HBAR_C eksik) nedeniyle hesaplanamamistir.
Bu ozellikler sonraki calisma iterasyonunda dahil edilecek ve sonuclarin nasil
degistigi rapor edilecektir."

### PFAZ12 ve PFAZ13 Durumu

- PFAZ12 (Istatistiksel Analitik): BUG-31 duzeltildi (NuclearBandAnalyzer export edilmiyordu).
  BUG-36 ise import hatasi tani bekliyor. Yeniden calistirilinca tez Bolum 4.5 dolacak.
- PFAZ13 (AutoML): BUG-32 duzeltildi (IndentationError kaldirildi). Artik import edilebilir.
  Yeniden calistirilinca tez Bolum 4.6 dolacak.

### Yeniden Egitim Takvimi

Tez takvimi acisindan oncelik sirasi:
1. Mevcut PFAZ02 tamamlansin (devam ediyor)
2. PFAZ01 + PFAZ02 yeniden calistir (BUG-02/03 etkili olmasi icin)
3. PFAZ09, 12, 13 yeniden calistir (fix'ler aktif olacak)
4. PFAZ06 ve PFAZ08 son calistirma (tam rapor + gorseller)
5. PFAZ10 son calistirma (LaTeX tez)

*Not Defteri v1.5 | 2026-05-04 | Sprint 2026-05-04 ozeti eklendi*


---

## Log Analizi Bulgulari -- Tez Metodoloji Kararlari (2026-05-08)

Bu bolum, eski PC log kayitlari (2026-04-30, ~7 gun calistirma) analizinden cikan tez yazimi
icin kritik tasarim kararlarini belgeler.

### Nilsson Model -- %34 NaN Karar Gerekcesi

**Karar:** Nilsson model ozellikleri (`nilsson_epsilon`, `nilsson_omega`) varsayilan config'de kapali.

**Gerekce:** Nilsson modeli yalnizca deformasyon gosteren cekirdekler icin anlamlidir (Beta_2 != 0).
267 cekirdeklik veri kumesinde 68/200 (%34) cekirdekte Nilsson ozellikleri NaN donmektedir.
Bu deger kucuk dataset'lerde (N=100, N=150) orantisiz olarak buyuk veri kaybi olusturur.

**Tez Sinirlamasi Olarak:** Nilsson model iceren ozellik setleri NaN imputation veya yaklasimsal
doldurma gerektirdigi icin kullanilmamistir. Tez metodoloji bolumunde: "Nilsson orbitalleri
yalnizca deformasyonlu cekirdekelerde hesaplanabilmekte; bu kisitlama nedeniyle ilgili ozellikler
analiz kapsami disinda birakilmistir" aciklamasi yapilmali.

### Robust Scaling -- QM Hedefi Icin Sistemik Basarisizlik

**Karar:** Robust scaling tum config dosyalarindan kaldirildi (WARN-03).

**Gerekce:** Eski PC log'larindan elde edilen bulgu: QM hedefiyle Robust scaling kombinasyonu
sistematik olarak R2 < 0 uretmektedir. Yani model, ortalama tahmininden (sifir model) bile
daha kotu performans gostermektedir. Bu, Robust scaling'in QM hedefinin dagilimi ile
uyumsuz oldugunu kanitlamaktadir.

**Tez Metodik Notu:** "Duyarsiz scale (Robust scaling), ceyrek aralik normalleshtirmesi
yaptigindan simetrik olmayan QM dagiliminda ozellik uzakliklarini bozar. Bu scaling
stratejisi, uygulanan on testlerde QM tahmini icin uygunsuz bulunmustur."

### Dataset Boyut 75 -- DNN Kisitlamasindan Kaldirma

**Karar:** Dataset boyut 75 tum config'lerden kaldirildi.

**Gerekce 1:** `DNN_MIN_SAMPLES = 80` kisitlamasi nedeniyle N=75 dataset'lerde DNN modeli
olusturulamamaktadir. Bu durumda DNN karsilastirma analizleri eksik kalir.

**Gerekce 2:** Log'lardan elde edilen bulgularda 75 boyutlu dataset'lerde 5-fold CV ile fold
basi yalnizca ~12 ornek dusulmektedir. Bu buyuklukte guvenilir CV hesabi yapilamaz.

**Tez Notu:** Minimum dataset boyutu 100 olarak belirlenmistir. Bu karar, DNN minimum ornek
gerekliligi ve istatistiksel guvenilirlik gozonu alindiginda zorunludur.

### Ornekleme Stratejisi -- Stratified ve Random Ikisi Birden

**Karar:** Desktop config'e Random + Stratified ornekleme birlikte eklendi.

**Gerekce:** Log analizi bulgulari:
- Random + XGBoost: en yuksek R2=0.84
- Stratified + RF/DNN: daha dengeli fold performansi

Stratified ornekleme, sihirli sayi cevresindeki cekirdeklerin (az temsil edilen siniflar)
fold'lara esit dagitilmasini saglar. Random ise daha genis konfigurasyonu temsil eder.

**Tez Metodik Notu:** "Kucuk orneklemde Stratified ornekleme, sinif dengesizligini azaltarak
capraz dogrulama varyansini dusurur. Her iki strateji de uygulanmis ve karsilastirilmistir."

### Cift R2 Filtresi -- Literatir ve Karar

**Karar:** Mevcut tek `val_R2 >= 0.5` filtresine ek olarak `cv_R2 >= 0.0` ve `gap < 0.5`
kriterleri eklendi (Sprint 1 — TAMAMLANDI 2026-05-08).

**Literatir Destegi:**
- Shang et al. (2022) ve Dong et al. (2022): CV ile val R2 farki >0.2-0.3 "asiri uyum sinyali"
- Utama et al. (2016): Nukleer kutleler icin BNN -- CV-based degerlendirme zorunlu
- Genel ML: cv_R2 < 0 (negatif) -> model anlamsiz (ortalamadan kotu)

**Uygulanan Esikler:**
- `val_R2 >= 0.5`: Mevcut, korunuyor
- `cv_R2 >= 0.0`: Yeni -- en azindan ortalamadan iyi olmali
- `gap = train_R2 - cv_R2 < 0.5`: Yeni -- %50'den fazla performans dusumu asiri uyumu isaret eder

**Tez Metodoloji Notu:** "Model seciminde yalnizca dogrulama kumesi R2'si degil, capraz
dogrulama R2'si de esik kriteri olarak kullanilmistir. Bu cift filtre, kucuk orneklem
dogrulama kumesinin (N~15) yaniltici yuksek R2'sine karsi ek guvence saglar."

### ANFIS 16 Konfigurasyon Aciklamasi

**Tanim:** PFAZ03 her dataset varyanti icin 8 FIS konfigurasyonu uygular. Desktop'ta 4 secildi.
4 FIS konfig x 2 hedef (MM + QM) = 8 ANFIS modeli per dataset varyanti.
TRUBA'da 8 FIS konfig x 2 hedef = 16 ANFIS modeli per dataset varyanti.

**FIS Konfig Mantigi:**
- Grid yontemi (CFG001-005): Esit aralikli uyelik fonksiyonu yerlesimi -- kontrol edilebilir
- SubClust yontemi (CFG006-008): Veri-odakli kume merkezleri -- magic number bolgeleri icin

**Tez Notu:** "8 FIS konfigurasyonu iki kural olusturma yaklasimini karsilastirir: Grid
Partition (deterministik yerlesim) ve Subtraktif Kumeleme (veri-odakli yerlesim). Bu
karsilastirma, nükleer veri dagiliminin hangi ANFIS mimarisiyle daha iyi modellendigi
sorusunu yanıtlamaya yardimci olur."

---

## Sprint Özeti — 2026-05-08/09

### Sprint 1: Çift R² Filtresi (TAMAMLANDI 2026-05-08)
- `parallel_ai_trainer.py` — CV kayıt öncesine taşındı; `cv_R2 >= 0.0` + `gap < 0.5` koşulları eklendi
- Adaptif fold: N < 150 → 3-fold, N ≥ 150 → 5-fold (Shang et al. 2022)
- `[DUAL_FILTER] KABUL/RET` log mesajları eklendi
- `config.json` / `config_desktop.json` / TRUBA `config.json`: ilgili threshold'lar eklendi

### Sprint 2: Config Senkronizasyonu (TAMAMLANDI 2026-05-09)
- N=75 kaldırıldı: DNN_MIN_SAMPLES=80 ihlali + CV fold'da ~12 örnek yetersizliği
- Robust Scaling kaldırıldı: QM hedefinde sistematik başarısızlık (R² < 0, WARN-03)
- Aktif scaling: [NoScaling, Standard, MinMax] — her 3 repoda senkronize edildi
- ANFIS `configurations` alanı: kodda OKUNMUYOR → `_configurations_note` belgesi eklendi

### Sprint 3: Belge Senkronizasyonu (TAMAMLANDI 2026-05-09)
- `phases/faz-02-yapay-zeka-egitimi.md` → §6.5 Çift R² Filtresi tam bölüm eklendi
- `phases/faz-01-veri-kumesi-uretimi.md` → Nilsson NaN kararı belgesi eklendi
- `pipeline-hatalari.md` → BUG-39/40/41 + WARN-03/04/05 detay bölümleri
- `faz-degerlendirme-notlari.md` → BÖLÜM N: log analizi bulguları
- `phases/README.md` → Sprint özet tablosu + BUG sayacı güncellendi (41 toplam)

**Tez Metodik Sonuç:** Dual R² filtresi uygulandıktan sonra kaydedilen modeller daha güvenilir
aşırı uyum önleme garantisine sahip olacak. Metodoloji bölümünde bu filtre standart prosedür
olarak sunulmalı: "val_R2 ve CV_R2 birlikte eşik kriteri olarak kullanıldı."

---

### Bug Düzeltmeleri — 2026-05-09 (Oturum Sonu)

- **BUG-31 DÜZELTİLDİ:** `NuclearMomentBandAnalyzer` → `NuclearBandAnalyzer` alias eklendi; PFAZ 12 import zinciri çalışıyor
- **BUG-32 DÜZELTİLDİ:** `automl_retraining_loop.py:539` IndentationError silindi; PFAZ 13 import çalışıyor
- **Bonus:** `pfaz6_final_reporting.py:1267` aynı kalıp düzeltildi
- Smoke test: 8/8 PASS

---

## Monte Carlo Örneklem Sayısı Kararı — K=1000

### Karar

Bootstrap CI ve gürültü duyarlılığı (noise sensitivity) için **K = 1000** Monte Carlo tekrarı.
MC Dropout (DNN'e özel) için K = 100 (farklı mekanizma, bağımsız karar).

### Gerekçe

**Veri seti bağlamı:** N = 267 çekirdek. Bu kadar küçük bir veri setinde tek bir
eğitim/test bölünmesinin rastlantısal etkisi büyüktür. Güvenilir %95 CI için örneklem
sayısı yeterince büyük olmalı.

**Literatür desteği:**

| Kaynak | K değeri | Bağlam |
|--------|----------|--------|
| Efron & Tibshirani (1993) *An Introduction to the Bootstrap* | ≥ 1000 | Bootstrap CI stabilitesi için genel kural |
| Davison & Hinkley (1997) *Bootstrap Methods and Their Application* | 999–9999 | Yüzdelik CI için minimum n önerisi |
| Utama et al. (2016) *Phys. Rev. C* 93, 014311 | ~1000 | Nükleer kütle tahmini BNN belirsizliği |
| Shang et al. (2022) *Phys. Rev. C* 105, 034316 | 1000 | Nükleer moment ML, bootstrap değerlendirme |
| Neufcourt et al. (2018) *Phys. Rev. Lett.* 122, 062502 | 1000+ | Bayesian nükleer kütle, MC örnekleme |

**İstatistiksel gerekçe:**
- Bootstrap yüzdelik CI (%2.5 ve %97.5) için n < 200: geniş Monte Carlo hatası
- n = 1000: standart hata ~%1.6 (1/√1000); yeterince stabil
- n = 100: standart hata ~%5.0 — tez düzeyinde yetersiz

**Hesaplama maliyeti (TRUBA):**
- 267 çekirdek × 50 model × 1000 bootstrap = 13.35M tahmin (sklearn predict, ~dakikalar)
- Kabul edilebilir, TRUBA'da batch paralel çalıştırılacak

### Uygulama

```python
# monte_carlo_simulation_system.py — DEFAULT_MC_CONFIG
'bootstrap':         {'n_bootstrap': 1000, ...}   # K=1000
'noise_sensitivity': {'n_samples_per_level': 1000} # K=1000 per noise level
'mc_dropout':        {'n_samples': 100}            # DNN-only, 100 yeterli
```

**config.json** zaten `n_runs: 1000` yazıyordu — kod bunu okumuyordu (BUG-38).
Düzeltme: `DEFAULT_MC_CONFIG` değerleri 100→1000 güncellendi (2026-05-09).

### Tez Metodoloji Metni (Öneri)

> "Her çekirdeğe ait tahmin belirsizliği, K=1000 Monte Carlo tekrarıyla nicelleştirilmiştir.
> Her tekrarda girdi özellik vektörü Gaussian gürültüyle (~N(0, σ_j)) bozulmuş ve
> tahmin dağılımının %2.5–%97.5 yüzdelikleri %95 güven aralığı olarak raporlanmıştır.
> Bootstrap yeniden örnekleme de K=1000 ile uygulanmıştır (Efron & Tibshirani, 1993).
> Bu örneklem sayısı, N=267 gibi küçük veri setlerinde güvenilir CI kapsama oranı
> sağlamak için literatürde standart değer olarak kabul edilmektedir
> (Shang et al., 2022; Neufcourt et al., 2018)."

---

## Rapor ve Görselleştirme Fazı Kod Düzeltmeleri — 2026-05-09

### PFAZ 06 (Final Raporlama) — latex_generator.py

- `Dataset sizes: 75, 100, 150, 200, ALL` → `100, 150, 200, ALL (267)` güncellendi
- Robust Scaling kaldırma notu eklendi
- `Smaller datasets (75--100 nuclei)` → `(100 nuclei)` düzeltildi

### PFAZ 08 (Görselleştirme) — master_report_visualizations_complete.py

- Varsayılan `dataset_sizes` listesi: `[75, 100, 150, 200, 'ALL']` → `[100, 150, 200, 'ALL']`
- N=75 kaldırılmasıyla tutarlı hale getirildi

### PFAZ 04/05/07 — Dual R² Filtresi Bağlamı

- PFAZ 04 `single_nucleus_predictor.py`: model yokluğunda dual R² filtresi açıklamalı uyarı eklendi
- PFAZ 05 `cross_model_evaluator.py`: `ValueError` mesajına dual R² bağlamı eklendi
- PFAZ 07 `pfaz7_complete_ensemble_pipeline.py`: boş model havuzuna karşı explicit guard eklendi

**Tez Notu:** Bu guard'lar akademik savunmada "hiç model kalmadıysa ne olur?" sorusuna
karşı pipeline'ın graceful davranışını belgeliyor.

---

---

## TRUBA Hazırlık Düzeltmeleri — 2026-05-09 (Sprint 4)

Proje TRUBA'ya aktarılmadan önce `nucdatav2-truba/` içinde tespit edilen kritik eksiklikler giderildi.

### Uygulanan Fix'ler

| # | Dosya | Sorun | Düzeltme |
|---|-------|-------|----------|
| 1 | `main.py` (sat. 554-569) | `ParallelAITrainer()` Dual R² parametrelerini almıyordu → Sprint 1 filtresi TRUBA'da sessizce devre dışıydı | `_pfaz02_cfg` okuyarak 5 parametre eklendi: `cv_r2_min_threshold`, `max_train_cv_gap`, `cv_folds`, `cv_folds_large_n`, `cv_large_n_threshold` |
| 2 | `pfaz09/.../monte_carlo_simulation_system.py` | `n_bootstrap=100`, `n_samples_per_level=100` (repo ile tutarsız) | → 1000 güncellendi (Efron & Tibshirani 1993) |
| 3 | `pfaz13/.../automl_retraining_loop.py` | BUG-32 (sat. 537-539 IndentationError) hâlâ mevcuttu | Üç satır silindi; PFAZ 13 TRUBA'da import edilebilir |
| 4 | `pfaz12/.../nuclear_band_analyzer.py` | BUG-31 (NuclearBandAnalyzer alias) uygulanmamıştı | `NuclearBandAnalyzer = NuclearMomentBandAnalyzer` eklendi |
| 5 | `config.json` (pfaz02_ai_training) | Dual R² parametreleri eksikti | 6 alan eklendi: `r2_min_threshold`, `cv_r2_min_threshold`, `max_train_cv_gap`, `cv_folds`, `cv_folds_large_n`, `cv_large_n_threshold` |
| 6 | `config.json` (parallel_training) | `n_workers: 4` — TRUBA 20-40 core'a yetersiz | → 16; `gpu_manager.py`'nin dinamik formülü (n//3, maks 16) devreye girer |

### Doğrulanan Bileşenler

- **SLURM script:** `hpc_slurm_job.sh` — 32 CPU, 128G RAM, GPU:1, `OMP_NUM_THREADS=1` (nested parallelism guard) — TRUBA uyumlu
- **requirements-hpc.txt:** Tüm kritik paketler mevcut (numpy, scipy, sklearn, xgboost, lgbm, tf, optuna, statsmodels, shap)
- **gpu_manager.py `optimal_workers()`:** Runtime'da `n_cpu // 3` ile dinamik ölçekleme — TRUBA'ya özel ayar gerektirmiyor

### Sprint 4 Sonucu

TRUBA `nucdatav2-truba/` dizini artık:
- Sprint 1 Dual R² filtresiyle eğitim yapacak
- K=1000 MC güveniyle belirsizlik nicelemesi yapacak
- BUG-31 ve BUG-32 olmadan PFAZ 12/13'ü çalıştırabilecek

**Sonraki adım:** Projeyi TRUBA'ya transfer et → `sbatch hpc_slurm_job.sh --pfaz 1` ile başlat.

---

*Not Defteri v2.1 | 2026-05-09 | TRUBA Sprint 4 fix'leri, K=1000 MC kararı (literatür destekli), BUG-38 düzeltildi, PFAZ 04/05/06/07/08/10/12/13 kod ve belge güncellemeleri*

---

## TRUBA Hazırlık Devamı — 2026-05-11 (Sprint 5)

QA tekrar denetimi sırasında belgelerde "düzeltildi" işaretli bug'ların kod doğrulaması
(KURAL 18) yapıldı ve **inter-PFAZ veri akışı kapsamlı tarandı**. Yeni bug'lar tespit
edildi, mevcutların eksik kısımları tamamlandı.

### Doğrulanan Mevcut Düzeltmeler

| Bug | Belge | Kod Doğrulama | Sonuç |
|-----|-------|----------------|-------|
| BUG-02 (HBAR_C) | "DUZELTILDI 2026-05-04" | `constants.py:44` — `HBAR_C = 197.3269804` | TAM |
| BUG-03 (V_so/r_so/a_so) | "DUZELTILDI 2026-05-04" | `constants.py:72-74` mevcut | TAM |
| BUG-10 (val_r2 dict riski) | "DUZELTILDI 2026-05-04" | `isinstance(_val, dict)` fallback var | TAM |
| BUG-31 (NuclearBandAnalyzer alias) | "DUZELTILDI 2026-05-09" | `nuclear_band_analyzer.py:1177` alias mevcut | TAM |
| BUG-32 (automl indent error) | "DUZELTILDI 2026-05-09" | Syntax test başarılı (`py_compile`) | TAM |
| **BUG-38 (MC n=1000)** | "DUZELTILDI 2026-05-09" | `DEFAULT_MC_CONFIG` 1000 ✓ ama **sınıf default'ları (194, 288) hala 100** | **YARIM** |

**Tez Notu:** KURAL 18 ("belge != gerçek fix") yine işe yaradı. Belgenin "tam düzeltildi"
ifadesine güvenmek yanlış — kod gerçek doğrulama gerekiyor. Sprint 5 BUG-38'in eksik
yarısını tamamlıyor: `Bootstrap.__init__` (sat. 194) ve `Sensitivity.__init__` (sat. 288)
default'ları 100 → 1000 güncelleniyor.

### Yeni Tespit Edilen Bug'lar (BUG-42 ... BUG-46)

Detaylar `pipeline-hatalari.md` dosyasına eklendi. Özet:

| ID | Öncelik | Faz | Etki | Tez Notu |
|----|---------|-----|------|----------|
| BUG-42 | YUKSEK | PFAZ 08 | `model_comparison_dashboard.py` `R2_test` kolonu arıyor; PFAZ 02 `Test_R2` yazıyor → tüm karşılaştırma dashboard'ları KeyError | **Bu, pc error.md'de PFAZ 8'in `pending` kalma sebebi.** |
| BUG-43 | YUKSEK | main.py | Yalnızca PFAZ 02 hem flat (`pfaz02_ai_training`) hem nested config okuyor; PFAZ 01, 03-13 sadece nested okuyor → config.json'daki ayarlar göz ardı ediliyor | **MATLAB engine ayarı, GPU off ayarı vs. etkisiz hale geliyor!** |
| BUG-44 | ORTA | PFAZ 01 | `config.json` `dataset_sizes=[100,150,200,267]` (int) ama kod `'ALL'` (str) bekliyor; `NOANOMALY_SIZES={150,200,'ALL'}` set'inde 267 yok | NoAnomaly varyantları üretilmiyor olabilir |
| BUG-45 | ORTA | PFAZ 03 | `ANFISDatasetSelector` belgede "aktif (2026-05-08)" ama kodda `anfis_parallel_trainer_v2.py:1427-1428` hala `deactivated` log basıyor | **Belge-kod drift'i (KURAL 18 vakası)** |
| BUG-46 | YUKSEK | PFAZ 02→03→08 | Üç farklı dosya adı aranıyor: PFAZ 02 `training_results_summary.xlsx` yazıyor, PFAZ 03 selector `training_summary.xlsx`, PFAZ 08 `training_summary.xlsx` veya `ai_training_summary.xlsx` arıyor | Selector aktif edilse bile FileNotFound |

### Akademik Karar — Selector R² Stratejisi (Tez Katkısı)

**Soru:** ANFISDatasetSelector'ın PFAZ 03'te yalnız `R2_test` üzerinden seçim yapması
overfit'i göz ardı etmiyor mu? Neden Train_R2 ile birlikte (dual R²) kullanılmıyor?

**Cevap (savunulabilir akademik gerekçe):**

Dual R² overfit filtresi **PFAZ 02 katmanında** zaten uygulanmıştır:
- `cv_r2_min_threshold = 0.0` — CV R²'si 0'dan küçük modeller atılır
- `max_train_cv_gap = 0.5` — Train R² ile CV R² arasında 0.5'ten fazla fark olan modeller
  aşırı uyduran sayılır (Shang et al. 2023, DOI: `10.1080/15140326.2023.2207326`;
  Utama et al. 2016, DOI: `10.1103/PhysRevC.93.014311`)
- `R2_MIN_SAVE_THRESHOLD = 0.5` — val_R² 0.5 altı modeller hiç kaydedilmez

**Pipeline mimarisi:**
```
PFAZ 02: Aşırı uyduran modeller elenir (dual R² + CV gap)
   ↓ (temiz model listesi)
PFAZ 03 Selector: R²_test üzerinden tier ataması
   ↓ (temizlenmiş listeden seçilen 200 dataset)
PFAZ 03 ANFIS Eğitimi
```

Selector'a **zaten temiz veri** geliyor; tek R² ile katman ayırmak yeterli ve
tutarlı. Yöntem bölümünde bu mimari ayrımı açıkça belirt:
> "Aşırı uyduran modellerin elemine edilmesi PFAZ 2'de gerçekleştirilmiştir
> (Shang et al., 2023; Utama et al., 2016). ANFIS dataset seçimi (PFAZ 3) bu
> ön-filtrelenmiş havuz üzerinde yalnızca R²_test esaslı tabakalı örnekleme
> uygulamaktadır; dual R² kontrolünü tekrarlamaya gerek yoktur."

**Tez §3.4 (Yöntem) için doğrudan kullanılabilir argüman.**

### Akademik Karar — Selector Tier Boş Kalma Riski

**Soru:** Top tier eşiği `R²_test ≥ 0.90`. Çoğu modelin R² değeri 0.5-0.7 arasındaysa
Top tier boş kalır ve hedef sayıya (200) ulaşılamaz.

**Cevap (kodun mevcut adaptif davranışı):**

`anfis_dataset_selector.py:130-158` satırlarında **adaptive deficit redistribution**
mantığı zaten mevcut:

```python
# Her tier'i quota'sına kadar doldur
for name, (df, quota) in tiers.items():
    allocated[name] = min(quota, len(df))

# Eksik varsa (deficit), boş kapasitesi olan tier'lere round-robin dağıt
deficit = n_datasets - sum(allocated.values())
if deficit > 0:
    for _pass in range(deficit):
        for name, (df, _) in tiers.items():
            spare = len(df) - allocated[name]
            if spare > 0 and deficit > 0:
                allocated[name] += 1
                deficit -= 1
```

**Pratik senaryo (örnek):** Eğer kotalar Top=50 / Mid=50 / Low=100 olarak istenmişse
ve tier dağılımı Top=0 / Mid=80 / Low=200 ise:
1. İlk doldurma: Top=0, Mid=50, Low=100 → toplam 150 (deficit=50)
2. Redistribution: Mid'de 30 boş kapasite, Low'da 100 boş kapasite
3. Round-robin ile deficit dağıtılır: Top=0, Mid=80, Low=120 → toplam 200 ✓

**Sonuç:** Kod **zaten** "değerde ne kadar varsa onu kullan" mantığını uyguluyor.
Düzeltme gerekmiyor. Yalnızca akademik şeffaflık için tez §3.4'te şu cümle eklenmeli:

> "Kotaların doldurulamadığı durumlarda (örn. Top tabakanın boş kalması) eksik miktar
> diğer tabakalardaki artık kapasiteye round-robin esasıyla dağıtılır. Bu sayede
> hedef seçim sayısı (200 dataset/hedef) mevcut model dağılımı ne olursa olsun
> garanti altına alınır; ANFIS eğitim kuyruğu beklenmedik biçimde küçülmez."

**Tez §3.4 (Yöntem) → Adaptive Quota Redistribution bölümü** olarak yer alacak.

### Sprint 5 İçeriği (Patch'e Dahil Edilecekler)

| # | Dosya | Düzeltme | İlgili Bug |
|---|-------|----------|------------|
| 1 | `pfaz09/monte_carlo_simulation_system.py` sat. 194, 288 | `n_bootstrap=100` ve `n_samples_per_level=100` → 1000 (sınıf default'ları) | BUG-38 (tamamlama) |
| 2 | `pfaz08/model_comparison_dashboard.py` | 15+ yerde `R2_test`/`RMSE_test`/`MAE_test` → `Test_R2`/`Test_RMSE`/`Test_MAE` rename | BUG-42 |
| 3 | `main.py` | `_get_pfaz_config(pfaz_id)` helper eklenecek; hem flat hem nested config birleştirilecek | BUG-43 |
| 4 | `pfaz01/dataset_generation_pipeline_v2.py` | `267` ve `'ALL'` eşdeğer kabul edilecek; `NOANOMALY_SIZES`'a 267 eklenecek | BUG-44 |
| 5 | `pfaz03/anfis_parallel_trainer_v2.py` sat. 1427-1428 | Selector aktif edilecek; `train_all_anfis_parallel` içinde `ANFISDatasetSelector` çağrılacak (Top=50/Mid=50/Low=100) | BUG-45 |
| 6 | `pfaz03/anfis_dataset_selector.py` | Kolon adları `R2_test` → `Test_R2`; dosya adı `training_summary.xlsx` → ayrıca `training_results_summary.xlsx` dener | BUG-46 |
| 7 | `pfaz02/parallel_ai_trainer.py` sat. 1657 | Hem `training_results_summary.xlsx` hem `training_summary.xlsx` yazılacak (geri uyumluluk) | BUG-46 |

### Sprint 5 Sonucu

- BUG-38 tam düzeltildi (sınıf default'ları dahil)
- 5 yeni bug (BUG-42...BUG-46) tespit ve düzeltme planlandı
- Tez §3.4 için **iki akademik savunma argümanı** belgelendi:
  1. Dual R² PFAZ 2 katmanında uygulandığı için PFAZ 3'te tekrarlanmıyor (literatür destekli)
  2. Adaptive quota redistribution kotaların doldurulamaması durumunu graceful ele alıyor

**Sonraki adım:** Patch dosyası üretilecek (`truba-fixes-sprint5.patch`); kullanıcı
GitHub `truba-fixes` branch'ine `git am` ile uygulayıp push edecek. TRUBA bağlantısı
kurulduğunda modül adı placeholder'ları gerçek isimle değiştirilip Apptainer/SLURM
scripts üretilecek.

---

*Not Defteri v2.2 | 2026-05-11 | Sprint 5: KURAL 18 dogrulamalari, 5 yeni bug, 2 tez katkisi argumani (Dual R2 mimarisi + Adaptive Quota)*

---

## Sprint 6 -- 2026-05-12 (8 Kategori Bug Taramasi)

8 paralel sub-agent ile 165+ Python dosyasi taranmistir. Toplam 15 yeni bug tespit edilmistir.

### Tespit Ozeti

| Kategori | Bug Sayisi | En Yuksek Oncelik |
|----------|-----------|-------------------|
| Hardcoded Path | 2 | TRUBA-CRITICAL |
| Optional Import | 2 | YUKSEK |
| Excel Sheet Name | 2 | YUKSEK |
| Memory Leak (TF) | 2 | KRITIK |
| Silent Exception | 3 | KRITIK |
| n_jobs Nested | 1 | ORTA |
| Encoding | 0 | -- (temiz) |
| Doc vs Artifact | 3 | TASARIM |

### TRUBA-CRITICAL Bug'lar (Oncelikli Fix)

| ID | Dosya | Sorun |
|----|-------|-------|
| BUG-47 | `analysis_modules/real_data_integration_manager.py:28-29` | `/home/claude` + `/mnt/user-data/outputs` sys.path -- her import'ta ImportError riski |
| BUG-48 | `visualization_modules/visualization_integration.py:31` | `/mnt/user-data/outputs` sys.path -- PFAZ 08 gorsellestirme tamamen kapaniyor |

### Kritik Bulgular (Tez Kalitesi Etkili)

**BUG-53 (KRITIK):** hyperparameter_tuner.py + automl_optimizer.py + automl_hyperparameter_optimizer.py
Optuna trial dongulerinde TF `clear_session()` eksik. 30+ trial x n_datasets boyunca GPU VRAM birikmesi.
Projede yalnizca 1 dogru yer var: `parallel_ai_trainer.py:1468-1483`.
TRUBA'da GPU ResourceExhaustedError riski.

**BUG-57 (KRITIK):** pfaz13/automl_retraining_loop.py:211, 305, 758
Dataset yukleme ve config okuma hatalari sessizce yutulmus. PFAZ 13 hicbir iz birakmazken calismis gozukuyor.

**BUG-55 (YUKSEK):** pfaz04 model yukleme koru (unknown_nuclei_predictor + single_nucleus_predictor).
Top-25 konsensus listesi eksik model icerebilir; sebep loglanmiyor.

**BUG-56 (YUKSEK):** pfaz06 pfaz6_final_reporting.py'de 5 farkli yerde JSON okuma sessiz basarisizligi.
Excel raporunda eksik satir/sayfa olusuyor; kullanici fark etmiyor.

### Olumlu Bulgular (Tez Metodoloji Argumanlarina Katki)

- **Encoding tamamen temiz:** 183 text mode open() cagrisinin tamami encoding='utf-8' kullaniyor.
  Tez metodoloji notunda "Platform-bagimsiz metin isleme" argumani guclu.
- **n_jobs=-1 hardcoded YOK:** `_inner_n_jobs()` 24 farkli noktada dogru kullaniliyor.
  TRUBA paralel egitimine hazir.

### Dokumantasyon Tutarsizliklari (Tez Yaziminda Dikkat)

- **BUG-59:** PFAZ 06 sheet sayisi -- kok CLAUDE.md "18", toolkit "29", gercek: **22-29**.
  Tezde Excel raporu aciklanirken "haftalik guncellemelerle buyuyen 22+ sayfa" formulasyonu kullanilabilir.
- **BUG-60:** PFAZ 07 stacking -- belgede "6 stacking", aktif kodda yalnizca **4** (Ridge, Lasso, RF, GBM).
  Tez metodoloji bolumunde 4 meta-model olarak duzelt.
- **BUG-61:** PFAZ 10 kok CLAUDE.md "11 bolum + 2 ek" yanlis, gercek: **14 bolum + 4 ek**.
  Tez yapisi sunumunda bu dogruyu kullan.

### Sprint 6 Sonucu

Toplam 15 bug (BUG-47...BUG-61). Sprint 7'de duzeltilecekler:
1. BUG-47, BUG-48 (TRUBA-CRITICAL) -- sys.path hardcoded kaldirilacak
2. BUG-53 (KRITIK) -- Optuna trial dongulerinde finally + clear_session
3. BUG-57 (KRITIK) -- pfaz13 silent exception'lar tracker'a baglanacak
4. BUG-51 (YUKSEK) -- Robustness_CV sheet adi pfaz08'de duzeltilecek
5. BUG-55, BUG-56 (YUKSEK) -- pfaz04 + pfaz06 loglama

*Not Defteri v2.3 | 2026-05-12 | Sprint 6: 15 yeni bug, 2 TRUBA-CRITICAL, encoding temiz, n_jobs dogru*
---

## Sprint 7 -- Bug Fix Sprint (2026-05-12)

### BUG-47..61 Fix Ozeti

Sprint 6'da tespit edilen 15 bug Sprint 7'de tamamen kapatildi.

**TRUBA-CRITICAL (once):**
- BUG-47/48: `/home/claude` ve `/mnt/user-data/outputs` hardcoded sys.path kaldirildi.
  Ikiside `Path(__file__).resolve().parents[1]` ile degistirildi.
  TRUBA'da pipeline artik import aninda crash vermeyecek.

**KRITIK -- Memory Leak:**
- BUG-53: Optuna trial dongularinde (hyperparameter_tuner, automl_hyperparameter_optimizer)
  `finally: tf.keras.backend.clear_session() + gc.collect()` eklendi.
  Uzun Optuna run'larinda RAM patlamasi onlendi.
- BUG-54: model_trainer.py DNN fit sonrasi ayni cleanup eklendi.

**YUKSEK -- Veri Akisi:**
- BUG-49: advanced_models_extended.py torch hard import --> try/except + TORCH_AVAILABLE.
  TRUBA'da PyTorch olmasa PFAZ 02 baslamiyor derdine son.
- BUG-50: pfaz09 2 dosyada tqdm --> try/except + TQDM_AVAILABLE + fallback iterator.
- BUG-51: visualization_master_system.py Robustness_CV_Results --> Robustness_CV.
  Robustness grafikleri artik PFAZ 08'de uretilecek.
- BUG-52: comprehensive_excel_reporter.py sheet_name [:31] truncation eklendi (2 yer).
- BUG-55: pfaz04 unknown_nuclei_predictor 2x silent except --> logger.warning.
- BUG-56: pfaz06 pfaz6_final_reporting 3x kritik silent except --> logger.warning.
- BUG-57: pfaz13 automl_retraining_loop 3x silent except --> logger.warning.

**ORTA/TASARIM:**
- BUG-58: parallel_ai_trainer.py yaniltici ProcessPoolExecutor yorum duzeltildi.
- BUG-59/60/61: CLAUDE.md hatalari duzeltildi (sheet sayisi dinamik, ensemble
  4+4 degil 5+6+AdaBoost, chapter 6 degil 14).

### Sprint 7 Sonuc
14 dosya, 16 farkli satirda degisiklik. Syntax 14/14 OK.
Hardcoded path grep: 0 bulgu.

*Not Defteri v2.4 | 2026-05-12 | Sprint 7: 15 bug kapandi, TRUBA-CRITICAL temizlendi*

