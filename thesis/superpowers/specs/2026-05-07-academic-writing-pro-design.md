# Academic Writing Pro — Tasarım Belgesi

**Tarih:** 2026-05-07
**Durum:** Kullanıcı Onayı Bekleniyor
**Hedef:** Üniversiteden bağımsız, hakemli dergi makalesi + tez yazımı için tam akademik yazı ekosistemi

---

## 1. Problem Tanımı

### Mevcut Durum
- `academic-shield` SAÜ tezine özgül — üniversite bağımsız değil
- Agent entegrasyonu pipeline dışında, genel not olarak tanımlı
- Kaynak yoksa `[KAYNAK]` placeholder kullanılıyor — araştırma yapılmıyor
- Literatür taraması ayrı bir modül olarak yok
- Makale formatı (LaTeX, DOCX, Vancouver) desteklenmiyor
- 3 alan profili (Fen/Sosyal/Sağlık) yok

### Hedef Durum
- `literature-review` bağımsız skill — çok dilli, DOI zorunlu, 30+ veritabanı
- `academic-writing-pro` — 3 alan, 3 atıf sistemi, LaTeX/DOCX çıktısı
- `academic-shield` güncellendi — 5-rol pipeline, literature-review entegrasyonu
- Her iki skill'de agent'lar pipeline adımlarına gömülü
- Kaynak yoksa önce araştır, bulamazsan uyar

---

## 2. Mimari Kararlar

| Karar | Seçilen | Gerekçe |
|-------|---------|---------|
| Alan kapsamı | Fen + Sosyal + Sağlık (D) | Tüm alanlar, otomatik tespit |
| Dergi seviyesi | Ulusal + SCI/SSCI/ESCI + Alan indeksi | Kalibrasyon seviyeye göre ayarlanır |
| Makale tipi | Araştırma + Derleme + Olgu sunumu | Otomatik tespit |
| academic-shield ilişkisi | Skill zinciri (C) | Separation of concerns, tek kaynak of truth |
| LaTeX şablonu | Genel + dergi spesifik (C) | Varsayılan genel, override mümkün |
| Ses profili | Ayrı dosyalar + karma özet (C) | Bağımsız güncelleme + hızlı referans |
| Genel mimari | Modüler katman (B) | Her parça bağımsız güncellenebilir |
| Literatür taraması | Bağımsız skill (B) | Her iki skill çağırır, tek kaynak of truth |

---

## 3. Dosya Yapısı

```
skillv1/
│
├── literature-review/
│   └── SKILL.md                          ← YENİ
│
├── academic-shield/
│   ├── SKILL.md                          ← GÜNCELLENİR (5-rol pipeline)
│   └── KULLANIM-REHBERI.md              ← GÜNCELLENİR
│
├── academic-writing-pro/
│   └── SKILL.md                          ← YENİ
│
├── references/
│   ├── ai-detector-mechanics.md          ← GENİŞLETİLİR (makale dedektörleri)
│   ├── plagiarism-rules.md               ← değişmez
│   ├── turkish-academic-voice.md         ← değişmez
│   ├── sau-format-rules.md               ← değişmez
│   ├── article-voice-fen.md              ← YENİ
│   ├── article-voice-sosyal.md           ← YENİ
│   ├── article-voice-saglik.md           ← YENİ
│   └── article-voice-summary.md         ← YENİ (karma özet)
│
├── citations-log.md                      ← YENİ (proje kökünde)
│
├── CLAUDE.md                             ← GÜNCELLENİR
│
└── skills/
    ├── INDEX.md                          ← GÜNCELLENİR
    ├── academic-shield-rehber.md         ← GÜNCELLENİR
    ├── literature-review-rehber.md       ← YENİ
    └── academic-writing-pro-rehber.md   ← YENİ
```

---

## 4. `literature-review/SKILL.md` Tasarımı

### Tetikleyiciler
- "literatür tara", "kaynak bul", "araştır", "tarama yap"
- academic-shield veya academic-writing-pro içinden agent çağrısı
- Bağımsız kullanım: "şu konuda literatür taraması yap"

### 5 Aşamalı Araştırmacı Workflow

**Aşama 1 — Arama Stratejisi**
- Konu → ana kavramlar → sinonimler → boolean operatörler
- Türkçe ve İngilizce karşılıklar paralel hazırlanır
- Yayın yılı filtresi: varsayılan son 10 yıl (override mümkün)
- Alan filtresi: Fen→IEEE+arXiv / Sosyal→SSRN+JSTOR / Sağlık→PubMed+Cochrane

**Aşama 2 — Paralel Tarama**

Türkçe & Ulusal:
- DergiPark, YÖK Tez Merkezi, TR Dizin, ULAKBİM, Atatürk Kütüphanesi Digital

Genel İngilizce:
- Google Scholar, ResearchGate, Semantic Scholar, OpenAlex, BASE, CORE

İndeksli Veritabanları:
- Web of Science, Scopus, IEEE Xplore, ACM Digital Library
- ScienceDirect, SpringerLink, Wiley Online, Taylor & Francis
- Oxford Academic, Cambridge Core

Sağlık & Biyomedikal:
- PubMed/MEDLINE, PubMed Central, Cochrane Library
- ClinicalTrials.gov, medRxiv, bioRxiv

Sosyal Bilimler:
- SSRN, JSTOR, EBSCO (PsycINFO, ERIC), APA PsycNET, ProQuest

Fen & Mühendislik Özel:
- arXiv, ChemRxiv, DOAJ

Diğer Diller:
- Kaynak hangi dilde olursa — agent okur, Türkçe özet üretir, dil bilgisini korur, DOI ile kaydeder

**Aşama 3 — Kaynak Değerlendirme**
- Etki faktörü / atıf sayısı
- Metodoloji uyumu
- Yayın yılı: son 5 yıl (yüksek), 5-10 yıl (orta), 10+ (sadece temel)
- Alan standardı: SCI/SSCI/ESCI/Scopus/TR Dizin
- Final skor → en uygun 10-15 kaynak seçilir

**Aşama 4 — Araştırmacı Notu Formatı (Her kaynak)**

```markdown
## [No] Kaynak Künyesi
- Yazar(lar): Soyadı, A. A.
- Yıl: YYYY
- Başlık: Tam başlık
- Dergi: Ad, Cilt(Sayı), ss. XX-XX
- DOI: https://doi.org/10.xxxx   ← ZORUNLU
- URL: https://...               ← DOI yoksa
- Erişim Tarihi: GG/AA/YYYY     ← URL varsa zorunlu
- Dil: TR / EN / Diğer
- Veritabanı: nereden bulundu
- Atıf IEEE: [X] Soyadı A., (Yıl). ...
- Atıf APA: Soyadı, A. A. (Yıl). ...
- Atıf Vancouver: X. Soyadı A, ...
- Ana Bulgu: [2-3 cümle]
- Metodoloji: [kısa özet]
- Sınırlılık: [varsa]
- Bu çalışmayla ilgisi: [bağlantı]
- Alıntılanabilir: "..." (s. XX)
```

**Aşama 5 — Boşluk Analizi + citations-log Güncelleme**
- "X konusu Y-Z yılları arası incelendi, ama Ş eksik"
- "Türkçe literatür yetersiz: sadece N çalışma"
- "Metodolojik boşluk: Q yaklaşımı hiç denenmemiş"
- Her kaynak → citations-log.md otomatik güncelleme (alan standardına göre formatlanmış)

---

## 5. 5-Rol Pipeline (Her İki Skill)

```
[KULLANICI GİRDİSİ]
        ↓
INTENT PARSER
  ├── Mod A (dönüşüm) / Mod B (üretim)?
  ├── Alan: Fen / Sosyal / Sağlık / Belirsiz?
  ├── Makale tipi / Tez bölümü?
  ├── Kaynak var mı?
  └── Format: Markdown / LaTeX / DOCX?
        ↓
ROL 1 — RESEARCH ORCHESTRATOR
  Tetikleyici: Kaynak yok + yazma talebi
  ├── literature-review/SKILL.md çağır (paralel agent'lar)
  ├── Alan filtresini uygula
  └── citations-log.md güncelle
  Atla: Kullanıcı kaynak verdiyse
        ↓
ROL 2 — SOURCE EVALUATOR
  ├── Kalite skoru hesapla
  ├── En uygun 10-15 kaynak seç
  └── Öncelik sırası oluştur
        ↓
ROL 3 — DOMAIN EXPERT + WRITER
  ├── Alan profili yükle
  ├── AŞAMA 1: TANI (Mod A için)
  ├── AŞAMA 2: DERİN DÖNÜŞÜM (4 Katman)
  └── Her kaynak kullanımında → ROL 4 tetiklenir
        ↓
ROL 4 — CITATION SPECIALIST (her kaynak kullanımında)
  ├── Alan standardı formatla (IEEE / APA Türkçe / Vancouver)
  ├── DOI zorunlu kontrolü
  └── citations-log.md güncelle
        ↓
ROL 5 — BYPASS ENGINEER + QUALITY GATE (zorunlu, atlanamaz)
  ├── verification-before-completion çağır
  ├── 3 Katman bypass kontrolü:
  │   Katman 1: Kural belgesi ✓
  │   Katman 2: Test protokolü ✓
  │   Katman 3: Doğrulama adımı ✓
  ├── Dedektör simülasyonu:
  │   GPTZero / Turnitin / Copyleaks / iThenticate / YÖK İntihal / QuillBot
  ├── GEÇTİ → çıktı üret
  └── KALDI → ilgili role geri dön (max 3 iterasyon)
        ↓
[ÇIKTI: Markdown / LaTeX / DOCX]
```

---

## 6. `academic-writing-pro/SKILL.md` Tasarımı

### Alan Otomatik Tespiti

| Sinyal Kelimeler | Alan | Atıf | Profil Dosyası |
|-----------------|------|------|----------------|
| "deney", "simülasyon", "MATLAB", "Hz", "MPa", "mühendislik", "IEEE" | Fen/Müh | IEEE `[1]` | article-voice-fen.md |
| "anket", "nitel", "örneklem", "SPSS", "psikoloji", "eğitim", "sosyal" | Sosyal | APA Türkçe | article-voice-sosyal.md |
| "hasta", "klinik", "prevalans", "p<0.05", "tıp", "hemşirelik" | Sağlık | Vancouver `(1)` | article-voice-saglik.md |
| Belirsiz | — | Sor | — |

Manuel override: "APA kullan" / "IEEE kullan" / "Vancouver kullan" → uygula

### Makale Tipi Tespiti

| Sinyal | Tip | Bölüm Yapısı |
|--------|-----|--------------|
| "özgün bulgu", "deney", "veri topladım" | Araştırma makalesi | Özet→Giriş→Yöntem→Bulgular→Tartışma |
| "literatür tara", "sentez", "sistematik" | Derleme | PRISMA formatı |
| "olgu", "hasta vakası", "case" | Olgu sunumu | Özet→Giriş→Olgu→Tartışma→Sonuç |
| Belirsiz | — | Sor | |

### LaTeX Çıktısı

```latex
% Varsayılan (genel):
\documentclass[12pt]{article}
\usepackage[turkish]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
% Fen/Müh  → \usepackage[style=ieee]{biblatex}
% Sosyal   → \usepackage[style=apa]{biblatex}
% Sağlık   → \usepackage[style=vancouver]{biblatex}

% Kullanıcı dergi belirtirse:
% Elsevier    → \documentclass{elsarticle}
% IEEE Trans  → \documentclass[journal]{IEEEtran}
% Springer    → \documentclass{svjour3}
```

### DOCX Çıktısı
```bash
pandoc input.md -o output.docx \
  --reference-doc=template.docx \
  --bibliography=references.bib \
  --csl=[ieee|apa|vancouver].csl
```

### Dergi Seviyesi Kalibrasyonu

| Seviye | Fark |
|--------|------|
| Ulusal (TR Dizin) | Türkçe ağırlıklı, DergiPark formatı |
| SCI/SSCI/ESCI | İngilizce abstract zorunlu, IMRAD katı, atıf yoğunluğu yüksek |
| Scopus/Alan indeksi | Orta — alan normlarına göre |

### Kritik Kısıtlar

1. Kaynak yoksa → literature-review otomatik tetikle → bul → yaz. Sadece tarama da başarısız olursa `[KAYNAK]` + uyar
2. DOI yoksa → `[DOI EKSİK]` yaz, uyar
3. Alan tespiti yapılmadan yazma — IEEE/APA/Vancouver karıştırma
4. APA Türkçe: "vd." (et al. değil), "ve" (and değil)
5. Bypass 3 katman tamamlanmadan "bitti" deme
6. citations-log.md her kaynak sonrası güncellenmeli

---

## 7. `academic-shield` Güncellemeleri

### Ekleme 1 — 5-Rol Pipeline
```
[BAŞLANGIÇ]
  IF Mod A → code-explorer (mevcut tez yapısını analiz et)
  IF kaynak yok → literature-review/SKILL.md çağır
  AŞAMA 1 → AŞAMA 2 → AŞAMA 3
  verification-before-completion (zorunlu)
  IF kritik bölüm → requesting-code-review
```

### Ekleme 2 — Kaynak Kuralı Güncelleme
```
Mevcut: [KAYNAK] placeholder direkt
Yeni:
  IF kaynak yok:
    1. literature-review otomatik tetikle
    2. Bulunan kaynaklarla yaz
    3. Bulunamazsa → [KAYNAK] + uyar
```

### Ekleme 3 — Tetikleyiciler Tablosu (academic-shield-rehber.md)

| Kullanıcı Yazdığında | Tetiklenen | Mod |
|----------------------|------------|-----|
| "academic-shield" | academic-shield | Soru sor |
| "akademik yaz" | academic-shield | Mod B |
| "tez yaz" | academic-shield | Mod B |
| "bölüm yaz" | academic-shield | Mod B |
| "giriş yaz" | academic-shield | Mod B |
| "metodoloji yaz" | academic-shield | Mod B |
| "literature review yaz" | academic-shield | Mod B |
| "dedektörden geç" | academic-shield | Mod A |
| "ai izi temizle" | academic-shield | Mod A |
| "humanize akademik" | academic-shield | Mod A |
| "şu metni düzenle" + akademik | academic-shield | Mod A |
| "literatür tara" | literature-review | Bağımsız |
| "kaynak bul" + tez bağlamı | literature-review | Bağımsız |
| "makale yaz" / "paper" | academic-writing-pro | Yönlendirme |

### Ekleme 4 — İlgili Skill'ler Bölümü
```markdown
## İlgili Skill'ler
- **literature-review** — kaynak tarama modülü
  → "literatür tara" yazınca otomatik devreye girer
  → Kaynak yoksa pipeline içinden otomatik tetiklenir
- **academic-writing-pro** — dergi makalesi versiyonu
  → Tez bölümü → makale adaptasyonu:
     academic-shield (Mod B) → academic-writing-pro (Mod A)
```

### Ekleme 5 — Yeni Combo Zincirleri
```
COMBO-AC5: Literatür → Tez Bölümü
  literature-review → academic-shield (Mod B)

COMBO-AC6: Tez → Makale Adaptasyonu
  academic-shield (Mod B) → academic-writing-pro (Mod A)
```

---

## 8. Destekleyici Dosyalar

### `references/article-voice-fen.md`
- Cümle uzunluğu dağılımı: Kısa %20 / Orta %50 / Uzun %30
- Paragraf açılış stratejileri (A-G havuzu + frekanslar)
- Geçiş ifadesi repertuarı
- Fiil sonu dağılımı (Fen makalesine özgü)
- Bölüm bazlı ses şeması: Özet/Giriş/Yöntem/Bulgular/Tartışma
- AI klişe listesi (Fen makalesine özgü)
- İnsan sinyal işaretleri (IEEE makalelerinden)

### `references/article-voice-sosyal.md`
- Aynı yapı + APA Türkçe atıf örnekleri, nitel/nicel ses farkı

### `references/article-voice-saglik.md`
- Aynı yapı + Vancouver tam örnekleri, klinik dil profili

### `references/article-voice-summary.md`
- 3 profilin karma özeti, alan tespiti tablosu, hızlı referans

### `citations-log.md`
```markdown
# Citations Log
> Her kaynak kullanımında güncellenir.
> literature-review, academic-shield, academic-writing-pro okur/yazar.

## Kayıt Formatı
## [No] — [Alan Standardı]
- Yazar(lar): ...
- Yıl: ...
- Başlık: ...
- Dergi/Yayınevi: ...
- DOI: https://doi.org/10.xxxx  ← ZORUNLU
- URL: ... (DOI yoksa)
- Erişim Tarihi: GG/AA/YYYY (URL varsa)
- Dil: TR/EN/Diğer
- Veritabanı: ...
- Atıf IEEE: ...
- Atıf APA: ...
- Atıf Vancouver: ...
- Kullanılan sayfalar: ...
- Metin içi kullanım yeri: ...
```

---

## 9. INDEX.md Güncel Hali

| # | Dosya | Plugin | Durum | Kapsam |
|---|-------|--------|-------|--------|
| 1 | everything-claude-code-rehber.md | ECC 2.0.0-rc.1 | ✅ Kurulu | 182 skill, 48 agent |
| 2 | superpowers-rehber.md | superpowers 5.0.7 | ✅ Kurulu | 14 skill |
| 3 | ui-ux-pro-max-rehber.md | ui-ux-pro-max 2.5.0 | ✅ Kurulu | 7 skill |
| 4 | humanizer-rehber.md | humanizer 2.5.1 | ✅ Kurulu | 1 skill |
| 5 | anthropics-skills-rehber.md | anthropics | ❌ Yok | referans |
| 6 | academic-shield-rehber.md | custom | ✅ Kurulu | Tez, AI bypass — GÜNCELLENDİ |
| 7 | literature-review-rehber.md | custom | ✅ Kurulu | Çok dilli tarama, DOI, 5 aşama |
| 8 | academic-writing-pro-rehber.md | custom | ✅ Kurulu | 3 alan, LaTeX/DOCX, bypass |

---

## 10. CLAUDE.md Güncellemeleri

### Otomatik Tetikleme Tablosuna Eklenecekler
```
| `literature-review`    | custom | "literatür tara", "kaynak bul", "araştır", "tarama yap" |
| `academic-writing-pro` | custom | "makale yaz", "paper", "artikel", "article", "latex ver",
|                         |        | "overleaf için", "docx ver", "dergi", "journal", "scopus",
|                         |        | "ieee xplore", "dergipark", "abstract yaz", "özet yaz" |
```

### Yükleme Notları
```
academic-writing-pro yüklenirken oku:
  references/article-voice-[alan].md
  references/article-voice-summary.md
  citations-log.md
  references/plagiarism-rules.md
  references/ai-detector-mechanics.md

literature-review yüklenirken oku:
  citations-log.md
```

---

## 11. Doğrulama Checklist (ADIM 6)

```
□ literature-review/SKILL.md mevcut → boyut > 0
□ academic-writing-pro/SKILL.md mevcut → boyut > 0
□ references/article-voice-fen.md → cümle profili var
□ references/article-voice-sosyal.md → APA Türkçe örnekler var
□ references/article-voice-saglik.md → Vancouver örnekler var
□ references/article-voice-summary.md → 3 alan özeti var
□ citations-log.md → şablon + araştırma kaynakları var
□ ai-detector-mechanics.md → makale dedektörleri genişletildi
□ academic-shield/SKILL.md → 5-rol pipeline eklendi
□ CLAUDE.md → literature-review + academic-writing-pro satırları var
□ skills/INDEX.md → 7. ve 8. satır var
□ skills/literature-review-rehber.md → mevcut
□ skills/academic-writing-pro-rehber.md → mevcut
□ skills/academic-shield-rehber.md → tetikleyiciler tablosu + İlgili Skill'ler var
```

---

## 12. Başarı Kriteri

> **Dedektörden geçemeyen = skill başarısız.**
> GPTZero, Turnitin, Copyleaks, iThenticate, YÖK İntihal, QuillBot — hepsinden geçmek zorunlu.
> Bypass 3 katman (kural + test + doğrulama) tamamlanmadan "bitti" denmez.

---

*Tasarım Belgesi v1.0 | 2026-05-07*
*academic-writing-pro + literature-review + academic-shield güncellemesi*
