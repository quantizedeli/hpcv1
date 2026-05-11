# Master Skill Guide — Tüm Projeler İçin Otomatik Skill Seçim Rehberi

> **Kapsam:** ECC (182 skill) + superpowers (14 skill) + ui-ux-pro-max (7 skill)  
>            + humanizer + unified-master-controller + ultimate-research-tool  
> **Hedef:** Claude Code'un her görev için doğru skill'i otomatik seçmesi  
> **Son Güncelleme:** 2026-05-06  
> **Konum:** `trading-bot-research/guide/MASTER-SKILL-GUIDE.md`

---

## İçindekiler

1. [Genel Karar Akışı](#genel-karar-akışı)
2. [Görev Kategorisi → Skill Haritası](#görev-kategorisi)
3. [Otomatik Tetikleme Kuralları](#otomatik-tetikleme)
4. [Manuel Tetikleme Gereken Skill'ler](#manuel-tetikleme)
5. [Plugin Çakışma Çözümü — Tiebreaker'lar](#plugin-çakışma)
6. [Model Seçimi Rehberi](#model-seçimi)
7. [Proje Tipine Göre Skill Stack'i](#proje-tipi)
8. [Token & Maliyet Optimizasyonu](#token-maliyet)
9. [Günlük / Haftalık / Aylık Rutin](#rutin)
10. [Bu Projeye Özel Kurallar (Trading Bot)](#trading-bot-özel)

---

## 1. Genel Karar Akışı

```
Görev geldi
    │
    ├─► "araştır/research/akademik/trend" → ultimate-research-tool
    ├─► "BIST/THYAO/KAP/Türkiye finans" → bist-research-intelligence
    ├─► "token/context/compaction/sandbox" → unified-master-controller
    │
    ├─► "yeni özellik/feature" → brainstorming → writing-plans → tdd-workflow
    ├─► "bug/hata/çalışmıyor" → systematic-debugging → tdd-workflow
    ├─► "refactor/temizle" → refactor-clean → tdd-workflow
    │
    ├─► "UI/design/component/layout" → ui-ux-pro-max
    ├─► "yayın/blog/maket/içerik" → article-writing → humanizer
    ├─► "API/endpoint/güvenlik" → security-review
    │
    ├─► "kod inceleme/review" → code-review
    └─► "test/coverage" → test-coverage → tdd-workflow
```

**3 saniye kuralı:** Görevi 3 kelimeyle özetle. O 3 kelime hangi kategoriye giriyor?

---

## 2. Görev Kategorisi → Skill Haritası

### A. Araştırma & Bilgi Edinme

| Görev | Skill | Plugin |
|-------|-------|--------|
| Çok-kaynaklı akademik araştırma (>=10 kaynak) | `ultimate-research-tool` | Bu proje |
| BIST hisse/KAP/Türkiye finans araştırması | `bist-research-intelligence` | Bu proje |
| Hızlı 1-3 kaynak tarama | `deep-research` | ECC |
| Doğrudan Exa API sorgusu | `exa-search` | ECC |
| Pazar araştırması | `market-research` | ECC |
| API/SDK dokümantasyon araması | `documentation-lookup` | ECC |
| Rekabet analizi | `ultimate-research-tool` | Bu proje |
| Son 30 gün trend analizi | `ultimate-research-tool` | Bu proje |

### B. Kod Geliştirme

| Görev | Skill/Agent | Plugin |
|-------|-------------|--------|
| **Brainstorming** (yeni idea → spec) | `brainstorming` | superpowers |
| **Plan yazma** (detaylı) | `writing-plans` | superpowers |
| **Hızlı plan** | `/plan` (ECC komut) | ECC |
| **TDD** (RED→GREEN→REFACTOR) | `test-driven-development` | superpowers |
| **Feature geliştirme** (tam flow) | `feature-dev` | ECC |
| **Bug debug** | `systematic-debugging` | superpowers |
| **Verification** | `verification-before-completion` | superpowers |
| **Code review** | `code-review` | ECC |
| **Security review** | `security-review` | ECC |
| **Quality gate** | `quality-gate` | ECC |
| **Refactor / dead code** | `refactor-clean` | ECC |

### C. Dil Spesifik

| Dil | Reviewer | Build-Fixer | Test |
|-----|----------|-------------|------|
| Python | `python-reviewer` | `build-fix` | `python-testing` |
| TypeScript/JS | `typescript-reviewer` | `build-error-resolver` | ECC test |
| Go | `go-reviewer` | `go-build-resolver` | `golang-testing` |
| Rust | `rust-reviewer` | `rust-build-resolver` | `rust-testing` |
| Java/Spring | `java-reviewer` | `java-build-resolver` | ECC test |
| Flutter/Dart | `flutter-reviewer` | `dart-build-resolver` | `flutter-test` |
| C++ | `cpp-reviewer` | `cpp-build-resolver` | `cpp-testing` |

### D. Frontend & Tasarım

| Görev | Skill | Plugin |
|-------|-------|--------|
| UI bileşen tasarımı | `ui-ux-pro-max` | UIUX |
| Design system | `design-system` | UIUX |
| Brand & marka kimliği | `brand` | UIUX |
| Banner/görsel | `banner-design` | UIUX |
| Sunum/slides | `slides` | UIUX |
| React/Next.js pattern | `frontend-patterns` | ECC |
| Dashboard | `dashboard-builder` | ECC |

### E. İçerik & İletişim

| Görev | Skill | Plugin |
|-------|-------|--------|
| Blog post/artikel | `article-writing` | ECC |
| Sosyal medya içerik | `content-engine` | ECC |
| AI yazı temizleme (genel) | `humanizer` | humanizer |
| Türkçe akademik AI iz temizleme | `academic-shield` | skillv1 |
| Brand voice (yazı sesi) | `brand-voice` | ECC |
| SEO | `seo` | ECC |

### F. Proje Yönetimi & Otomasyon

| Görev | Skill/Araç | Plugin |
|-------|------------|--------|
| GitHub PR pipeline | `prp-prd → prp-plan → prp-implement → prp-pr` | ECC |
| Çoklu ajan paralel | `dispatching-parallel-agents` | superpowers |
| Worktree ile izolasyon | `using-git-worktrees` | superpowers |
| Oturum kaydet | `/save-session` | ECC |
| Oturuma devam | `/resume-session` | ECC |
| Git workflow | `git-workflow` | ECC |

### G. Token & Context Yönetimi

| Görev | Araç | Katman |
|-------|------|--------|
| Shell çıktısı sıkıştır | rtk | L1 |
| Araç çıktısı sandbox | context-mode | L2 |
| Tekrarlı MCP cache | token-optimizer-mcp | L2 |
| Blast radius analizi | code-review-graph | L3a |
| Symbol navigation | token-savior | L3b |
| Token kullanım ölçüm | alexgreensh dashboard | L-M |

---

## 3. Otomatik Tetikleme Kuralları

Claude aşağıdaki ifadeleri gördüğünde **sormadan** ilgili skill'i başlatır:

| İfade / Anahtar Kelime | Otomatik Skill |
|------------------------|----------------|
| "yeni özellik", "feature ekle", "implement" | `brainstorming` → `test-driven-development` |
| "bug", "hata", "çalışmıyor", "broken" | `systematic-debugging` |
| "tamam", "tamamlandı", "düzeltildi", "geçti" | `verification-before-completion` |
| "araştır", "research", "akademik", "literatür" | `ultimate-research-tool` |
| "BIST", "THYAO", "GARAN", "KAP", "hisse" | `bist-research-intelligence` |
| "UI", "design", "component", "layout", "color" | `ui-ux-pro-max` |
| "auth", "security", "API endpoint", "payment" | `security-review` |
| "review", "code review", "incele" | `code-review` |
| "refactor", "temizle", "dead code" | `refactor-clean` |
| "token", "context", "compaction", "sandbox" | `unified-master-controller` |
| "humanize", "AI yazı temizle", "çevirisi kötü" | `humanizer` |
| "tez yaz", "akademik yaz", "ai izi temizle", "dedektörden geç" | `academic-shield` |
| "Python" kod yazma | `python-reviewer` (otomatik sonrası) |
| "test yaz", "coverage", "pytest" | `test-driven-development` |
| "PR", "pull request", "merge" | `git-workflow` → `requesting-code-review` |

**Öncelik sırası:** superpowers process skill'leri > ECC implementation skill'leri  
Çakışmada: superpowers `test-driven-development` > ECC `tdd-workflow`

---

## 4. Manuel Tetikleme Gereken Skill'ler

Bu skill'ler **pahalı**, **özel** veya **kontrol kaybı riski** nedeniyle açık çağrı bekler:

| Skill | Neden Manuel | Çağırma |
|-------|-------------|---------|
| `deep-research` | Maliyetli araç kullanımı | `/skill deep-research` |
| `gan-build`, `gan-design` | Pahalı iterasyon loop'u | `/gan-build` |
| `autonomous-loops` | Kontrol kaybı riski | `/loop-start` |
| `chief-of-staff` | Kişisel iletişim bağlamı | Agent tool |
| `manim-video`, `remotion-*` | Uzun işlem süresi | Açık talep |
| `fal-ai-media` | Üçüncü taraf API maliyeti | Açık talep |
| `opensource-pipeline` | Yayın seviyesi karar | Açık talep |
| `slides` | İnteraktif çıktı | "sunum hazırla" |
| `banner-design` | Tasarım asset üretimi | "banner oluştur" |

---

## 5. Plugin Çakışma Çözümü — Tiebreaker'lar

### TDD Çakışması
- **superpowers `test-driven-development`** > ECC `tdd-workflow`
- Sebep: Daha disiplinli, RED-GREEN-REFACTOR formal kuralı

### Code Reviewer Çakışması
- Subagent çalışması sonrası → **`superpowers:code-reviewer`**
- Genel kod kalitesi → **`everything-claude-code:code-reviewer`**

### Plan Çakışması
- Hızlı (5dk) → ECC `/plan`
- Detaylı görev planı → **`superpowers:writing-plans`**
- Mimari karar → ECC `planner` agent (Opus modeli)

### Research Çakışması
- >=10 kaynak + citation → **`ultimate-research-tool`**
- 1-3 kaynak hızlı → ECC `deep-research`
- BIST/KAP/TR finans → **`bist-research-intelligence`**
- Tek Exa sorgusu → ECC `exa-search`

### Brand Çakışması
- Yazı sesi → ECC `brand-voice`
- Görsel kimlik → UIUX `brand`

### Paralel Agent Çakışması
- Bağımsız görevler → **`superpowers:dispatching-parallel-agents`**
- Ağır codegen loop → ECC `dmux-workflows`

---

## 6. Model Seçimi Rehberi

| Görev | Model | Neden |
|-------|-------|-------|
| Mimari karar, planlama | Opus 4.7 | En derin anlama, karmaşık reasoning |
| Standart kod yazma/review | **Sonnet 4.6** (varsayılan) | Hız+kalite dengesi |
| Docs, format dönüşüm, basit edit | Haiku 4.5 | Hızlı ve ucuz |
| GAN/autonomous loop | Opus (max 5 iter) | Kalite kritik |
| Paralel subagent'lar | Sonnet | Çok sayıda çağrı |
| Bu proje (genel) | **Sonnet 4.6** | Varsayılan |

---

## 7. Proje Tipine Göre Skill Stack'i

### A. Python ML/Data Science Projesi (Bu Proje)
```
Zorunlu: python-reviewer, test-driven-development, verification-before-completion
           systematic-debugging, security-review
Araştırma: ultimate-research-tool (akademik ML), bist-research-intelligence (BIST)
Context: unified-master-controller (büyük kod tabanı)
Raporlama: article-writing + academic-shield (akademik yazı, AI iz temizleme)
```

### B. Web Full-Stack (Next.js + FastAPI)
```
Frontend: ui-ux-pro-max, frontend-patterns, typescript-reviewer
Backend: python-reviewer, database-reviewer, security-review
TDD: test-driven-development, e2e-testing (Playwright)
Deploy: docker-patterns, deployment-patterns
```

### C. Mobile (Flutter/React Native)
```
UI: ui-ux-pro-max (--stack flutter), flutter-reviewer
Build: dart-build-resolver, flutter-build
Test: flutter-test
Patterns: dart-flutter-patterns
```

### D. Akademik Tez / Araştırma
```
Araştırma: ultimate-research-tool (SCOPE→RETRIEVE→SCORE→CRITIQUE→SYNTHESIS)
Yazı: article-writing + academic-shield (AI iz temizleme, SAÜ uyum)
Sıfırdan: academic-shield MOD B (konu → AI izi taşımayan tez bölümü)
Kaynak yönetimi: disk-persisted citations (.research/<topic>/)
Analiz: python-reviewer + pytorch-patterns (model kodu)
```

### E. İçerik & Pazarlama
```
Metin: article-writing, content-engine, brand-voice
Temizlik: humanizer (AI kalıplarını kaldır)
Görsel: banner-design, fal-ai-media
Sunum: slides, investor-materials
SEO: seo
```

---

## 8. Token & Maliyet Optimizasyonu

### Öncelik Sırası
```
1. Görev scope'u daralt → küçük, atomik iş parçaları
2. L1 rtk — shell çıktısı %60-90 küçültür
3. L2 context-mode — araç çıktısı %98 küçültür
4. L3a crg — blast radius → minimal dosya okuma
5. L0 caveman — büyük codegen loop için (manuel açılır)
```

### Kaçın
- ❌ Tüm repo'yu `Glob` + `Read` ile okuma
- ❌ 20+ dosya seri `Read` döngüsü
- ❌ Ham HTML doğrudan context'e (ctx_fetch_and_index kullan)
- ❌ Pahalı skill'ler gereksiz yere (GAN, autonomous-loops)

### Compaction Stratejisi
```
Context > 60% → /compact
Oturum uzadı → /save-session → yeni oturum + /resume-session
Büyük araştırma → .research/ disk'e, context'e özet
```

---

## 9. Günlük / Haftalık / Aylık Rutin

### Günlük Sabah (2 dk)
```bash
/resume-session          # Önceki oturum özeti
rtk gain                 # Dünden devam (varsa)
ctx stats                # Context-mode durumu
```

### Günlük Akşam (2 dk)
```bash
/save-session            # Oturumu kaydet
alexgreensh checkpoint   # Token kullanımı kaydet
```

### Haftalık (15 dk)
```bash
/instinct-status         # Bu hafta öğrenilen kalıplar
/skill-health            # Skill portföy sağlığı
pytest --cov=src         # Coverage kontrolü
```

### Aylık (30 dk)
```bash
claude update            # Claude Code güncelle
/plugin list             # Plugin sürümleri kontrol
/harness-audit           # Harness skoru
/learn-eval              # Bu ay öğrenmeler
/prune                   # Eski instinct'leri temizle
```

---

## 10. Bu Projeye Özel Kurallar (BIST100 Trading Bot)

### Faz 7 (Aktif) — Sektörel Haber Analizi
```
Araştırma flow:
  ultimate-research-tool (global trend) → 
  bist-research-intelligence (THYAO/GARAN implementasyon) →
  python-reviewer (kod kalitesi) →
  test-driven-development (RED→GREEN→REFACTOR)
```

### ML Pipeline
```
Feature engineering: python-reviewer + pytorch-patterns (veya lightgbm patterns)
Backtest: verification-before-completion (kanıt olmadan "geçti" yasak)
Model eğitimi: systematic-debugging (hata durumunda)
```

### KAP Research
```
"THYAO araştır" → bist-research-intelligence (KAP + EODHD + FinanceToolkit)
"Genel piyasa trend" → ultimate-research-tool (global + akademik)
```

### Ticker Formatı
```
yfinance: "AKBNK.IS"
KAP: "AKBNK"
ticker_validator.py otomatik dönüşüm yapar — Manuel dönüştürme
```

### Kritik Kurallar
```
Kill switch bypass edilemez (L1-L4)
SHA256 cache doğrulaması zorunlu
HMM rejim overlay tüm stratejileri etkiler
WINDOWS = {"1H": 5, "1A": 21, "3A": 63, "6A": 126} — değiştirme
```

---

*Master Skill Guide v1.0 | 2026-05-06*  
*ECC 182 skill + superpowers 14 skill + UIUX 7 skill + UMC + URT*
