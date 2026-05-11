# Agent Karar Rehberi — Ne Zaman Hangi Agent?

> Claude Code'daki agent'lar (subagent'lar) isolated context'te çalışır.  
> Ana context'i korur, paralel iş yapabilir, uzmanlaşmış yetenekler sunar.  
> **Son Güncelleme:** 2026-05-06

---

## İçindekiler

1. [Agent vs Skill Farkı](#agent-vs-skill)
2. [Mevcut Tüm Agent'lar](#mevcut-agentlar)
3. [Ne Zaman Agent Kullan?](#ne-zaman-agent)
4. [Agent Seçim Matrisi](#seçim-matrisi)
5. [Paralel Agent Stratejisi](#paralel-strateji)
6. [Agent Çağırma Sözdizimi](#çağırma-sözdizimi)
7. [Bu Projede Agent Kullanım Kalıpları](#proje-kalıpları)
8. [Anti-Pattern'ler](#anti-patterns)

---

## 1. Agent vs Skill Farkı

| Özellik | Skill | Agent (Subagent) |
|---------|-------|------------------|
| Çalışma yeri | Ana context | İzole context |
| Araçlar | Tüm araçlar | Spesifik araçlar |
| Durum | Ana oturumla paylaşımlı | Bağımsız |
| Token etkisi | Ana context'e yazar | Sadece sonuç döner |
| Kullanım | Hafif görevler | Ağır/uzun görevler |
| Paralel | Hayır (sıralı) | Evet (birden fazla) |

**Ne zaman agent kullan:**
- Uzun araştırma (ana context'i şişirmemek için)
- Paralel bağımsız işler
- Uzman görüşü gerektiren isolated review
- Büyük dosya okuma/analiz (context kirletmemek için)

---

## 2. Mevcut Tüm Agent'lar

### Superpowers Agent'ı
| Agent | Çağırma | Ne Yapar |
|-------|---------|---------|
| `superpowers:code-reviewer` | `Agent({subagent_type:"superpowers:code-reviewer"})` | Subagent çalışmasından sonra isolated code review |

### Everything-Claude-Code (ECC) Agent'ları (48 adet)
```
Kod İnceleme:
  code-reviewer          → Genel kod kalitesi
  python-reviewer        → Python spesifik
  typescript-reviewer    → TypeScript/JS
  go-reviewer            → Go
  rust-reviewer          → Rust
  java-reviewer          → Java/Spring
  flutter-reviewer       → Flutter/Dart
  cpp-reviewer           → C++
  csharp-reviewer        → C#
  kotlin-reviewer        → Kotlin/Android
  security-reviewer      → Güvenlik açıkları
  database-reviewer      → SQL/schema
  healthcare-reviewer    → Klinik güvenlik

Build Düzelticiler:
  build-error-resolver   → TypeScript build
  go-build-resolver      → Go build
  rust-build-resolver    → Rust/cargo
  java-build-resolver    → Java/Maven/Gradle
  kotlin-build-resolver  → Kotlin/Gradle
  dart-build-resolver    → Dart/Flutter
  cpp-build-resolver     → C++/CMake
  pytorch-build-resolver → PyTorch/CUDA

Mimari & Planlama:
  architect              → Sistem tasarımı, mimari kararlar
  code-architect         → Feature mimarisi (codebase analizi)
  planner                → Implementasyon planı (Opus modeli)
  a11y-architect         → Erişilebilirlik (WCAG 2.2)

Araştırma:
  code-explorer          → Mevcut feature deep dive
  
Test:
  e2e-runner             → E2E test (Playwright)
  pr-test-analyzer       → PR test coverage

Kalite:
  performance-optimizer  → Bottleneck, bundle size
  refactor-cleaner       → Dead code, duplikasyon
  silent-failure-hunter  → Swallowed errors
  comment-analyzer       → Yorum kalitesi
  type-design-analyzer   → Type design

Özel:
  chief-of-staff         → Çok-kanallı iletişim (email, Slack, LINE)
  gan-evaluator          → GAN harness: test
  gan-generator          → GAN harness: uygulama
  gan-planner            → GAN harness: spec
  loop-operator          → Otonom loop monitörü
  seo-specialist         → Teknik SEO
```

---

## 3. Ne Zaman Agent Kullan?

### Evet, Agent Kullan:
- **Code review:** Her önemli kod değişikliğinden sonra
- **Security review:** Auth, API endpoint, user input kodu sonrası
- **Parallel research:** 3+ bağımsız araştırma sorusu
- **Büyük analiz:** 20+ dosya okuyacaksan (context kirletmemek)
- **Iterative generation:** GAN-style build/evaluate döngüsü
- **PR review:** GitHub PR'ı gözden geçirmek

### Hayır, Direkt Skill Yeterli:
- Tek dosya düzenleme
- Basit soru-cevap
- Küçük bug fix
- Kısa araştırma (1-3 kaynak)
- Config değişikliği

---

## 4. Agent Seçim Matrisi

| Senaryo | Birincil Agent | Yardımcı |
|---------|---------------|---------|
| Python kod review | `python-reviewer` | `security-reviewer` (API kodu ise) |
| TS/JS kod review | `typescript-reviewer` | `security-reviewer` |
| Mimari karar | `architect` (Opus) | `planner` |
| Feature mimarisi | `code-architect` | `planner` |
| Build hatası | `build-error-resolver` (dile göre) | — |
| E2E test | `e2e-runner` | — |
| Performance | `performance-optimizer` | `refactor-cleaner` |
| Güvenlik denetimi | `security-reviewer` | `silent-failure-hunter` |
| PR review (subagent'tan sonra) | `superpowers:code-reviewer` | — |
| PR review (genel) | `everything-claude-code:code-reviewer` | — |
| Yüksek-hacim GAN build | `gan-generator` + `gan-evaluator` | `gan-planner` (başta) |

---

## 5. Paralel Agent Stratejisi

`superpowers:dispatching-parallel-agents` kullan — bağımsız görevler için.

### Ne Zaman Paralel Çalıştır?
```
✅ Bağımsız görevler:
  Agent 1: src/ml/ analiz
  Agent 2: src/sector/ analiz
  Agent 3: tests/ coverage analiz
  → Hepsi paralel → sonuçları birleştir

❌ Bağımlı görevler (SIRAYLA yapılmalı):
  1. Feature A yaz
  2. Feature B (A'ya bağlı)
  → Paralel OLMAZ
```

### Paralel Critique Loop (ultimate-research-tool)
```
Task 1: SKEPTIC persona
Task 2: DOMAIN-EXPERT persona
Task 3: FACT-CHECKER persona
→ Hepsi paralel → verdict birleştir
```

### Paralel Code Review
```
Agent 1: python-reviewer (kod kalitesi)
Agent 2: security-reviewer (güvenlik)
→ Paralel → sonuçlar birleştirilir
```

---

## 6. Agent Çağırma Sözdizimi

```python
# Temel kullanım
Agent({
    subagent_type: "everything-claude-code:python-reviewer",
    description: "Python kod review",
    prompt: """
    Şu dosyayı review et: src/ml/lightgbm_trainer.py
    Context: LightGBM trainer, BIST trading bot projesi
    Odak: type hints, error handling, performance
    """
})

# Arka planda çalıştırma (bağımsız iş)
Agent({
    subagent_type: "everything-claude-code:security-reviewer",
    description: "Security audit",
    prompt: "src/web/app.py FastAPI endpoint'lerini güvenlik açısından incele",
    run_in_background: True  # Ana iş devam eder
})

# Worktree ile izolasyon
Agent({
    subagent_type: "everything-claude-code:code-architect",
    description: "Feature mimarisi",
    prompt: "Sektörel haber analizi feature mimarisi: src/sector/ altında",
    isolation: "worktree"
})

# Haiku ile ucuz görev
Agent({
    subagent_type: "everything-claude-code:comment-analyzer",
    model: "haiku",
    description: "Yorum analizi",
    prompt: "src/sector/ klasörü yorumlarını analiz et"
})
```

---

## 7. Bu Projede Agent Kullanım Kalıpları

### Pattern-1: Python Reviewer Her Commit Sonrası
```python
# src/ değiştirdikten sonra:
Agent({
    subagent_type: "everything-claude-code:python-reviewer",
    prompt: "Şu değişiklikleri review et: [değişen dosyalar listesi]"
})
```

### Pattern-2: Araştırma Critiques (3 Paralel Agent)
```python
# ultimate-research-tool Aşama 4:
# 3 agent paralel başlatılır (aynı message'da)
Agent(skeptic_task)
Agent(expert_task)
Agent(checker_task)
# → hepsi tamamlayınca verdict birleştirilir
```

### Pattern-3: Mimari Karar (Opus ile)
```python
Agent({
    subagent_type: "everything-claude-code:architect",
    model: "opus",  # Karmaşık karar için
    prompt: "EventPatternAgent mimarisi: yeni agent mı, mevcut sector/ modüle entegre mi?"
})
```

### Pattern-4: Build Hatası Düzeltme
```python
# pytest başarısız olunca:
Agent({
    subagent_type: "everything-claude-code:build-error-resolver",
    prompt: "Şu test hataları: [hata çıktısı]. Minimal fix uygula."
})
```

### Pattern-5: Güvenlik + Kalite Paralel
```python
# API endpoint yazıldıktan sonra (paralel):
Agent(security_review_task)    # security-reviewer
Agent(performance_task)         # performance-optimizer
# → iki agent paralel çalışır
```

---

## 8. Anti-Pattern'ler

| Hata | Doğru |
|------|-------|
| Her küçük görev için agent | Küçük görevler → direkt yap |
| Bağımlı görevleri paralel çalıştırma | Sıralı yürüt |
| Agent'a context vermeden gönderme | Proje bağlamını her zaman ekle |
| Tek kod inceleme için iki reviewer | Dile uygun tek reviewer seç |
| Opus'u rutin görevler için kullanma | Opus sadece mimari/planlama |
| Agent sonucunu doğrulamadan kabul etme | verification-before-completion |
| Ana context büyükken agent başlatma | /compact önce, sonra agent |

---

*Agent Decision Guide v1.0 | 2026-05-06*  
*48 ECC agent + 1 superpowers agent = 49 toplam agent*
