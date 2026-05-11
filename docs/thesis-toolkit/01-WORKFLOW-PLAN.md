# 01 — Workflow Plan: Faz Analiz Akışı

> **Amaç:** `quantizedeli/v10` repo'sundaki her fazı tezde kullanılacak seviyede dokümante etmek.

> **Yaklaşım:** Önce repo keşfi (Faz 0), sonra her faz için aynı protokol.

---

## İçindekiler

1. [Süreç Genel Bakış](#süreç-genel-bakış)
2. [Faz 0: Repo Keşfi](#faz-0-repo-keşfi)
3. [Per-Faz Analiz Protokolü](#per-faz-analiz-protokolü)
4. [Skill & Agent Atamaları](#skill--agent-atamaları)
5. [MCP Kullanım Stratejisi](#mcp-kullanım-stratejisi)
6. [Repo Klonlama & Senkronizasyon](#repo-klonlama--senkronizasyon)
7. [Tez Bölümlerine Eşleme](#tez-bölümlerine-eşleme)
8. [Kalite Kapısı](#kalite-kapısı)
9. [Risk & Mitigasyon](#risk--mitigasyon)

---

## Süreç Genel Bakış

```
[REPO]
   ↓
Faz 0: Repo Keşfi
   ↓ (faz listesi belirlenir)
   ↓
Per Faz × N:
   1. Code Inspection (05-CODE-INSPECTION-CHECKLIST.md)
   2. Documentation Generation (03-PHASE-DOC-TEMPLATE.md)
   3. Catalog Update (06 + 07)
   4. Memory MCP Update
   5. Per-faz analiz raporu
   ↓
Final Synthesis
   ↓
Tez Bölüm Taslakları (thesis/)
```

---

## Faz 0: Repo Keşfi

### Amaç

Kod tabanını tanımak ve "faz" yapısını çıkarmak.

### Kontrol Listesi

```
[ ] git clone -b "dev updates" https://github.com/quantizedeli/v10.git repo
[ ] cd repo && git status (branch doğrulaması)
[ ] git log --oneline -20 (son commit'lerin özeti)

[ ] Üst düzey yapı:
    [ ] tree -L 3 -I '__pycache__|*.pyc|venv|.git|node_modules'
    [ ] Ana giriş noktası tespiti (main.py / __main__.py / cli.py / app.py / run.py)
    [ ] Bağımlılık dosyaları (requirements.txt, pyproject.toml, setup.py)
    [ ] Config dosyaları (config.yaml, .env.example, settings.py)
    [ ] Veri dizinleri (data/, datasets/, raw/, processed/)
    [ ] Model dizinleri (models/, checkpoints/, weights/)
    [ ] Test dizinleri (tests/, test_*.py)
    [ ] Notebook'lar (.ipynb dosyaları)
    [ ] Dokümantasyon (docs/, README.md, .md dosyaları)

[ ] Faz tanımlama:
    [ ] "phase" kelimesi geçen dosyalar (grep)
    [ ] Pipeline/workflow yönlendirme (numbered: 01_, 02_, vs.)
    [ ] Modül başlıkları (preprocess, train, evaluate, ...)
    [ ] Sınıf isimleri (Pipeline, Stage, Step, ...)

[ ] Bağımlılık analizi:
    [ ] Hangi major kütüphaneler? (numpy, pandas, torch, sklearn, ...)
    [ ] Hangi nükleer/fizik kütüphaneler? (uproot, ROOT, MCNP wrappers, ...)
    [ ] Hangi veri formatları? (HDF5, ROOT, npz, parquet)

[ ] AI/ML mimarisi (varsa):
    [ ] Hangi model? (CNN, LSTM, Transformer, RF, XGBoost, ...)
    [ ] Hangi framework? (PyTorch, TensorFlow, scikit-learn)
    [ ] Eğitim scripti var mı?
    [ ] Saved checkpoint formatı?

[ ] Veri pipeline:
    [ ] Veri kaynağı (sentetik mi, deneysel mi?)
    [ ] Önişleme adımları
    [ ] Format dönüşümleri
    [ ] Augmentation
```

### Çıktı

- `reports/faz-0-repo-kesfi.md` — tam keşif raporu
- `phases/README.md` — faz indeksi (sonradan dolacak)
- Memory MCP entity: "Thesis Nuclear AI Project" + faz alt-entity'leri
- `07-GLOSSARY-SYMBOLS.md` — repo'da geçen domain-spesifik terimler

### Kullanılacak Skills/Agents

- `code-explorer` agent (sonnet) — execution path + dependency map
- `code-architect` agent (sonnet) — implementation blueprint
- `update-codemaps` skill — token-lean mimari haritası
- `documentation-lookup` skill — kullanılan kütüphanelerin docs'ı
- GitHub MCP — uzaktan repo browsing (alternatif)

---

## Per-Faz Analiz Protokolü

Her faz için aynı 7-adımlı protokol.

### Adım 1: Kapsam Belirleme (5 dk)

```
1.1 Bu fazın .py dosyalarını listele
1.2 Faz girişi/çıkışı (input/output veri akışı)
1.3 Bağımlılıklar:
    - Önceki fazlar (önemli!)
    - Sonraki fazlar (bu fazın çıktısını kim kullanıyor?)
    - Harici kütüphaneler
1.4 Bu faz repo'da hangi modül/klasör?
```

### Adım 2: Kod İncelemesi (15-30 dk)

`05-CODE-INSPECTION-CHECKLIST.md`'deki tam protokolü uygula.

```
2.1 Her .py dosyasını sırayla:
    - Read tool ile tam içerik
    - Üst düzey yapı (sınıflar, fonksiyonlar)
    - Docstring'ler
    - Comment'ler
    - Hardcoded sabitler
    - Hardcoded formüller
    - External dependencies
    - I/O işlemleri (read/write file, network, ...)

2.2 Kalite review:
    - python-reviewer agent → kalite, idiomatic Python
    - comment-analyzer agent → comment kalitesi
    - silent-failure-hunter agent → sessiz hata ihtimalleri
    - type-design-analyzer agent → type tasarımı

2.3 Akademik fact-check:
    - Hangi algoritmalar uygulanmış? (kaynak gerekli)
    - Hangi formüller kullanılmış? (kaynak veya türetim?)
    - Hangi varsayımlar yapılmış? (assumption listesi)
    - Hangi heuristic'ler? (justification var mı?)
```

### Adım 3: Formül & Sembol Çıkarma (10 dk)

```
3.1 Kodda geçen her matematiksel ifadeyi tespit et:
    - np.mean, np.std → istatistiksel formüller
    - hardcoded sabitler (Avogadro, lambda, vb.)
    - Manual hesaplama (loops, vectorized ops)
    - sklearn metric'leri
    - PyTorch loss fonksiyonları

3.2 Her formül için:
    - LaTeX form'u
    - Değişken tanımları
    - Birim (varsa)
    - Kaynak (paper, kitap, türetim)
    - 06-FIGURE-TABLE-CATALOG.md'ye F-NN ID ile ekle

3.3 Her sembol/kısaltma için:
    - Türkçe + İngilizce ad
    - Birim
    - Bağlam (hangi fazda kullanılıyor)
    - 07-GLOSSARY-SYMBOLS.md'ye ekle
```

### Adım 4: Veri Akışı Diyagramı (5 dk)

```
4.1 Bu fazın input → process → output akışını mermaid ile çiz:

flowchart LR
    A[Input: ham veri] --> B[Önişlem]
    B --> C[Faz mantığı]
    C --> D[Output: işlenmiş veri]

4.2 Veri tipleri:
    - Input shape, dtype
    - Output shape, dtype
    - Ara değişken boyutları

4.3 Performans:
    - Hesaplama karmaşıklığı (O notation tahmini)
    - Bellek tüketimi (rough)
    - GPU gerektiriyor mu?
```

### Adım 5: Faz Dokümanı Yazımı (15-20 dk)

`03-PHASE-DOC-TEMPLATE.md`'deki TÜM bölümleri doldur. Atla yapma.

```
phases/faz-N-{kısa-ad}.md oluştur. Şablon başlıkları:

1. Genel Bakış
2. Motivasyon (Niçin bu faz var?)
3. Bağlam (Önceki/sonraki fazlar)
4. Girdi/Çıktı Spec'i
5. Yöntem (Nasıl yapıyor?)
6. Algoritmalar (varsa pseudocode)
7. Formüller (LaTeX, numaralı)
8. Değişkenler & Parametreler (tablo)
9. Kısaltmalar & Semboller (bu fazda kullanılan)
10. Uygulama Detayları (ana .py dosyaları, sınıflar, fonksiyonlar)
11. Hesaplama Karmaşıklığı
12. Doğrulama & Test (varsa)
13. Sınırlamalar
14. Sonuçlar (varsa metrik, çıktı örneği)
15. Tezdeki Yeri (hangi bölüm/alt-bölüm)
16. Kaynaklar (atıflar)
17. Açık Sorular
```

### Adım 6: Doğrulama (5 dk)

```
6.1 verification-before-completion skill devreye gir:
    - Tüm template bölümleri dolu mu?
    - Tüm formüller LaTeX ile mi?
    - Her sembol 07'de tanımlı mı?
    - Cross-reference linkler doğru mu?
    - Atıflar var mı (yoksa açık soru olarak işaretle)?

6.2 Akademik kalite:
    - "Muhtemelen" gibi belirsiz ifade var mı?
    - Atıfsız iddia var mı?
    - Türkçe yazım/dilbilgisi temiz mi?
```

### Adım 7: Kayıt & Geçiş (3 dk)

```
7.1 reports/faz-N-analiz-notu.md
    - Bu fazda ne yapıldı?
    - Hangi sorularla karşılaştın?
    - Sonraki faz için notlar

7.2 Memory MCP güncelle:
    - Faz entity'sine yeni observation
    - İlişkili sınıf/fonksiyon entity'leri
    - Faz-faz relation'ları

7.3 phases/README.md'yi güncelle:
    - Faz N tamamlandı işareti
    - Doc dosya linki

7.4 /save-session "Faz N tamamlandı"

7.5 Bana özet rapor ver:
    - Faz adı, ana bulgular
    - 06 ve 07'ye eklenen
    - Açık soruların listesi
    - Sonraki faz önerisi
```

---

## Skill & Agent Atamaları

### Per-Faz Standart Aktivasyon

| Skill / Agent | Adım | Plugin | Amaç |
|---------------|------|--------|------|
| `code-explorer` (sonnet) | 1, 2 | ECC | Execution path, dependency map |
| `code-architect` (sonnet) | 2 | ECC | Implementation blueprint |
| `python-reviewer` (sonnet) | 2 | ECC | Kod kalitesi review |
| `python-patterns` skill | 2 | ECC | Idiomatic Python kontrolü |
| `comment-analyzer` (sonnet) | 2 | ECC | Comment doğruluğu |
| `silent-failure-hunter` (sonnet) | 2 | ECC | Sessiz hata tespiti |
| `type-design-analyzer` (sonnet) | 2 | ECC | Type tasarım |
| `documentation-lookup` skill | 1, 2, 3 | ECC | Context7 ile kütüphane docs |
| `pytorch-patterns` skill | 2, 6 | ECC | PyTorch kullanılıyorsa |
| `eval-harness` skill | 6 | ECC | Eval framework varsa |
| `update-codemaps` skill | 5 | ECC | Mimari haritası |
| `update-docs` skill | 5 | ECC | Doküman üretimi |
| `verification-before-completion` | 6 | superpowers | Kalite kapısı |
| `article-writing` skill | 5, Final | ECC | Akademik prose |
| `humanizer` skill | Final (sadece) | humanizer | Tonu insanlaştır (akademik kor) |

### Manuel Çağrı (Faz-Spesifik)

| Faz Tipi | Ek Skill / Agent |
|----------|------------------|
| Veri önişleme | `python-patterns`, `database-reviewer` (DB varsa) |
| ML model eğitimi | `pytorch-patterns`, `ai-regression-testing`, `eval-harness` |
| Görselleştirme | `dashboard-builder`, `frontend-patterns` |
| API/Web | `backend-patterns`, `api-design`, `mcp-server-patterns` |
| Test | `tdd-workflow`, `e2e-testing`, `pr-test-analyzer` |
| Performans | `performance-optimizer` |
| Güvenlik | `security-review`, `security-reviewer` |

### Skip — Bu Projede KULLANMA

| Skill / Agent | Sebep |
|---------------|-------|
| `brainstorming` (superpowers) | Plan zaten yazılı |
| `writing-plans` (superpowers) | Plan zaten yazılı |
| `gan-*` (ECC) | Loop pahalı, ihtiyaç yok |
| `chief-of-staff` (ECC) | İletişim spesifik |
| `banner-design`, `slides` (UIUX) | Tezde gerekirse manuel |
| `humanizer` her metinde | Akademik ton tehlikeli — sadece final pass |

---

## MCP Kullanım Stratejisi

| MCP | Adım | Kullanım |
|-----|------|----------|
| **GitHub MCP** | 0 | Repo browsing, commit history, issues |
| **Context7** | 0, 2, 3 | Kütüphane docs (numpy, torch, sklearn, ...) |
| **Exa** | 3, 6 | Algoritma kaynak doğrulama, paper araması |
| **Firecrawl** | 3 | Spesifik blog/dokümantasyon scrape |
| **Memory** | 0, 7 | Bilgi grafiği — fazlar arası ilişki |
| **Sequential Thinking** | 2, 5 | Karmaşık akıl yürütme |
| **Playwright** | (varsa) | Web tabanlı sonuç doğrulama |

### Token Bütçesi

- Faz başına ~300K token tavanı
- Toplam ~3M token (10 faz tahminiyle)
- `strategic-compact` her 100K'da kontrol
- Subagent kullan (isolated context = tasarruf)

---

## Repo Klonlama & Senkronizasyon

### İlk Klonlama

```bash
cd /c/Users/Hakan\ Yakut/Desktop/ahmet/skillv1/thesis-nuclear-ai
git clone -b "dev updates" https://github.com/quantizedeli/v10.git repo
cd repo
git status  # Branch doğrulama
git log --oneline -10  # Son commit'ler
```

### Sonraki Senkronizasyon (Yeni Commit Geldi)

```bash
cd repo
git fetch origin
git status  # Local değiştirilmemiş mi?
git pull origin "dev updates"
```

### Etkilenmiş Faz Tespiti

Bir senkronizasyon sonrası hangi fazın yeniden analiz edilmesi gerek?

```bash
cd repo
git log --oneline HEAD@{1}..HEAD  # Son pull'da gelen commit'ler
git diff --stat HEAD@{1}..HEAD    # Değişen dosya listesi
```

Değişen dosyaları faz dosyalarına eşle (phases/README.md ile cross-check).

---

## Tez Bölümlerine Eşleme

```
TEZ BÖLÜMÜ                  →  FAZLAR
─────────────────────────────────────────────────────
1. Giriş                    →  (faz dışı: literatür + amaç)
2. Yöntem                   →  Tüm fazlar (toplu)
   2.1 Veri Toplama         →  Faz 1 (varsayım)
   2.2 Önişleme             →  Faz 2-3
   2.3 Model Mimarisi       →  Faz 4-5
   2.4 Eğitim Stratejisi    →  Faz 6
   2.5 Değerlendirme        →  Faz 7
3. Bulgular                 →  Faz çıktıları + metrikler
4. Tartışma                 →  Cross-faz analiz
5. Sonuç                    →  Final synthesis
```

> **Not:** Gerçek faz sayısı/isimleri Faz 0'dan sonra kesinleşir.

---

## Kalite Kapısı

Her faz dokümanı için:

- [ ] `03-PHASE-DOC-TEMPLATE.md`'deki tüm 17 bölüm dolu
- [ ] Formüller LaTeX ile yazılmış
- [ ] Her formül `06-FIGURE-TABLE-CATALOG.md`'de F-NN ID'siyle var
- [ ] Her kısaltma/sembol `07-GLOSSARY-SYMBOLS.md`'de tanımlı
- [ ] Kod referansları satır numaralı (`src/foo.py:42`)
- [ ] Mermaid akış diyagramı var
- [ ] Akademik dil — "muhtemelen" yok
- [ ] Atıfsız iddia yok (yoksa "Açık Sorular" bölümünde işaretli)
- [ ] Tezdeki yer belirtilmiş (hangi bölüm/alt-bölüm)
- [ ] Memory MCP entity güncel
- [ ] reports/faz-N-analiz-notu.md yazılmış

---

## Risk & Mitigasyon

| Risk | Etki | Mitigasyon |
|------|------|-----------|
| Repo'da "faz" yapısı belirsiz | Faz tanımı yanlış olur | Faz 0'da kullanıcıyla mutabakat, plan onayı al |
| Kod yorumsuz/docstring'siz | Bağlam çıkarmak zor | comment-analyzer + Context7 + kullanıcıya sor |
| Hardcoded sabit kaynaksız | Tezde kaynak eksik | exa-search ile arşa, "Açık Sorular"a not |
| Branch güncellenir araştırma sırasında | Doc demode olur | Pull öncesi snapshot al, etkilenmiş fazları işaretle |
| Karmaşık model (transformer vs.) tam anlamak zor | Yanlış doc | pytorch-patterns + Context7 + paper kaynak |
| Veri formatı egzotik (ROOT, HDF5) | Pipeline anlaşılmaz | Format spec'i ayrı bölümde anlat |
| Türkçe terminoloji eksik | Akademik dil zayıf | 07-GLOSSARY ile TR-EN eşle |
| Token patlaması | Faz yarım kalır | strategic-compact + faz-bazlı session |

---

*Workflow Plan v1.0 | 2026-05-02*
