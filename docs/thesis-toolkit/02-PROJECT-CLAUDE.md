# 02 — PROJECT-CLAUDE.md (Thesis Nuclear AI)

> **Aktivasyon:**
> ```bash
> cd thesis-nuclear-ai/
> cp 02-PROJECT-CLAUDE.md CLAUDE.md
> ```

---

## Proje Kimliği

**Proje:** PhD Tezi — Yapay Zeka Destekli Nükleer Veri Analizi  
**Repo:** https://github.com/quantizedeli/v10 (branch: `dev updates`)  
**Yerel kopya:** `./repo/`  
**Aşama:** Code Analysis → Documentation → Thesis Writing  
**Hedef çıktı:** Per-faz `.md` dokümanları + tez bölüm taslakları  
**Dil:** Türkçe (akademik) — İngilizce sadece açıkça istendiğinde  
**Geliştirici:** Hakan Yakut

---

## Skill Tetikleme Tercihleri

### Otomatik Aktif

| Skill / Agent | Plugin | Sebep |
|---------------|--------|-------|
| `code-explorer` | ECC | Repo execution path |
| `code-architect` | ECC | Mimari blueprint |
| `python-reviewer` | ECC | Kod review |
| `python-patterns` | ECC | Idiomatic Python |
| `comment-analyzer` | ECC | Comment kalitesi |
| `silent-failure-hunter` | ECC | Sessiz hata |
| `documentation-lookup` | ECC | Context7 docs |
| `update-codemaps` | ECC | Mimari haritası |
| `update-docs` | ECC | Doküman üretimi |
| `verification-before-completion` | superpowers | Kanıtla |

### Faz-Spesifik

| Tetik | Skill |
|-------|-------|
| PyTorch tespit | `pytorch-patterns`, `ai-regression-testing` |
| Eğitim/eval | `eval-harness` |
| DB | `database-reviewer` |
| API/Web | `backend-patterns`, `api-design` |
| Test suite | `tdd-workflow`, `pr-test-analyzer` |
| Performans | `performance-optimizer` |

### Skip

| Skill | Sebep |
|-------|-------|
| `brainstorming` | Plan yazılı |
| `writing-plans` | Plan yazılı |
| `gan-*` | Gereksiz |
| `chief-of-staff` | Spesifik değil |
| `banner-design`, `slides` | Manuel |
| `humanizer` her metinde | Akademik ton tehlikeli — sadece final |

---

## MCP Kullanım

| MCP | Sıklık | Kullanım |
|-----|--------|----------|
| Memory | Her oturum | Knowledge graph |
| Context7 | Sık | Kütüphane docs |
| Exa | Faz başına | Paper kaynak |
| GitHub | Faz 0 | Repo browsing |
| Sequential Thinking | Karmaşık | Akıl yürütme |
| Firecrawl | Nadir | Web kaynak |

**Token bütçesi:** Faz başına ~300K, `strategic-compact` her 100K'da.

---

## Akademik Disiplin

### Yasaklı İfadeler

❌ "Muhtemelen", "Genelde", "Düşünüyorum ki"
❌ "Bu kütüphane harika"
❌ "İnsanlar şunu kullanıyor"
❌ "Çok iyi sonuçlar" (metrik göstermeden)
❌ "State-of-the-art" (atıfsız)

### Tercih Edilen

✅ "X kaynağına göre..." [atıf]
✅ "Kod satırında [src/foo.py:42] şu hesaplanır..."
✅ "Algoritma şu şekilde uygulanmıştır..."
✅ "%Z performans, ölçüm: ..."

### Türkçe Akademik Stil

- 3. tekil şahıs ("uygulanmıştır", "hesaplanır")
- Pasif yapı kabul
- Yabancı terimler ilk geçişte parantezli Türkçe karşılık
- Kısaltma ilk geçişte tam ad + parantez

**Örnek:**
> "Konvolüsyonel Sinir Ağı (Convolutional Neural Network — CNN), gama enerji spektrumlarındaki örüntüleri öğrenmek için kullanılmıştır."

---

## Doküman Yazma Kuralları

### Her Faz Dokümanı

1. `03-PHASE-DOC-TEMPLATE.md`'deki **17 bölümü eksiksiz**
2. Bilgi yoksa "Açık Sorular" bölümüne yaz, atla yapma
3. Formüller LaTeX
4. `06-FIGURE-TABLE-CATALOG.md`'ye F-NN ID
5. `07-GLOSSARY-SYMBOLS.md`'ye kısaltma/sembol
6. Kod referansı: `src/path/file.py:42`
7. Akış diyagramları mermaid

### Dosya İsimlendirme

- `phases/faz-NN-{kebab-case}.md` (örn: `faz-01-veri-yukleme.md`)
- `reports/faz-NN-analiz-notu.md`
- `thesis/0N-bolum-adi.md` (örn: `thesis/02-yontem.md`)

### ID Sistemi

- Formül: `F-NNN`
- Şekil: `S-NNN`
- Tablo: `T-NNN`
- Algoritma: `A-NNN`
- Kod referansı: `C-NNN`

### Cross-Reference

- `Bkz. F-005`
- `Bkz. faz-03-onisleme.md`
- `Bkz. 07-GLOSSARY-SYMBOLS.md#cnn`

---

## Asla Yapma

### Akademik Dürüstlük

❌ Hayal kütüphane, fonksiyon, paper
❌ Atıfsız algoritma
❌ Repo'da olmayan metrik tezde
❌ Plagiarism

### Teknik Disiplin

❌ Çalışmayan örnek kod
❌ Kod ile uyuşmayan formül
❌ Birimsiz sayısal değer
❌ Kod-doc çelişkisi

### Faz Yönetimi

❌ Faz atlama (0→1→2 sırası)
❌ Plan dışı dalma
❌ Yarım dokümante
❌ Memory MCP boş bırakma

### Repo

❌ Gerçek API key/secret
❌ Kullanıcı verisi (sentetik kullan)
❌ Yanlış branch (`dev updates` zorunlu)

---

## Çakışma Çözücü

```
1. Kullanıcı açık talimatı
2. PROJECT-CLAUDE.md (bu dosya)
3. ~/.claude/CLAUDE.md (global)
4. Plugin varsayılanları
```

### Repo'nun Kendi CLAUDE.md'si Varsa

Eğer `repo/CLAUDE.md` varsa:
- Referans olarak oku
- **Bu dosya kuralları geçerli**
- Çakışma → "Açık Sorular"a yaz, sor

### Plan vs Spontane

Plan dışı bulgu çıkarsa:
1. "Açık Sorular"a ekle
2. Plan'a sadık kal
3. Faz sonunda kullanıcıya öner

---

## Faz Geçişi Kontrol Listesi

- [ ] `phases/faz-N-*.md` 17 bölüm dolu
- [ ] `06-FIGURE-TABLE-CATALOG.md` güncel
- [ ] `07-GLOSSARY-SYMBOLS.md` güncel
- [ ] Memory MCP entity + relation
- [ ] `phases/README.md` güncel
- [ ] `reports/faz-N-analiz-notu.md` yazıldı
- [ ] Açık sorular kullanıcıya iletildi
- [ ] `/save-session "Faz N tamamlandı"`

---

## Devam Eden Oturum Şablonu

```
[YENİ OTURUM — Thesis Tez Asistanı, Faz N]

1. Bu klasördeki dosyaları oku:
   - 02-PROJECT-CLAUDE.md
   - 01-WORKFLOW-PLAN.md
   - 03-PHASE-DOC-TEMPLATE.md
   - phases/README.md
   - reports/faz-(N-1)-analiz-notu.md

2. 06-FIGURE-TABLE-CATALOG.md ve 07-GLOSSARY-SYMBOLS.md tara

3. Memory MCP sorgula:
   mcp__memory__search_nodes "Thesis Nuclear AI Project"

4. Faz N kapsamı: phases/README.md'den

5. Bana özet ver: önceki + bu faz + sıra

6. ONAY BEKLE
```

---

## Acil Komutlar

| Durum | Komut |
|-------|-------|
| Yan soru | `/aside` |
| Checkpoint | `/checkpoint create "açıklama"` |
| Oturum kaydet | `/save-session "Faz N — durum"` |
| Önceki oturum | `/resume-session` |
| Token sıkıntısı | `/skill strategic-compact` |
| Repo update | `cd repo && git pull origin "dev updates"` |

---

## Dış Kaynak Politikası

### İzinli (Akademik)

✅ arXiv, SSRN, DOI'li peer-reviewed
✅ Resmi kütüphane docs
✅ Üniversite tez arşivleri
✅ Akademik konferans yayınları

### Dikkatli

⚠️ Wikipedia (sadece başlangıç)
⚠️ Medium / blog
⚠️ Stack Overflow (akademik atıf değil)

### Yasaklı

❌ Atıfsız "trust me" siteleri
❌ Predatory journal
❌ AI-üretimi şüpheli kaynak
❌ Wikipedia'dan doğrudan tezde atıf

---

## Final Synthesis Hedefi

Tüm fazlar bitince:

1. `reports/00-FINAL-SYNTHESIS.md` — bütünleşik özet
2. `thesis/` taslakları:
   - `00-icindekiler.md`
   - `01-giris.md`
   - `02-yontem.md`
   - `03-bulgular.md`
   - `04-tartisma.md`
   - `05-sonuc.md`
3. `thesis/kaynakca.md` (BibTeX dostu)

---

*Thesis Nuclear AI Project — PROJECT-CLAUDE.md v1.0 | 2026-05-02*
