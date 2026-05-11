# Skill Combo Zincirleri — Etki Çarpanı Olan Birleşimler

> Tek bir skill iyi, iki skill daha iyi, doğru sırayla üç skill = çarpan etki.  
> Bu dosya sadece **kanıtlanmış** ve **bu projede kullanılan** combo'ları listeler.  
> **Son Güncelleme:** 2026-05-06

---

## İçindekiler

1. [Geliştirme Combo'ları](#geliştirme)
2. [Araştırma Combo'ları](#araştırma)
3. [Review & Kalite Combo'ları](#review-kalite)
4. [İçerik & Dokümantasyon Combo'ları](#içerik)
5. [Bu Projeye Özel Combo'lar (Trading Bot)](#trading-bot)
6. [Anti-Combo'lar — Birlikte Kullanma](#anti-combos)

---

## 1. Geliştirme Combo'ları

### COMBO-D1: Tam Feature Geliştirme (Altın Standart)
```
superpowers:brainstorming
    → superpowers:writing-plans
    → superpowers:using-git-worktrees (izole branch)
    → superpowers:test-driven-development (RED→GREEN→REFACTOR)
    → superpowers:verification-before-completion
    → superpowers:requesting-code-review
    → everything-claude-code:finishing-a-development-branch
```
**Ne zaman:** Yeni bir feature sıfırdan geliştirilirken.  
**Süre:** 30dk - birkaç saat  
**Çıktı:** Clean, test-edilmiş, review-edilmiş kod + PR

### COMBO-D2: Hızlı Bug Fix
```
superpowers:systematic-debugging
    → superpowers:test-driven-development (bug'ı yakalayan RED test)
    → superpowers:verification-before-completion
    → (kritik ise) superpowers:requesting-code-review
```
**Ne zaman:** Bozuk bir şeyi düzeltirken.  
**Süre:** 15-45 dk  
**Çıktı:** Düzeltilmiş kod + bug'ı yakalayan test

### COMBO-D3: Python ML Feature (Bu Proje)
```
superpowers:brainstorming
    → superpowers:writing-plans
    → superpowers:test-driven-development
    → everything-claude-code:python-reviewer
    → superpowers:verification-before-completion
```
**Ne zaman:** src/ml/, src/sector/, src/backtest/ dosyası geliştirirken.  
**Örnek:** "LightGBM'e yeni feature ekle"

### COMBO-D4: Paralel Feature (Birden Fazla Bağımsız Alt Görev)
```
superpowers:brainstorming
    → superpowers:writing-plans
    → superpowers:dispatching-parallel-agents
        ├── Agent 1: Feature A (izole worktree)
        ├── Agent 2: Feature B (izole worktree)
        └── Agent 3: Test yazımı
    → superpowers:verification-before-completion (her agent için)
    → superpowers:requesting-code-review (merge öncesi)
```
**Ne zaman:** Birbirinden bağımsız 2-4 görev aynı anda.  
**Uyarı:** Bağımlı görevleri paralel çalıştırma.

### COMBO-D5: Token-Lean Büyük Refactor
```
unified-master-controller (L3a crg blast radius)
    → superpowers:systematic-debugging (kök neden)
    → superpowers:test-driven-development
    → everything-claude-code:refactor-clean
    → superpowers:verification-before-completion
```
**Ne zaman:** Büyük refactor yapılırken, context yönetimi kritik.

---

## 2. Araştırma Combo'ları

### COMBO-R1: Akademik + Implementasyon
```
ultimate-research-tool
    (SCOPE→RETRIEVE→SCORE→CRITIQUE→SYNTHESIS)
    → everything-claude-code:python-reviewer (bulunan yöntemi uygula)
    → superpowers:test-driven-development (RED→GREEN)
```
**Ne zaman:** "X akademik yöntemini kodla"  
**Örnek:** "Momentum faktörü SOTA araştır → LightGBM'e ekle"

### COMBO-R2: BIST Hisse Araştırma + Sinyal
```
bist-research-intelligence
    (KAP + EODHD + FinanceToolkit + Tavily)
    → src/research/pipeline.py çalıştır
    → src/strategies/ güncelle
    → superpowers:verification-before-completion
```
**Ne zaman:** Belirli bir hisse için araştırma + sinyal güncellemesi.  
**Örnek:** "THYAO araştır, sinyal güncelle"

### COMBO-R3: Trend → Feature → Backtest
```
ultimate-research-tool (son 30 gün trend, global)
    → bist-research-intelligence (Türkiye implementasyon)
    → src/ml/feature_enricher.py güncelle
    → src/backtest/model_backtest.py çalıştır
    → superpowers:verification-before-completion
```
**Ne zaman:** Yeni piyasa trendiyle feature güncelleme.

### COMBO-R4: Karşılaştırmalı Analiz → Karar
```
ultimate-research-tool (X vs Y akademik)
    → superpowers:brainstorming (hangi yaklaşım?)
    → superpowers:writing-plans (implementasyon planı)
    → COMBO-D1 (geliştirme)
```
**Ne zaman:** "LightGBM mi XGBoost mi?" gibi karar noktaları.

---

## 3. Review & Kalite Combo'ları

### COMBO-Q1: Production-Ready Kalite Kapısı
```
everything-claude-code:python-reviewer
    → everything-claude-code:security-review
    → everything-claude-code:quality-gate
    → superpowers:verification-before-completion
```
**Ne zaman:** PR merge öncesi, özellikle API endpoint veya auth kodu.  
**Çıktı:** Temiz, güvenli, production-ready kod

### COMBO-Q2: Tam PR Pipeline
```
everything-claude-code:/prp-prd (PRD oluştur)
    → everything-claude-code:/prp-plan (codebase analizi + plan)
    → everything-claude-code:/prp-implement (uygula)
    → COMBO-Q1 (kalite kapısı)
    → everything-claude-code:/prp-pr (GitHub PR aç)
```
**Ne zaman:** Büyük bir feature için tam PR süreci.

### COMBO-Q3: Test Coverage Artırma
```
everything-claude-code:test-coverage (eksik coverage bul)
    → superpowers:test-driven-development (yeni testler RED→GREEN)
    → superpowers:verification-before-completion (coverage kanıtla)
```
**Ne zaman:** "Coverage %75, %80'e çıkar"

---

## 4. İçerik & Dokümantasyon Combo'ları

### COMBO-C1: Akademik Yazı (Tez Bölümü) — Güncellendi
```
ultimate-research-tool (literatür review)
    → everything-claude-code:article-writing (bölüm taslağı)
    → academic-shield MOD A (AI izi temizle, SAÜ uyumu sağla)
```
**Ne zaman:** Tez veya akademik makale bölümü yazarken.  
**Not:** `humanizer` yerine `academic-shield` — akademik bağlam için derin dönüşüm gerekli.

### COMBO-AC1: Araştırma → Yazma → Kalite Kapısı (Yeni)
```
ultimate-research-tool (kaynak tara)
    → academic-shield MOD B (kaynakla sıfırdan yaz)
    → superpowers:verification-before-completion
```
**Ne zaman:** Elinde kaynaklar var, tez bölümü sıfırdan üreteceksin.

### COMBO-AC2: Sıfırdan Tez Bölümü (Yeni)
```
academic-shield MOD B (konu + argüman → akademik metin)
    → superpowers:requesting-code-review
```
**Ne zaman:** Hızlı bölüm üretimi, kaynaklar verilmiş.

### COMBO-AC3: Mevcut Tez Metnini Kurtarma (Yeni)
```
academic-shield MOD A (mevcut AI metin → dönüştür)
    → GPTZero / QuillBot manuel test
```
**Ne zaman:** Elimdeki metin AI dedektörünü geçemiyor.

### COMBO-C2: Dokümantasyon Güncelleme
```
everything-claude-code:update-codemaps (yapı haritası)
    → everything-claude-code:update-docs (docs güncelle)
    → (gerekirse) everything-claude-code:doc-updater
```
**Ne zaman:** Kod değiştikten sonra docs güncelleme.

---

## 5. Bu Projeye Özel Combo'lar (BIST100 Trading Bot)

### COMBO-T1: Faz 7 — Sektörel Haber Feature
```
ultimate-research-tool (global haber-fiyat ilişki araştırması)
    → superpowers:brainstorming (BIST implementasyon)
    → superpowers:writing-plans
    → superpowers:test-driven-development
        → src/sector/news_retriever.py
        → src/sector/event_embedder.py
        → src/sector/pattern_matcher.py
    → everything-claude-code:python-reviewer
    → superpowers:verification-before-completion
```

### COMBO-T2: LightGBM Feature Engineering
```
ultimate-research-tool ("ML trading feature engineering SOTA")
    → superpowers:writing-plans (hangi feature'lar?)
    → superpowers:test-driven-development
        → tests/test_feature_enricher.py (RED)
        → src/ml/feature_enricher.py (GREEN)
    → src/backtest/model_backtest.py çalıştır (verify)
    → superpowers:verification-before-completion
```

### COMBO-T3: Günlük Sinyal Kontrolü
```
run.py signals çalıştır
    → (signal varsa) bist-research-intelligence (hisse araştır)
    → (karar ver) risk/position_sizing.py kontrol
    → (kaydet) reports/excel/ güncelle
```

### COMBO-T4: WFA Backtest + OOS Test
```
superpowers:brainstorming (hangi strateji testi?)
    → src/backtest/walk_forward.py çalıştır
    → src/backtest/model_backtest.py çalıştır
    → superpowers:verification-before-completion (sonuçları doğrula)
    → BOT_STATUS.md güncelle
```

### COMBO-T5: Bug Fix → Test → Deploy Flow
```
superpowers:systematic-debugging (BUG_TRACKER.md'e bak)
    → superpowers:test-driven-development (failing test)
    → fix uygula
    → pytest çalıştır (TÜM testler)
    → superpowers:verification-before-completion
    → BUG_TRACKER.md güncelle ([FIXED])
    → git commit (conventional: "fix: ...")
```

---

## 6. Anti-Combo'lar — Birlikte Kullanma

Bu kombinasyonlar birlikte çalışmaz veya çakışır:

| Anti-Combo | Neden | Alternatif |
|-----------|-------|-----------|
| `gan-*` + `autonomous-loops` | İç içe pahalı loop, kontrol kaybı | Biri seç |
| `caveman (full+)` + `humanizer` | caveman kısaltır, humanizer insan tonu ekler — çelişki | Ayrı aşamalarda kullan |
| `code-review-graph` + `zilliz` aynı anda | Vector budget overshoot, sync drift | Tek seçim (T-2 kuralı) |
| `context-mode` + `token-optimizer-mcp` aynı tool | Çift cache, manifest overshoot | Tool seviyesinde ayır |
| `deep-research` + `ultimate-research-tool` | Duplikasyon | Biri seç (scope'a göre) |
| `bist-research-intelligence` + `ultimate-research-tool` aynı BIST sorusu | Yanlış scope | BIST → bist-research-intelligence |
| `rtk` + `alexgreensh bash compression` | Çift rewrite, stderr bozulur | TOKEN_OPTIMIZER_BASH_COMPRESS=0 |

---

*Skill Combos v1.0 | 2026-05-06*  
*Kanıtlanmış combo'lar — gözlemlenmiş pattern'lar temelinde*
