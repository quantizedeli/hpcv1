# Academic Writing Pro — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** literature-review bağımsız skill, academic-writing-pro (3 alan, LaTeX/DOCX, 5-rol pipeline), ve academic-shield güncellemesi (5-rol pipeline, agent entegrasyonu) oluşturmak.

**Architecture:** Modüler katman — SKILL.md'ler ince orkestratörler, ağır içerik references/ altındaki profil dosyalarında. literature-review her iki skill tarafından çağrılan ortak modül. citations-log.md tüm kaynakların canlı kaydı.

**Tech Stack:** Markdown skill dosyaları, LaTeX (biblatex), pandoc DOCX, Claude agent çağrıları (docs-lookup, verification-before-completion, requesting-code-review)

---

## Dosya Haritası

| Durum | Dosya | Sorumluluk |
|-------|-------|-----------|
| CREATE | `literature-review/SKILL.md` | Çok dilli tarama, 30+ veritabanı, araştırmacı notu |
| CREATE | `academic-writing-pro/SKILL.md` | 3 alan, 5-rol pipeline, LaTeX/DOCX |
| MODIFY | `academic-shield/SKILL.md` | 5-rol pipeline, literature-review entegrasyonu |
| MODIFY | `academic-shield/KULLANIM-REHBERI.md` | Yeni combolar, tetikleyiciler |
| CREATE | `references/article-voice-fen.md` | Fen/Müh makale dil profili |
| CREATE | `references/article-voice-sosyal.md` | Sosyal bilimler makale dil profili |
| CREATE | `references/article-voice-saglik.md` | Sağlık bilimleri + Vancouver profili |
| CREATE | `references/article-voice-summary.md` | 3 profilin karma özeti |
| MODIFY | `references/ai-detector-mechanics.md` | Makale formatına özgü dedektör davranışları |
| CREATE | `citations-log.md` | Canlı kaynak kaydı, DOI zorunlu |
| CREATE | `skills/literature-review-rehber.md` | Kullanım rehberi |
| CREATE | `skills/academic-writing-pro-rehber.md` | Kullanım rehberi |
| MODIFY | `skills/academic-shield-rehber.md` | Tetikleyiciler tablosu, İlgili Skill'ler |
| MODIFY | `skills/INDEX.md` | 7. ve 8. satır ekleme |
| MODIFY | `CLAUDE.md` | Yeni tetikleyiciler ve yükleme notları |

---

## Task 1: Araştırma — Fen/Müh Makale Dil Profili

**Bağımlılık:** Yok (ilk görev)
**Çıktı:** `references/article-voice-fen.md` için ham araştırma notları

- [ ] **Adım 1: Araştırma agentı çalıştır**

```python
Agent({
  subagent_type: "everything-claude-code:docs-lookup",
  prompt: """
    DergiPark ve IEEE Xplore üzerinden Türkçe hakemli dergilerde yayımlanmış
    mühendislik ve fen bilimleri makalelerinden cümle yapısı, paragraf kuruluşu,
    geçiş ifadesi repertuarı ve burstiness profili araştır.
    Her alandan minimum 5 makale incele.
    Çıktı: cümle uzunluğu dağılımı (kısa/orta/uzun yüzdeler),
    sık geçiş kalıpları, paragraf açılış stratejileri, fiil sonu dağılımı,
    bölüm bazlı ses şeması (Özet/Giriş/Yöntem/Bulgular/Tartışma).
    AI klişesi olarak görülen kelime/yapılar listesi.
  """
})
```

- [ ] **Adım 2: Sonuçları not al**

Araştırma tamamlanınca çıktıyı Task 3'te kullanmak üzere kopyala.

---

## Task 2: Araştırma — Sosyal Bilimler + Sağlık Makale Dil Profili

**Bağımlılık:** Yok (Task 1 ile paralel çalışabilir)
**Çıktı:** `article-voice-sosyal.md` ve `article-voice-saglik.md` için ham notlar

- [ ] **Adım 1: Sosyal bilimler araştırması**

```python
Agent({
  subagent_type: "everything-claude-code:docs-lookup",
  prompt: """
    DergiPark sosyal bilimler bölümünden Türkçe hakemli makaleler.
    Psikoloji, eğitim, işletme, sosyoloji — min. 5 makale.
    APA Türkçe atıf kullanımı örnekleri, 'vd.' kullanımı, paragraf yapısı.
    Burstiness analizi: kısa ve uzun cümle dağılımı.
    Nitel vs nicel makale ses farkı.
  """
})
```

- [ ] **Adım 2: Sağlık bilimleri araştırması**

```python
Agent({
  subagent_type: "everything-claude-code:docs-lookup",
  prompt: """
    PubMed ve DergiPark sağlık bilimleri bölümünden Türkçe/İngilizce makaleler.
    Tıp, hemşirelik, klinik araştırma — min. 5 makale.
    Vancouver atıf sistemi örnekleri, IMRAD yapısına özgü ses profili,
    klinik dil kalıpları (prevalans, p değeri, hasta sayısı).
    Cochrane sistematik derleme yapısı özeti.
  """
})
```

---

## Task 3: Araştırma — LaTeX + Dedektör Güncellemesi

**Bağımlılık:** Yok (paralel)
**Çıktı:** LaTeX şablonları, güncellenmiş dedektör bilgisi

- [ ] **Adım 1: LaTeX dokümantasyonu**

```python
Agent({
  subagent_type: "everything-claude-code:docs-lookup",
  prompt: """
    LaTeX Overleaf uyumlu article şablonu:
    babel turkish paketi, biblatex IEEE format, biblatex APA format,
    biblatex Vancouver format. Türkçe makale minimal working example.
    Elsevier elsarticle, IEEE IEEEtran, Springer svjour3 class dosyaları.
    pandoc DOCX üretimi: Times New Roman 12pt, 1.5 satır, reference template.
  """
})
```

- [ ] **Adım 2: Dedektör araştırması**

```python
Agent({
  subagent_type: "everything-claude-code:docs-lookup",
  prompt: """
    GPTZero, Turnitin, Copyleaks, iThenticate, YÖK İntihal — makale formatına özgü davranışlar.
    Tez ile makale arasındaki dedektör davranış farkları.
    iThenticate makale modu özellikleri.
    Turnitin makale editörü sürümü özellikleri.
    Copyleaks makale modu eşik değerleri.
    Mevcut referans: references/ai-detector-mechanics.md — eksikleri tespit et.
  """
})
```

---

## Task 4: `citations-log.md` Oluştur

**Bağımlılık:** Yok
**Çıktı:** `citations-log.md` (proje kökünde)

- [ ] **Adım 1: Dosyayı oluştur**

`citations-log.md` içeriği:

```markdown
# Citations Log

> Her kaynak kullanımında bu dosya güncellenir.
> literature-review, academic-shield, academic-writing-pro her çalışmada okur/yazar.
> Son güncelleme: [otomatik — her kaynak eklemesinde güncelle]

---

## Kayıt Formatı

Her kaynak şu şablonla eklenir:

### [No] — [IEEE / APA Türkçe / Vancouver]
- Yazar(lar): Soyadı, A. A.
- Yıl: YYYY
- Başlık: Tam başlık
- Dergi/Yayınevi: Ad, Cilt(Sayı), ss. XX-XX
- DOI: https://doi.org/10.xxxx   ← ZORUNLU — yoksa [DOI EKSİK] yaz
- URL: https://...               ← DOI yoksa
- Erişim Tarihi: GG/AA/YYYY     ← URL varsa zorunlu
- Dil: TR / EN / Diğer
- Veritabanı: Google Scholar / PubMed / Scopus / DergiPark / vb.
- Atıf IEEE:  [X] Soyadı A. A., (Yıl). Başlık. Dergi, Cilt, ss.
- Atıf APA:   Soyadı, A. A. (Yıl). Başlık. *Dergi*, Cilt(Sayı), ss. DOI
- Atıf VAN:   X. Soyadı AA. Başlık. Dergi. Yıl;Cilt(Sayı):ss. DOI
- Kullanılan sayfalar: s. XX veya ss. XX-XX
- Metin içi kullanım yeri: [bölüm adı / paragraf özeti]
- Ana Bulgu: [2-3 cümle]
- Metodoloji: [kısa özet]
- Sınırlılık: [varsa]
- Alıntılanabilir: "tam alıntı" (s. XX)

---

## Kaynaklar

<!-- Araştırma ve yazım sürecinde buraya otomatik eklenir -->
```

- [ ] **Adım 2: Doğrula**

Dosya mevcut ve boyutu > 0 ise geç.

---

## Task 5: `references/article-voice-fen.md` Oluştur

**Bağımlılık:** Task 1 (araştırma sonuçları)
**Çıktı:** `references/article-voice-fen.md`

- [ ] **Adım 1: Dosyayı oluştur**

Task 1 araştırma sonuçlarını kullanarak aşağıdaki yapıda oluştur:

```markdown
# Fen/Mühendislik Makale Dil Profili

> Kaynak: DergiPark IEEE makaleleri + IEEE Xplore Türkçe araştırma
> Kullanım: academic-writing-pro Fen/Müh alanı için Rol 3 (Domain Expert)

---

## 1. Cümle Uzunluğu Dağılımı

| Tip | Kelime Sayısı | Yüzde | Örnek Bağlam |
|-----|--------------|-------|--------------|
| Kısa-keskin | 5-10 | %20 | Tablo/denklem referansları, sonuç vurgusu |
| Orta | 15-25 | %50 | Yöntem açıklaması, literatür özeti |
| Uzun-karmaşık | 30-50 | %30 | Karşılaştırma, çok atıflı cümleler |

Burstiness hedefi: Standart sapma > 12 kelime

## 2. Paragraf Açılış Stratejileri (A-G Havuzu)

[Task 1 araştırma çıktısından doldur — 7 strateji, her biri için frekans ve örnek]

## 3. Geçiş İfadesi Repertuarı

[Task 1 araştırma çıktısından doldur — kategorilere göre: karşıt, ekleyici, sonuç, referans]

## 4. Fiil Sonu Dağılımı

[Task 1 araştırma çıktısından doldur — fen makalesine özgü dağılım]

## 5. Bölüm Bazlı Ses Şeması

### Özet
### Giriş
### Yöntem
### Bulgular
### Tartışma/Sonuç

[Her bölüm için: dominant fiil sonu, geçiş kalıbı, paragraf stratejisi]

## 6. AI Klişe Listesi (Fen Makalesine Özgü)

[Task 1'den + turkish-academic-voice.md'deki listeden genişlet]

## 7. İnsan Sinyal İşaretleri

[Task 1'den — IEEE makalelerinde sık görülen, AI'nın kaçındığı yapılar]
```

- [ ] **Adım 2: Doğrula**

Dosya şu bölümleri içeriyor mu kontrol et:
```
□ Cümle uzunluğu dağılımı (yüzdeler var mı?)
□ Paragraf açılış stratejileri (A-G arası, 7 strateji)
□ Geçiş ifadeleri (4 kategori)
□ Fiil sonu dağılımı (minimum 6 tip)
□ Bölüm bazlı ses şeması (5 bölüm)
□ AI klişe listesi (minimum 8 madde)
□ İnsan sinyal işaretleri (minimum 5 madde)
```

---

## Task 6: `references/article-voice-sosyal.md` Oluştur

**Bağımlılık:** Task 2 (araştırma sonuçları)
**Çıktı:** `references/article-voice-sosyal.md`

- [ ] **Adım 1: Task 5 ile aynı yapıda oluştur**

Ek zorunlu bölümler:
```markdown
## 8. APA Türkçe Örnekler

- Tek yazar: (Soyadı, 2023)
- İki yazar: (Soyadı ve Soyadı2, 2023)  ← "ve" — "and" değil
- 3+ yazar: (Soyadı vd., 2023)           ← "vd." — "et al." değil
- Sayfalı: (Soyadı, 2023, s. 45)
- Çoklu: (Soyadı, 2023; Soyadı2 vd., 2024)

## 9. Nitel vs Nicel Ses Farkı

[Task 2 araştırma çıktısından doldur]
```

- [ ] **Adım 2: Doğrula**

Task 5 kontrol listesi + APA Türkçe örnekler bölümü var mı?

---

## Task 7: `references/article-voice-saglik.md` Oluştur

**Bağımlılık:** Task 2 (araştırma sonuçları)
**Çıktı:** `references/article-voice-saglik.md`

- [ ] **Adım 1: Task 5 ile aynı yapıda oluştur**

Ek zorunlu bölümler:
```markdown
## 8. Vancouver Atıf Sistemi Örnekleri

Metin içi: Sayı parantezli (1) veya üst simge¹
- Tek: (1) veya ¹
- Çoklu ardışık: (1-3)
- Çoklu seçili: (1,3,5)

Kaynakça formatı:
1. Soyadı AA, Soyadı2 BB. Makale başlığı. Dergi Kısaltması. Yıl;Cilt(Sayı):ss-ss. DOI

## 9. Klinik Dil Profili

[Task 2'den — hasta, prevalans, p<0.05, odds ratio, confidence interval kullanım kalıpları]

## 10. IMRAD Ses Şeması (Sağlık Özgü)

[Introduction/Methods/Results/Discussion — her bölüm için klinik dil normları]
```

- [ ] **Adım 2: Doğrula**

Task 5 kontrol listesi + Vancouver örnekleri + klinik dil profili var mı?

---

## Task 8: `references/article-voice-summary.md` Oluştur

**Bağımlılık:** Task 5, Task 6, Task 7 tamamlanmış olmalı
**Çıktı:** `references/article-voice-summary.md`

- [ ] **Adım 1: Dosyayı oluştur**

```markdown
# Makale Ses Profili — Karma Özet

> 3 alan profilinin hızlı referans özeti.
> Detay için: article-voice-fen.md / article-voice-sosyal.md / article-voice-saglik.md

---

## Alan Tespiti Tablosu

| Sinyal Kelimeler | Alan | Atıf | Profil Dosyası |
|-----------------|------|------|----------------|
| "deney", "simülasyon", "MATLAB", "Hz", "MPa", "mühendislik", "IEEE" | Fen/Müh | IEEE `[1]` | article-voice-fen.md |
| "anket", "nitel", "örneklem", "SPSS", "psikoloji", "eğitim", "sosyal" | Sosyal | APA Türkçe | article-voice-sosyal.md |
| "hasta", "klinik", "prevalans", "p<0.05", "tıp", "hemşirelik" | Sağlık | Vancouver `(1)` | article-voice-saglik.md |
| Belirsiz | — | Sor | — |

## Her Alanın 5 Kritik Ses Kuralı

### Fen/Müh
1. IEEE köşeli parantez atıf: [1], [1-5], [1,3,7]
2. Pasif fiil baskın: hesaplanmıştır, elde edilmiştir
3. Tablo/şekil referansı kısa cümle üretir (burstiness)
4. Her parametre için kaynak: ref. [36]'dan alınmıştır
5. Aralık atıf: [6-29] — 24 kaynağı tek atıfta göster

### Sosyal
1. APA Türkçe: "vd." (et al. değil), "ve" (and değil)
2. Nitel: katılımcı ses, tırnak içi veri
3. Nicel: istatistik + atıf birlikte
4. Tartışma: "bu sonuç X ile örtüşmektedir (Yazar, yıl)"
5. Sınırlılık bölümü zorunlu

### Sağlık
1. Vancouver: (1) veya üst simge, sıralı numaralama
2. IMRAD yapısı katı: sapma yok
3. Hasta sayısı + güven aralığı zorunlu
4. Etik kurul onay numarası belirt
5. Çıkar çatışması beyanı ekle

## Atıf Sistemi Karşılaştırma

| Özellik | IEEE | APA Türkçe | Vancouver |
|---------|------|-----------|-----------|
| Metin içi | [1] | (Yazar, yıl) | (1) |
| Çok yazar | [1,3] | (Yazar vd., yıl) | (1,3) |
| Sıralama | Atıf sırası | Alfabetik | Atıf sırası |
| Sayfa | [1, s.5] | (Yazar, yıl, s.5) | (1 s.5) |
```

- [ ] **Adım 2: Doğrula**

Alan tespiti tablosu + 3 alan kural listesi + atıf karşılaştırma tablosu var mı?

---

## Task 9: `references/ai-detector-mechanics.md` Güncelle

**Bağımlılık:** Task 3 (dedektör araştırması)
**Çıktı:** Genişletilmiş `references/ai-detector-mechanics.md`

- [ ] **Adım 1: Mevcut dosyayı oku**

`references/ai-detector-mechanics.md` dosyasını oku — mevcut içeriği koru.

- [ ] **Adım 2: Makale bölümü ekle**

Dosyanın sonuna ekle:

```markdown
---

## 7. Makale Formatına Özgü Dedektör Davranışları

### iThenticate Makale Modu
- Hakemli dergi gönderimlerinde kullanılan versiyon
- Tez moduna göre farklar:
  - Kaynakça otomatik hariç tutulur (tezde manuel)
  - Yazar kendi önceki yayınları için öz-intihal uyarısı
  - Dergi editörü raporu: eşleşme kaynakları gösterilir
- Eşik: %15 altı — çoğu dergi kabul eder
- Bypass: gerçek parafraz + kaynaklı alıntılar

### Turnitin Makale Editörü
- Teze göre daha katı semantik analiz
- Abstract özellikle taranır — AI sinyali için yüksek hassasiyet
- Referans listesi hariç tutulabilir
- Bypass: bölüm bazlı ses değişkeni, somut veri, atıf yoğunluğu

### Copyleaks Makale Modu
- Akademik makale için özel model
- Teze göre fark: bölüm başlıkları (Abstract, Introduction vb.) ekstra ağırlık taşır
- Bypass: IMRAD başlık altında ses kalibrasyonu, her bölüm farklı ses tonu

### YÖK İntihal — Makale Farkı
- Tez sisteminden bağımsız — makale için ayrı portal
- Türkçe makale: DergiPark arşivi taranır
- İngilizce makale: uluslararası veritabanları
- Bypass: Tezle aynı — gerçek parafraz + atıf

## 8. Makale Dedektör Bypass Özeti

| Dedektör | Makale Özgü Zayıf Nokta | Bypass |
|---------|------------------------|--------|
| iThenticate | Öz-intihal tespiti | Atıflı alıntı — kendi çalışmanı da kaynak göster |
| Turnitin | Abstract AI tespiti yüksek | Abstract'ı en son yaz, en fazla burstiness uygula |
| Copyleaks | Bölüm başlığı ağırlığı | IMRAD altında her bölümde farklı ses tonu |
| YÖK | DergiPark arşivi taraması | Türkçe makalelerde %15 altı benzerlik hedefle |
```

- [ ] **Adım 3: Doğrula**

Dosyada "Makale Formatına Özgü" bölümü var mı?

---

## Task 10: `literature-review/SKILL.md` Oluştur

**Bağımlılık:** Task 1, Task 2, Task 3 tamamlanmış olmalı (araştırma notları hazır)
**Çıktı:** `literature-review/SKILL.md`

- [ ] **Adım 1: Dizini oluştur**

`literature-review/` klasörü yoksa oluştur.

- [ ] **Adım 2: SKILL.md yaz**

```markdown
---
name: literature-review
description: >
  Çok dilli akademik literatür tarama skill'i. 30+ veritabanı (DergiPark, Google Scholar,
  PubMed, Scopus, IEEE Xplore, ResearchGate ve daha fazlası). Gerçek araştırmacı workflow:
  arama stratejisi → paralel tarama → kaynak değerlendirme → araştırmacı notu → boşluk analizi.
  DOI zorunlu. citations-log.md otomatik günceller. academic-shield ve academic-writing-pro
  tarafından ortak modül olarak kullanılır.
triggers:
  - "literatür tara"
  - "kaynak bul"
  - "araştır"
  - "tarama yap"
  - "literature review"
  - "kaynak araştır"
  - "makale bul"
  - "literatür araştır"
---

# Literature Review Skill

> **Referans dosyaları:**
> - `citations-log.md` — her bulunan kaynak buraya eklenir (her çalışmada oku)

---

## TETIKLEYICI KOŞULLAR

Bu skill şu durumlarda devreye girer:
1. **Doğrudan:** Kullanıcı "literatür tara", "kaynak bul", "araştır" yazar
2. **academic-shield içinden:** Kaynak yokken tez yazma talebi geldiğinde
3. **academic-writing-pro içinden:** Kaynak yokken makale yazma talebi geldiğinde

---

## AŞAMA 1: ARAMA STRATEJİSİ

Kullanıcının konusundan otomatik çıkar:

```
1. Ana kavramları belirle
   "yapay sinir ağı nükleer fizik" →
   Ana: [yapay sinir ağı, nükleer fizik, manyetik moment]

2. Sinonimler ekle
   yapay sinir ağı → ANN, neural network, YSA
   nükleer fizik → nuclear structure, çekirdek fiziği

3. Boolean sorgu oluştur
   TR: "yapay sinir ağı" AND "nükleer fizik"
   EN: "artificial neural network" AND "nuclear structure"
   EN-geniş: (ANN OR "neural network") AND ("nuclear moment" OR "nuclear structure")

4. Filtreler
   Yayın yılı: son 10 yıl (override: kullanıcı belirtirse)
   Dil: TR + EN + diğer (hepsi)
   Alan: otomatik tespit veya kullanıcı belirler
```

---

## AŞAMA 2: PARALEL TARAMA

Aşağıdaki veritabanları **paralel agent'larla** taranır:

### Türkçe & Ulusal
- DergiPark — hakemli Türkçe dergiler
- YÖK Tez Merkezi — lisansüstü tezler
- TR Dizin — ulusal atıf indeksi
- ULAKBİM — TÜBİTAK + TÜBA yayınları
- Atatürk Kütüphanesi Digital — tarihsel kaynaklar

### Genel İngilizce
- Google Scholar — en geniş kapsam
- ResearchGate — tam metin + yazar profilleri
- Semantic Scholar — AI destekli alıntı analizi
- OpenAlex — açık bibliyometri
- BASE — 300M+ akademik doküman
- CORE — açık erişim odaklı

### İndeksli Veritabanları
- Web of Science (SCI/SSCI/ESCI)
- Scopus
- IEEE Xplore
- ACM Digital Library
- ScienceDirect (Elsevier)
- SpringerLink
- Wiley Online Library
- Taylor & Francis Online
- Oxford Academic
- Cambridge Core

### Sağlık & Biyomedikal
- PubMed / MEDLINE
- PubMed Central (PMC)
- Cochrane Library
- ClinicalTrials.gov
- medRxiv
- bioRxiv

### Sosyal Bilimler
- SSRN
- JSTOR
- EBSCO (PsycINFO, ERIC)
- APA PsycNET
- ProQuest

### Fen & Mühendislik Özel
- arXiv
- ChemRxiv
- DOAJ

### Diğer Diller
- Kaynak hangi dilde olursa: agent okur, Türkçe özet üretir, dil bilgisini korur, DOI ile kaydeder

---

## AŞAMA 3: KAYNAK DEĞERLENDİRME

Her bulunan kaynak için puan hesapla:

| Kriter | Puan | Açıklama |
|--------|------|---------|
| Son 5 yıl | 30 | 2020-2025 arası |
| 5-10 yıl | 15 | 2015-2020 arası |
| 10+ yıl | 5 | Sadece temel/klasik |
| SCI/SSCI/ESCI | 30 | Uluslararası indeks |
| Scopus | 20 | Uluslararası |
| TR Dizin | 15 | Ulusal indeks |
| DOI mevcut | 10 | Atıf güvenilirliği |
| 50+ atıf | 10 | Alanda tanınan |

**Seçim:** En yüksek puanlı 10-15 kaynak — alan dağılımına dikkat et

---

## AŞAMA 4: ARAŞTIRMACI NOTU

Seçilen her kaynak için şu format zorunlu:

```markdown
### [No] Kaynak Künyesi

- **Yazar(lar):** Soyadı, A. A.
- **Yıl:** YYYY
- **Başlık:** Tam başlık
- **Dergi/Yayınevi:** Ad, Cilt(Sayı), ss. XX-XX
- **DOI:** https://doi.org/10.xxxx   ← ZORUNLU — yoksa [DOI EKSİK] yaz
- **URL:** https://...               ← DOI yoksa
- **Erişim Tarihi:** GG/AA/YYYY     ← URL varsa zorunlu
- **Dil:** TR / EN / Diğer
- **Veritabanı:** Google Scholar / PubMed / Scopus / vb.
- **Atıf IEEE:**  [X] Soyadı A. A., (Yıl). Başlık. Dergi, Cilt(Sayı), ss.
- **Atıf APA:**   Soyadı, A. A. (Yıl). Başlık. *Dergi*, Cilt(Sayı), ss. https://doi.org/...
- **Atıf VAN:**   X. Soyadı AA. Başlık. Dergi Kısa. Yıl;Cilt(Sayı):ss. DOI
- **Kullanılan sayfalar:** s. XX
- **Ana Bulgu:** [2-3 cümle]
- **Metodoloji:** [kısa özet]
- **Sınırlılık:** [varsa]
- **Bu çalışmayla ilgisi:** [bağlantı açıkla]
- **Alıntılanabilir:** "tam cümle" (s. XX)
```

---

## AŞAMA 5: BOŞLUK ANALİZİ + citations-log GÜNCELLEME

### Boşluk Analizi Şablonu

```
LİTERATÜR BOŞLUK ANALİZİ
─────────────────────────
Kapsanan dönem: [yıllar arası]
Toplam bulunan kaynak: N
Seçilen kaynak: 10-15

Güçlü alanlar:
• [İyi kapsanmış konular]

Boşluklar:
• [Eksik metodoloji/yaklaşım]
• [Az çalışılmış alt konu]
• [Türkçe literatür eksikliği varsa belirt]

Öneri:
• [Bu boşluğu doldurmak için önerilen yaklaşım]
```

### citations-log.md Güncelleme

Her kaynak için `citations-log.md` dosyasına Aşama 4 formatında ekle.
DOI eksikse [DOI EKSİK] yaz ve kullanıcıyı uyar.

---

## KRİTİK KISITLAR

1. DOI eksik kaynak → [DOI EKSİK] yaz, kullanıcıyı uyar
2. Gerçek kaynak bulunamazsa → [KAYNAK] placeholder + açık uyarı
3. citations-log.md her kaynak sonrası güncellenmeli — atlanırsa uyar
4. Araştırmacı notunu kısaltma — her bölüm doldurulmalı

---

## EKOSİSTEM ENTEGRASYONU

Bu skill şu şekillerde kullanılır:

**Bağımsız:**
```
literature-review → kullanıcıya kaynak listesi + araştırmacı notları
```

**academic-shield içinden (tez):**
```
Kaynak yok + tez yazma → literature-review → academic-shield (Mod B)
```

**academic-writing-pro içinden (makale):**
```
Kaynak yok + makale yazma → literature-review → academic-writing-pro (Mod B)
```

**Tam pipeline:**
```
literature-review → academic-writing-pro (Mod B) → LaTeX → Overleaf
```

---

*Literature Review Skill v1.0 | 2026-05-07*
*30+ veritabanı, DOI zorunlu, araştırmacı notu formatı*
```

- [ ] **Adım 3: Doğrula**

```
□ Frontmatter var (name, description, triggers)
□ 5 aşama eksiksiz
□ 30+ veritabanı listelenmiş
□ Araştırmacı notu formatı DOI zorunluluğuyla birlikte
□ Boşluk analizi şablonu
□ citations-log.md entegrasyonu
□ Kritik kısıtlar
```

---

## Task 11: `academic-writing-pro/SKILL.md` Oluştur

**Bağımlılık:** Task 5, 6, 7, 8, 9, 10 tamamlanmış olmalı
**Çıktı:** `academic-writing-pro/SKILL.md`

- [ ] **Adım 1: Dizini oluştur**

`academic-writing-pro/` klasörü yoksa oluştur.

- [ ] **Adım 2: SKILL.md yaz**

```markdown
---
name: academic-writing-pro
description: >
  Hakemli dergi makalesi için AI iz temizleme ve üretim skill'i.
  Alan otomatik tespiti: Fen/Müh (IEEE), Sosyal (APA Türkçe), Sağlık (Vancouver).
  GPTZero, Turnitin, Copyleaks, iThenticate, YÖK İntihal bypass — 3 katmanlı güvence.
  LaTeX (Overleaf) ve DOCX çıktısı. Kaynak yoksa literature-review otomatik tetikler.
  Her kaynak kullanımında citations-log.md günceller.
triggers:
  - "makale yaz"
  - "paper"
  - "artikel"
  - "article"
  - "abstract yaz"
  - "özet yaz"
  - "academic-writing-pro"
  - "tam akademik"
  - "latex ver"
  - "overleaf için"
  - "docx ver"
  - "fen bilimleri makalesi"
  - "mühendislik makalesi"
  - "sosyal bilimler makalesi"
  - "sağlık makalesi"
  - "dergi"
  - "journal"
  - "scopus"
  - "ieee xplore"
  - "dergipark"
---

# Academic Writing Pro Skill

> **Referans dosyaları (alan tespitine göre yükle):**
> - `references/article-voice-fen.md` — Fen/Müh alanında
> - `references/article-voice-sosyal.md` — Sosyal alanda
> - `references/article-voice-saglik.md` — Sağlık alanında
> - `references/article-voice-summary.md` — Her durumda (hızlı referans)
> - `citations-log.md` — Her durumda (kaynak takibi)
> - `references/plagiarism-rules.md` — Her durumda
> - `references/ai-detector-mechanics.md` — Her durumda

---

## INTENT PARSER

Kullanıcı girdisinden otomatik çıkar:

### Mod Tespiti
- **Mod A — Dönüşüm:** Mevcut metin varsa ("bunu düzenle", "dedektörden geçir", "insanlaştır")
- **Mod B — Üretim:** Konu/argüman veriliyorsa ("şu konuda yaz", "abstract yaz")
- Belirsizse sor: "Mevcut metni mi dönüştüreceğiz, yoksa konudan sıfırdan mı üretelim?"

### Alan Tespiti
| Sinyal | Alan | Atıf | Profil |
|--------|------|------|--------|
| "deney", "simülasyon", "MATLAB", "Hz", "MPa", "mühendislik" | Fen/Müh | IEEE `[1]` | article-voice-fen.md |
| "anket", "nitel", "örneklem", "SPSS", "psikoloji", "eğitim" | Sosyal | APA Türkçe | article-voice-sosyal.md |
| "hasta", "klinik", "prevalans", "p<0.05", "tıp", "hemşirelik" | Sağlık | Vancouver | article-voice-saglik.md |
| Belirsiz | — | Sor | — |

Manuel override: "APA kullan" / "IEEE kullan" / "Vancouver kullan" → uygula

### Makale Tipi Tespiti
| Sinyal | Tip | Yapı |
|--------|-----|------|
| "özgün bulgu", "deney", "veri" | Araştırma | Özet→Giriş→Yöntem→Bulgular→Tartışma |
| "sentez", "sistematik", "derleme" | Derleme | PRISMA formatı |
| "olgu", "vaka", "case" | Olgu sunumu | Özet→Giriş→Olgu→Tartışma→Sonuç |

### Format Tespiti
- "latex ver", "overleaf" → LaTeX çıktısı
- "docx ver", "word" → DOCX çıktısı
- Belirtilmezse → Markdown

---

## 5-ROL PIPELINE

```
[Kullanıcı Girdisi]
        ↓
ROL 1 — RESEARCH ORCHESTRATOR
  IF kaynak yok + yazma talebi:
    → literature-review/SKILL.md çağır
    → Alan filtresini uygula
    → citations-log.md güncelle
  IF kaynak verildi: bu rolü atla
        ↓
ROL 2 — SOURCE EVALUATOR
  → Kalite skoru hesapla (yıl + indeks + DOI)
  → En uygun 10-15 kaynak seç
  → Öncelik sırası oluştur
        ↓
ROL 3 — DOMAIN EXPERT + WRITER
  → Alan profili yükle (fen/sosyal/saglik)
  → AŞAMA 1: TANI (Mod A için)
  → AŞAMA 2: DERİN DÖNÜŞÜM (4 Katman)
  → Her kaynak kullanımında ROL 4 tetikle
        ↓
ROL 4 — CITATION SPECIALIST (her kaynak)
  → Alan standardı formatla
  → DOI kontrol: yoksa [DOI EKSİK] + uyar
  → citations-log.md güncelle
        ↓
ROL 5 — BYPASS ENGINEER (zorunlu, atlanamaz)
  → verification-before-completion çağır
  → 3 katman bypass kontrolü
  → Dedektör simülasyonu
  → GEÇTİ → çıktı | KALDI → ilgili role dön (max 3)
        ↓
[Çıktı: Markdown / LaTeX / DOCX]
```

---

## AŞAMA 1: TANI (Mod A için)

```
TANI RAPORU
───────────
AI Sinyalleri:
• Cümle uzunluğu: [uniform mu? std. sapma tahmini]
• Tekrar eden fiil sonu: [-mektedir × kaç kez ardışık?]
• Tekrar eden geçiş: [hangileri?]
• AI klişeleri: [listele — alan profilindeki listeden karşılaştır]
• Atıf eksikliği: [kaynak yok veya az]

İntihal Risk Noktaları:
• [%30+ kelime örtüşmesi şüpheli bölgeler]
• [DOI eksik kaynaklar]

Alan Uyumsuzlukları:
• [IEEE/APA/Vancouver karışımı]
• [Yanlış atıf formatı]
```

---

## AŞAMA 2: DERİN DÖNÜŞÜM (4 Katman)

### Katman 1: Yapısal Yeniden Yazım
(academic-shield ile aynı — alan profiline göre kalibrate et)
- Cümle uzunluğu çeşitlendirme: kısa+orta+uzun
- Paragraf stratejisi çeşitlendirme (A-G havuzu)
- Somut veri ekleme
- Paragraflar arası bağlantı

### Katman 2: Makale Ses Kalibrasyonu
- İlgili article-voice-*.md dosyasını oku
- Fiil sonu çeşitliliği (alan normuna göre)
- Geçiş kalıbı çeşitliliği
- Alan bazlı AI klişe temizleme

### Katman 3: Atıf Entegrasyonu
- Alan standardı: IEEE / APA Türkçe / Vancouver
- DOI zorunlu kontrolü
- İntihal önleme: %30 altı örtüşme, yapısal dönüşüm
- Blok alıntı: ≥4 satır → 1cm girinti + 11pt + tırnak yok

### Katman 4: Burstiness Optimizasyonu
- Kısa cümle enjeksiyonu (4-8 kelime)
- Parantez genişletme
- Tablo/şekil referans cümleleri
- Hedef: std. sapma > 12 kelime

---

## AŞAMA 3: DOĞRULAMA (Rol 5)

```
DEDEKTÖR SİMÜLASYONU
□ Burstiness: en kısa < 10 kelime VE en uzun > 30 kelime?
□ Cümle çeşitliliği: 15-22 kelime aralığında sıkışma var mı?
□ Geçiş: aynı kalıp 2+ ardışık?
□ Fiil: her 5 cümlede 3+ farklı son?
□ Alan klişesi: article-voice-*.md listesinde bir madde var mı?
□ DOI: tüm kaynaklar için var mı?

İNTİHAL KONTROL
□ Kısa alıntılar: tırnak + atıf?
□ Blok alıntılar: 1cm girinti + 11pt + tırnak yok + atıf?
□ Parafrazlar: %30 altı örtüşme + yapısal dönüşüm + atıf?

ALAN UYUMU
□ Atıf stili alan ile tutarlı?
□ APA'da "vd." kullanıldı?
□ DOI eksik kaynak var mı?
```

**Başarı = Tüm kutular işaretli.**
**Başarısızlık = İlgili katmana geri dön, yeniden çalıştır (max 3 iterasyon).**

---

## ÇIKTI FORMATLARI

### Markdown (varsayılan)
Doğrudan üret.

### LaTeX (Overleaf)
```latex
\documentclass[12pt]{article}
\usepackage[turkish]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage{setspace}
\onehalfspacing
% Alan standardı:
% Fen/Müh  → \usepackage[style=ieee,backend=biber]{biblatex}
% Sosyal   → \usepackage[style=apa,backend=biber]{biblatex}
% Sağlık   → \usepackage[style=vancouver,backend=biber]{biblatex}

% Dergi spesifik (kullanıcı belirtirse):
% Elsevier   → \documentclass{elsarticle}
% IEEE Trans → \documentclass[journal]{IEEEtran}
% Springer   → \documentclass{svjour3}
```

### DOCX (pandoc)
```bash
pandoc input.md -o output.docx \
  --reference-doc=template.docx \
  --bibliography=references.bib \
  --csl=[ieee.csl|apa.csl|vancouver.csl]
# Times New Roman 12pt, 1.5 satır aralığı
```

---

## DERGİ SEVİYESİ KALİBRASYONU

| Seviye | Ek Gereklilik |
|--------|--------------|
| Ulusal (TR Dizin) | Türkçe abstract yeterli, DergiPark yükleme formatı |
| SCI/SSCI/ESCI | İngilizce abstract zorunlu, IMRAD katı, atıf yoğunluğu yüksek |
| Scopus/Alan indeksi | Alan normlarına göre, orta düzey |

---

## KRİTİK KISITLAR

1. Kaynak yoksa → literature-review otomatik tetikle → bul → yaz. Sadece tarama başarısız olursa [KAYNAK] + uyar
2. DOI yoksa → [DOI EKSİK] yaz, uyar
3. Alan tespiti yapılmadan yazma — IEEE/APA/Vancouver karıştırma
4. APA Türkçe: "vd." (et al. değil), "ve" (and değil)
5. Bypass 3 katman tamamlanmadan "bitti" deme
6. citations-log.md her kaynak sonrası güncellenmeli

---

## EKOSİSTEM ENTEGRASYONU

```
COMBO-AW1: Araştırma → Yazma → Kalite
  literature-review → academic-writing-pro (Mod B) → verification-before-completion

COMBO-AW2: Mevcut Makale Kurtarma
  academic-writing-pro (Mod A) → requesting-code-review

COMBO-AW3: Tam Pipeline
  literature-review → academic-writing-pro (Mod B) → LaTeX → Overleaf

COMBO-AW4: Tez → Makale
  academic-shield (Mod B) → academic-writing-pro (Mod A)
```

---

*Academic Writing Pro Skill v1.0 | 2026-05-07*
*3 alan profili, 5-rol pipeline, LaTeX/DOCX, 30+ veritabanı*
```

- [ ] **Adım 3: Doğrula**

```
□ Frontmatter (name, description, triggers)
□ Intent Parser (mod + alan + tip + format)
□ 5-Rol Pipeline şeması
□ Aşama 1: Tanı şablonu
□ Aşama 2: 4 Katman
□ Aşama 3: Doğrulama checklist
□ LaTeX şablonu (alan bazlı + dergi spesifik)
□ DOCX pandoc komutu
□ Kritik kısıtlar (literature-review tetikleme dahil)
□ Combo zincirleri
```

---

## Task 12: `academic-shield/SKILL.md` Güncelle

**Bağımlılık:** Task 10 (literature-review hazır)
**Çıktı:** Güncellenmiş `academic-shield/SKILL.md`

- [ ] **Adım 1: Mevcut dosyayı oku**

`academic-shield/SKILL.md` dosyasını oku.

- [ ] **Adım 2: MOD TESPİTİ bölümünden önce 5-ROL PIPELINE ekle**

Mevcut "## MOD TESPİTİ" başlığından hemen önce şunu ekle:

```markdown
## 5-ROL PIPELINE

```
[Kullanıcı Girdisi]
        ↓
ROL 1 — RESEARCH ORCHESTRATOR
  IF kaynak yok + yazma talebi:
    → literature-review/SKILL.md çağır
    → SAÜ kabul gören dergi filtresi uygula
    → citations-log.md güncelle
  IF kaynak verildi: bu rolü atla
  IF Mod A: code-explorer ile mevcut tez yapısını analiz et
        ↓
ROL 2 — SOURCE EVALUATOR
  → Kalite skoru hesapla
  → En uygun 10-15 kaynak seç
        ↓
ROL 3 — DOMAIN EXPERT + WRITER
  → turkish-academic-voice.md + sau-format-rules.md yükle
  → 3 AŞAMALI PIPELINE çalıştır
  → Her kaynak kullanımında ROL 4 tetikle
        ↓
ROL 4 — CITATION SPECIALIST (her kaynak)
  → IEEE veya APA Türkçe formatla
  → DOI kontrol: yoksa [DOI EKSİK] + uyar
  → citations-log.md güncelle
        ↓
ROL 5 — BYPASS ENGINEER (zorunlu)
  → verification-before-completion çağır
  → Dedektör simülasyonu
  → GEÇTİ → çıktı | KALDI → ilgili role dön (max 3)
```
```

- [ ] **Adım 3: KRİTİK KISITLAR bölümündeki 1. maddeyi güncelle**

Mevcut:
```
1. **Gerçek kaynak olmadan atıf üretme** — `[KAYNAK]` yaz
```

Yeni:
```
1. **Kaynak yoksa** → literature-review/SKILL.md otomatik tetikle → bul → yaz.
   Sadece tarama başarısız olursa `[KAYNAK]` + uyar.
   DOI eksik kaynak → `[DOI EKSİK]` yaz, uyar.
```

- [ ] **Adım 4: EKOSİSTEM ENTEGRASYONU bölümüne yeni combolar ekle**

"### Combo Zincirleri" bölümünün sonuna ekle:

```markdown
**COMBO-AC5: Literatür → Tez Bölümü**
```
literature-review → academic-shield (MOD B)
```

**COMBO-AC6: Tez → Makale Adaptasyonu**
```
academic-shield (MOD B) → academic-writing-pro (MOD A)
```
```

- [ ] **Adım 5: Agent Entegrasyonu bölümünü güncelle**

Mevcut "### Agent Entegrasyonu" bölümünü değiştir:

```markdown
### Agent Entegrasyonu

**Pipeline içinde (otomatik tetiklenir):**
- **ROL 1 başında, Mod A:** `everything-claude-code:code-explorer` — mevcut tez bölümü yapısını anlamak için
- **ROL 1 başında, kaynak yoksa:** `literature-review/SKILL.md` — kaynak ve literatür toplamak için
- **ROL 5 sonunda (zorunlu):** `superpowers:verification-before-completion` — bypass doğrulama
- **ROL 5 sonunda, kritik bölüm:** `superpowers:requesting-code-review` — kalite kontrolü
```

- [ ] **Adım 6: Doğrula**

```
□ 5-ROL PIPELINE bölümü eklendi
□ Kritik kısıtlar 1. madde güncellendi (literature-review tetikleme)
□ COMBO-AC5 ve COMBO-AC6 eklendi
□ Agent Entegrasyonu bölümü pipeline'a gömüldü
```

---

## Task 13: `skills/academic-shield-rehber.md` Güncelle

**Bağımlılık:** Task 12
**Çıktı:** Güncellenmiş `skills/academic-shield-rehber.md`

- [ ] **Adım 1: Mevcut dosyayı oku**

- [ ] **Adım 2: Hızlı Başlangıç Kartı'nı tetikleyiciler tablosuna dönüştür**

Mevcut kod bloğu yerine tablo ekle:

```markdown
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
```

- [ ] **Adım 3: Kaynaklar bölümünden önce İlgili Skill'ler ekle**

```markdown
## İlgili Skill'ler

- **literature-review** — kaynak tarama modülü
  → "literatür tara" yazınca otomatik devreye girer
  → Kaynak yokken yazma talebi geldiğinde pipeline içinden otomatik tetiklenir
  → [literature-review-rehber.md](literature-review-rehber.md)

- **academic-writing-pro** — dergi makalesi versiyonu
  → Tez bölümü → makale adaptasyonu:
     `academic-shield (Mod B) → academic-writing-pro (Mod A)`
  → [academic-writing-pro-rehber.md](academic-writing-pro-rehber.md)
```

- [ ] **Adım 4: Yeni combo zincirleri ekle**

"COMBO-AC4" den sonra ekle:

```markdown
**COMBO-AC5: Literatür → Tez Bölümü**
```
literature-review (kaynak tarama) → academic-shield (MOD B) → çıktı
```

**COMBO-AC6: Tez → Makale Adaptasyonu**
```
academic-shield (MOD B, tez bölümü yaz)
  → academic-writing-pro (MOD A, makale formatına dönüştür)
```
```

- [ ] **Adım 5: Doğrula**

```
□ Tetikleyiciler tablosu var (14 satır)
□ İlgili Skill'ler bölümü var
□ COMBO-AC5 ve COMBO-AC6 var
```

---

## Task 14: `skills/literature-review-rehber.md` Oluştur

**Bağımlılık:** Task 10
**Çıktı:** `skills/literature-review-rehber.md`

- [ ] **Adım 1: Dosyayı oluştur**

```markdown
# Literature Review — Tam Kapsamlı Rehber

> **Sürüm:** 1.0
> **Son Güncelleme:** 2026-05-07

---

## Tetikleyiciler

| Kullanıcı Yazdığında | Devreye Giriş |
|----------------------|---------------|
| "literatür tara" | Doğrudan |
| "kaynak bul" | Doğrudan |
| "araştır" + konu | Doğrudan |
| "tarama yap" | Doğrudan |
| "literature review" | Doğrudan |
| Kaynak yok + academic-shield yazma talebi | Pipeline içinden otomatik |
| Kaynak yok + academic-writing-pro yazma talebi | Pipeline içinden otomatik |

---

## 5 Aşama Özeti

| Aşama | Görev | Çıktı |
|-------|-------|-------|
| 1 | Arama stratejisi | Boolean sorgular (TR + EN + Diğer) |
| 2 | Paralel tarama | 30+ veritabanında sonuçlar |
| 3 | Kaynak değerlendirme | Puanlama → 10-15 seçili kaynak |
| 4 | Araştırmacı notu | Her kaynak için DOI'li tam kayıt |
| 5 | Boşluk analizi + log | citations-log.md güncelleme |

---

## Veritabanı Listesi (30+)

**Türkçe & Ulusal:** DergiPark, YÖK Tez Merkezi, TR Dizin, ULAKBİM

**Genel:** Google Scholar, ResearchGate, Semantic Scholar, OpenAlex, BASE, CORE

**İndeksli:** WoS, Scopus, IEEE Xplore, ACM, ScienceDirect, SpringerLink, Wiley, Taylor&Francis, Oxford Academic, Cambridge Core

**Sağlık:** PubMed/MEDLINE, PMC, Cochrane, ClinicalTrials.gov, medRxiv, bioRxiv

**Sosyal:** SSRN, JSTOR, EBSCO, APA PsycNET, ProQuest

**Fen:** arXiv, ChemRxiv, DOAJ

---

## DOI Zorunluluğu

Her kayıtta DOI **şarttır.**

- DOI mevcut: `https://doi.org/10.xxxx`
- DOI yoksa: `[DOI EKSİK]` yaz ve kullanıcıyı uyar
- URL kullanılıyorsa: Erişim Tarihi zorunlu (GG/AA/YYYY)

---

## citations-log.md Entegrasyonu

Her bulunan ve seçilen kaynak `citations-log.md` dosyasına eklenir.
Format: IEEE + APA Türkçe + Vancouver — üçü birden yazılır.

---

## Combo Zincirleri

```
COMBO-LR1: Bağımsız Tarama
  literature-review → kullanıcıya kaynak listesi

COMBO-LR2: Tez Yazımı
  literature-review → academic-shield (Mod B)

COMBO-LR3: Makale Yazımı
  literature-review → academic-writing-pro (Mod B)

COMBO-LR4: Tam Pipeline
  literature-review → academic-writing-pro (Mod B) → LaTeX → Overleaf
```

---

## Örnek Kullanım Promptları

**1. Bağımsız literatür taraması:**
```
literatür tara: yapay sinir ağları ve nükleer fizik
Son 10 yıl, IEEE indeksli öncelikli
```

**2. Tez bölümü için kaynak:**
```
literatür tara: derin öğrenme görüntü sınıflandırma
Alan: Fen Bilimleri, IEEE atıf
En az 15 kaynak
```

**3. Makale için kaynak:**
```
literatür tara: COVID-19 psikolojik etkileri üniversite öğrencileri
Alan: Sağlık, Vancouver
SCI/SSCI öncelikli
```

**4. Çok dilli tarama:**
```
literatür tara: kuantum hesaplama kriptografi
Türkçe + İngilizce + Almanca
DOI zorunlu
```

**5. Sistematik derleme için:**
```
literatür tara: okul öncesi eğitim teknoloji entegrasyonu
Sistematik derleme için PRISMA uyumlu
APA Türkçe, TR Dizin + Scopus öncelikli
```

---

## Referans Dosyaları

- [literature-review/SKILL.md](../literature-review/SKILL.md)
- [citations-log.md](../citations-log.md)
- [INDEX.md](INDEX.md)

---

*Üretilme: 2026-05-07 | Literature Review Skill v1.0*
```

- [ ] **Adım 2: Doğrula**

```
□ Tetikleyiciler tablosu
□ 5 aşama özeti tablosu
□ 30+ veritabanı listesi
□ DOI zorunluluğu bölümü
□ citations-log entegrasyonu
□ 4 combo zinciri
□ 5 örnek prompt
```

---

## Task 15: `skills/academic-writing-pro-rehber.md` Oluştur

**Bağımlılık:** Task 11
**Çıktı:** `skills/academic-writing-pro-rehber.md`

- [ ] **Adım 1: Dosyayı oluştur**

`skills/academic-shield-rehber.md` formatında, şu zorunlu bölümlerle:

```markdown
# Academic Writing Pro — Tam Kapsamlı Rehber

> **Sürüm:** 1.0 | **Son Güncelleme:** 2026-05-07

---

## Tetikleyiciler

| Kullanıcı Yazdığında | Mod |
|----------------------|-----|
| "makale yaz", "paper", "article" | Mod B |
| "abstract yaz", "özet yaz" | Mod B |
| "latex ver", "overleaf için" | Mod B + LaTeX çıktı |
| "docx ver" | Mod B + DOCX çıktı |
| "dedektörden geçir" + makale | Mod A |
| "bunu düzenle" + makale bağlamı | Mod A |
| "dergi", "scopus", "ieee xplore" | Mod tespiti |
| "fen bilimleri makalesi" | Mod B + Fen/Müh |
| "sağlık makalesi" | Mod B + Sağlık |
| "sosyal bilimler makalesi" | Mod B + Sosyal |

---

## Alan Tespiti

[Bölüm 6'daki tablo]

## 5-Rol Pipeline Özeti

[Kısa şema]

## Makale Tipi Tespiti

[Bölüm 6'daki tablo]

## Dergi Seviyesi Kalibrasyonu

[Bölüm 6'daki tablo]

## Çıktı Formatları

[Markdown / LaTeX / DOCX]

## academic-shield ile Fark ve Zincir

| | academic-shield | academic-writing-pro |
|--|-----------------|---------------------|
| Hedef | Tez bölümü | Hakemli dergi makalesi |
| Alan profili | turkish-academic-voice.md | article-voice-fen/sosyal/saglik.md |
| Atıf | IEEE / APA Türkçe | IEEE / APA Türkçe / Vancouver |
| Format | Markdown | Markdown / LaTeX / DOCX |
| Üniversite | SAÜ uyumlu | Üniversiteden bağımsız |

Zincir: `academic-shield (Mod B) → academic-writing-pro (Mod A)`

## Combo Zincirleri

[4 combo]

## Örnek Kullanım Promptları (5+)

1. Fen Bilimleri araştırma makalesi giriş
2. Sosyal bilimler sistematik derleme abstract
3. Sağlık olgu sunumu
4. Mevcut makale dedektörden geçirme
5. LaTeX formatında tam makale

## Referans Dosyaları

[Bağlantılar]
```

- [ ] **Adım 2: Doğrula**

```
□ Tetikleyiciler tablosu (10+ satır)
□ Alan tespiti
□ Pipeline özeti
□ academic-shield karşılaştırma tablosu
□ 4 combo zinciri
□ 5+ örnek prompt
```

---

## Task 16: `skills/INDEX.md` Güncelle

**Bağımlılık:** Task 14, Task 15
**Çıktı:** Güncellenmiş `skills/INDEX.md`

- [ ] **Adım 1: Mevcut dosyayı oku**

- [ ] **Adım 2: Tablo son satırından sonra 2 satır ekle**

Mevcut satır 6'dan sonra:
```markdown
| 7 | [literature-review-rehber.md](literature-review-rehber.md) | literature-review (custom) | ✅ Kurulu | Çok dilli tarama, 30+ veritabanı, DOI zorunlu, 5 aşama |
| 8 | [academic-writing-pro-rehber.md](academic-writing-pro-rehber.md) | academic-writing-pro (custom) | ✅ Kurulu | 3 alan profili, LaTeX/DOCX, 5-rol pipeline, bypass |
```

- [ ] **Adım 3: Hızlı Notlar bölümüne ekle**

```markdown
- **literature-review** — `literature-review/SKILL.md` ile yüklenir; academic-shield ve academic-writing-pro ortak modülü
- **academic-writing-pro** — `academic-writing-pro/SKILL.md` ile yüklenir; 3 alan (Fen/Sosyal/Sağlık), LaTeX/DOCX çıktısı
```

- [ ] **Adım 4: Doğrula**

INDEX.md 8 satırlı tablo içeriyor mu?

---

## Task 17: `CLAUDE.md` Güncelle

**Bağımlılık:** Task 10, Task 11
**Çıktı:** Güncellenmiş `CLAUDE.md`

- [ ] **Adım 1: Mevcut dosyayı oku**

- [ ] **Adım 2: Otomatik tetikleme tablosuna ekle**

`academic-shield` satırından sonra:
```markdown
| `literature-review` | custom (`literature-review/SKILL.md`) | "literatür tara", "kaynak bul", "araştır", "tarama yap", "literature review" |
| `academic-writing-pro` | custom (`academic-writing-pro/SKILL.md`) | "makale yaz", "paper", "artikel", "article", "abstract yaz", "özet yaz", "latex ver", "overleaf için", "docx ver", "dergi", "journal", "scopus", "ieee xplore", "dergipark" |
```

- [ ] **Adım 3: academic-shield yükleme notuna ekle**

`academic-shield` yükleme notunun altına:
```markdown
**`literature-review` yüklenirken şu dosyayı da oku:**
- `citations-log.md` (her durumda)

**`academic-writing-pro` yüklenirken şu dosyaları da oku:**
- `references/article-voice-fen.md` (Fen/Müh alanında)
- `references/article-voice-sosyal.md` (Sosyal alanında)
- `references/article-voice-saglik.md` (Sağlık alanında)
- `references/article-voice-summary.md` (her durumda)
- `citations-log.md` (her durumda)
- `references/plagiarism-rules.md` (her durumda)
- `references/ai-detector-mechanics.md` (her durumda)
```

- [ ] **Adım 4: Doğrula**

```
□ literature-review tetikleyici satırı var
□ academic-writing-pro tetikleyici satırı var
□ literature-review yükleme notu var
□ academic-writing-pro yükleme notu var
```

---

## Task 18: Tam Doğrulama

**Bağımlılık:** Tüm önceki tasklar
**Çıktı:** Doğrulama raporu

- [ ] **Adım 1: Dosya varlığı kontrol**

```powershell
# Her dosya için kontrol:
Test-Path "literature-review/SKILL.md"
Test-Path "academic-writing-pro/SKILL.md"
Test-Path "references/article-voice-fen.md"
Test-Path "references/article-voice-sosyal.md"
Test-Path "references/article-voice-saglik.md"
Test-Path "references/article-voice-summary.md"
Test-Path "citations-log.md"
Test-Path "skills/literature-review-rehber.md"
Test-Path "skills/academic-writing-pro-rehber.md"
```

- [ ] **Adım 2: İçerik doğrulama**

```powershell
# Her dosya boyutu > 0 mu?
(Get-Item "literature-review/SKILL.md").Length -gt 0
(Get-Item "academic-writing-pro/SKILL.md").Length -gt 0
```

- [ ] **Adım 3: Spesifik içerik kontrolleri**

```
□ literature-review/SKILL.md → "30+" veya "veritabanı" kelimesi var mı?
□ academic-writing-pro/SKILL.md → "5-ROL PIPELINE" bölümü var mı?
□ references/article-voice-fen.md → "Cümle Uzunluğu" bölümü var mı?
□ citations-log.md → "DOI" kelimesi var mı?
□ academic-shield/SKILL.md → "5-ROL PIPELINE" bölümü var mı?
□ CLAUDE.md → "literature-review" satırı var mı?
□ skills/INDEX.md → "7 |" satırı var mı?
□ skills/academic-shield-rehber.md → "İlgili Skill'ler" bölümü var mı?
```

- [ ] **Adım 4: verification-before-completion çağır**

```python
Agent({
  subagent_type: "superpowers:verification-before-completion",
  prompt: """
    İddia: academic-writing-pro sistemi tamamlandı.
    Kontrol et:
    - literature-review/SKILL.md mevcut ve 5 aşama eksiksiz
    - academic-writing-pro/SKILL.md mevcut ve 5-rol pipeline var
    - 3 alan profil dosyası mevcut (fen/sosyal/saglik)
    - citations-log.md DOI zorunluluğuyla mevcut
    - academic-shield/SKILL.md 5-rol pipeline ile güncellendi
    - CLAUDE.md yeni tetikleyiciler eklendi
    - INDEX.md 8 satırlı tablo
    - 3 rehber dosyası mevcut (literature-review + academic-writing-pro + shield güncelleme)
    Hepsi geçmeden tamamlandı deme.
  """
})
```

---

## Task 19: Code Review

**Bağımlılık:** Task 18 (doğrulama geçti)
**Çıktı:** Review raporu

- [ ] **Adım 1: Code review çağır**

```python
Agent({
  subagent_type: "superpowers:code-reviewer",
  prompt: """
    Implementation review: academic-writing-pro sistemi

    Kontrol et:
    1. literature-review/SKILL.md
       - 30+ veritabanı listelenmiş mi?
       - DOI zorunluluğu her yerde tutarlı mı?
       - citations-log.md güncelleme talimatı var mı?
       - Araştırmacı notu formatı eksiksiz mi?

    2. academic-writing-pro/SKILL.md
       - Alan otomatik tespiti tutarlı mı?
       - 5-rol pipeline eksiksiz mi?
       - Kaynak yoksa literature-review tetikleme var mı?
       - LaTeX Overleaf uyumlu mu? (babel turkish, biblatex)
       - DOCX pandoc komutu doğru mu?
       - Bypass 3 katman (kural + test + doğrulama) var mı?

    3. academic-shield/SKILL.md güncelleme
       - 5-rol pipeline eklendi mi?
       - Agent entegrasyonu pipeline'a gömüldü mü?
       - Kaynak yoksa kuralı güncellendi mi?

    4. Tetikleyici tutarlılığı
       - CLAUDE.md, rehber dosyaları ve SKILL.md tetikleyicileri eşleşiyor mu?

    Critical / Important / Suggestion formatında raporla.
  """
})
```

---

## Self-Review

**Spec coverage:**

| Spec Gereksinimi | Karşılayan Task |
|-----------------|----------------|
| literature-review bağımsız skill | Task 10 |
| 30+ veritabanı çok dilli tarama | Task 10 |
| DOI zorunluluğu | Task 4, 10, 11 |
| academic-writing-pro 3 alan | Task 11 |
| IEEE/APA/Vancouver otomatik | Task 11 |
| LaTeX Overleaf uyumlu | Task 11 |
| DOCX pandoc | Task 11 |
| 5-rol pipeline her iki skill | Task 11, 12 |
| academic-shield güncelleme | Task 12 |
| citations-log.md | Task 4 |
| 3 alan profil dosyası | Task 5, 6, 7 |
| article-voice-summary.md | Task 8 |
| ai-detector-mechanics genişletme | Task 9 |
| Rehber dosyaları (3 adet) | Task 13, 14, 15 |
| INDEX.md güncelleme | Task 16 |
| CLAUDE.md güncelleme | Task 17 |
| Doğrulama | Task 18 |
| Code review | Task 19 |

**Placeholder taraması:** Temiz — her task tam içerik içeriyor.

**Tip tutarlılığı:** `literature-review/SKILL.md`, `academic-writing-pro/SKILL.md` — tüm dosya yolları tutarlı.

---

*Implementation Plan v1.0 | 2026-05-07*
*19 task, modüler sıra, bağımlılık zincirine göre*
