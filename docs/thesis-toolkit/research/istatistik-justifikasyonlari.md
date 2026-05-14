# İstatistiksel Seçim Gerekçeleri — Senaryolar, Ölçekleme, Anomali Tespiti

> **Amaç:** S70/S80, ölçekleme yöntemleri, IQR=3.0 ve örnekleme stratejilerinin akademik justifikasyonu  
> **Tarih:** 2026-05-03

---

## 1. Eğitim/Doğrulama/Test Senaryoları

### 1.1 Neden S70 (70/15/15) ve S80 (80/10/10)?

**Küçük veri kümesi kısıtı:**
267 çekirdek, nükleer fizik ML çalışmaları için orta-küçük bir veri kümesidir. Bu büyüklükte:
- Eğitim kümesi ne kadar büyükse model o kadar iyi öğrenir
- Test kümesi ne kadar büyükse sonuçlar o kadar güvenilir
- Bu iki gereksinim çelişir

**S70 tercih gerekçesi:**
```
Eğitim: 0.70 × 197 ≈ 138 örnek (ALL boyutu için)
Doğrulama: 0.15 × 197 ≈ 30 örnek
Test: 0.15 × 197 ≈ 30 örnek
```
30 test örneği istatistiksel güvenilirlik için kabul edilebilir minimum.
Hyperparameter tuning için yeterli doğrulama seti.

**S80 tercih gerekçesi:**
```
Eğitim: 0.80 × 197 ≈ 158 örnek
Doğrulama: 0.10 × 197 ≈ 20 örnek
Test: 0.10 × 197 ≈ 20 örnek
```
Daha fazla eğitim verisi → özellikle DNN için önemli.
20 test örneği → sonuçların varyansı daha yüksek, ama eğitim avantajı telafi eder.

**Neden S60 veya S90 değil?**
- S60: ~120 eğitim → DNN_MIN_SAMPLES=80 sınırına tehlikeli yakınlık; RF/GBM için de sınırda
- S90: ~18 test → tek bir outlier çekirdeğin sonuçları tamamen bozabileceği büyüklük

**İki senaryo birlikte:**
Aynı veriyle iki farklı bölme politikasının karşılaştırılması, model seçiminin bölme politikasına duyarlılığını ölçer. Bu bir tür robustness analizi işlevi görür.

---

## 2. Ölçekleme (Normalizasyon) Yöntemleri

### 2.1 StandardScaler (Z-skor)

```
x_scaled = (x - μ) / σ
```

**Tercih koşulu:** Özelliğin Gaussian dağılım gösterdiği durumlarda optimal.
**Nükleer bağlam:** BE, S_n gibi sürekli fiziksel büyüklükler yaklaşık normal dağılım gösterir.
**Uyarı:** Outlier'lara hassas — bu nedenle IQR temizliğinden sonra uygulanır.

### 2.2 MinMaxScaler [0,1]

```
x_scaled = (x - x_min) / (x_max - x_min)
```

**Tercih koşulu:** Verinin sınırları anlamlıysa (örneğin β₂ için -0.6 < β₂ < 0.6).
**Nükleer bağlam:** magic_character (0/1 binary) için MinMax zaten anlamsız — bu özellik ölçeklenmez.
**Avantaj:** Nükleer özelliklerin fiziksel yorumlanabilir aralıkları korunur.

### 2.3 RobustScaler

```
x_scaled = (x - median) / IQR
```

**Tercih koşulu:** Outlier'ların varlığında daha sağlam normalizasyon.
**Nükleer bağlam:** Kabuk kapanması çekirdekleri (sihirli sayılar) aşırı değerler üretir.
RobustScaler bu uç değerlere karşı dirençli → kabuk kapanması bölgelerindeki bilgi korunur.
**Ne zaman tercih edilir?** Anomali filtrelemesiz (NoAnomaly flag olmayan) veri setlerinde.

### 2.4 Ölçekleme Yok (NoScale)

**Tercih koşulu:** Ağaç tabanlı modeller (RF, GBM, XGBoost) ölçeklemeden etkilenmez.
**Nükleer bağlam:** Bu modeller eşik değer (threshold) öğrenir, Öklid mesafesi kullanmaz.
Ölçeklenemez ayrık özellikler (magic_character, parite) için zorunlu.

### 2.5 Ayrık Özellik Koruma (Discrete Protection)

Özellikler {0,1} veya {-1,0,1} değerleri alıyorsa ölçeklenmez.
Gerekçe: Bu özellikler fizik kategorisini kodlar, sürekli değer değil.
Ölçeklenseydi magic_character = 0.5 anlamsız olurdu.

---

## 3. Anomali Tespiti

### 3.1 IQR Yöntemi, Eşik = 3.0

**Standart kural:** IQR=1.5 ile Q1-1.5·IQR ve Q3+1.5·IQR dışındakiler "mild outlier".
**Nükleer veri için sorun:**
Kabuk kapanması çekirdeklerinde S_n, BE, μ değerleri gerçekten aşırıdır — ama bu bilgidir, gürültü değil.

IQR=1.5 uygulanırsa → ~30-40 sihirli çekirdek anomali olarak işaretlenir → silinir → MODEL KABİLİYET KAYBI.

IQR=3.0 uygulanırsa → yalnızca istatistiksel olarak imkansız değerler kaldırılır:
```
Kaldırılacak: Q1 - 3·IQR < x veya x > Q3 + 3·IQR
```
Bu çok muhafazakar bir eşiktir. Nükleer verinin doğal aralığını korur.

**Pratik etki:** ~267 çekirdeğin ancak 5-10'u bu eşikle kaldırılır (muhtemelen ölçüm hataları).

### 3.2 IsolationForest, contamination = 0.08

**Gerekçe:**
IQR tek boyutludur — her özelliği ayrı ayrı değerlendirir.
IsolationForest çok boyutludur — özelliklerin birlikte "tuhaf" göründüğü örnekleri bulur.

contamination = 0.08:
```
267 × 0.08 ≈ 21 örnek anomali olarak işaretlenir
```

Sihirli sayı çekirdek sayısı tahmini:
- Z sihirli: He(Z=2), O(Z=8), Ca(Z=20), Ni(Z=28), Sn(Z=50), Pb(Z=82) → ~6 element × birkaç izotop ≈ 40+ çekirdek
- N sihirli: benzer sayı

Bu durumda contamination=0.08 (%8) nükleer sihirli çekirdeklerin tamamını dışarıda bırakmaz — yalnızca ölçüm kalitesi şüpheli olanları hedefler.

**Uyarı:** Bu parametre, hangi çekirdeklerin silindiği incelenerek doğrulanmalıdır (açık soru S-004).

---

## 4. Örnekleme Stratejileri

### 4.1 Rastgele Örnekleme (Random)

Temel durum — bölme stratejisi yok, sadece rasgele karıştır.
**Sorun:** Az sayıda sihirli çekirdek test kümesine hiç gelmeyebilir → değerlendirme yanlı.

### 4.2 Stratified (A bölgesi)

Hafif/orta/ağır/çok ağır kütle gruplarında orantılı temsil.
```
Hafif (A<60): ~X çekirdek → eğitime 0.7·X, teste 0.15·X
Orta (60≤A<120): ~Y çekirdek → orantılı bölme
...
```
**Neden?** Kütle bölgelerine göre farklı fizik dominanttır — modelin her bölgeyi öğrenmesi için her bölgeden örnekler gerekir.

### 4.3 StratifiedMagic (%30 sihirli)

```
Test kümesinin %30'u sihirli sayı çekirdeklerinden oluşur
```
**Neden?** Modelin en zor bölgede (ani değişim noktaları) nasıl performans gösterdiğini özellikle test etmek için.

### 4.4 StratifiedHybrid

Kütle grubu ve sihirli sayı özelliğini birlikte kullanarak stratified bölme.
**Neden?** En kapsamlı değerlendirme — hem kütle bölgesi hem de kabuk yapısı dengeli temsil.

---

## 5. Boyut Seçimi (75, 100, 150, 200, ALL)

**ALL (tüm veri, ~197):** Maksimum bilgi, minimum veri kaybı.
**200, 150:** 267 çekirdekten 200/150 örnek seçimi → hangilerinin seçildiği stratified olarak belirlenir.
**100, 75:** Küçük boyut → DNN için S70 yeterli örnek sağlarken S80'de 80 (minimum sınır) problemi olabilir.

**Neden boyut varyasyonu?**
Model performansının eğitim boyutuna duyarlılığı öğrenme eğrisi analizine izin verir.
Gerçek nükleer veride 267'den fazla ölçüm mevcut değildir — bu nedenle örnekleme boyutu gerçekçi bir "veri kıtlığı" simulasyonu sağlar.

---

*Araştırma notu — 2026-05-03*

---

## 6. İstatistiksel Sınama (Sprint 4-13 Güncellemesi)

Bu bölüm Sprint 13 sonrası eklendi; PFAZ12 BootstrapCI + ANFIS karşılaştırması aktif edildiğinde tez §3.7 (İstatistiksel Doğrulama) bölümünün doğrudan kaynağı olacaktır.

### 6.1 Bootstrap CI — K=1000 Standart

**Karar:** Bootstrap CI ve gürültü duyarlılığı için K=1000 Monte Carlo tekrarı (Sprint 4 BUG-38 + Sprint 8 BUG-64 ile tamamlandı). MC Dropout DNN için K=100 (farklı mekanizma).

**Literatür desteği:**
- Efron & Tibshirani (1993) *An Introduction to the Bootstrap* — K≥1000 standart
- Davison & Hinkley (1997) *Bootstrap Methods and Their Application* — K=999-9999 minimum
- Utama et al. (2016) *Phys. Rev. C* 93, 014311 — Nükleer kütle BNN, K~1000
- Shang et al. (2022) *Phys. Rev. C* 105, 034316 — Nükleer moment ML, K=1000
- Neufcourt et al. (2018) *Phys. Rev. Lett.* 122, 062502 — Bayesian nükleer kütle, K=1000+

**İstatistiksel gerekçe:**
- N<200: geniş Monte Carlo hatası
- N=1000: standart hata ~%1.6 (1/√1000); tez düzeyinde yeterli
- N=100: standart hata ~%5.0; tez düzeyinde yetersiz

### 6.2 CV Gate Çift R² Filtresi (Sprint 1 + Sprint 8)

Tez metodolojisinde model seçim filtresi:

- `val_R²>=0.5` (POOR_R2_FILTER)
- `cv_R²>=0.0` (CV gate, Shang 2022 + Utama 2016)
- `gap = train_R² - cv_R² < 0.6` (Vabalas et al. 2019; küçük N varyans toleransı için 0.5 yerine 0.6)

**Gerekçe:** Tek `val_R²` esnek; küçük dogrulama setlerinde yaniltici. Cift filtre asiri uyum kontrolü.

### 6.3 PFAZ12 AI vs ANFIS Paired Test (Sprint 13 BUG-97)

Sprint 13 ile aktif: her dataset varyantı için paired t-test ve Wilcoxon signed-rank test:

- H0: AI ve ANFIS performansı eşit
- H1: Farklı (iki-yönlü)
- alpha=0.05
- Etki büyüklüğü: Cohen's d ve Cliff's delta

**Tez §3.7 hazır metin:**
> "Manyetik ve kuadrupol moment tahminlerinde AI ve ANFIS yaklaşımları paired t-test ve Wilcoxon signed-rank test ile karşılaştırılmıştır. Etki büyüklüğü Cohen's d ile ölçülmüş, alpha=0.05 anlamlılık eşiği uygulanmıştır. Tüm karşılaştırmalar K=1000 Bootstrap ile %95 CI raporlanmıştır."

### 6.4 PFAZ12 BootstrapCI -- Sprint 13 BUG-95

PFAZ12 artık `bootstrap_ci_results.xlsx` üretiyor:
- Model_Performance sheet: her model için R²_mean, CI_lower, CI_upper
- Bootstrap_Distribution PNG: her model için dağılım grafiği

PFAZ6 raporuna `Bootstrap_CI` sayfası olarak besleniyor.

### 6.5 Inter-PFAZ Akış (Sprint 5 KURAL 19)

Sprint 5'te tanımlanan KURAL 19: "Inter-PFAZ veri akışı her sprint sonu denetlenir." Bu istatistik analiz için kritik:
- PFAZ2 metrics → PFAZ12 BootstrapCI: kolon adı `Test_R2` (eski `R2_test` değil)
- PFAZ3 anfis_vs_ai.xlsx → PFAZ12: kolon yapısı `{'metrics': {'val': {'r2': ...}}}` iç sözlük

Sprint 10 BUG-65..74 ile sütun seviyesinde doğrulandı.

---

*Sprint 4-13 güncelleme: 2026-05-14*
