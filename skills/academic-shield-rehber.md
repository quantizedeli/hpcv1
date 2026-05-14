# Academic Shield — Tam Kapsamlı Rehber

> **Sürüm:** 1.0 | **Lisans:** MIT  
> **Proje:** skillv1 özel skill  
> **Son Güncelleme:** 2026-05-06

---

## İçindekiler

1. [Hızlı Başlangıç Kartı](#hızlı-başlangıç-kartı)
2. [Skill Anatomisi](#skill-anatomisi)
3. [İki Mod](#iki-mod)
4. [3 Aşamalı Pipeline](#3-aşamalı-pipeline)
5. [Aşama 1: Tanı](#aşama-1-tanı)
6. [Aşama 2: Derin Dönüşüm (4 Katman)](#aşama-2-derin-dönüşüm-4-katman)
7. [Aşama 3: Doğrulama](#aşama-3-doğrulama)
8. [Mod B: Üretim Protokolü](#mod-b-üretim-protokolü)
9. [Bölüm Bazlı Ses Şeması](#bölüm-bazlı-ses-şeması)
10. [Türkçe Akademik Ses Profili](#türkçe-akademik-ses-profili)
11. [SAÜ Format Kuralları](#saü-format-kuralları)
12. [Ekosistem Entegrasyonu](#ekosistem-entegrasyonu)
13. [Humanizer ile Fark](#humanizer-ile-fark)
14. [Kaynaklar](#kaynaklar)

---

## Hızlı Başlangıç Kartı

```
# Skill otomatik tetiklenir:
"tez yaz", "bölüm yaz", "giriş yaz"       → Mod B (üretim)
"şu metni düzenle", "dedektörden geçir"    → Mod A (dönüşüm)
"ai izi temizle", "humanize akademik"      → Mod A
"academic-shield"                          → Mod sorusu sor
```

---

## Tetikleyiciler

| Kullanıcı Yazdığında | Tetiklenen | Mod |
|----------------------|------------|-----|
| `academic-shield` | academic-shield | Soru sor |
| "akademik yaz" | academic-shield | Mod B |
| "tez yaz" | academic-shield | Mod B |
| "bölüm yaz" | academic-shield | Mod B |
| "giriş yaz" | academic-shield | Mod B |
| "metodoloji yaz" | academic-shield | Mod B |
| "literature review yaz" | academic-shield | Mod B |
| "dedektörden geç" | academic-shield | Mod A |
| "ai izi temizle" | academic-shield | Mod A |
| "humanize akademik" | academic-shield | Mod A |
| "şu metni düzenle" + akademik bağlam | academic-shield | Mod A |
| "literatür tara" | literature-review | Bağımsız |
| "kaynak bul" + tez bağlamı | literature-review | Bağımsız |
| "makale yaz" / "paper" | academic-writing-pro | Yönlendirme |

**Ne sunar:**
- AI iz tespiti ve temizleme (GPTZero, Turnitin, Copyleaks, ZeroGPT, YÖK İntihal bypass)
- 4 katmanlı derin dönüşüm pipeline
- 12 onaylı SAÜ/Türkiye tezinden çıkarılan gerçek akademik ses kalibrasyonu
- IEEE ve APA Türkçe atıf sistemi entegrasyonu
- İntihal önleme ve parafraz kalite kontrolü
- SAÜ tez format uyumu

---

## Skill Anatomisi

```
skillv1/
├── academic-shield/
│   └── SKILL.md              ← Skill tanımı ve tüm protocol
├── references/
│   ├── turkish-academic-voice.md     ← 12 onaylı tezden ses profili
│   ├── sau-format-rules.md           ← SAÜ tez format + atıf kuralları
│   ├── ai-detector-mechanics.md      ← Dedektör mekanizmaları
│   └── plagiarism-rules.md           ← İntihal tespit + parafraz kriterleri
```

**Tetikleyiciler:**
- `academic-shield` (doğrudan)
- "akademik yaz", "tez yaz", "dedektörden geç"
- "ai izi temizle", "humanize akademik"

---

## İki Mod

### Mod A — Dönüşüm

**Kullanım:** Mevcut AI metni veya taslak varsa

- "bunu düzenle", "bunu insanlaştır", "dedektörden geçir", "şu metni..."
- Tanı Raporu + Dönüşüm + Uygulanan Değişiklikler + Kalan Riskler çıktısı

### Mod B — Üretim

**Kullanım:** Konu/argüman/not varsa — sıfırdan yazma

- "şu konuda yaz", "bu bölümü yaz", "giriş yaz", "metodoloji yaz"
- **Bu mod en kritiktir** — AI yazarken iz bırakmadan üretmek

**Mod belirsizse sor:** "Bu metni dönüştürmemi mi istiyorsunuz, yoksa konudan sıfırdan üreteyim mi?"

---

## 3 Aşamalı Pipeline

```
[Girdi]
   ↓
AŞAMA 1 — TANI
   ↓
AŞAMA 2 — DERİN DÖNÜŞÜM (4 Katman)
   ↓
AŞAMA 3 — DOĞRULAMA
   ↓
[Çıktı]
```

---

## Aşama 1: Tanı

**Mod A için çıktıya ekle:**

```
TANI RAPORU
───────────
AI Sinyalleri:
• Cümle uzunluğu: [uniform mu? std. sapma tahmini]
• Tekrar eden fiil sonu: [-mektedir × kaç kez ardışık?]
• Tekrar eden geçiş kalıpları: [hangileri?]
• AI klişeleri: [listele]
• Atıf eksikliği: [kaynak yok veya az]
• Paragraf yapısı: [hepsi aynı şema mı?]

İntihal Risk Noktaları:
• [%30+ kelime örtüşmesi şüpheli bölgeler]
• [Atıfsız parafraz olası noktalar]

SAÜ Uyumsuzlukları:
• [Atıf stili hatası, blok alıntı formatı, URL erişim tarihi eksikliği]
```

**Mod B için:** Tanı atla, doğrudan üretim protokolüne geç.

---

## Aşama 2: Derin Dönüşüm (4 Katman)

### Katman 1: Yapısal Yeniden Yazım

**Hedef:** Burstiness artır, Perplexity yükselt

**Kural 1 — Cümle Uzunluğu Değiştir:**
- Her 3-4 uzun cümle (25-45 kelime) sonrasında 1 kısa cümle (4-8 kelime) ekle
- Uzun cümleyi ikiye böl: "X doğrudur. Y de doğrudur, ama farklı nedenlerle."
- Parantez ile içeriden uzat: "...değerleri (bkz. Tablo 3.2) bu hipotezi desteklemektedir."

**Kural 2 — Paragraf Yapısını Değiştir:**

"topic → 3 destek → sonuç" kalıbı her paragrafta olmaz. Seçenekler:
- Karşıt görüşle başla → çürüt
- Spesifik örnekle başla → genelleştir
- Tarihsel bağlamla başla → günümüze bağla
- Önceki paragrafın son fikrine referansla başla
- Kısa retorik soruyla başla → cevapla

**Kural 3 — Somut Veri Ekle:**
- "birçok çalışma" → "26 bağımsız çalışma [X-Y]"
- "son dönemde" → "Yazar (2021) tarafından"
- "başarılı" → "%94.3 doğruluk oranıyla"

**Kural 4 — Paragraflar Arası Bağlantı:**
- Her yeni paragraf bir öncekine referans ver
- "Yukarıda da belirtildiği üzere...", "Bu bulguyla bağlantılı olarak..."

---

### Katman 2: Türkçe Akademik Ses Kalibrasyonu

**Fiil Sonu Çeşitliliği — Her 5 cümlede EN AZ 3 farklı tip:**

| Son | Bağlam |
|-----|--------|
| `-mektedir/-maktadır` | Genel kabul, tanım, literatür özeti |
| `-mıştır/-miştir` | Tamamlanmış eylem, tarihsel bilgi |
| `-görülmüştür` | Gözleme dayalı sonuç |
| `-düşünülmektedir` | Yorumsal, tartışmalı |
| `-gerekmektedir` | Zorunluluk, öneri |
| `-bilmektedir` | Olasılık, hedging |
| `-değerlendirilmektedir` | Aktif yorum |
| `-elde edilmiştir` | Analiz sonucu |

**Geçiş Kalıbı Çeşitliliği — Aynı kalıp 2 ardışık kullanılamaz:**

```
Karşıt:   Ancak, | Bununla birlikte, | Öte yandan, | Ne var ki,
Ekleyici: Bunun yanı sıra, | Nitekim, | Ayrıca, | Özellikle, | Buna ek olarak,
Sonuç:    Bu nedenle, | Dolayısıyla, | Bu bağlamda, | Bu çerçevede,
Referans: Söz konusu | Bahsi geçen | Yukarıda da ifade edildiği üzere,
Kendi:    Bu tez kapsamında, | Mevcut çalışmada, | Bu araştırmada,
```

**Paragraf Başlangıç Çeşitliliği — Ardışık iki paragraf aynı stratejiyle başlayamaz:**

```
A: Alan/konuyla direkt açılış
B: Geçiş + ekleyici
C: Tarihsel bağlam + yıl
D: Yazar/araştırmacı atfıyla
E: Zıtlık çerçevesi ("bir yandan...sa da")
F: Spesifik tanım veya kısaltma
G: Önceki paragrafa geri referans
```

**AI Klişe Temizleme — Aşağıdaki kalıplar varsa yeniden yaz:**

```
❌ "Bu bağlamda değerlendirmek gerekirse"
❌ "önemli bir yer tutmaktadır" / "kritik bir öneme sahiptir"
❌ "kapsamlı bir şekilde ele alınmaktadır"
❌ "günümüz dünyasında" / "hızla gelişen"
❌ "Araştırmalar göstermektedir ki" (kaynak yok)
❌ "birçok araştırmacı tarafından vurgulanmıştır" (kaynak yok)
❌ 3+ ardışık cümlede aynı fiil sonu
❌ Her paragraf "Bu çalışmada..." ile başlıyor
❌ "Belirtmek/Vurgulamak gerekir ki"
```

---

### Katman 3: Atıf Entegrasyonu

**Alan Tespiti (zorunlu ilk adım):**
- Fen/Mühendislik/Biyomedikal → IEEE: `[1]`, `[2-5]`, `[41-44]`
- Sosyal/Eğitim/Psikoloji/İşletme → APA Türkçe: `(Yazar, yıl)`, `(Yazar vd., yıl)`

**IEEE Kuralları:**
```
[1]                    → tek kaynak
[1-5]                  → ardışık aralık
[1, 3, 7]              → seçili birden fazla
ref. [36]'dan          → pasif kaynak
[42, s. 15]            → sayfayla
Yazar ve ark. [41-44]  → yazar + atıf beraber
```

**APA Türkçe Kuralları:**
```
(Yazar, 2021)           → tek yazar
(Yazar ve Yazar2, 2021) → iki yazar: "ve" (NOT "and")
(Yazar vd., 2021)       → 3+ yazar: "vd." (NOT "et al.")
(A, 2021; B vd., 2023)  → çoklu: noktalı virgülle
(Yazar, 2021, s. 45)    → sayfayla
```

**Doğrudan Alıntı Formatı:**
- <4 satır: tırnak + atıf, italik YOK, 12pt
- ≥4 satır: 1cm girintili blok, 11pt, tırnak YOK, atıf sonda

**İntihal Önleme:**
- Parafrazda kelime örtüşmesi <%30
- Yapısal dönüşüm zorunlu (sadece kelime/fiil değiştirme yetmez)
- Her parafrazda atıf var mı?

---

### Katman 4: Burstiness Optimizasyonu

1. **Kısa cümle enjeksiyonu:** Uzun paragrafın ortasına 4-7 kelimelik cümle
   - "Bu sonuç beklenmedikti." / "Tablo 4.1 bu durumu özetlemektedir."

2. **Bölünmüş cümle:** Noktalı virgül veya noktayla böl, sonra bağla
   - "X çalışır; Y ise farklı bir mekanizmayla aynı sonuca ulaşır."

3. **Parantez genişletme:** İçeriden uzatmak için
   - "...parametreleri (bkz. Tablo 4.2, Şekil 3.1) hesaba katıldığında..."

4. **Tablo/şekil referans cümlesi:** Doğal kısa cümle
   - "Sonuçlar Şekil 4.6'da verilmiştir."

**Kontrol:** Her paragrafta minimum 3 farklı uzunluk kategorisi:
- Kısa (4-10 kelime) + Orta (15-25 kelime) + Uzun (30-50 kelime)

---

## Aşama 3: Doğrulama

```
DEDEKTÖR SİMÜLASYONU
□ Burstiness: En kısa < 10 kelime VE en uzun > 30 kelime var mı?
□ Cümle çeşitliliği: Sadece 15-22 kelime aralığında kalan var mı? (varsa düzelt)
□ Geçiş: Aynı kalıp 2+ ardışık var mı? (varsa değiştir)
□ Fiil: Her 5 cümlede 3+ farklı son tipi var mı?
□ Özgünlük: Gerçek sayı/yıl/veri var mı?
□ Paragraf başlangıçları: Aynı strateji 2+ ardışık var mı? (varsa değiştir)
□ AI klişe tarama: 9 yasaklı kalıptan biri var mı?

İNTİHAL KONTROL
□ Doğrudan alıntılar: tırnak + atıf var mı?
□ Blok alıntılar: 1cm girinti + 11pt + tırnak yok + atıf var mı?
□ Parafrazlar: %30 altı örtüşme + yapısal dönüşüm + atıf?
□ URL'ler: E.T. tarihi var mı?

SAÜ UYUM
□ Atıf stili alan ile uyumlu? (IEEE veya APA Türkçe)
□ APA'da "vd." kullanıldı (et al. değil)?
□ Tablo başlıkları üstte, şekil başlıkları altta?
```

---

## Çıktı Formatı

```markdown
## TANI RAPORU
**AI sinyalleri:** [liste]
**İntihal risk noktaları:** [liste]
**SAÜ uyumsuzlukları:** [liste]

---

## DÖNÜŞTÜRÜLMÜŞ / ÜRETİLMİŞ METİN

[Final metin]

---

## UYGULANAN DÖNÜŞÜMLER
- **Yapısal:** [cümle uzunluğu, paragraf yapısı değişiklikleri]
- **Ses:** [fiil son değişiklikleri, klişe temizleme, geçiş çeşitlendirmesi]
- **Atıf:** [format düzeltmeleri]
- **Burstiness:** [kısa cümle enjeksiyonu, bölünmüş cümleler]

## KALAN RİSKLER
[Gerçek kaynak verilmediğinde uyar: "[KAYNAK]" placeholder kullanıldı]
[Dedektör risk tahmini: Düşük / Orta / Yüksek]
```

---

## Mod B: Üretim Protokolü (Sıfırdan Yazma)

**Girdi:** Konu + temel argümanlar + kaynaklar (varsa)

**Adım 1 — Argüman iskeleti:**
- Ana tez nedir?
- 3-5 destekleyici alt argüman?
- Karşı argümanlar / sınırlılıklar?

**Adım 2 — Her paragraf için:**
1. Paragraf stratejisi seç (A-G havuzundan)
2. Savunulacak pozisyonu belirle
3. 1-2 karşı argüman veya sınırlama ekle
4. Gerçek kaynak verisi/sayısı entegre et (varsa)
5. Katman 2 ses kalibrasyonunu uygula
6. Burstiness kontrolü: 3 farklı uzunluk kategorisi var mı?

**Adım 3 — Paragraflar arası bağlantı:**
- Her paragrafın son cümlesi → bir sonrakinin konusunu ima et
- Bölüm geçiş cümlesi: "Bu kısımda öncelikle...ele alınacaktır. Sonrasında ise..."

**Kaynak yoksa uyar:**
> "Bu bölüm için gerçek kaynaklar verilmedi. Atıf `[KAYNAK]` ile işaretlendi — gerçek atıflarla doldurun."

---

## Bölüm Bazlı Ses Şeması

### ÖZET

- Şimdiki zaman baskın: `-mektedir`, `-sunmaktadır`
- Yüzde + sayı: "%80 eğitim, %20 test"
- Son cümle: ilk kez iddiası veya ana bulgu
- 150-300 kelime

**Örnek açılış:**
> "Bu tez çalışması, yapay sinir ağları, bulanık mantık ve sinirsel-bulanık mantık gibi yaygın kullanılan yapay zekâ yöntemlerinin ayrıntılarını ele almakta..."

---

### GİRİŞ

- Tarihsel açılış + alan önemi
- Aralık atıflar: "[6-29]"
- Zıtlık: "...olmasına rağmen hâlâ tatmin edici teori yok"
- Köprü: "Bu nedenle, mevcut çalışmada..."

**Fen Bilimleri şablonu:**
> "[Alan], [önem iddiası]. [Tarihsel süreç + sayı]. [IEEE atıf]"

**Sosyal Bilimler şablonu:**
> "Genel fenomen (APA atıf) → özelleştirme (APA atıf) → alan bağlantısı"

---

### MATERYAL VE METOD

- Gelecek zaman yol haritası: "...hesaplanacaktır. Sonrasında ise..."
- Her parametre için kaynak: "ref. [36]'dan alınmıştır"
- Pasif baskın: "...ayrılmıştır", "...uygulanmıştır"

**Adım sıralaması:** "Öncelikle...Sonrasında ise..."

---

### BULGULAR

- Tablo/şekil referansları: "Tablo 4.1'de verilmiştir"
- Değerlendirme kalıbı: "iyi sonuçlar verdiği görülmüştür"
- Karşılaştırma: "...ile karşılaştırıldığında"

**Fen:** `-verdiği görülmüştür`, `-hesaplanmıştır`, `-elde edilmiştir`

**Sosyal:** "Araştırma sonucunda...belirlendi/tespit edildi"

---

### TARTIŞMA / SONUÇ

- Hedged prediction: "...değerlendirilebilir", "...açabilir"
- Literatür karşılaştırma: "(Yazar, yıl) ile örtüşmektedir"
- Sınırlılık: "Bu çalışmanın sınırlılıkları arasında..."
- Gelecek: "İleride yapılacak çalışmalarda..."

---

## Türkçe Akademik Ses Profili

*12 onaylı SAÜ/Türkiye tezi doğrudan incelendi (822345, 949921, 980050, 980384, 465309, 244456, 246515, 424326, 651082, 963786, 971168, 167516)*

### Gerçek Tezlerde Var Olan İnsan Sinyalleri

```
✅ Kısa keskin cümle: "Bu iki yöntem karşılaştırılacaktır." (5 kelime)
✅ Tablo referansı: "...değerleri Tablo 4.1'de verilmiştir."
✅ Parantez açıklama: "(bkz. Tablo 4.1, Şekil 3.2)"
✅ Teknik kısaltma: "Kuaziparçacık Tamm-Dancoff Yaklaşımı (QTDA)"
✅ Atıf aralığı: "[6-29]", "[41-44]"
✅ Denklem referansı: "(3.23) genel bağlantısı..."
✅ Önceki bölüme referans: "Üçüncü bölümde de belirtildiği üzere..."
✅ Yazar+atıf beraber: "Yakut ve ark. [41-44] tarafından"
✅ Spesifik sayılar: "%80 eğitim, %20 test", "715 öğrenci"
✅ İlk kez iddiası: "Bu izotoplar...ilk kez ele alınmıştır"
✅ Sınırlılık itirafı: "Mevcut sistemlere yalnızca veri yükleyerek..."
```

### Gerçek Tezlerde Hiç Bulunmayan AI Klişeleri

```
❌ "Bu bağlamda değerlendirmek gerekirse"
❌ "önemli bir yer tutmaktadır" / "kritik bir öneme sahiptir"
❌ "kapsamlı bir şekilde ele alınmaktadır"
❌ "günümüz dünyasında" / "hızla gelişen teknoloji dünyasında"
❌ "Araştırmalar göstermektedir ki" (kaynak yok)
❌ "birçok araştırmacı tarafından vurgulanmıştır" (kaynak yok)
❌ 3+ ardışık cümlede aynı fiil sonu
❌ Her paragraf tam "topic → 3 destek → sonuç" şablonu
❌ Paragraflar arası geçişsiz bağlantı
```

---

## SAÜ Format Kuralları

*Kaynak: SAÜ Tez Yazım Kılavuzu (16.02.pdf) + 12 onaylı tez*

### Sayfa Düzeni

| Özellik | Kural |
|---------|-------|
| Kağıt | A4 |
| Sol kenar boşluk | 3.5 cm |
| Sağ, üst, alt | 2.5 cm |
| Yazı tipi | Times New Roman |
| Ana metin boyutu | 12 pt |
| Satır aralığı | 1.5 |

### Başlık Hiyerarşisi

| Seviye | Format |
|--------|--------|
| 1. Seviye | BÜYÜK HARF, Kalın, Ortalı (**1. GİRİŞ**) |
| 2. Seviye | Başlık Harfleri, Kalın (**1.1 Manyetik Moment**) |
| 3. Seviye | Başlık Harfleri, İtalik (*1.1.1 QPNM Yöntemi*) |

### Atıf Sistemi

**Alan tespiti:** `[1]` görüyorsan → IEEE. `(Yazar, yıl)` görüyorsan → APA.

| Alan | Enstitü | Atıf Stili |
|------|---------|-----------|
| Fizik, Mühendislik, Biyomedikal | Fen Bilimleri Enstitüsü | IEEE |
| Sosyal Hizmet, Eğitim, Psikoloji | Sosyal Bilimler Enstitüsü | APA Türkçe |
| İşletme, İktisat | Sosyal Bilimler Enstitüsü | APA Türkçe |

### URL ve Web Kaynağı

SAÜ zorunluluğu: Erişim tarihi zorunlu

```
IEEE: [X] Yazar A., (Yıl). Başlık. [Online]. Available: https://... [E.T. 15/03/2023]
APA:  Yazar, A. A., Yıl, Başlık. Site. https://... Erişim tarihi: 15 Mart 2023.
```

### SAÜ Uyum Kontrol Listesi

```
□ Font: Times New Roman 12pt
□ Satır aralığı: 1.5
□ Kenar boşlukları: Sol 3.5 cm, diğerleri 2.5 cm
□ Kısa alıntılar (<4 satır): tırnak içinde + atıf, italik değil
□ Uzun alıntılar (≥4 satır): 1cm girintili blok, 11pt, tırnak yok
□ Atıf stili: Alan tespiti yapıldı mı? (IEEE mi APA mi?)
□ APA'da "vd." kullanıldı mı? (et al. değil)
□ URL'lerde erişim tarihi var mı? (E.T. xx/xx/xxxx)
□ Tablo başlıkları tablonun üstünde
□ Şekil başlıkları şeklin altında
□ Ondalık ayraç: virgül (3,5 — Türkçe kuralı)
```

---

## Ekosistem Entegrasyonu

### Combo Zincirleri

**COMBO-AC1: Araştırma → Yazma → Kalite Kapısı**
```
ultimate-research-tool → article-writing → academic-shield (MOD A)
```

**COMBO-AC2: Sıfırdan Tez Bölümü**
```
academic-shield (MOD B) → superpowers:requesting-code-review
```

**COMBO-AC3: Mevcut Tez Metnini Kurtarma**
```
academic-shield (MOD A) → GPTZero/QuillBot manuel test
```

**COMBO-AC4: Tam Literatür → Bölüm Pipeline**
```
ultimate-research-tool (kaynak tarama)
  → everything-claude-code:article-writing (taslak)
  → academic-shield MOD A (AI izi temizle)
  → superpowers:verification-before-completion
```

**COMBO-AC5: Literatür → Tez Bölümü**
```
literature-review (kaynak tarama) → academic-shield (MOD B) → çıktı
```

**COMBO-AC6: Tez → Makale Adaptasyonu**
```
academic-shield (MOD B, tez bölümü yaz)
  → academic-writing-pro (MOD A, makale formatına dönüştür)
```

### Auto-Trigger Kuralları

| Tetikleyici | Mod |
|-------------|-----|
| "tez yaz", "bölüm yaz", "giriş yaz" | Mod B |
| "şu metni düzenle", "dedektörden geçir" | Mod A |
| "ai izi temizle", "humanize akademik" | Mod A |
| "literature review yaz", "metodoloji yaz" | Mod B |
| "academic-shield" (doğrudan) | Mod sorusu sor |

### Agent Entegrasyonu

- **Önce:** `ultimate-research-tool` — kaynak ve literatür toplamak için
- **Sonra:** `superpowers:requesting-code-review` — çıktı kalite kontrolü için

---

## Humanizer ile Fark

| | `humanizer` | `academic-shield` |
|--|-------------|-------------------|
| **Hedef** | Genel yazı (blog, sosyal medya) | Akademik tez/makale |
| **Yöntem** | Yüzey AI kalıbı temizleme | Derin yapısal dönüşüm (4 katman) |
| **Çıktı dili** | Genel Türkçe/İngilizce | Türkçe akademik ses (SAÜ uyumlu) |
| **Atıf** | Yok | IEEE ve APA Türkçe entegre |
| **İntihal** | Yok | Parafraz kalite kontrolü |
| **Burstiness** | Yok | Perplexity + Burstiness optimizasyonu |

**Kural:** Akademik metin → `academic-shield`. Genel yazı → `humanizer`.

---

## Kritik Kısıtlar

1. **Gerçek kaynak olmadan atıf üretme** — `[KAYNAK]` yaz
2. **Alan tespiti zorunlu** — IEEE veya APA? Karıştırma
3. **YÖK formatı:** "vd." (et al. değil), "ve" (and değil), E.T. tarihi
4. **Parafraz sınırı:** %30 altı kelime örtüşmesi, yapısal dönüşüm şart
5. **Blok alıntı:** ≥4 satır → 1cm girinti + 11pt + tırnak yok

---

## Kaynaklar

### Referans Dosyaları

- [references/turkish-academic-voice.md](../references/turkish-academic-voice.md) — 12 onaylı SAÜ/Türkiye tezinden ses profili
- [references/sau-format-rules.md](../references/sau-format-rules.md) — SAÜ format + atıf kuralları
- [references/ai-detector-mechanics.md](../references/ai-detector-mechanics.md) — Dedektör mekanizmaları
- [references/plagiarism-rules.md](../references/plagiarism-rules.md) — İntihal tespit + parafraz kriterleri

### İlgili Belgeler

- [INDEX.md](INDEX.md) — Ana indeks
- [humanizer-rehber.md](humanizer-rehber.md) — Genel AI yazı temizleme

---

## İlgili Skill'ler

- **literature-review** — kaynak tarama modülü
  → "literatür tara" yazınca otomatik devreye girer
  → Kaynak yokken yazma talebi geldiğinde pipeline içinden otomatik tetiklenir
  → Rehber: [literature-review-rehber.md](literature-review-rehber.md)

- **academic-writing-pro** — dergi makalesi versiyonu
  → Tez bölümü → makale adaptasyonu: `academic-shield (Mod B) → academic-writing-pro (Mod A)`
  → Rehber: [academic-writing-pro-rehber.md](academic-writing-pro-rehber.md)

---

*Üretilme tarihi: 2026-05-06 | Academic Shield v1.0*  
*Kaynak: 12 onaylı SAÜ tezi + AI dedektör araştırması + SAÜ tez formatı*
