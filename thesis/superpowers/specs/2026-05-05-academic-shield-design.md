# Academic Shield Skill — Tasarım Belgesi

**Tarih:** 2026-05-05  
**Durum:** Onay Bekliyor  
**Hedef:** AI dedektörlerini atlayan, SAÜ kurallarına uygun Türkçe akademik yazı skill'i

---

## 1. Problem Tanımı

### Mevcut Durum
- `humanizer` skill'i 29 yüzey AI kalıbını temizliyor — kelime ve cümle düzeyinde
- Turnitin AI, GPTZero, QuillBot gibi dedektörler artık **yapısal** ve **istatistiksel** sinyallere bakıyor
- Kelime değiştirmek yetmiyor; **perplexity**, **burstiness**, **semantic coherence** ölçümleri yapılıyor
- Türkçe akademik yazıya özgü insan sinyalleri yok

### Hedef Durum
- AI metnini, dedektörlerin "insan yazdı" dediği Türkçe akademik metne dönüştür
- Yazarken (sıfırdan) de aynı kaliteyi üret — sadece post-editing değil
- SAÜ tez format kurallarına ve IEEE/APA atıf stiline uygun çıktı ver
- İntihal riskini tespit et, doğru parafraz/alıntı kararı ver

---

## 2. Hedef Dedektörler

| Dedektör | Yöntem | Zayıf Noktası |
|---------|--------|---------------|
| GPTZero | Perplexity + Burstiness | Düşük burstiness = AI sinyali |
| Turnitin AI | Transformer tabanlı sınıflandırıcı | Semantik tutarlılık + kelime seçimi |
| Copyleaks | Hibrit: kelime + semantik | Cümle yapısı varyasyonu |
| ZeroGPT | N-gram analizi | Tekrar eden kalıplar |
| Originality.ai | GPT-2 tabanlı perplexity | Token olasılık dağılımı |
| iThenticate | Kelime eşleştirme + intihal | Kaynak benzerliği |
| YÖK İntihal | Türkçe kelime eşleştirme | Doğrudan kopyalama |
| Unicopy.ai | Hibrit AI+intihal | Kombinasyon tespiti |
| QuillBot AI | Transformer tabanlı | Üretken model imzası |

---

## 3. Mimari: İki Mod

### Mod A — Dönüşüm (Transform)
Girdi: Yazılmış AI metni → Çıktı: İnsanlaştırılmış akademik metin

### Mod B — Üretim (Write)
Girdi: Konu/argüman/notlar → Çıktı: Sıfırdan AI izi taşımayan akademik metin

Her iki modda da aynı 3 aşamalı pipeline çalışır:

```
[Girdi]
   ↓
AŞAMA 1 — TANI (Diagnose)
   ├── Perplexity/Burstiness analizi simülasyonu
   ├── Yapısal AI iz tespiti (cümle ritmi uniformluğu, geçiş kalıpları)
   ├── İntihal risk noktaları
   └── SAÜ format uyum eksiklikleri
   ↓
AŞAMA 2 — DERİN DÖNÜŞÜM (Deep Transform)
   ├── Katman 1: Yapısal yeniden yazım
   ├── Katman 2: Türkçe akademik ses kalibrasyonu
   ├── Katman 3: Atıf entegrasyonu
   └── Katman 4: Burstiness optimizasyonu
   ↓
AŞAMA 3 — DOĞRULAMA (Verify)
   ├── Self-test: dedektör simülasyonu
   ├── SAÜ uyum kontrolü
   └── Final çıktı + değişiklik raporu
```

---

## 4. Derin Dönüşüm Katmanları

### Katman 1: Yapısal Yeniden Yazım

**AI metninin yapısal izleri:**
- Uniform cümle uzunluğu (her cümle 15-25 kelime)
- Her paragraf aynı akış: "topic sentence → 3 destek → sonuç"
- Akıcı, hatasız, hiç beklenmedik kelime seçimi yok

**İnsan yazısının yapısal özellikleri (12 SAÜ tezi analizinden):**
- Kısa keskin cümleler + uzun bileşik Türkçe cümleler (değişken ritim)
- Paragraf içinde "sinyal verme": "Nitekim,", "Ancak," ile sürpriz dönüş
- Kendi önceki argümanına geri referans
- Somut sayı/ölçüm (soyut iddia değil)

**Dönüşüm kuralları:**
1. Her 3-4 uzun cümleden sonra 1 kısa keskin cümle (burstiness yaratır)
2. Paragraf başlangıçlarını çeşitlendir: özel durumla başla, zıt görüş sun
3. Bir argümanı 2 farklı açıdan sun (redundancy = insan sinyali)
4. Soyut iddiayı somut veriye dönüştür

### Katman 2: Türkçe Akademik Ses Kalibrasyonu

**Fiil sonları — kesinlik spektrumu (SAÜ tezlerinden):**
- `-mektedir/-maktadır` → otoriter, yerleşik bilgi
- `-mıştır/-miştir` → tamamlanmış eylem, sonuç
- `-malıdır/-melidir` → öneri, zorunluluk
- `-bilmektedir` → olasılık, hedging
- `-görülmektedir` → gözlem tabanlı yorum
- `-düşünülmektedir` → yorumsal, tartışmalı

**Doğal Türkçe geçiş kalıpları (tezlerden çıkarıldı):**
- Karşıt: "Ancak,", "Bununla birlikte,", "Öte yandan,"
- Ekleyici: "Bunun yanı sıra,", "Nitekim,", "Ayrıca,"
- Sonuç: "Bu nedenle,", "Dolayısıyla,", "Bu bağlamda,"
- Açıklayıcı: "Söz konusu", "Bahsi geçen", "Yukarıda da ifade edildiği üzere,"
- Kendi çalışmaya: "Bu tez kapsamında,", "Çalışmamızda,", "Mevcut araştırmada,"

**Kaçınılacak AI kalıpları (Türkçe'ye özgü):**
- "Bu bağlamda değerlendirmek gerekirse" (çok smooth)
- Her paragraf "Bu çalışmada..." ile başlıyor (uniform)
- Aynı fiil sonu 3+ ardışık cümlede (monotonluk)
- "önemli bir yer tutmaktadır" / "kritik bir öneme sahiptir" (AI klişesi)
- Belirsiz özne: "Araştırmalar göstermektedir ki" (kaynak yok)

### Katman 3: Atıf Entegrasyonu

**SAÜ tez formatı — atıf stilleri:**
- Teknik/fen bilimleri: **IEEE numaralı** `[1]`, `[2]`, `[9-10]`
- Sosyal bilimler: **APA** `(Yazar, yıl; Yazar vd., yıl)` — "vd." Türkçe!
- Doğrudan alıntı <4 satır: metin içinde tırnak, italik değil, 12pt
- Doğrudan alıntı >4 satır: 1cm girintili blok, 11pt, tırnak içinde
- Parafraz: atıf şart, tırnak yok

**İntihal risk seviyeleri:**
- 🔴 Yüksek: Direkt kopyalama, sadece fiil sonu değiştirme
- 🟡 Orta: Kelime değiştirme (%50+ örtüşme), atıfsız parafraz
- 🟢 Düşük: Doğru parafraz + atıf, veya doğrudan alıntı + atıf

**Gerçek parafraz kriterleri:**
- Kaynaкla %30'dan az kelime örtüşmesi
- Sadece kelime değiştirme = semantic plagiarism riski
- Fikri yeniden yap, farklı yapıyla sun, atıf ver

### Katman 4: Burstiness Optimizasyonu

**Temel kavramlar:**
- **Perplexity**: Metnin tahmin edilemezliği. AI düşük perplexity üretir (çok smooth).
- **Burstiness**: Cümle uzunluğunun değişkenliği. İnsanlar yüksek burstiness = kısa+uzun karışık. AI uniform.

**Burstiness artırma teknikleri:**
1. Ara sıra çok kısa cümle: "Bu sonuç beklenmedikti." (4 kelime)
2. Bir cümleyi ikiye böl — sonra bağlaç: "X çalışır. Y de çalışır, ama farklı mekanizmayla."
3. Parantez içi açıklama: "...değerleri (bkz. Tablo 3.2) bu hipotezi desteklemektedir."
4. Bağlaçlı uzun cümle: "...olmakla birlikte, ...olduğu düşünülürse, ...sonucuna ulaşılabilir."

---

## 5. Mod B — Yazarken Kullanım (Üretim Modu)

**Girdi:** Konu + temel argümanlar + kaynaklar  
**Çıktı:** Dedektörlerden geçecek Türkçe akademik metin

**Üretim Protokolü:**
1. Argüman iskeletini çıkar
2. Her paragraf için:
   - Savunulacak bir pozisyon seç
   - 1-2 karşı argüman/sınırlama ekle (tartışma derinliği = insan sinyali)
   - Gerçek kaynak verisini/sayısını entegre et
   - Katman 2 ses kalibrasyonunu uygula
3. Paragraflar arası geçiş kontrolü: son cümle → ilk cümle bağlantısı
4. Burstiness optimizasyonu uygula

---

## 6. SAÜ Format Kompliansı

Skill çıktısı şu kurallara uyar:
- Doğrudan alıntı <4 satır: tırnak + italik değil + atıf (aynı paragraf, 12pt)
- Doğrudan alıntı >4 satır: 1cm girintili blok, 11pt, tırnak
- Atıf stili: tezin alanına göre IEEE veya APA tespit edip uygula
- URL'lerde erişim tarihi zorunlu: "Erişim Tarihi xx/xx/xxxx" veya "E.T. xx/xx/xxxx"

---

## 7. Self-Test Protokolü (Aşama 3)

```
DEDEKTÖR SİMÜLASYONU:
□ Burstiness: Cümle uzunlukları değişken mi? (min ~5, max ~40 kelime var mı?)
□ Geçiş çeşitliliği: Aynı geçiş kalıbı 3+ kez tekrar ediyor mu?
□ Fiil sonu çeşitliliği: 3+ farklı son tipi kullanıldı mı?
□ Özgünlük: Gerçek veri/sayı var mı, soyut iddia değil?
□ Paragraf başlangıçları: Hepsi aynı yapıda mı?

İNTİHAL KONTROL:
□ Doğrudan alıntılar tırnak + atıf içeriyor mu?
□ Parafrazlar kaynaklı mı?
□ Kaynak örtüşmesi %30 altında mı?

SAÜ UYUM:
□ Atıf stili tutarlı mı?
□ Alıntı formatı kurallara uygun mu?
```

---

## 8. Çıktı Formatı

```
## TANI RAPORU
- Tespit edilen AI sinyalleri: [liste]
- İntihal risk noktaları: [liste]
- SAÜ uyumsuzlukları: [liste]

## DÖNÜŞTÜRÜLMÜŞ METİN
[Final metin]

## UYGULANAN DÖNÜŞÜMLER
- Yapısal: [özet]
- Ses: [özet]
- Atıf: [özet]
- Burstiness: [özet]

## KALAN RİSKLER
[Varsa uyarılar]
```

---

## 9. C Dokümantasyonu — Tam Akademik Yazı Sistemi (Gelecek)

**Hedef:** Araştırma notları → Bitmiş tez bölümü  
**Gerekli subagent'lar:**
1. `research-integrator`: Kaynak tarama, özet çıkarma
2. `argument-builder`: Kaynaklardan argüman zincirleri oluşturma
3. `academic-writer`: Katman 2 ses ile yazma
4. `academic-shield`: Bu skill — AI iz temizleme + atıf entegrasyonu

**Tahmini token maliyeti:** ~50K token/bölüm → Pahalı, manuel onay gerektiren adımlar olmalı  
**Önkoşullar:** Bu skill (academic-shield) önce tamamlanmalı

---

## 10. Uygulama Planı (writing-plans'a girecek)

### Aşama 1: Araştırma (Paralel Agentlar)
- AI dedektör mekanizmaları (perplexity, burstiness, transformer sınıflandırıcılar)
- Akademik intihal tespiti, YÖK/Turnitin/iThenticate kuralları
- SAÜ format kurallarının tam MD çıkarımı
- Türkçe akademik ses profili (tez örneklerinden)

### Aşama 2: Referans Dosyaları
- `references/sau-format-rules.md`
- `references/turkish-academic-voice.md`
- `references/ai-detector-mechanics.md`
- `references/plagiarism-rules.md`

### Aşama 3: Skill Yazımı
- `academic-shield/SKILL.md` (frontmatter + tüm protokoller)

### Aşama 4: Test
- Tez örneği üzerinde Mod A testi
- Konu verilerek Mod B testi
- GPTZero/QuillBot ile manuel doğrulama

---

*Tasarım Belgesi v1.0 | 2026-05-05*
