# Anthropic Skills Repo — Tam Kapsamlı Rehber

> ⚠️ **Bu repo şu an KURULU DEĞİL — referans amaçlı belgelendi.**

> **Kaynak:** https://github.com/anthropics/skills  
> **Lisans:** MIT  
> **Yıldız:** 127K | **Fork:** 14.9K  
> **Son Güncelleme:** 2026-05-02

---

## İçindekiler

1. [Hızlı Başlangıç Kartı](#hızlı-başlangıç-kartı)
2. [Plugin Anatomisi](#plugin-anatomisi)
3. [Kurulum](#kurulum)
4. [Slash Komutları](#slash-komutları)
5. [Skills — Tam Katalog (17 skill)](#skills--tam-katalog)
6. [Agents](#agents)
7. [Hooks](#hooks)
8. [Scripts & CLI Tools](#scripts--cli-tools)
9. [Config Dosyaları](#config-dosyaları)
10. [MCP Servers](#mcp-servers)
11. [Skill Birleştirme](#skill-birleştirme)
12. [Kendi Skill'ini Oluşturma](#kendi-skillini-oluşturma)
13. [Agent Skills Standardı](#agent-skills-standardı)
14. [Sorun Giderme](#sorun-giderme)
15. [Gerçek Dünya Senaryoları](#gerçek-dünya-senaryoları)
16. [Bakım & Güncelleme](#bakım--güncelleme)
17. [Kaynaklar](#kaynaklar)

---

## Hızlı Başlangıç Kartı

```bash
# 30 saniyede aktif:
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
/reload-plugins
```

**Ne sunar:**
- 17 örnek/eğitim skill — Anthropic'in resmi gösterimi
- Belge işleme: docx, pdf, pptx, xlsx
- Tasarım: algorithmic-art, brand-guidelines, canvas-design, theme-factory
- Geliştirme: claude-api, mcp-builder, web-artifacts-builder, webapp-testing
- İletişim: internal-comms, doc-coauthoring, slack-gif-creator
- Meta: skill-creator (yeni skill yazımı için)
- Görsel: frontend-design

> **Not:** Bu skill'ler **gösteri ve eğitim amaçlıdır** — production garantisi vermez.

---

## Plugin Anatomisi

```
anthropics/skills/
├── .claude-plugin/             ← Plugin yapılandırması
├── skills/                     ← 17 skill (ad alfabetik)
│   ├── algorithmic-art/
│   │   ├── SKILL.md
│   │   ├── LICENSE.txt
│   │   └── templates/
│   ├── brand-guidelines/
│   ├── canvas-design/
│   ├── claude-api/
│   ├── doc-coauthoring/
│   ├── docx/
│   │   └── scripts/
│   ├── frontend-design/
│   ├── internal-comms/
│   ├── mcp-builder/
│   ├── pdf/
│   ├── pptx/
│   ├── skill-creator/
│   │   ├── agents/
│   │   ├── assets/
│   │   ├── eval-viewer/
│   │   ├── references/
│   │   └── scripts/
│   ├── slack-gif-creator/
│   ├── theme-factory/
│   ├── web-artifacts-builder/
│   ├── webapp-testing/
│   └── xlsx/
├── spec/                       ← Agent Skills standardı
├── template/
│   └── SKILL.md
├── README.md
├── THIRD_PARTY_NOTICES.md
└── LICENSE                     ← MIT
```

**Dil dağılımı:** Python 84.4%, HTML 12.4%, Shell 1.9%, JavaScript 1.3%

---

## Kurulum

### Yöntem 1: Plugin Marketplace (Önerilen)

```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills    # docx, pdf, pptx, xlsx
/plugin install example-skills@anthropic-agent-skills     # diğer 13 skill
/reload-plugins
```

### Yöntem 2: Claude.ai (Web)

1. Pro veya Team planı gerekli
2. Settings → Skills
3. "Add Skill" — yükle veya custom skill oluştur

### Yöntem 3: Claude API

```python
from anthropic import Anthropic
client = Anthropic()
# Docs: https://docs.claude.com/en/api/skills-guide
```

### Yöntem 4: Manuel Klonlama (Tek Skill)

```bash
git clone https://github.com/anthropics/skills /tmp/anthropics-skills
cp -r /tmp/anthropics-skills/skills/<skill-adı> ~/.claude/skills/
/reload-plugins
```

### Bağımlılıklar

| Bileşen | Gereksinim |
|---------|------------|
| Claude Code | v1.0.33+ |
| Python | 3.x (skill'lerin çoğu için) |
| Node.js | Bazı skill'ler için |
| (xlsx) | pandas, openpyxl |
| (pdf) | pypdf, pdfplumber, reportlab, pytesseract |
| (pptx) | python-pptx, PptxGenJS |
| (docx) | docx (JS lib), pandoc |

---

## Slash Komutları

Anthropic skills repo **slash komut sağlamaz** — tüm skill'ler otomatik tetiklenir veya `/skill <ad>` ile çağrılır.

---

## Skills — Tam Katalog

17 skill, 5 kategoride.

### Skill Çağırma Mekanizması

| Yöntem | Detay |
|--------|-------|
| Otomatik | Skill `description` alanı kullanıcı mesajıyla eşleşir |
| Manuel (CLI) | `/skill <skill-adı>` |
| Manuel (Tool) | `Skill` tool ile `skill: "<skill-adı>"` |

---

### A) Belge & Dosya İşleme (4 skill)

#### `docx` — Word Belgesi

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "Word doc", ".docx", "TOC", "letterhead", "tracked changes" |
| **Yetenekler** | Sıfırdan oluştur, oku, düzenle, TOC, tablo, görsel, tracked changes |
| **Kütüphane** | `docx` (JS) |
| **Anti-pattern** | Yüzde tablo genişliği (Google Docs'u bozar), manuel bullet karakteri |

**Teknik Kurallar:**
- Sayfa boyutu varsayılan A4 — US Letter için ayar gerek
- Font: Arial (evrensel uyumluluk)
- Tablo: `columnWidths` array + cell `width` (DXA birim)
- Görseller: `type` parametresi zorunlu (png, jpg)
- Page break Paragraph içine nest
- Tracked changes: `<w:ins>` / `<w:del>`, varsayılan author "Claude"
- Smart quotes: `&#x201C;` XML entity
- Otomatik validation + auto-repair

---

#### `pdf` — PDF İşleme

| Alan | Değer |
|------|-------|
| **Tetikleyici** | ".pdf", "PDF oluştur/oku/birleştir/böl", "OCR", "form doldur" |
| **Yetenekler** | Birleştir, böl, döndür, watermark, sıfırdan, metin/tablo çıkar, OCR, form fill, encrypt |

**Kütüphaneler:**

| Kütüphane | Kullanım |
|-----------|----------|
| `pypdf` | Birleştir, böl, döndür, metadata |
| `pdfplumber` | İçerik + tablo çıkarımı, pandas entegrasyonu |
| `reportlab` | Sıfırdan PDF (Canvas veya Platypus) |
| `pytesseract` + `pdf2image` | OCR |

**Önemli:** Unicode subscript/superscript yerleşik fontlarda yok — `<sub>` ve `<super>` XML etiketleri kullan.

---

#### `pptx` — PowerPoint Sunum

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "deck", "slides", "presentation", ".pptx" |
| **Yetenekler** | Sıfırdan oluştur, oku, düzenle, thumbnail, speaker notes, comments, PPTX→Web |
| **Kütüphaneler** | `python-pptx` (oku), `PptxGenJS` (oluştur) |

**Tasarım İlkeleri:**
- Generic mavi tasarım kullanma — bold content-informed palet seç
- 60-70% baskın renk + vurgu
- Tekrar eden layout YASAK
- Her slayta görsel öge (sadece metin yasak)

**Kalite Kontrol:** İçerik → Görsel dönüştür → İncele → Subagent fresh perspective → Düzelt → Doğrula

---

#### `xlsx` — Excel İşleme

| Alan | Değer |
|------|-------|
| **Tetikleyici** | ".xlsx", ".xlsm", ".csv", ".tsv", "spreadsheet", "Excel" |
| **Yetenekler** | Oluştur, düzenle, formül, grafik, finansal model, format dönüştürme |
| **Kütüphaneler** | `pandas`, `openpyxl` |

**Kritik Kurallar:**
- Python'da hesaplayıp hardcode etme — Excel formülü kullan
- Sıfır hata kuralı (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Oluşturma sonrası `scripts/recalc.py` çalıştır

**Finansal Model Renk Kodlaması:**

| Renk | Anlam |
|------|-------|
| Mavi metin | Hardcoded girdi |
| Siyah metin | Tüm formüller |
| Yeşil metin | Çalışma sayfaları arası link |
| Kırmızı metin | Harici dosya link |
| Sarı arka plan | Dikkat gerektiren varsayım |

**Sayı Formatı:** Yıllar text ("2024"), para birimi $#,##0, sıfırlar "-", yüzde 0.0%, negatif parentez

---

### B) Tasarım & Görsel (5 skill)

#### `algorithmic-art` — Algoritmik Sanat

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "algoritmik sanat", "generative art", "flow field", "particle system", "p5.js" |
| **Yetenekler** | p5.js + seeded randomness + interaktif parametreler |

**Yaratıcı Süreç:**
1. Felsefe önce — "Algoritma güzelliği nasıl ifade edecek?"
2. p5.js uygulama — `templates/viewer.html`'den başla
3. Seed sistemi — Aynı seed = aynı çıktı (Art Blocks pattern)
4. Parametreler — Sistemden doğal çıkan miktar/ölçek/olasılık

**Çıktı:** Tek self-contained HTML artifact (Anthropic branding dahil)

---

#### `brand-guidelines` — Anthropic Marka

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "Anthropic stili", "marka renkleri", "kurumsal tasarım" |
| **Yetenekler** | Anthropic resmi marka renk + tipografi her artifact'a uygulanır |

**Renk Paleti:**

| Renk | Hex |
|------|-----|
| Koyu Gri (Ana) | `#141413` |
| Krem (Arka Plan) | `#faf9f5` |
| Turuncu (Vurgu) | `#d97757` |
| Mavi (Vurgu) | `#6a9bcc` |
| Yeşil (Vurgu) | `#788c5d` |

**Tipografi:** Başlıklar 24pt+: **Poppins** (yedek: Arial) | Body: **Lora** (yedek: Georgia)

---

#### `canvas-design` — Görsel Sanat (.png/.pdf)

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "poster", "sanat eseri", "tasarım", "statik görsel" |
| **Yetenekler** | .png ve .pdf formatında özgün eserler |
| **Çıktı** | %90 görsel, %10 metin — müze/dergi kalitesi |

**Metodoloji:**
1. Tasarım hareketi adını belirle
2. Estetiğin görsel olarak nasıl tezahür ettiğini anlatan felsefe yaz
3. Esere gömülü kavramsal DNA'yı tanımla
4. Tek sayfa canvas + kompozisyon rafine

---

#### `frontend-design` — Özgün Frontend UI

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "distintif UI", "özel arayüz", "production frontend" |
| **Yetenekler** | Brutalist, maximalist, retro-futurist, refined minimalism stilleri |

**İlkeler:**
- Generic font kullanma (Arial, Inter) — özgün seç
- Öngörülebilir layout'lardan kaçın
- Yüksek etkili animasyon
- Asimetrik, üst üste binen layout
- Atmosferik derinlik (doku, degrade)

---

#### `theme-factory` — Tema Üretici

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "tema uygula", "tasarım stili" |
| **Yetenekler** | 10 hazır tema (renk + font) + custom üretim |

**Süreç:** Theme showcase göster → Kullanıcı tercih et → Tema uygula

**Hazır temalar:** Ocean Depths, Midnight Galaxy ve 8 tane daha

---

### C) Geliştirme & Teknik (5 skill)

#### `claude-api` — Claude API Geliştirme

| Alan | Değer |
|------|-------|
| **Tetikleyici** | `anthropic` veya `@anthropic-ai/sdk` import, "Claude API", "Managed Agents" |
| **Yetenekler** | Python, TS, Java, Go, Ruby, C#, PHP, cURL ile entegrasyon |
| **Default model** | `claude-opus-4-7` |
| **Adaptive thinking** | `{type: "adaptive"}` (yeni; `budget_tokens` deprecated) |

**Karar Ağacı:**

| İhtiyaç | Kullanım |
|---------|---------|
| Tekli çağrı | Claude API |
| Multi-step pipeline | Claude API + tool use |
| Anthropic-hosted agent + workspace | Managed Agents |
| 3rd party (Bedrock, Vertex) | Claude API + tool use |

**Yetenekler:** Prompt caching, adaptive thinking, batch, Files API, Citations, Memory, Compaction

**Guardrails:**
- Sadece Anthropic SDK — OpenAI tespit edilirse dur
- Maliyet için downgrade YOK
- Tahmin etmeden documented signature kullan

---

#### `webapp-testing` — Web App Testi

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "Playwright", "yerel web app testi", "browser otomasyon", "UI doğrulama" |
| **Yetenekler** | UI test, debug, screenshot, log, çoklu sunucu |
| **Helper** | `with_server.py` (sunucu lifecycle yönetimi) |

**İş Akışı (Reconnaissance-Then-Action):**
1. Navigate + `page.wait_for_load_state('networkidle')`
2. Screenshot veya DOM incele
3. CSS selector / accessibility role ile element bul
4. Test eylem çalıştır

---

#### `mcp-builder` — MCP Sunucu Geliştirme

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "MCP server oluştur", "LLM tool entegrasyonu" |
| **Yetenekler** | TypeScript (önerilen) veya Python ile MCP — tool, resource, prompt, Zod, stdio/HTTP |

**4 Aşama:**
1. **Araştırma & Planlama** — MCP protokolü incele, stack seç
2. **Uygulama** — Project, API client, error handling, tools
3. **İnceleme & Test** — MCP Inspector
4. **Değerlendirme** — 10 karmaşık test sorusu (multiple tool calls)

**Tasarım İlkeleri:** Tutarlı action-oriented isimlendirme, yönlendirici hata mesajları, hem text hem yapılandırılmış data, pagination

---

#### `web-artifacts-builder` — Karmaşık HTML Artifact

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "karmaşık artifact", "shadcn ile UI", "state management", "routing" |
| **Stack** | React 18 + TypeScript + Vite + Parcel + Tailwind + shadcn/ui |

**5 Adım:**
1. Frontend repo başlat
2. Artifact geliştir
3. Tek HTML'e bundle
4. Sun
5. (Opsiyonel) test

**Tasarım uyarısı:** Aşırı centered layout, mor gradient, uniform yuvarlak köşe, Inter font kaçın.

---

#### `slack-gif-creator` — Slack GIF Üretici

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "Slack emoji", "animasyonlu GIF" |
| **Yetenekler** | 8 animasyon tekniği — sallama, nabız, zıplama, dönme, solma, kaydırma, zoom, parçacık patlaması |
| **Kütüphaneler** | Pillow, imageio, numpy |

**Boyutlar:**

| Tür | Boyut |
|-----|-------|
| Emoji | 128×128 px |
| Mesaj | 480×480 px |
| FPS | 10-30 |
| Süre | <3 sn (emoji) |

---

### D) İletişim & İçerik (2 skill)

#### `internal-comms` — İç İletişim

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "şirket newsletter", "status raporu", "leadership update", "incident report" |
| **6 Format** | 3P updates, newsletter, FAQ, status report, leadership update, incident report |

**3 Adım:** İletişim türü belirle → `examples/` dizininden guideline yükle → Biçim + ton uygula

---

#### `doc-coauthoring` — Belge Birlikte Yazımı

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "dokümantasyon yaz", "öneri", "spec" |
| **Yetenekler** | 3 aşamalı işbirlikçi belge oluşturma |

**3 Aşama:**
1. **Bağlam Toplama** — Belge türü, kitle, etki, kısıtlar
2. **Rafine & Yapılandır** — Soru → Beyin fırtınası (5-20) → Seç → Taslak → Yinele
3. **Okuyucu Testi** — Bağlamı bilmeyen okuyucu simülasyonu

---

### E) Meta — Skill Geliştirme (1 skill)

#### `skill-creator` — Yeni Skill Oluşturma

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "yeni skill yaz", "skill optimize", "skill eval" |
| **Yetenekler** | Sıfırdan skill, eval ile test, varyans analizi, description optimizasyonu |

**4 Adım:**
1. **Niyeti Yakala** — Ne yapmalı, ne zaman tetiklenmeli, çıktı formatı
2. **Skill Taslağı** — `SKILL.md` + frontmatter; description "ısrarcı" olmalı
3. **Eval ile Test** — 2-3 test prompt, paralel skill var/yok karşılaştırma
4. **İnceleme & Yineleme** — Eval viewer, kalıplardan genelleştir

**Eval Viewer:** Quantitatif metrikler + görsel çıktı karşılaştırma

---

## Agents

`skill-creator/agents/` altında — yeni skill yazımına yardım eden uzmanlık ajanları (eval-runner, etc.).

---

## Hooks

Anthropic skills repo **hook sağlamaz** — saf skill koleksiyonu.

---

## Scripts & CLI Tools

| Skill | Scriptler |
|-------|-----------|
| `docx` | `scripts/` (validation, repair) |
| `xlsx` | `scripts/recalc.py` (formül recalc) |
| `webapp-testing` | `with_server.py` (sunucu lifecycle) |
| `skill-creator` | `eval-viewer/`, eval scripts |

---

## Config Dosyaları

### Skill Frontmatter Şablonu

```yaml
---
name: my-skill-name           # Küçük harf, tire ayraç
description: |                # NE yaptığı + NE ZAMAN — her ikisi de zorunlu
  Skill ne yaptığı VE ne zaman kullanılacağı.
  "Make sure to use this skill whenever the user mentions..."
---
```

---

## MCP Servers

Anthropic skills repo **MCP server sağlamaz** ama bazı skill'ler MCP'lerle uyumludur.

---

## Skill Birleştirme

### Belge İş Akışı Zinciri

```
docx → pdf (PDF dönüşüm)
pptx → pdf (sunum → PDF)
xlsx → docx (rapor üretimi)
```

### Tasarım Pipeline

```
brand-guidelines → canvas-design → theme-factory
```

### Geliştirme Pipeline

```
claude-api → mcp-builder → webapp-testing → web-artifacts-builder
```

---

## Kendi Skill'ini Oluşturma

### Minimum Yapı

```
my-skill/
└── SKILL.md
```

### SKILL.md Şablonu

```yaml
---
name: my-skill-name
description: |
  Bu skill'in ne yaptığı ve ne zaman tetikleneceği.
  Make sure to use this skill whenever the user mentions [konu].
---

# My Skill Name

[Talimatlar]

## Examples
- Örnek 1

## Guidelines
- Rehber 1
```

### Kritik Kurallar

| Alan | Kural |
|------|-------|
| `name` | Küçük harf, tire ayraç |
| `description` | NE yaptığı + NE ZAMAN — her ikisi de zorunlu |
| Tetikleme | "Make sure to use this skill whenever..." (ısrarcı) |
| Talimatlar | "Neden"i açıkla — sınır durumlarında daha iyi karar |

---

## Agent Skills Standardı

Anthropic skills repo, **Agent Skills Standard** (`agentskills.io`) implementasyonunu gösterir:

- Klasör tabanlı (taşınabilir)
- `SKILL.md` tek zorunlu dosya
- Harici scripts/templates/assets opsiyonel
- Dinamik yükleme — bağlamsal performans
- Çerçeveler arası uyum (Claude, Codex, vs.)

Resmi spec: `spec/` dizini (anthropics/skills repo'sunda).

---

## Sorun Giderme

### Plugin marketplace'te bulunamıyor

```bash
# Doğru komut
/plugin marketplace add anthropics/skills

# Yanlış (SSH URL):
/plugin marketplace add git@github.com:anthropics/skills.git
```

### docx skill çıktısı Google Docs'ta bozuk

**Sebep:** Tablo genişliği yüzde olarak verilmiş.

**Çözüm:** DXA birim kullan:

```javascript
columnWidths: [4500, 4500],  // DXA
// hücrelerde de width: { size: 4500, type: WidthType.DXA }
```

### xlsx formül #REF! hatası

```bash
python scripts/recalc.py output.xlsx
```

### pptx sunum jenerik mavi

Konu-bilinçli palet seç + her slayta görsel öge ekle.

---

## Gerçek Dünya Senaryoları

### Senaryo 1: Aylık Rapor (Tam Zincir)

```
1. internal-comms → "Q2 status report" formatı
2. xlsx → Veri tabloları + grafikler
3. docx → Raporu birleştir, TOC, başlıklar
4. brand-guidelines → Anthropic stili uygula
5. pdf → Final PDF ihracı
```

### Senaryo 2: Pitch Sunumu

```
1. internal-comms → Stratejik mesajlaşma
2. canvas-design → Hero görsel
3. pptx → 12 slayt sunum
4. theme-factory → Cohesive tema
5. brand-guidelines → Marka uyumu kontrolü
```

### Senaryo 3: AI Uygulama Geliştirme

```
1. claude-api → API design
2. mcp-builder → MCP server
3. web-artifacts-builder → Frontend artifact
4. webapp-testing → Playwright testleri
```

---

## Bakım & Güncelleme

```bash
/plugin update document-skills@anthropic-agent-skills
/plugin update example-skills@anthropic-agent-skills

/plugin marketplace list
/plugin
```

---

## Kaynaklar

- **GitHub:** https://github.com/anthropics/skills
- **Resmi Docs:** https://support.claude.com/en/articles/12512176-what-are-skills
- **Agent Skills Standard:** http://agentskills.io
- **Skills API Quickstart:** https://docs.claude.com/en/api/skills-guide
- **Lisans:** MIT

### İlgili Belgeler

- [INDEX.md](INDEX.md) — Ana indeks
- [everything-claude-code-rehber.md](everything-claude-code-rehber.md) — ECC mega-plugin
- [superpowers-rehber.md](superpowers-rehber.md) — Geliştirme metodolojisi
- [ui-ux-pro-max-rehber.md](ui-ux-pro-max-rehber.md) — UI/UX tasarım
- [humanizer-rehber.md](humanizer-rehber.md) — AI yazı temizleme

---

*Üretilme tarihi: 2026-05-02 | Anthropic Skills referans*  
*KURULU DEĞİL — referans amaçlı saklandı*
