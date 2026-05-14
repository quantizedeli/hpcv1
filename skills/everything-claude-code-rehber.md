# Everything Claude Code (ECC) — Tam Kapsamlı Rehber

> **Sürüm:** 2.0.0-rc.1 | **Lisans:** MIT  
> **Yazar:** Affaan Mustafa ([@affaanmustafa](https://x.com/affaanmustafa))  
> **Kaynak:** https://github.com/affaan-m/everything-claude-code  
> **Site:** https://ecc.tools  
> **Son Güncelleme:** 2026-05-01

---

## İçindekiler

1. [Hızlı Başlangıç Kartı](#hızlı-başlangıç-kartı)
2. [Plugin Anatomisi](#plugin-anatomisi)
3. [Kurulum](#kurulum)
4. [Slash Komutları Tam Referansı (68 komut)](#slash-komutları-tam-referansı)
5. [Skills — Tam Katalog (182 skill)](#skills--tam-katalog)
6. [Agents — Tam Liste (48 agent)](#agents--tam-liste)
7. [Hooks Sistemi](#hooks-sistemi)
8. [Scripts & CLI Tools](#scripts--cli-tools)
9. [Config Dosyaları](#config-dosyaları)
10. [MCP Servers Entegrasyonu](#mcp-servers-entegrasyonu)
11. [Skill Birleştirme — İş Akışı Zincirleri](#skill-birleştirme--iş-akışı-zincirleri)
12. [Sorun Giderme](#sorun-giderme)
13. [Gerçek Dünya Senaryoları](#gerçek-dünya-senaryoları)
14. [Bakım & Güncelleme](#bakım--güncelleme)
15. [Kaynaklar](#kaynaklar)

---

## Hızlı Başlangıç Kartı

```bash
# 30 saniyede aktif:
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
/reload-plugins

# İlk komutun:
/plan "yeni bir özellik düşünüyorum"
```

**Ne sunar:**
- 182 otomatik skill — kod, araştırma, içerik, medya, sektörel uzmanlık
- 48 özel agent — kod review, mimari, güvenlik, dil-spesifik
- 68 slash komutu — TDD, plan, gan-loop, prp-pipeline, harness audit
- Üretim seviyesinde hooks — pre-Bash güvenlik, kalite kapısı, GateGuard

---

## Plugin Anatomisi

```
everything-claude-code/2.0.0-rc.1/
├── .claude-plugin/
│   ├── plugin.json              ← Plugin manifest (version, description)
│   ├── marketplace.json         ← Marketplace yapılandırması
│   ├── PLUGIN_SCHEMA_NOTES.md   ← Manifest validatör notları
│   └── README.md
├── agents/                      ← 48 agent .md dosyası
├── commands/                    ← 68 slash komut .md dosyası
├── skills/                      ← 182 skill klasörü (her birinde SKILL.md)
├── hooks/
│   ├── hooks.json               ← Hook konfigürasyonu (PreToolUse, PostToolUse)
│   └── README.md
├── scripts/                     ← Hook bootstrap, dispatcher, lib/
│   ├── hooks/
│   │   ├── plugin-hook-bootstrap.js
│   │   ├── pre-bash-dispatcher.js
│   │   └── ...
│   └── lib/utils.js
├── schemas/
│   └── hooks.schema.json        ← JSON şema doğrulaması
├── .claude/
│   ├── ecc-tools.json           ← ECC tool kayıtları
│   ├── identity.json            ← Plugin kimliği
│   ├── package-manager.json     ← Tercih edilen package manager
│   ├── enterprise/controls.md   ← Kurumsal yönetim
│   ├── research/                ← Araştırma playbook'ları
│   └── rules/                   ← Korkuluklar (guardrails)
├── .codex/                      ← Codex CLI entegrasyonu
├── .codex-plugin/               ← Codex plugin yapılandırması
├── .codebuddy/                  ← CodeBuddy IDE adapter
├── .cursor/
│   ├── hooks.json               ← Cursor için hooks
│   └── rules/                   ← Cursor için kurallar
└── .kiro/agents/                ← Kiro IDE adapter
```

---

## Kurulum

### Yöntem 1: Plugin Marketplace (Önerilen)

```bash
# Sürüm kontrolü (v1.0.33+ gerekli)
claude --version

# Marketplace ekle
/plugin marketplace add affaan-m/everything-claude-code

# Plugin'i kur
/plugin install everything-claude-code@everything-claude-code

# Aktif et
/reload-plugins
```

### Yöntem 2: Manuel Klonlama

```bash
git clone https://github.com/affaan-m/everything-claude-code ~/.claude/plugins/everything-claude-code
/reload-plugins
```

### Bağımlılıklar

| Bileşen | Gereksinim | Neden |
|---------|------------|-------|
| Claude Code | v1.0.33+ | `/plugin` komutu için |
| Node.js | v18+ | Hook script'leri için |
| Git | herhangi bir sürüm | Repo işlemleri için |
| (Opsiyonel) MCP servers | Context7, Exa, GitHub | Belirli skill'ler için |

### Doğrulama

```bash
# Plugin'in yüklendiğini doğrula
/plugin

# Tanı kontrolü
claude /doctor

# Belirli bir skill'in aktif olduğunu test et
/code-review
```

### Kaldırma

```bash
/plugin uninstall everything-claude-code@everything-claude-code

# veya manuel:
rm -rf ~/.claude/plugins/cache/everything-claude-code
```

### Özel Endpoint Yapılandırması

ECC, Claude Code'un transport ayarlarını geçersiz kılmaz:

```bash
export ANTHROPIC_BASE_URL=https://your-gateway.example.com
export ANTHROPIC_AUTH_TOKEN=your-token
claude
```

---

## Slash Komutları Tam Referansı

Aşağıdaki **68 komut** doğrudan kullanılabilir. Her komut `commands/<ad>.md` dosyasında tanımlıdır.

### Plan & İmplementasyon İş Akışı

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/plan` | - | Gereksinimleri yeniden ifade et, riskleri değerlendir, adım adım plan oluştur. Kod yazmadan ÖNCE kullanıcı onayını bekler. |
| `/feature-dev` | - | Codebase anlayışı ve mimari odak ile rehberli feature geliştirme. |
| `/multi-plan` | - | Çoklu model paralel planlama (production kodunu modifiye etmez). |
| `/multi-execute` | - | Multi-model implementation planını çalıştır. Filesystem'a yalnızca Claude yazar. |
| `/multi-workflow` | - | Tam multi-model: araştırma + plan + uygulama + optimizasyon + review. |
| `/multi-frontend` | - | Component, layout, animasyon, UI polish için frontend-odaklı multi-model. |
| `/multi-backend` | - | API, algoritma, veri, business logic için backend-odaklı multi-model. |

### PRP (Project Requirements Pipeline) Komutları

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/prp-prd` | - | İnteraktif PRD üretimi — problem-first, hipotez-driven |
| `/prp-plan` | - | Codebase analizi ve pattern çıkarımı ile feature planı |
| `/prp-implement` | - | Plan'ı titiz validation döngüleriyle uygula |
| `/prp-pr` | - | Mevcut branch'ten GitHub PR oluştur (template + analiz + push) |
| `/prp-commit` | - | Doğal dilli dosya targeting ile hızlı commit |

### Code Review

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/code-review` | `[pr-number\|pr-url]` veya boş | Local değişiklik review veya GitHub PR review |
| `/review-pr` | - | Çoklu uzman agent ile kapsamlı PR review |
| `/santa-loop` | - | Adversarial dual-review convergence — iki bağımsız reviewer onayı zorunlu |

### Build & Test (Dile Göre)

| Komut | Dil | Açıklama |
|-------|-----|----------|
| `/build-fix` | otomatik tespit | Build sistemini tespit et, build/type hatalarını çöz |
| `/cpp-build` | C++ | CMake/linker hatalarını cpp-build-resolver ile çöz |
| `/cpp-review` | C++ | Memory safety, modern C++, concurrency, security review |
| `/cpp-test` | C++ | GoogleTest TDD; gcov/lcov coverage |
| `/flutter-build` | Dart/Flutter | dart-build-resolver ile minimum cerrahi düzeltme |
| `/flutter-review` | Dart/Flutter | Widget, state management, performance, a11y |
| `/flutter-test` | Dart/Flutter | Unit + widget + golden + integration test |
| `/go-build` | Go | go-build-resolver, go vet, linter |
| `/go-review` | Go | Idiomatic Go, concurrency, error handling |
| `/go-test` | Go | Table-driven test, %80+ coverage |
| `/gradle-build` | Gradle | Android, KMP build hataları |
| `/kotlin-build` | Kotlin | kotlin-build-resolver, dependency çözümleme |
| `/kotlin-review` | Kotlin | Idiomatic patterns, null safety, coroutine safety |
| `/kotlin-test` | Kotlin | Kotest TDD, %80+ coverage (Kover) |
| `/python-review` | Python | PEP 8, type hints, security, idiomatic |
| `/rust-build` | Rust | rust-build-resolver, borrow checker, Cargo.toml |
| `/rust-review` | Rust | Ownership, lifetime, unsafe usage, idiomatic |
| `/rust-test` | Rust | TDD, %80+ coverage (cargo-llvm-cov) |
| `/test-coverage` | hepsi | Coverage gap analizi + eksik test üretimi |
| `/quality-gate` | - | ECC kalite pipeline'ını çalıştır + remediation adımları |

### Refactor & Bakım

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/refactor-clean` | - | Dead code'u güvenli tespit et ve sil (her değişiklikten sonra doğrula) |
| `/update-codemaps` | - | Proje yapısını tara, token-lean mimari codemap'i üret |
| `/update-docs` | - | Source-of-truth dosyalardan dokümantasyonu senkronize et |
| `/setup-pm` | - | npm/pnpm/yarn/bun arasında package manager seçimi |
| `/pm2` | - | Tespit edilen frontend/backend/db için PM2 service komutları üret |

### Hookify (Davranış Otomasyonu)

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/hookify` | - | Konuşma analizinden veya talimattan istenmeyen davranışı engelleyen hook üret |
| `/hookify-list` | - | Tüm yapılandırılmış hookify kurallarını listele |
| `/hookify-configure` | - | Hookify kurallarını interaktif olarak aç/kapa |
| `/hookify-help` | - | Hookify sistemiyle ilgili yardım |

### GAN (Generator-Adversarial-Network) İş Akışı

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/gan-build` | - | Generator/evaluator implementation döngüsü, sınırlı iterasyon ve skor |
| `/gan-design` | - | Frontend/visual için generator/evaluator döngüsü |

### Otonom Loop'lar

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/loop-start` | - | Yönetilen otonom loop başlat (güvenlik varsayılanları + açık dur koşulları) |
| `/loop-status` | - | Aktif loop durumunu, ilerlemesini, hata sinyallerini incele |

### Öğrenme & Instinct

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/learn` | - | Mevcut oturumdan yeniden kullanılabilir kalıp çıkar |
| `/learn-eval` | - | Kalıp çıkar, kaliteyi self-eval et, doğru lokasyona kaydet (Global vs Project) |
| `/instinct-export` | `<file>` | Instinct'leri dosyaya aktar |
| `/instinct-import` | `<file\|url>` | Instinct'leri içeri al |
| `/instinct-status` | - | Öğrenilmiş instinct'leri ve confidence değerlerini göster |
| `/projects` | - | Bilinen projeleri ve instinct istatistiklerini listele |
| `/promote` | - | Project-scoped instinct'i global'e yükselt |
| `/prune` | - | 30 günden eski promote edilmemiş pending instinct'leri sil |

### Skill Yönetimi

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/skill-create` | - | Local git geçmişinden kalıp çıkar, SKILL.md üret |
| `/skill-health` | - | Skill portföy sağlık dashboard'u (chart + analitik) |
| `/evolve` | - | Instinct'leri analiz et, evolve edilmiş yapılar öner |

### Session Yönetimi

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/save-session` | - | Mevcut oturumu `~/.claude/session-data/` altında dated dosyaya kaydet |
| `/resume-session` | - | En son session'ı yükle ve tam context ile devam et |
| `/sessions` | - | Session geçmişi, alias, metadata yönetimi |
| `/checkpoint` | `[create\|verify\|list] [name]` | Workflow checkpoint oluştur, doğrula veya listele |
| `/aside` | - | Mevcut görevi kesmeden hızlı yan soruyu cevapla, sonra devam et |
| `/auto-update` | - | ECC repo'sunu güncelle ve managed target'ları yeniden yükle |

### Diğer

| Komut | Argüman | Açıklama |
|-------|---------|----------|
| `/jira` | `<ticket-id>` | Jira ticket al, gereksinimleri analiz et, durum güncelle, yorum ekle |
| `/harness-audit` | - | Deterministik harness audit, prioritized scorecard döndür |
| `/model-route` | - | Görev karmaşıklık, risk, bütçeye göre model seçimi öner |
| `/add-language-rules` | `<dil>` | Yeni programlama dili için kurallar ekle |
| `/database-migration` | - | Database schema migration dosyaları oluştur |

---

## Skills — Tam Katalog

ECC içinde **182 skill** vardır. Aşağıda kategorize edilmiş tam liste; her skill'in adı `skills/<ad>/SKILL.md` dosyasıyla tanımlıdır.

### 📋 Skill Çağırma Mekanizması

ECC skill'leri **iki şekilde** tetiklenir:
1. **Otomatik** — Skill'in `description` alanındaki anahtar kelimeler kullanıcı mesajında geçtiğinde
2. **Manuel** — `/skill <skill-name>` komutu (varsayılan tetikleyici)

### 1) 🛠️ Geliştirici Temel Skill'leri (15 skill)

| Skill | Ne Yapar |
|-------|----------|
| `coding-standards` | Evrensel kod standartları (naming, immutability, code-quality) |
| `tdd-workflow` | RED-GREEN-REFACTOR, %80+ coverage, unit/integration/E2E |
| `verification-loop` | Build + test + lint + typecheck + security döngüsü |
| `security-review` | Auth, user input, secret, API, payment için güvenlik kontrolü |
| `e2e-testing` | Playwright Page Object Model, CI/CD, flaky test |
| `eval-harness` | Eval-Driven Development (EDD) çerçevesi |
| `agent-introspection-debugging` | Agent failure debug — capture, diagnosis, recovery |
| `agent-sort` | Repo'ya göre ECC bileşenlerini DAILY vs LIBRARY sınıflandır |
| `strategic-compact` | Manuel context compaction (görev fazlarına göre) |
| `code-tour` | Codebase'de adım adım gezinti |
| `codebase-onboarding` | Yeni projeye dahil olma rehberliği |
| `repo-scan` | Hızlı repo taraması, kalıp çıkarımı |
| `rules-distill` | Repo geçmişinden kuralları çıkarma |
| `quality-nonconformance` | Kalite uyumsuzluk tespit ve raporlama |

### 2) 🎨 Frontend & UI (12 skill)

| Skill | Ne Yapar |
|-------|----------|
| `frontend-patterns` | React, Next.js, state management, performance |
| `nextjs-turbopack` | Next.js 16+, Turbopack, incremental bundling |
| `frontend-slides` | Animasyonlu HTML sunum, PPTX→Web dönüşümü |
| `bun-runtime` | Bun runtime, package manager, bundler, test runner |
| `dashboard-builder` | Dashboard oluşturma kalıpları |
| `liquid-glass-design` | Glassmorphism varyantı tasarım |
| `ui-demo` | UI demo oluşturma |
| `compose-multiplatform-patterns` | Compose Multiplatform |
| `dart-flutter-patterns` | Dart/Flutter best practices |
| `swiftui-patterns` | SwiftUI mimarisi ve kalıpları |
| `swift-actor-persistence` | Swift Actor + persistence |
| `swift-concurrency-6-2` | Swift 6.2 concurrency |

### 3) 🔧 Backend & API (15 skill)

| Skill | Ne Yapar |
|-------|----------|
| `backend-patterns` | Node.js, Express, Next.js API routes mimari kalıpları |
| `api-design` | REST API tasarım: naming, status code, pagination, versioning, rate limiting |
| `api-connector-builder` | API connector geliştirme |
| `mcp-server-patterns` | TypeScript/Node.js ile MCP sunucu — tool, resource, prompt, Zod |
| `nodejs-keccak256` | Node.js ile Keccak256 hash |
| `python-patterns` | Python kalıpları |
| `python-testing` | Python test stratejileri |
| `golang-patterns` | Go kalıpları |
| `golang-testing` | Go test stratejileri |
| `nestjs-patterns` | NestJS mimarisi |
| `springboot-patterns` | Spring Boot kalıpları |
| `springboot-security` | Spring Security |
| `springboot-tdd` | Spring Boot TDD |
| `springboot-verification` | Spring Boot doğrulama |
| `laravel-patterns` | Laravel kalıpları |

### 4) 🧬 Veritabanı & Migration (5 skill)

| Skill | Ne Yapar |
|-------|----------|
| `database-migrations` | DB schema değişiklikleri, migration dosyaları |
| `postgres-patterns` | PostgreSQL en iyi uygulamaları |
| `clickhouse-io` | ClickHouse I/O kalıpları |
| `jpa-patterns` | JPA persistence kalıpları |
| `kotlin-exposed-patterns` | Kotlin Exposed ORM |

### 5) 📦 DevOps & Deployment (8 skill)

| Skill | Ne Yapar |
|-------|----------|
| `deployment-patterns` | Deployment kalıpları |
| `docker-patterns` | Dockerfile, compose en iyi uygulamaları |
| `git-workflow` | Branch, merge, rebase iş akışları |
| `github-ops` | GitHub PR/issue/release yönetimi |
| `automation-audit-ops` | Otomasyon audit operasyonları |
| `enterprise-agent-ops` | Kurumsal agent operasyonları |
| `gateguard` | Pre-commit / pre-push gate sistemleri |
| `canary-watch` | Canary release izleme |

### 6) 🔍 Araştırma & Bilgi (8 skill)

| Skill | Ne Yapar |
|-------|----------|
| `exa-search` | Exa MCP üzerinden neural web araması |
| `deep-research` | Firecrawl + Exa ile çoklu kaynak derin araştırma |
| `documentation-lookup` | Context7 MCP ile güncel kütüphane dokümantasyonu |
| `market-research` | Pazar araştırması, rekabet analizi |
| `iterative-retrieval` | Yinelemeli bilgi çekme |
| `search-first` | "Önce ara" disiplini |
| `research-ops` | Araştırma operasyonları |
| `lead-intelligence` | Lead intel toplama |

### 7) 📝 İçerik Üretimi (8 skill)

| Skill | Ne Yapar |
|-------|----------|
| `article-writing` | Makale, blog, tutorial, newsletter |
| `brand-voice` | Verilmiş yazılardan marka sesi profili çıkar |
| `content-engine` | X, LinkedIn, TikTok, YouTube, newsletter için platform-spesifik içerik |
| `crosspost` | X, LinkedIn, Threads, Bluesky'a uyarlanmış paylaşım |
| `x-api` | X/Twitter API entegrasyonu (OAuth, rate limit) |
| `seo` | SEO optimizasyonu |
| `videodb` | Video veritabanı yönetimi |
| `manim-video` | Manim ile matematiksel video |

### 8) 💼 Yatırımcı & İş (4 skill)

| Skill | Ne Yapar |
|-------|----------|
| `investor-materials` | Pitch deck, one-pager, memo, finansal model |
| `investor-outreach` | Cold email, intro blurb, follow-up |
| `product-capability` | PRD'yi capability planına çevir |
| `product-lens` | Ürün bakış açısı analizi |

### 9) 🎬 Medya & Yaratıcı (4 skill)

| Skill | Ne Yapar |
|-------|----------|
| `fal-ai-media` | fal.ai MCP ile görsel/video/ses üretimi |
| `video-editing` | FFmpeg, Remotion, ElevenLabs pipeline |
| `remotion-video-creation` | Remotion ile programatik video |
| `gan-style-harness` | GAN style harness |

### 10) 🤖 Agent & Otomasyon (15 skill)

| Skill | Ne Yapar |
|-------|----------|
| `agent-eval` | Agent değerlendirme harness |
| `agent-harness-construction` | Agent harness inşa |
| `agent-payment-x402` | x402 protokolü ile agent ödeme |
| `agentic-engineering` | Agentic engineering ilkeleri |
| `ai-first-engineering` | AI-first engineering yaklaşımı |
| `autonomous-agent-harness` | Otonom agent harness |
| `autonomous-loops` | Otonom loop kalıpları |
| `continuous-agent-loop` | Sürekli agent loop |
| `dmux-workflows` | dmux ile multi-agent orkestrasyon |
| `loop-operator` | Loop operatörü |
| `nanoclaw-repl` | Nanoclaw REPL |
| `openclaw-persona-forge` | Persona forge |
| `claude-devfleet` | Claude dev fleet |
| `team-builder` | Agent ekibi inşa |
| `enterprise-agent-ops` | Kurumsal agent ops |

### 11) 🧠 LLM & AI Geliştirme (8 skill)

| Skill | Ne Yapar |
|-------|----------|
| `ai-regression-testing` | AI regresyon testi |
| `cost-aware-llm-pipeline` | Maliyet bilinçli LLM pipeline |
| `prompt-optimizer` | Prompt optimizasyonu |
| `llm-trading-agent-security` | LLM trading agent güvenliği |
| `regex-vs-llm-structured-text` | Regex vs LLM seçimi |
| `foundation-models-on-device` | On-device foundation model |
| `pytorch-patterns` | PyTorch kalıpları |
| `safety-guard` | Güvenlik koruması |

### 12) 🔒 Güvenlik & Compliance (10 skill)

| Skill | Ne Yapar |
|-------|----------|
| `security-bounty-hunter` | Security bug bounty |
| `security-scan` | Güvenlik taraması |
| `defi-amm-security` | DeFi AMM güvenliği |
| `evm-token-decimals` | EVM token decimals |
| `hipaa-compliance` | HIPAA uyumluluğu |
| `healthcare-phi-compliance` | PHI compliance |
| `customs-trade-compliance` | Gümrük & ticaret uyumluluğu |
| `django-security` | Django güvenliği |
| `laravel-security` | Laravel güvenliği |
| `perl-security` | Perl güvenliği |

### 13) 🏥 Sağlık (3 skill)

| Skill | Ne Yapar |
|-------|----------|
| `healthcare-cdss-patterns` | Klinik karar destek sistemleri |
| `healthcare-emr-patterns` | EMR/EHR kalıpları |
| `healthcare-eval-harness` | Sağlık eval harness |

### 14) 🛒 İş & Ops (12 skill)

| Skill | Ne Yapar |
|-------|----------|
| `customer-billing-ops` | Müşteri faturalama |
| `email-ops` | E-posta operasyonları |
| `finance-billing-ops` | Finans faturalama |
| `google-workspace-ops` | Google Workspace |
| `inventory-demand-planning` | Envanter & talep planlama |
| `knowledge-ops` | Bilgi operasyonları |
| `logistics-exception-management` | Lojistik istisna yönetimi |
| `messages-ops` | Mesaj operasyonları |
| `production-scheduling` | Üretim planlama |
| `project-flow-ops` | Proje akış ops |
| `returns-reverse-logistics` | İade & ters lojistik |
| `unified-notifications-ops` | Birleşik bildirim ops |

### 15) 🏗️ Mimari (8 skill)

| Skill | Ne Yapar |
|-------|----------|
| `architecture-decision-records` | ADR yazımı |
| `hexagonal-architecture` | Hexagonal mimari |
| `android-clean-architecture` | Android Clean Architecture |
| `blueprint` | Mimari blueprint |
| `code-architect` | Kod mimarı |
| `connections-optimizer` | Bağlantı optimizasyonu |
| `social-graph-ranker` | Sosyal graph sıralayıcı |
| `data-scraper-agent` | Veri scraper agent |

### 16) 🎯 Skill Meta (4 skill)

| Skill | Ne Yapar |
|-------|----------|
| `skill-comply` | Skill uyumluluğu |
| `skill-stocktake` | Skill envanteri |
| `configure-ecc` | ECC yapılandırma |
| `everything-claude-code` | Plugin'in kendisini yöneten skill |

### 17) 🔬 Diğer Spesifik (~43 skill)

Diğer spesifik skill'ler şunları kapsar: `accessibility`, `benchmark`, `browser-qa`, `carrier-relationship-management`, `ck`, `click-path-audit`, `compose-multiplatform-patterns`, `content-hash-cache-pattern`, `context-budget`, `continuous-learning`, `continuous-learning-v2`, `council`, `cpp-coding-standards`, `cpp-testing`, `csharp-testing`, `django-patterns`, `django-tdd`, `django-verification`, `dotnet-patterns`, `ecc-tools-cost-audit`, `energy-procurement`, `flutter-dart-code-review`, `hermes-imports`, `hookify-rules`, `java-coding-standards`, `jira-integration`, `kotlin-coroutines-flows`, `kotlin-ktor-patterns`, `kotlin-patterns`, `kotlin-testing`, `laravel-plugin-discovery`, `laravel-tdd`, `laravel-verification`, `nutrient-document-processing`, `nuxt4-patterns`, `opensource-pipeline`, `perl-patterns`, `perl-testing`, `plankton-code-quality`, `production-scheduling`, `ralphinho-rfc-pipeline`, `rust-patterns`, `rust-testing`, `santa-method`, `terminal-ops`, `token-budget-advisor`, `visa-doc-translate`, `workspace-surface-audit`, `connections-optimizer`.

### Önemli Skill'lerin Detaylı Profilleri

#### `tdd-workflow` (Detaylı)

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "yeni özellik", "bug fix", "refactor" — otomatik |
| **Ne Zaman Kullan** | Yeni feature, bug fix, refactor |
| **Ne Zaman KULLANMA** | Sadece dokümantasyon, salt-okunur araştırma |
| **Yetenekler** | RED-GREEN-REFACTOR, %80+ coverage, unit/integration/E2E |
| **Bağımlılıklar (önceki)** | `coding-standards`, `verification-loop` |
| **Bağımlılıklar (sonraki)** | `code-reviewer` agent |
| **Reference dosyaları** | `skills/tdd-workflow/SKILL.md` |
| **Çıktı formatı** | Test dosyaları + implementation + coverage raporu |
| **Anti-pattern** | Test'siz prod kodu, geç yazılmış test |

#### `security-review` (Detaylı)

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "auth", "user input", "secret", "API endpoint", "payment", "encryption" — otomatik |
| **Ne Zaman Kullan** | Auth ekleme, kullanıcı girdisi işleme, sensitive feature |
| **Ne Zaman KULLANMA** | Sadece UI styling, salt-okunur kod |
| **Yetenekler** | OWASP Top 10, secrets detection, SSRF, injection, unsafe crypto |
| **Bağımlılıklar (sonraki)** | `security-reviewer` agent |
| **Reference** | `skills/security-review/SKILL.md` |
| **Çıktı formatı** | Sorun listesi (Critical/Important/Suggestion) + remediation |
| **Anti-pattern** | Hardcoded secret, eval(), unsanitized SQL |

#### `dmux-workflows` (Detaylı)

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "paralel agent", "multi-agent", "tmux" |
| **Ne Zaman Kullan** | Birden fazla bağımsız görev paralel çalışacaksa |
| **Yetenekler** | tmux pane manager ile Claude Code, Codex, OpenCode paralel orkestrasyon |
| **Reference** | `skills/dmux-workflows/SKILL.md` |
| **Anti-pattern** | İnterconnected görevler, ortak dosya editleyen ajanlar |

---

## Agents — Tam Liste

ECC **48 agent** sağlar. Hepsi `Task` tool aracılığıyla çağrılır.

### Agent Çağırma Sözdizimi

```python
# Otomatik (PROACTIVE):
# Agent description'ı eşleşen tetikleyici görüldüğünde Claude otomatik çağırır

# Manuel:
Agent({
  description: "Kısa görev tanımı",
  subagent_type: "agent-name",
  prompt: "Detaylı görev brief'i"
})
```

### 1) 📋 Plan & Mimari

| Agent | Model | Tools | Açıklama |
|-------|-------|-------|----------|
| `planner` | opus | Read, Grep, Glob | Karmaşık feature ve refactor için kapsamlı plan |
| `architect` | opus | Read, Grep, Glob | Sistem tasarımı, ölçeklenebilirlik, teknik kararlar |
| `code-architect` | sonnet | Read, Grep, Glob | Mevcut codebase analiziyle implementation blueprint |
| `code-explorer` | sonnet | Read, Grep, Glob | Execution path izleme, mimari katman haritalaması |
| `chief-of-staff` | opus | Read, Grep, Glob, Bash, Edit, Write | Email, Slack, LINE, Messenger triage |

### 2) 🔍 Code Review

| Agent | Model | Açıklama |
|-------|-------|----------|
| `code-reviewer` | sonnet | Genel code review (proactive) |
| `code-simplifier` | sonnet | Kodu netlik için sadeleştir |
| `comment-analyzer` | sonnet | Comment kalitesi ve rot risk |
| `database-reviewer` | sonnet | PostgreSQL: query opt, schema, security |
| `pr-test-analyzer` | sonnet | PR test coverage kalitesi |
| `silent-failure-hunter` | sonnet | Sessiz hata, swallowed error tespiti |
| `type-design-analyzer` | sonnet | Type encapsulation, invariant tasarımı |

### 3) 🔒 Güvenlik & Sağlık

| Agent | Model | Açıklama |
|-------|-------|----------|
| `security-reviewer` | sonnet | OWASP Top 10, secrets, SSRF, injection |
| `healthcare-reviewer` | opus | CDSS doğruluk, PHI compliance, EMR güvenliği |
| `a11y-architect` | sonnet+opus | WCAG 2.2 erişilebilirlik |

### 4) 🏗️ Build & Test (Dile Göre)

| Agent | Dil | Açıklama |
|-------|-----|----------|
| `build-error-resolver` | TypeScript | Build/type hata cerrahi düzeltmesi |
| `cpp-build-resolver` | C++ | CMake, linker, template hatası |
| `dart-build-resolver` | Dart/Flutter | dart analyze, pub dependency |
| `go-build-resolver` | Go | go build, vet, linter |
| `java-build-resolver` | Java | Maven/Gradle build |
| `kotlin-build-resolver` | Kotlin | Gradle, Kotlin compiler |
| `pytorch-build-resolver` | PyTorch | Tensor shape, CUDA, gradient |
| `rust-build-resolver` | Rust | cargo build, borrow checker |
| `e2e-runner` | hepsi | Playwright/Vercel Agent Browser ile E2E |

### 5) 🌐 Dil-Spesifik Reviewer'lar

| Agent | Dil |
|-------|-----|
| `cpp-reviewer` | C++ — memory safety, modern C++ |
| `csharp-reviewer` | C# — .NET, async, nullable |
| `flutter-reviewer` | Flutter — widget, state, performance |
| `go-reviewer` | Go — idiomatic, concurrency |
| `java-reviewer` | Java/Spring — layered, JPA, security |
| `kotlin-reviewer` | Kotlin — coroutine, Compose |
| `python-reviewer` | Python — PEP 8, idiomatic |
| `rust-reviewer` | Rust — ownership, lifetime |
| `typescript-reviewer` | TypeScript — type safety, async |

### 6) 🛠️ Bakım

| Agent | Açıklama |
|-------|----------|
| `refactor-cleaner` | Dead code, knip, depcheck |
| `tdd-guide` | TDD enforcement |
| `doc-updater` (haiku) | /update-codemaps + /update-docs |
| `docs-lookup` | Context7 ile güncel docs |
| `performance-optimizer` | Bottleneck, bundle size, response time |

### 7) 🤖 Otonom & GAN

| Agent | Açıklama |
|-------|----------|
| `loop-operator` | Otonom loop monitoring + müdahale |
| `harness-optimizer` | Local agent harness reliability + cost |
| `gan-planner` | GAN spec'i tam product specification'a açar |
| `gan-generator` | GAN feature implementer |
| `gan-evaluator` | Live app'i Playwright ile test edip skor verir |

### 8) 📤 Open Source

| Agent | Açıklama |
|-------|----------|
| `opensource-forker` | Sanitize edilmiş fork (20+ secret pattern strip) |
| `opensource-packager` | Tam OSS packaging (CLAUDE.md, setup.sh, README, LICENSE) |
| `opensource-sanitizer` | Yayın öncesi son sanitize verification |

### 9) 🧠 Analiz

| Agent | Açıklama |
|-------|----------|
| `seo-specialist` | Teknik SEO, structured data, Core Web Vitals |
| `conversation-analyzer` | Konuşma transkriptlerinden hookable davranış çıkar |

---

## Hooks Sistemi

ECC, Claude Code'un hook sistemini güçlü şekilde kullanır. `hooks/hooks.json` içinde tanımlı.

### Hook Eventleri ve Dispatcher'lar

| Event | Matcher | Dispatcher | Etki |
|-------|---------|------------|------|
| **PreToolUse** | `Bash` | `pre-bash-dispatcher.js` | Kalite, tmux, push, GateGuard kontrolleri |
| **PreToolUse** | `Write` | (Write dispatcher) | Yazılacak dosya kalite kontrolü |
| **PostToolUse** | (varsa) | (post dispatcher) | Otomatik hook tetikleme sonrası |
| **SessionStart** | (varsa) | Plugin context inject | Plugin context'inin yüklenmesi |

### pre-bash-dispatcher.js Görevleri

1. **Quality Check** — Bash komutu kalite kurallarını ihlal ediyor mu?
2. **Tmux Check** — Tmux içinde çalışıyor mu, pane çakışması var mı?
3. **Push Check** — `git push` zorla/main'e mi yapılıyor?
4. **GateGuard Check** — `/quality-gate` öncesi kontroller geçti mi?

### Hook Bootstrap Mekanizması

ECC, plugin path'ini farklı kurulum yollarından otomatik tespit eder:

```javascript
// Aranan yollar:
~/.claude/plugins/ecc/
~/.claude/plugins/ecc@ecc/
~/.claude/plugins/marketplace/ecc/
~/.claude/plugins/everything-claude-code/
~/.claude/plugins/cache/<plugin>/<sub>/<version>/
```

`CLAUDE_PLUGIN_ROOT` env variable set edilirse o öncelikli kullanılır.

### Hookify Sistemi

`/hookify` komutu, kullanıcı davranış kalıbını engelleyen otomatik hook üretir:

```bash
/hookify "TS dosyalarını silmeden önce her zaman onay iste"
# → conversation-analyzer agent çağrılır
# → Yeni hook üretilir
# → settings.json'a eklenir
```

`/hookify-list` ile mevcut hook'ları gör; `/hookify-configure` ile aç/kapa.

---

## Scripts & CLI Tools

### Hook Script'leri (`scripts/hooks/`)

| Script | Görev |
|--------|-------|
| `plugin-hook-bootstrap.js` | Hook altyapı bootstrap |
| `pre-bash-dispatcher.js` | Bash öncesi konsolide kontroller |
| (diğer dispatcher'lar) | Write, PostToolUse, SessionStart |

### Lib (`scripts/lib/`)

| Modül | Görev |
|-------|-------|
| `utils.js` | Plugin path tespiti, ortak yardımcılar |

---

## Config Dosyaları

### `plugin.json` (Yapı)

```json
{
  "name": "everything-claude-code",
  "version": "2.0.0-rc.1",
  "description": "Battle-tested Claude Code plugin...",
  "author": { "name": "Affaan Mustafa" },
  "homepage": "https://ecc.tools",
  "repository": "https://github.com/affaan-m/everything-claude-code",
  "license": "MIT",
  "keywords": ["claude-code", "agents", "skills", "hooks"],
  "mcpServers": {},
  "skills": ["./skills/"],
  "commands": ["./commands/"]
}
```

### `.claude/ecc-tools.json` (Tool Kayıtları)

```json
{
  "version": "1.3",
  "schemaVersion": "1.0",
  "profiles": {
    "requested": "full",
    "recommended": "full",
    "effective": "full"
  },
  "tier": "enterprise",
  "selectedComponents": [
    "repo-baseline",
    "workflow-automation",
    "security-audits",
    "research-tooling",
    "team-rollout",
    "governance-controls"
  ]
}
```

### Profil Sistemi

| Tier | Erişim |
|------|--------|
| `free` | Temel skill ve komutlar |
| `pro` | + Multi-model, GAN, Continuous loop |
| `enterprise` | + Governance, audit, suppression yönetimi |

---

## MCP Servers Entegrasyonu

ECC MCP server'ları **kendisi sağlamaz**, mevcut MCP setup'ını kullanır. Önerilen MCP'ler:

| MCP | Sağladığı | Kullanan Skill |
|-----|----------|----------------|
| **Exa** | Neural web search, code search, company research | `exa-search`, `deep-research`, `lead-intelligence` |
| **Context7** | Güncel kütüphane dokümantasyonu | `documentation-lookup`, `docs-lookup` agent |
| **Firecrawl** | Web crawl + içerik çıkarma | `deep-research`, `data-scraper-agent` |
| **GitHub** | Repo, PR, issue yönetimi | `github-ops`, `code-review` |
| **Memory** | Oturumlar arası bellek | `continuous-learning`, `instinct-*` |
| **Playwright** | Browser otomasyonu | `e2e-testing`, `e2e-runner` agent, `browser-qa` |
| **Sequential Thinking** | Adım adım mantık yürütme | `agentic-engineering`, plan komutları |
| **Supabase** | DB sorgu | `database-migrations`, `postgres-patterns` |
| **fal.ai** | AI media (görsel, video, ses) | `fal-ai-media`, `video-editing` |

---

## Skill Birleştirme — İş Akışı Zincirleri

### Zincir 1: Yeni Feature (TDD + Review)

```
1. /plan "kullanıcı kayıt"                       → planner agent
2. tdd-workflow skill (otomatik)                  → RED test
3. tdd-workflow skill                             → GREEN implementation
4. tdd-workflow skill                             → REFACTOR
5. /code-review                                   → code-reviewer agent
6. /security-review                               → security-reviewer agent
7. verification-loop skill (otomatik)             → Build + lint + test
8. /quality-gate                                  → ECC kalite pipeline
9. /prp-pr                                        → GitHub PR
```

### Zincir 2: Bug Fix (Sistematik Debug)

```
1. /aside "bu hata neden çıkıyor?"                → Hızlı analiz
2. tdd-workflow → failing test                    → Bug'ı yakalayan test
3. (bug fix)
4. verification-loop → tüm testleri çalıştır
5. /code-review
6. /prp-commit "bug X fixed"
```

### Zincir 3: GAN Loop (Adversarial)

```
1. gan-planner → spec
2. gan-generator → implementation
3. gan-evaluator → live test + skor
4. (skor düşükse → 2'ye dön, max 5 iter)
5. /santa-loop → iki bağımsız reviewer onayı
```

### Zincir 4: Open Source Yayın

```
1. opensource-forker → secret strip + sanitize
2. opensource-packager → CLAUDE.md, setup.sh, README, LICENSE
3. opensource-sanitizer → final sanitize verification
4. /prp-pr → upstream'e PR (yeni repo)
```

---

## Sorun Giderme

### Plugin Kurulum Hataları

**Sorun:** `/plugin marketplace add` SSH hatası verir.

**Çözüm:** Marketplace ekleme için Owner/Repo formatı (HTTPS clone yapar). SSH URL kullanma.

```bash
# Doğru:
/plugin marketplace add affaan-m/everything-claude-code

# Yanlış:
/plugin marketplace add git@github.com:affaan-m/everything-claude-code.git
```

### Agent Çağrı Hataları

**Sorun:** `Agent type 'code-reviewer' not found`

**Çözüm:** ECC ve superpowers'da aynı isim var. Plugin prefix'i ekle:

```python
Agent({
  subagent_type: "everything-claude-code:code-reviewer",
  ...
})
```

---

## Gerçek Dünya Senaryoları

### Senaryo 1: Solo Geliştirici — Yeni SaaS Ürünü

```
Hafta 1: /prp-prd → İnteraktif PRD
Hafta 1: /prp-plan → Codebase analizi + plan
Hafta 2-4: /prp-implement → Validation loop'larıyla uygulama
Her gün: /code-review + /security-review
Her commit öncesi: /quality-gate
Yayın öncesi: /santa-loop → dual reviewer
Yayın: /prp-pr → GitHub PR
```

### Senaryo 2: Pazarlama İçeriği

```
1. brand-voice → ses profili çıkar
2. content-engine → X, LinkedIn, newsletter için içerik
3. crosspost → platform-spesifik adapt
4. /humanizer → AI kalıplarını temizle (Humanizer plugin)
```

---

## Bakım & Güncelleme

### Güncelleme

```bash
# Otomatik
/auto-update

# Manuel
cd ~/.claude/plugins/cache/everything-claude-code/everything-claude-code
git pull
/reload-plugins
```

### Sürüm Geçmişi

| Sürüm | Tarih | Önemli Değişiklikler |
|-------|-------|---------------------|
| 2.0.0-rc.1 | 2026 | 182 skill, 48 agent, 68 komut, hookify, GAN loop |
| 1.x | 2025 | İlk kararlı seri |

---

## Kaynaklar

- **GitHub Repo:** https://github.com/affaan-m/everything-claude-code
- **Site:** https://ecc.tools
- **Yazar:** [@affaanmustafa](https://x.com/affaanmustafa)
- **Lisans:** MIT

### İlgili Belgeler (Aynı Klasörde)

- [INDEX.md](INDEX.md) — Tüm plugin'ler için ana indeks
- [superpowers-rehber.md](superpowers-rehber.md) — Yazılım geliştirme metodolojisi
- [ui-ux-pro-max-rehber.md](ui-ux-pro-max-rehber.md) — UI/UX tasarım zekası
- [humanizer-rehber.md](humanizer-rehber.md) — AI yazı temizleme
- [academic-shield-rehber.md](academic-shield-rehber.md) — Türkçe akademik yazı & AI iz temizleme

---

*Üretilme tarihi: 2026-05-01 | ECC v2.0.0-rc.1*
