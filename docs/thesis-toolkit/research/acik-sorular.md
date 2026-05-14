# Açık Araştırma Soruları — PFAZ 01

> **Oluşturma:** 2026-05-03  
> **Amaç:** Dokümantasyon sürecinde ortaya çıkan, yanıtlanması gereken sorular

---

## Fizik Justifikasyon Soruları

### S-001: Neden tam olarak bu 7 fizik modülü seçildi?
- SEMF: evrensel bağlanma enerjisi tahmini → tüm ağır çekirdekler için temel referans
- Yarıçap: büyüklük ölçeği sağlar (R = R₀·A^(1/3))
- Ayrılma enerjisi: son nükleonun bağlanma gücü → moment büyüklüğüyle korele
- Kabuk modeli: sihirli sayı ani değişimi → MM/QM'nin asıl fizik kaynağı
- Deformasyon: β₂ → eksen simetrisi → kuadrupol moment için temel girdi
- Schmidt: teorik referans değerler → ML'nin "ne kadar şaştı" ölçüsü
- Woods-Saxon + Nilsson: tek parçacık orbital → spin konfigürasyonu

**Yanıtlanacak:** Her modülün teze katkısı ayrı belgelenmeli mi?

### S-002: Ani değişim (shell closure discontinuity) tam olarak nasıl ölçülüyor?
- magic_character: 0/1 binary flag — sihirli Z veya N'e sahip mi?
- Z_magic_dist, N_magic_dist: {2,8,20,28,50,82,126}'ya en yakın mesafe
- S_n/S_p'deki ani değişim = kabuk kapanmasının nükleer işareti
- **SORU:** ML modeli bu discontinuity'yi öğreniyor mu? SHAP değerleri ne diyor?

### S-003: IQR eşiği neden 3.0, standart 1.5 değil?
- Nükleer verinin doğası: kabuk kapanmalarındaki çekirdekler gerçek anlamda uç değer
- IQR=1.5 → kabuk kapanması çekirdeklerini (sihirli çekirdekler) siler → bilgi kaybı
- IQR=3.0 → sadece ölçüm hatası kaynaklı aykırıları kaldırır
- **Doğrulanacak:** Hangi çekirdekler IQR=3.0 ile kaldırılıyor?

### S-004: IsolationForest contamination=0.08 nasıl belirlendi?
- 267 çekirdeğin ~%8'i = ~21 çekirdek anomali olarak işaretlenebilir
- Sihirli sayı çekirdeği sayısı: Z=2(He),8(O),20(Ca),28(Ni),50(Sn),82(Pb) ~ toplam ~40 çekirdek
- **SORU:** Bu parametre grid search ile mi belirlendi yoksa literatür değeri mi?

---

## Senaryo ve Bölme Soruları

### S-005: Neden yalnızca S70 ve S80, S60 veya S75 değil?
- 267 çekirdek küçük bir veri kümesi → her bölme kararı kritik
- S70 (70/15/15): ~187/40/40 — yeterli test kümesi
- S80 (80/10/10): ~214/27/27 — sınırda test kümesi büyüklüğü
- S60 denenirse: ~160 eğitim → DNN min örnek sorununa yakın (DNN_MIN_SAMPLES=80)
- **Yanıtlanacak:** S70 ve S80 dışında başka senaryo test edildi mi?

### S-006: Kütle grubu ve izotop grubu nasıl tanımlanıyor?
- Kütle grubu: hafif (A<60), orta (60≤A<120), ağır (120≤A<200), çok ağır (A≥200)
- Bu gruplar stratified sampling'in temelini oluşturuyor
- **SORU:** Kütle grupları literatüre göre mi belirlendi yoksa veri dağılımına göre mi?

---

## Model Seçim Soruları

### S-007: Neden DNN mimarisi 128-64-32, örneğin 256-128-64 değil?
- 267 örnek → 128-64-32 (toplam ~12K parametre) → overfit riski düşük
- 256-128-64 → ~50K parametre → 267 örnekle overfit kaçınılmaz
- **Doğrulanacak:** Başka mimariler denendi mi?

### S-008: PINN physics_weight=0.5 nasıl belirlendi?
- physics_weight=0.5 → kayıp = 0.5*veri_hatası + 0.5*fizik_kısıtı
- Fizik kısıtı: SEMF tahmininden sapma penaltısı
- **SORU:** physics_weight için hyperparameter search yapıldı mı?

### S-009: Neden ANFIS için tam bu 8 konfigürasyon?
- 2 üyelik fonksiyonu tipi: Gauss (yumuşak geçiş) vs diğerleri
- 2 kümeleme yöntemi: Grid partition (uniform) vs subtractive clustering (veri güdümlü)
- **Yanıtlanacak:** ANFIS'in Schmidt değerlerini öğrenmesi teorik olarak mümkün mü?

---

## Özellik Kombinasyonu Soruları

### S-010: SHAP tabanlı özellik seçimi nasıl çalışıyor?
- İlk RF modeli tüm özelliklerle eğitiliyor
- SHAP değerleri hesaplanıyor → özellik önemi sıralanıyor
- En önemli N özellik seçiliyor (N farklı deneme setleri için farklı)
- **SORU:** SHAP seçimi hedef bağımlı mı? (MM için farklı, QM için farklı özellikler?)

---

*Güncelleme: 2026-05-03 | Yanıtlar araştırma dosyalarına eklenecek*

---

## Sprint 4-13 Güncellemeleri (2026-05-11 → 2026-05-14)

### Yanıtlanan / Daraltılan Sorular

**S-002 (SHAP/discontinuity):** Sprint 13 BUG-96 ile aktif edilen `RobustnessTester` (PFAZ2) `permutation importance` analizi sağlar. Bu çıktı TRUBA sonrası şu soruyu yanıtlar: "Kabuk kapanmasındaki çekirdeklerde hangi özellik en kritik?" Cevap `outputs/trained_models/robustness_per_model/*.png` dosyalarında. SHAP analizi ayrıca PFAZ8 `shap_analysis.py` ile devam eder.

**S-003 (IQR=3.0):** Sprint 6/7 BUG-47..61 tarama bulgularında IQR=3.0'ın savunulabilirliği teyit edildi. `research/istatistik-justifikasyonlari.md` §2.1'de detaylandırıldı. **Daraltılmış soru:** Hangi 21 çekirdek IQR=3.0 ile kaldırılıyor? (TRUBA çıktısı sonrası ölçülecek)

**S-004 (IsolationForest contamination=0.08):** Sprint 6/7 8 kategori taraması, contamination değerinin grid search ile değil sezgisel olarak belirlendiğini doğruladı. Tez sınırlılık bölümünde belirtilecek.

**S-005 (S70/S80 dışı senaryolar):** Sprint 2 N=75 kaldırma kararı ile S60 senaryosu zaten dışlandı (DNN_MIN_SAMPLES=80 ihlali). Sprint 8 BUG-62 CV gate ek koruma sağlıyor. **Yanıt:** S70/S80 yeterli; başka senaryo gerekmez.

**S-006 (Kütle grupları):** Sprint 10 BUG-65..74 inter-PFAZ denetiminde A_group tanımının veri dağılımına göre (literatür değil) belirlendiği teyit edildi. Tezde "veri-güdümlü tanım" olarak sunulmalı.

**S-007 (DNN 128-64-32):** Sprint 13 RobustnessTester sonrası alternatif mimari karşılaştırması için ek veri toplanabilir. Mevcut hâlinde tez sınırlılığı olarak belirtilebilir.

**S-008 (PINN physics_weight=0.5):** PINN Sprint 4'te Pipeline'dan çıkarıldı (bounds ±20 vs veri ±7 → ceza sıfır, etkisiz). `tez-yazim-not-defteri.md` 2026-05-08 karar günlüğü.

**S-009 (ANFIS 8 konfigürasyon):** Sprint 5 BUG-45 ile ANFISDatasetSelector aktif edildi. Tez §3.4 (Adaptif Dataset Seçimi) için zengin metin oluştu (Top=50/Mid=50/Low=100). Yanıt: 8 konfig 2 MF tipi × 4 kümeleme yöntemi yeterli kapsama sağlar; akademik gerekçe `tez-yazim-not-defteri.md`'de var.

**S-010 (SHAP hedef-bağımlı):** Sprint 13 PFAZ12 BootstrapCI + ANFIS karşılaştırması her hedef için ayrı analiz veriyor. SHAP seçimi hedef-bağımlıdır (MM ve QM ayrı özellik setleri); kodda `target` parametresi ile.

### Hâlâ Açık Kalan Sorular

- **²⁰⁸Pb IQR filtre durumu:** TRUBA çıktısı sonrası `outputs/generated_datasets/*/metadata.json` kayıtları ile kontrol edilebilir.
- **`epsilon_nilsson` birim:** Kod incelemesiyle hâlâ doğrulanmamış (yüksek öncelik değil; Nilsson özellikleri pipeline'da KAPALI tutuluyor, `tez-yazim-not-defteri.md` 2026-05-08 karar).
- **Ablation study (magic özellikler olmadan):** Sprint sonu işi olarak `research/ani-degisim-arastirmasi.md`'ye ek bölüm yazılması planlandı.

---

*Sprint 4-13 güncelleme: 2026-05-14*
