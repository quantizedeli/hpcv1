# UI UX Pro Max — Tam Kapsamlı Rehber

> **Sürüm:** 2.5.0 | **Lisans:** MIT  
> **Yazar:** NextLevelBuilder ([@nextlevelbuilder](https://github.com/nextlevelbuilder))  
> **Kaynak:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill  
> **Site:** https://uupm.cc | **Yıldız:** 72.9K  
> **Son Güncelleme:** 2026-05-02

---

## İçindekiler

1. [Hızlı Başlangıç Kartı](#hızlı-başlangıç-kartı)
2. [Plugin Anatomisi](#plugin-anatomisi)
3. [Kurulum](#kurulum)
4. [Slash Komutları](#slash-komutları)
5. [Skills — Tam Katalog (7 skill)](#skills--tam-katalog)
6. [Agents](#agents)
7. [Hooks](#hooks)
8. [Scripts & CLI Tools](#scripts--cli-tools)
9. [Config Dosyaları](#config-dosyaları)
10. [MCP Servers](#mcp-servers)
11. [Skill Birleştirme — İş Akışı Zincirleri](#skill-birleştirme--iş-akışı-zincirleri)
12. [Referans Veritabanları](#referans-veritabanları)
13. [Sorun Giderme](#sorun-giderme)
14. [Gerçek Dünya Senaryoları](#gerçek-dünya-senaryoları)
15. [Bakım & Güncelleme](#bakım--güncelleme)
16. [Kaynaklar](#kaynaklar)

---

## Hızlı Başlangıç Kartı

```bash
# 30 saniyede aktif:
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
/reload-plugins

# İlk komut (skill otomatik tetiklenir):
"Güzellik spa'sı için landing page yap"
# → ui-ux-pro-max skill otomatik devreye girer
```

**Ne sunar:**
- 7 skill — ana zeka, design, design-system, brand, ui-styling, banner, slides
- 67 UI stili (Glassmorphism, Brutalism, Claymorphism, Bento, ...)
- 161 renk paleti (sektör eşleştirmeli)
- 57 Google Fonts eşleşmesi
- 161 sektör akıl yürütme kuralı
- 99 UX rehberi
- 25 grafik tipi
- **16 tech stack** desteği — React, Next.js, Vue, Svelte, Astro, Flutter, SwiftUI, vs.
- Python BM25 + regex hybrid arama motoru

---

## Plugin Anatomisi

```
ui-ux-pro-max/2.5.0/
├── .claude-plugin/
│   ├── plugin.json              ← Plugin manifest
│   └── README.md
├── .claude/
│   └── skills/
│       ├── ui-ux-pro-max/       ← Ana zeka skill
│       ├── design/              ← Unified design (logo, CIP, banner, slides, icon)
│       ├── design-system/       ← Token mimarisi
│       ├── brand/               ← Marka kimliği
│       ├── ui-styling/          ← shadcn/ui + Tailwind + Canvas
│       ├── banner-design/       ← Multi-format banner
│       └── slides/              ← HTML sunum (Chart.js)
├── src/ui-ux-pro-max/           ← Source of Truth
│   ├── data/                    ← Canonical CSV veritabanları
│   │   ├── products.csv         (161 ürün tipi)
│   │   ├── styles.csv           (67 stil + AI prompt + CSS)
│   │   ├── colors.csv           (161 palet)
│   │   ├── typography.csv       (57 font eşleşmesi)
│   │   ├── google-fonts.csv
│   │   ├── icons.csv            (15 ikon stili)
│   │   ├── charts.csv           (25 grafik tipi)
│   │   ├── landing.csv
│   │   ├── ux-guidelines.csv    (99 UX kuralı)
│   │   ├── ui-reasoning.csv     (161 akıl yürütme kuralı)
│   │   ├── design.csv           (CIP teslimatları)
│   │   ├── app-interface.csv
│   │   ├── react-performance.csv
│   │   ├── draft.csv
│   │   └── stacks/              (16 stack CSV'si)
│   ├── scripts/
│   │   ├── search.py            ← CLI giriş noktası
│   │   ├── core.py              ← BM25 + regex motoru
│   │   └── design_system.py     ← Tasarım sistemi üretici
│   └── templates/
├── cli/                         ← uipro-cli npm paketi
├── CLAUDE.md
├── README.md
└── skill.json
```

---

## Kurulum

### Yöntem 1: Plugin Marketplace (Önerilen)

```bash
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
/reload-plugins
```

### Yöntem 2: CLI ile Çoklu Platform

```bash
npm install -g uipro-cli

# Platform seç ve kur
uipro init --ai claude
# Diğer platformlar: cursor, windsurf, copilot, kiro, roocode, kilocode,
# codex, qoder, gemini, trae, opencode, continue, codebuddy, droid, warp, augment
```

### Bağımlılıklar

| Bileşen | Gereksinim | Neden |
|---------|------------|-------|
| Claude Code | v1.0.33+ | `/plugin` komutu için |
| **Python 3.x** | **ZORUNLU** | Arama motoru ve design system için |
| Node.js | v18+ | uipro-cli paketi için |

---

## Slash Komutları

UI UX Pro Max **slash komut sağlamaz** — tüm fonksiyonalite skill'ler ile otomatik tetiklenir. `search.py` Bash üzerinden CLI olarak kullanılabilir.

---

## Skills — Tam Katalog

### Skill Çağırma Mekanizması

1. **Otomatik** — UI/UX iş tanımı içeren mesajlar (button, modal, landing page, dashboard, color, typography, design system, ...)
2. **Manuel** — `/skill ui-ux-pro-max`

---

### 1. `ui-ux-pro-max` — Ana Tasarım Zekası

| Alan | Değer |
|------|-------|
| **Tetikleyici** | UI yapısı, görsel tasarım, etkileşim kalıbı, UX kalite kontrolü |
| **Ne Zaman Kullan** | Yeni sayfa, UI bileşeni, renk/tipografi/spacing/layout seçimi, UX review |
| **Ne Zaman KULLANMA** | Saf backend, API/DB tasarım, perf opt, DevOps, görsel olmayan otomasyon |
| **Çağırma** | Otomatik (UI/UX kelimesi) veya `/skill ui-ux-pro-max` |
| **Yetenekler** | 161 sektör kuralı, 67 stil, 161 palet, 57 font, BM25 arama |
| **Bağımlılıklar** | Python 3.x |

**10 Öncelik Kuralı:**

| # | Kategori | Etki | Zorunlu |
|---|----------|------|---------|
| 1 | Erişilebilirlik | KRİTİK | 4.5:1 kontrast, alt text, keyboard nav, aria |
| 2 | Dokunma & Etkileşim | KRİTİK | 44×44px min, 8px+ aralık, loading feedback |
| 3 | Performans | YÜKSEK | WebP/AVIF, lazy load, CLS<0.1 |
| 4 | Stil Seçimi | YÜKSEK | Ürün tipi uyumu, SVG ikon |
| 5 | Layout & Responsive | YÜKSEK | Mobile-first, viewport meta |
| 6 | Tipografi & Renk | ORTA | 16px base, line-height 1.5, semantic token |
| 7 | Animasyon | ORTA | 150-300ms, anlam taşıyan hareket |

---

### 2. `design` (claudekit:design) — Unified Tasarım Skill'i

| Alan | Değer |
|------|-------|
| **Sürüm** | 2.1.0 |
| **Tetikleyici** | Marka kimliği, logo, kurumsal kimlik, banner, sosyal medya, sunum, ikon |
| **Çağırma** | `/skill design [type] [context]` veya otomatik |

**Alt-Skill Yönlendirme:**

| Görev | Alt-Skill |
|-------|-----------|
| Marka kimliği, ses, varlıklar | `brand` |
| Token, spec, CSS değişkenleri | `design-system` |
| shadcn/ui, Tailwind, kod | `ui-styling` |
| Logo oluşturma | Logo (dahili) — `references/logo-design.md` |
| CIP mockup | CIP (dahili) — `references/cip-design.md` |
| Sunum, pitch deck | Slides (dahili) — `references/slides.md` |
| Banner, kapak, header | Banner (dahili) — `references/banner-sizes-and-styles.md` |
| Sosyal medya | Social Photos — `references/social-photos-design.md` |
| SVG ikon | Icon — `references/icon-design.md` |

**Logo Tasarımı:**
- 55+ stil, 30 renk paleti, 25 sektör rehberi
- ALWAYS beyaz arka plan

```bash
python3 ~/.claude/skills/design/scripts/logo/search.py "tech startup modern" --design-brief -p "BrandName"
python3 ~/.claude/skills/design/scripts/logo/search.py "minimalist clean" --domain style
python3 ~/.claude/skills/design/scripts/logo/search.py "healthcare medical" --domain industry
```

---

### 3. `design-system` (claudekit:design-system) — Token Mimarisi

| Alan | Değer |
|------|-------|
| **Sürüm** | 1.0.0 |
| **Tetikleyici** | Tasarım token, component spec, CSS değişken sistemi, Tailwind tema |

**3 Katmanlı Token Mimarisi:**

```
┌─────────────────────────────────┐
│  Component Tokens               │  Bileşen-spesifik override
│  --button-bg, --card-padding    │
├─────────────────────────────────┤
│  Semantic Tokens                │  Amaç-temelli takma adlar
│  --color-primary                │
├─────────────────────────────────┤
│  Primitive Tokens               │  Ham tasarım değerleri
│  --color-blue-600, --space-4    │
└─────────────────────────────────┘
```

```css
--color-blue-600: #2563EB;        /* Primitive */
--color-primary: var(--color-blue-600);  /* Semantic */
--button-bg: var(--color-primary);       /* Component */
```

```bash
node scripts/generate-tokens.cjs --config tokens.json -o tokens.css
node scripts/validate-tokens.cjs --dir src/
```

---

### 4. `brand` (claudekit:brand) — Marka Kimliği

| Alan | Değer |
|------|-------|
| **Sürüm** | 1.0.0 |
| **Tetikleyici** | Marka sesi, görsel kimlik, mesajlaşma çerçevesi, varlık yönetimi |

**Reference Dosyaları (10 dosya):** brand-guideline-template, color-palette-management, logo-usage-rules, typography-specifications, visual-identity, voice-framework, messaging-framework, consistency-checklist, asset-organization, approval-checklist

**Marka Senkronizasyon:**

```bash
node scripts/sync-brand-to-tokens.cjs
node scripts/inject-brand-context.cjs --json
node scripts/validate-asset.cjs <varlık-yolu>
node scripts/extract-colors.cjs --palette
```

---

### 5. `ui-styling` (claudekit:ui-styling) — shadcn/ui + Tailwind + Canvas

| Alan | Değer |
|------|-------|
| **Sürüm** | 1.0.0 |
| **Tetikleyici** | React tabanlı çerçeve UI, erişilebilir bileşen, responsive layout, dark mode |

**3 Katmanlı Stack:**

| Katman | Teknoloji | Açıklama |
|--------|-----------|----------|
| Bileşen | shadcn/ui | Radix UI üzerine kurulu erişilebilir bileşenler |
| Stil | Tailwind CSS | Utility-first, sıfır runtime overhead |
| Görsel | Canvas | Müze kalitesi görsel kompozisyon |

**shadcn/ui Kurulum:**

```bash
npx shadcn@latest add button
npx shadcn@latest add button card dialog
npx shadcn@latest add --all
```

**shadcn/ui Bileşenler:**
- **Form & Input:** Button, Input, Label, Textarea, Select, Checkbox, Radio, Switch, Slider, Toggle, Calendar, DatePicker
- **Layout:** Card, Separator, Tabs, Accordion, Collapsible, Resizable, ScrollArea, AspectRatio
- **Overlay:** Dialog, AlertDialog, Sheet, Drawer, Popover, Tooltip, HoverCard
- **Navigation:** Menubar, NavigationMenu, Breadcrumb, Pagination, ContextMenu, DropdownMenu
- **Data:** Table, DataTable, Skeleton
- **Feedback:** Alert, Toast, Sonner, Progress, Badge
- **Advanced:** Command (palette), Combobox, Form

---

### 6. `banner-design` (claudekit:banner-design) — Multi-Format Banner

| Alan | Değer |
|------|-------|
| **Sürüm** | 1.0.0 |
| **Tetikleyici** | Banner, kapak, header, sosyal medya kapak, reklam, hero, print, kampanya |

**5 Adım İş Akışı:**
1. Gereksinim topla (amaç, platform/boyut, içerik, marka, stil, adet)
2. Araştırma & Art Direction (ui-ux-pro-max + Pinterest)
3. Tasarım & Üret (frontend-design skill ile HTML/CSS)
4. Screenshot al
5. Sun & İncele — yan yana göster, tercih edileni rafine et

**22 Art Direction Stili:**
minimalist, gradient, bold typography, photo-based, illustrated, geometric, retro, glassmorphism, 3D, neon, duotone, editorial, collage, isometric, line-art, watercolor, paper-cut, organic, flat-color, monochrome, grid-based, asymmetric

---

### 7. `slides` (claudekit:slides) — Stratejik HTML Sunum

| Alan | Değer |
|------|-------|
| **Sürüm** | 1.0.0 |
| **Tetikleyici** | Pazarlama sunumu, pitch deck, veri-driven slayt |

**Bilgi Tabanı:**

| Konu | Dosya |
|------|-------|
| Layout Kalıpları | `references/layout-patterns.md` |
| HTML Şablonu | `references/html-template.md` |
| Copywriting Formülleri | `references/copywriting-formulas.md` |
| Slayt Stratejileri | `references/slide-strategies.md` |

---

## Agents

UI UX Pro Max **agent sağlamaz** — tüm iş skill'ler ile.

---

## Hooks

UI UX Pro Max **hook kullanmaz**.

---

## Scripts & CLI Tools

### `search.py` — Ana Arama CLI

```bash
python3 search.py "<query>" [opsiyonlar]
```

**Tüm Argümanlar:**

| Argüman | Kısa | Açıklama |
|---------|------|----------|
| `query` | (pozisyonel) | Arama sorgusu (ZORUNLU) |
| `--domain` | `-d` | Arama alanı |
| `--stack` | `-s` | Stack-spesifik arama |
| `--max-results` | `-n` | Sonuç sayısı (varsayılan: 3) |
| `--json` | - | JSON formatında çıktı |
| `--design-system` | `-ds` | Tam tasarım sistemi öner |
| `--project-name` | `-p` | Tasarım sistemi için proje adı |
| `--format` | `-f` | `ascii` (varsayılan) veya `markdown` |
| `--persist` | - | `design-system/MASTER.md`'ye kaydet |
| `--page` | - | Page-spesifik override dosyası |
| `--output-dir` | `-o` | Persistance çıktı dizini |

### 9 Domain (Alan)

| Domain | CSV | Ne Döndürür |
|--------|-----|-------------|
| `style` | styles.csv | UI stilleri + AI prompt'ları + CSS keywords |
| `prompt` | styles.csv | Stil için AI image prompt'ları |
| `color` | colors.csv | Ürün tipine göre renk paletleri |
| `chart` | charts.csv | Grafik tipleri + kütüphane önerileri |
| `landing` | landing.csv | Landing page yapısı + CTA stratejileri |
| `product` | products.csv | Ürün tipi önerileri |
| `ux` | ux-guidelines.csv | Best practice + anti-pattern |
| `typography` | typography.csv | Google Fonts importlu font eşleşmeleri |
| `google-fonts` | google-fonts.csv | Google Fonts veritabanı |

### 16 Stack

react, nextjs, vue, svelte, astro, swiftui, react-native, flutter, nuxtjs, nuxt-ui, html-tailwind (varsayılan), shadcn, jetpack-compose, threejs, angular, laravel

### Kullanım Örnekleri

```bash
# Domain araması
python3 search.py "glassmorphism modern fintech" --domain style
python3 search.py "saas tech professional" --domain color
python3 search.py "dashboard data-heavy analytics" --domain typography
python3 search.py "ecommerce conversion checkout" --domain landing
python3 search.py "financial revenue quarterly" --domain chart
python3 search.py "form validation error message" --domain ux

# Stack-spesifik
python3 search.py "card component" --stack nextjs
python3 search.py "dark mode adaptive" --stack flutter
python3 search.py "tab bar navigation" --stack swiftui

# Tasarım Sistemi Üretimi
python3 search.py "beauty spa wellness" --design-system -p "Serenity Spa"
python3 search.py "fintech banking" --design-system -p "PayFlow" --format markdown
python3 search.py "saas dashboard" --design-system --persist -p "MyApp" --page "dashboard"
```

### Çıktı Formatları

**ASCII (varsayılan):**
```
+----------------------------------------------------+
|  TARGET: Serenity Spa - RECOMMENDED DESIGN SYSTEM  |
+----------------------------------------------------+
|  PATTERN: Hero-Centric + Social Proof              |
|  STYLE: Soft UI Evolution                          |
|  COLORS:                                           |
|     Primary:    #E8B4B8 (Soft Pink)                |
|     Secondary:  #A8D5BA (Sage Green)               |
|     CTA:        #D4AF37 (Gold)                     |
|  TYPOGRAPHY: Cormorant Garamond / Montserrat       |
|  AVOID: Neon, harsh animations, dark mode          |
+----------------------------------------------------+
```

**Markdown:** Tam markdown formatında, copy-paste edilebilir.

**JSON (--json flag):** Programatik tüketim için yapılandırılmış veri.

### Master + Overrides Pattern

`--persist` ile aktif olur:

```
design-system/<project-slug>/
├── MASTER.md              ← Global Source of Truth
└── pages/
    ├── dashboard.md        ← Dashboard override
    ├── landing.md          ← Landing override
    └── ...
```

**Kural:** Sayfa kurarken önce `pages/<page>.md` kontrol et. Varsa override geçerli; yoksa `MASTER.md` kullan.

---

## Config Dosyaları

### `plugin.json`

```json
{
  "name": "ui-ux-pro-max",
  "version": "2.5.0",
  "author": { "name": "nextlevelbuilder" },
  "license": "MIT",
  "keywords": ["ui", "ux", "design", "styles", "typography", "color-palette", "accessibility", "charts"],
  "skills": ["./.claude/skills/ui-ux-pro-max"]
}
```

> **Dikkat:** plugin.json'da `skills` alanı SADECE `ui-ux-pro-max` skill'ini referans eder. Diğer 6 skill Claude tarafından otomatik tarama ile keşfedilir.

---

## MCP Servers

UI UX Pro Max **MCP server sağlamaz** ama **shadcn/ui MCP** (varsa) ile entegre olur.

---

## Skill Birleştirme — İş Akışı Zincirleri

### Zincir 1: Sıfırdan Landing Page

```
KULLANICI: "Güzellik spa'sı için landing page yap"
         ↓
1. ui-ux-pro-max → search.py "beauty spa wellness" --design-system -p "Spa Adı"
2. design skill (banner gerekirse) → banner-design alt-skill
3. design-system → tokens.css
4. ui-styling → npx shadcn@latest add button card form
5. brand → node scripts/inject-brand-context.cjs --json
6. Final HTML/CSS/TSX
```

### Zincir 2: Tam Marka Kimliği

```
1. brand → docs/brand-guidelines.md oluştur
2. design (logo) → AI logo brief + üretim
3. design-system → token + CSS
4. design (CIP) → 50 teslimat
5. banner-design → Sosyal medya kampanya banner'ları
6. brand → sync-brand-to-tokens.cjs
```

### Zincir 3: Dashboard Tasarımı

```
1. ui-ux-pro-max → search.py "dashboard data analytics" --design-system -p "Adım"
2. design-system → 3-katman token mimarisi
3. ui-styling → npx shadcn add table data-table command
4. design (charts) → search.py "revenue line chart" --domain chart
5. ui-styling → Final React/Next.js kod
```

### Zincir 4: Pitch Deck

```
1. brand → marka kontekst yükle
2. design-system → renk + font tokens
3. slides → "B2B SaaS investor pitch" 12
4. design (CIP) → kapak ve kapanış slaytları
5. Humanizer plugin → metin tonu
```

---

## Referans Veritabanları

### CSV Dosyaları

| CSV | Satır | İçerik |
|-----|-------|--------|
| `products.csv` | 161 | Ürün tipleri (SaaS, e-commerce, fintech, health, ...) |
| `styles.csv` | 67 | UI stilleri + AI image prompt + CSS keywords |
| `colors.csv` | 161 | Renk paletleri (ürün tipine göre) |
| `typography.csv` | 57 | Font eşleşmeleri (Google Fonts import dahil) |
| `icons.csv` | 15 | İkon stilleri |
| `charts.csv` | 25 | Grafik tipleri + kütüphane önerileri |
| `ux-guidelines.csv` | 99 | UX best practice + anti-pattern |
| `ui-reasoning.csv` | 161 | Sektör akıl yürütme kuralları |

### 67 UI Stil Listesi (Öne Çıkanlar)

| Stil | En İyi Kullanım |
|------|----------------|
| **Glassmorphism** | Fintech, premium SaaS |
| **Claymorphism** | Eğlence, çocuk uygulamaları |
| **Minimalism** | Portföy, blog, kurumsal |
| **Brutalism** | Sanat, yaratıcı ajans |
| **Neumorphism** | IoT dashboard, widget |
| **Bento Grid** | Dashboard, portföy |
| **Dark Mode** | Geliştirici araçları, medya |
| **Soft UI Evolution** | Wellness, güzellik, lifestyle |
| **Memphis** | Yaratıcı, retro |
| **Cyberpunk Neon** | Gaming, tech, futurist |
| **Editorial Magazine** | Blog, içerik platformu |
| **Liquid Glass** | Premium fintech, tech |
| **3D Isometric** | SaaS landing, infographic |

(...ve 54 stil daha)

### Banner Boyut Referansı

**Sosyal Medya:**

| Platform | Tür | Boyut |
|----------|-----|-------|
| Facebook | Cover (desktop) | 820×312 |
| Facebook | Event | 1920×1080 |
| Twitter/X | Header | 1500×500 |
| LinkedIn | Şirket cover | 1128×191 |
| LinkedIn | Kişisel banner | 1584×396 |
| YouTube | Channel art | 2560×1440 |
| Instagram | Stories | 1080×1920 |
| Instagram | Post | 1080×1080 |
| Pinterest | Pin | 1000×1500 |

**Web/Display Reklam:**

| Ad | Boyut |
|----|-------|
| Medium Rectangle | 300×250 |
| Leaderboard | 728×90 |
| Wide Skyscraper | 160×600 |
| Half Page | 300×600 |
| Billboard | 970×250 |
| Mobile Banner | 320×50 |

---

## Sorun Giderme

### Python Bulunamıyor

```bash
# Windows
python --version
py --version

# Mac/Linux
which python3
brew install python3
```

### Search.py Encoding Hatası (Windows)

`search.py` zaten UTF-8 fallback yapıyor. Hala hata alıyorsan:

```cmd
chcp 65001
```

### Plugin Yüklenmedi Görünüyor

```bash
/plugin marketplace list
/plugin
/reload-plugins
ls ~/.claude/plugins/cache/ui-ux-pro-max-skill/
```

### CSV Veri Bulunamadı

Sorguyu genişlet:

```bash
python3 search.py "minimalist" --domain style
```

---

## Gerçek Dünya Senaryoları

### Senaryo 1: Solo Kurucu — MVP UI

```
Hafta 1: python3 search.py "<sektör>" --design-system -p "MVP" --persist
Hafta 2: --page "landing" / --page "dashboard" / --page "settings"
Hafta 3: ui-styling skill ile shadcn bileşenleri + tokens.css
Hafta 4: brand skill → sync-brand-to-tokens.cjs
```

### Senaryo 2: Tasarım Ajansı — Yeni Müşteri Onboarding

```
1. python3 search.py "<sektör>" --domain product
2. 3 farklı stil sun (--max-results 3 --domain style)
3. Müşteri seçimi → tam tasarım sistemi (--design-system)
4. Logo → design (logo)
5. CIP → design (CIP) — 50 teslimat
6. Sosyal medya → banner-design + slides
```

### Senaryo 3: Mobil App (Flutter)

```
1. python3 search.py "<sektör>" --stack flutter --design-system
2. python3 search.py "navigation drawer" --stack flutter
3. python3 search.py "dark theme adaptive" --stack flutter
4. python3 search.py "google fonts mobile" --domain typography
```

---

## Bakım & Güncelleme

```bash
/plugin update ui-ux-pro-max@ui-ux-pro-max-skill

npm update -g uipro-cli
uipro init --ai claude
```

### Sürüm Geçmişi

| Sürüm | Önemli Değişiklikler |
|-------|---------------------|
| **2.5.0** | 7 skill, 67 stil, 161 palet, 57 font, 161 sektör kuralı, 16 stack |
| **2.0.0** | Design System Generator (`--design-system` flag), 161 reasoning rules |
| **1.x** | Temel search engine |

---

## Kaynaklar

- **GitHub:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **Site:** https://uupm.cc
- **NPM (CLI):** https://www.npmjs.com/package/uipro-cli
- **Lisans:** MIT

### İlgili Belgeler

- [INDEX.md](INDEX.md) — Tüm plugin'ler ana indeks
- [everything-claude-code-rehber.md](everything-claude-code-rehber.md) — ECC mega-plugin
- [superpowers-rehber.md](superpowers-rehber.md) — Geliştirme metodolojisi
- [humanizer-rehber.md](humanizer-rehber.md) — AI yazı temizleme

---

*Üretilme tarihi: 2026-05-02 | UI UX Pro Max v2.5.0*
