# Academic Writing Pro — Tam Kapsamlı Rehber

> **Sürüm:** 1.0 | **Son Güncelleme:** 2026-05-07

---

## Tetikleyiciler

| Kullanıcı Yazdığında | Mod |
|----------------------|-----|
| "makale yaz", "paper", "article" | Mod B |
| "abstract yaz", "özet yaz" | Mod B |
| "latex ver", "overleaf için" | Mod B + LaTeX çıktı |
| "docx ver", "word" | Mod B + DOCX çıktı |
| "dedektörden geçir" + makale | Mod A |
| "bunu düzenle" + makale bağlamı | Mod A |
| "dergi", "scopus", "ieee xplore" | Mod tespiti |
| "fen bilimleri makalesi" | Mod B + Fen/Müh |
| "sağlık makalesi" | Mod B + Sağlık |
| "sosyal bilimler makalesi" | Mod B + Sosyal |

---

## Alan Tespiti

| Sinyal | Alan | Atıf | Profil |
|--------|------|------|--------|
| "deney", "simülasyon", "MATLAB", "Hz", "MPa" | Fen/Müh | IEEE `[1]` | article-voice-fen.md |
| "anket", "nitel", "örneklem", "SPSS", "psikoloji" | Sosyal | APA Türkçe | article-voice-sosyal.md |
| "hasta", "klinik", "prevalans", "p<0.05", "tıp" | Sağlık | Vancouver | article-voice-saglik.md |
| Belirsiz | — | Sor | — |

---

## 5-Rol Pipeline Özeti

```
ROL 1 (Research Orchestrator) → Kaynak yok: literature-review tetikle
ROL 2 (Source Evaluator) → Kalite skoru ile 10-15 kaynak seç
ROL 3 (Domain Expert + Writer) → Alan profiliyle yaz (4 katman dönüşüm)
ROL 4 (Citation Specialist) → Her kaynak için IEEE/APA/Vancouver + DOI
ROL 5 (Bypass Engineer) → Dedektör simülasyonu + doğrulama (max 3 iterasyon)
```

---

## Makale Tipi Tespiti

| Sinyal | Tip | Yapı |
|--------|-----|------|
| "özgün bulgu", "deney", "veri" | Araştırma | Özet→Giriş→Yöntem→Bulgular→Tartışma |
| "sentez", "sistematik", "derleme" | Derleme | PRISMA formatı |
| "olgu", "vaka", "case" | Olgu sunumu | Özet→Giriş→Olgu→Tartışma→Sonuç |

---

## Dergi Seviyesi Kalibrasyonu

| Seviye | Ek Gereklilik |
|--------|--------------|
| Ulusal (TR Dizin) | Türkçe abstract yeterli, DergiPark formatı |
| SCI/SSCI/ESCI | İngilizce abstract zorunlu, IMRAD katı |
| Scopus | Alan normlarına göre |

---

## Çıktı Formatları

- **Markdown** — varsayılan
- **LaTeX** — "latex ver" veya "overleaf için" yazınca; alan bazlı biblatex (IEEE/APA/Vancouver)
- **DOCX** — "docx ver" yazınca; pandoc + Times New Roman 12pt, 1.5 satır

---

## academic-shield ile Fark ve Zincir

| | academic-shield | academic-writing-pro |
|--|-----------------|---------------------|
| Hedef | Tez bölümü | Hakemli dergi makalesi |
| Alan profili | turkish-academic-voice.md | article-voice-fen/sosyal/saglik.md |
| Atıf | IEEE / APA Türkçe | IEEE / APA Türkçe / Vancouver |
| Format | Markdown | Markdown / LaTeX / DOCX |
| Üniversite | SAÜ uyumlu | Üniversiteden bağımsız |

**Zincir:** `academic-shield (Mod B) → academic-writing-pro (Mod A)`

---

## Combo Zincirleri

```
COMBO-AW1: Araştırma → Yazma → Kalite
  literature-review → academic-writing-pro (Mod B) → verification-before-completion

COMBO-AW2: Mevcut Makale Kurtarma
  academic-writing-pro (Mod A)

COMBO-AW3: Tam Pipeline
  literature-review → academic-writing-pro (Mod B) → LaTeX → Overleaf

COMBO-AW4: Tez → Makale
  academic-shield (Mod B) → academic-writing-pro (Mod A)
```

---

## Örnek Kullanım Promptları

**1. Fen Bilimleri araştırma makalesi — Giriş bölümü:**
```
Konu: Derin öğrenme ile nükleer bağlanma enerjisi tahmini
Alan: Fen Bilimleri, IEEE atıf
Bölüm: Giriş
Dergi hedefi: Scopus
Kaynaklar: [mevcut literatür taraması]
```

**2. Sosyal bilimler sistematik derleme — Abstract:**
```
Konu: Uzaktan eğitimin öğrenci motivasyonuna etkisi
Alan: Eğitim, APA Türkçe
Tip: Sistematik derleme
PRISMA uyumlu özet yaz
```

**3. Sağlık bilimleri olgu sunumu:**
```
Konu: Nadir görülen kardiyak aritmi vakası
Alan: Tıp/Hemşirelik, Vancouver
Bölüm: Tüm makale
Etik onay: dahil et
```

**4. Mevcut makale dedektörden geçirme (Mod A):**
```
Ekli metni GPTZero ve Turnitin'den geçirecek şekilde düzenle
Alan: Sosyal Bilimler
Atıf: APA Türkçe
```

**5. LaTeX formatında tam araştırma makalesi:**
```
Konu: Güneş enerjisi sistemlerinde MPPT algoritması
Alan: Fen/Müh, IEEE
Format: LaTeX (Overleaf)
Dergi: Elsevier Energy
Tam makale üret
```

---

## Referans Dosyaları

- [academic-writing-pro/SKILL.md](../academic-writing-pro/SKILL.md)
- [references/article-voice-summary.md](../references/article-voice-summary.md)
- [citations-log.md](../citations-log.md)
- [literature-review-rehber.md](literature-review-rehber.md)
- [academic-shield-rehber.md](academic-shield-rehber.md)
- [INDEX.md](INDEX.md)

---

*Üretilme: 2026-05-07 | Academic Writing Pro Skill v1.0*
