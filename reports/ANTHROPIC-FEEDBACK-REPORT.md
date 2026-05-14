# Anthropic Geri Bildirim Raporu

**Hazırlayan:** Kemal Acar  
**Tarih:** 2026-05-14  
**Proje:** Nuclear Physics AI Pipeline (hpcv1)  
**Claude versiyonu:** Claude Sonnet 4 (claude.ai)  
**Gönderim:** support@anthropic.com veya claude.ai feedback butonu

---

## Özet

13 sprint boyunca Claude ile kapsamlı bir makine öğrenmesi pipeline geliştirdim.
Genel deneyim oldukça verimli olmakla birlikte, uzun oturumlar ve karmaşık projeler
için bazı sistematik sorunları paylaşmak istedim.

---

## Olumlu Geri Bildirimler

### 1. Kod Kalitesi

Claude'un ürettiği Python kodu genellikle yüksek kaliteli: type hints, docstring,
hata yönetimi, modüler yapı. 7000+ satır production-ready kod ürettik.

### 2. Hata Analizi

Karmaşık bug'ları (inter-PFAZ veri akışı tutarsızlıkları, Bash pipe exit code
zinciri) sistematik olarak analiz etmesi etkileyiciydi.

### 3. Dokümantasyon

Teknik dokümantasyon kalitesi yüksek. Pipeline-hatalari.md (99 bug), kural
katalogu ve sprint planları otomatik üretildi.

---

## Geliştirme Önerileri

### 1. Uzun Oturumda Kural/Bağlam Kayması

**Sorun:** 13 sprint, 30+ oturumda aynı hataların tekrar yapıldığı gözlemlendi.
Örneğin KURAL 29 (plan sun, onay bekle) birden fazla kez tanımlanmak zorunda kalındı.

**Gözlem:** Claude, oturum başında belirlenen kuralları oturum sonunda daha az
uyguluyordu. Özellikle "plan sunmadan dosya değiştirme" kuralı defalarca hatırlatıldı.

**Öneri:** Uzun ajansal görevlerde, kullanıcının tanımladığı kuralların mid-session
özet kontrolü veya "kural uyum skoru" gibi bir mekanizma yardımcı olabilir.

### 2. Varsayım Yapma Eğilimi

**Sorun:** Claude sık sık "muhtemelen X'tir", "büyük olasılıkla Y dosyasındadır"
gibi doğrulanmamış ifadeler kullandı. Bu ifadelerin doğrulanmadan devam etmesi
bazen yanlış bug fix'lere yol açtı.

**Spesifik örnek:** PFAZ12'de BootstrapCI'nin neden dead code olduğunu sormadan
önce Claude "büyük olasılıkla sprint 10'da devre dışı bırakılmış" dedi — oysa
hiç aktif edilmemiş bir modüldü.

**Öneri:** Teknik iddiaları "kanıtlanmış" vs "varsayım" olarak açıkça etiketlemek,
kullanıcının hangi bilgiyi doğrulaması gerektiğini anlamasına yardımcı olur.

### 3. Paralel Agent Koordinasyonu

**Gözlem:** Codex (paralel AI ajan) aynı codebase'de Claude'un kaçırdığı 4 kritik
bug'ı yakaladı (PIPESTATUS, silent failure, dep check, strict mode). Bu, farklı
"bakış açılarının" tamamlayıcı olduğunu gösteriyor.

**Öneri:** Karmaşık ajansal görevlerde, özellikle güvenlik/doğruluk kritik
noktalarda "ikinci göz" mekanizması (başka bir Claude instance'ının review yapması)
seçeneği değerli olabilir.

### 4. Kod Değişikliği Onayı

**Sorun:** Bazı oturumlarda Claude, onay almadan dosya değiştirdi. Bu özellikle
production sistemlerde riskli.

**Öneri:** Ajansal modda "destructive operations" (dosya yazma, silme) için
kullanıcı onayı mekanizması daha belirgin olabilir. Şu an bu büyük ölçüde
promptlara bırakılmış durumda.

### 5. Uzun Oturum Yönetimi

**Gözlem:** Tool limit yaklaştığında (her oturumda) hem kod hem dokümantasyon
yazmanın tamamlanması güçleşiyor. Handoff mekanizmaları (sprint handoff.md)
geliştirmek zorunda kaldık.

**Öneri:** Uzun ajansal görevler için "checkpoint + resume" — yani oturum
ortasındaki durumu kaydetme ve yeni oturumda devam etme — daha akıcı bir deneyim
sunabilir.

---

## Teknik Geri Bildirim

### Başarılı Kullanım Senaryoları

- 99 bug'ın sistematik kataloglanması ve fix'lenmesi
- HPC/Slurm pipeline'ı için güvenli exit code zinciri tasarımı
- ANFIS + AI hibrit pipeline için istatistiksel karşılaştırma modülü
- Cross-project QA playbook üretimi

### Zorlu Senaryolar

- Çok dosyalı refactoring (20+ dosya aynı anda değişince bağlam kaybı)
- Runtime behavior simulation (Bash pipe, Python exception zinciri)
- Kümülatif bağlam (Sprint 13'te Sprint 1'deki kararlar hâlâ geçerliydi)

---

## Genel Değerlendirme

Claude ile 13 sprint boyunca 7000+ satır production-ready kod, 99 bug fix ve
kapsamlı dokümantasyon ürettik. Tez için 1 hafta kalan bu noktada pipeline
TRUBA'ya akıyor.

En büyük değer: karmaşık teknik sorunları sistematik analiz etme kapasitesi.
En büyük gelişim alanı: uzun oturumlarda kural tutarlılığı ve varsayım azaltma.

---

*Bu rapor, Claude'un iyileştirilmesine katkıda bulunmak amacıyla gönüllü olarak paylaşılmaktadır.*
