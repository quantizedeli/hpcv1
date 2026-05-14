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
