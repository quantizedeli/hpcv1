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

**Türkçe & Ulusal:** DergiPark, YÖK Tez Merkezi, TR Dizin, ULAKBİM, Atatürk Kütüphanesi Digital

**Genel:** Google Scholar, ResearchGate, Semantic Scholar, OpenAlex, BASE, CORE

**İndeksli:** WoS, Scopus, IEEE Xplore, ACM, ScienceDirect, SpringerLink, Wiley, Taylor&Francis, Oxford Academic, Cambridge Core

**Sağlık:** PubMed/MEDLINE, PMC, Cochrane, ClinicalTrials.gov, medRxiv, bioRxiv

**Sosyal:** SSRN, JSTOR, EBSCO, APA PsycNET, ProQuest

**Fen:** arXiv, ChemRxiv

**Açık Erişim:** DOAJ (tüm disiplinler)

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
