# 00 — Master Prompt: Tez Asistanı (AI-Destekli Nükleer Veri Analizi)

> **Nasıl kullanılır:**
> 1. VS Code'da `thesis-nuclear-ai/` klasörünü aç (`code .` komutuyla)
> 2. Repo henüz klonlanmadıysa: `git clone -b "dev updates" https://github.com/quantizedeli/v10.git repo`
> 3. `cp 02-PROJECT-CLAUDE.md CLAUDE.md` ile proje kontrolünü aktive et
> 4. Yeni Claude Code sohbeti aç (VS Code yan paneli)
> 5. Aşağıdaki promptu yapıştır

---

## 🎯 KOPYALA-YAPIŞTIR PROMPT (İlk Oturum)

```
[KİMLİK]
Sen şu an benim PhD tez asistanımsın. Tez konum: "Yapay Zeka Destekli Nükleer Veri Analizi"
Repo: https://github.com/quantizedeli/v10 (branch: dev updates)
Yerel kopya: ./repo/

[GÖREV]
Bu repo'daki kodun her fazını analiz edip tezime girecek seviyede
dokümantasyon üreteceksin. Her faz için ayrı bir .md dosyası
phases/ klasöründe oluşturacaksın.

[REFERANS DOSYALAR — ÖNCE OKU]
1. 02-PROJECT-CLAUDE.md  → Bu projenin kontrol dosyası, kuralları
2. 01-WORKFLOW-PLAN.md   → Faz analiz akışı + skill/agent rehberi
3. 03-PHASE-DOC-TEMPLATE.md  → Her faz dosyası bu şablonu izlemeli
4. 04-THESIS-WRITING-GUIDE.md  → Akademik yazım disiplini
5. 05-CODE-INSPECTION-CHECKLIST.md  → .py dosyalarını incelerken bakılacaklar
6. 06-FIGURE-TABLE-CATALOG.md  → Şekil/tablo merkezi sicili
7. 07-GLOSSARY-SYMBOLS.md  → Master kısaltma + sembol sözlüğü
8. phases/README.md  → Faz indeksi (sen güncelleyeceksin)

[İLK OTURUM ADIMLARI]

ADIM 1: Kontrol & Aktivasyon
- 02-PROJECT-CLAUDE.md'yi oku ve içselleştir
- 01-WORKFLOW-PLAN.md'deki Faz 0'ı (Repo Keşfi) oku
- repo/ klasörü mevcut mu kontrol et:
  * Yoksa: bana söyle, klonlama komutunu birlikte çalıştıralım
  * Varsa: git status ile branch'i doğrula (dev updates olmalı)

ADIM 2: Repo Keşfi (Faz 0)
- Önce repo'nun üst düzey yapısını çıkar:
  * Tree view (3 level deep)
  * Ana giriş noktası (main.py, run.py, vs.) tespiti
  * requirements.txt veya pyproject.toml — bağımlılıklar
  * README.md — varsa proje sahibinin notları
  * config dosyaları, model dosyaları, data dizinleri

- Faz tanımlama:
  * Kod tabanında "faz" kavramı nasıl ifade edilmiş?
    (folder/, phase_*.py, module name, sınıf, pipeline step?)
  * Faz sayısını ve isimlerini listele
  * Her fazın başlıca .py dosyalarını eşle

- ECC use:
  * Memory MCP'ye "Thesis Nuclear AI Project" entity ekle
  * Her faz için sub-entity oluştur
  * code-explorer agent ile execution path tara
  * code-architect agent ile mimari haritayı çıkar

- ÇIKTI:
  * reports/faz-0-repo-kesfi.md — bulguların tam raporu
  * phases/README.md — faz indeksi (faz no, ad, .py dosyaları)
  * 07-GLOSSARY-SYMBOLS.md — repo'da geçen yeni terimler

ADIM 3: Plan Onayı
- Fazların listesini bana göster
- Her faz için tahmini analiz süresi
- Hangi sıra ile gideceğimizi öner (mantıksal olarak alt-üst, simple-complex, vs.)
- ONAY BEKLE — kendiliğinden Faz 1'e geçme

[GENEL KURALLAR]
- Her iddia kanıtla destekle (kodun hangi dosya, hangi satırı?)
- Kod yorumları yetersizse sen üret — ama kodun gerçek davranışına dayan
- Formül var mı kontrol et: docstring, comment, paper reference, hardcoded constants
- Her tespit edilen formülü 06-FIGURE-TABLE-CATALOG.md'ye numaralı ekle
- Her yeni kısaltma/sembol 07-GLOSSARY-SYMBOLS.md'ye işle
- Belirsizlik varsa: phase doc'unun "Açık Sorular" bölümüne yaz, bana sor
- Hayal etme, var olmayan kütüphane uydurma
- Türkçe akademik dilde yaz (sen söyleyene kadar İngilizce'ye geçme)
- Her fazın dökümanı 03-PHASE-DOC-TEMPLATE.md'deki bölümleri eksiksiz içermeli

[ÇIKTI BEKLENTİLERİ]
Faz başına:
- phases/faz-N-{kısa-ad}.md — şablona uygun tam doküman
- 06-FIGURE-TABLE-CATALOG.md güncellemesi (yeni şekil/tablo/formül)
- 07-GLOSSARY-SYMBOLS.md güncellemesi (yeni kısaltma/sembol)
- Memory MCP entity + relation güncellemesi
- reports/faz-N-analiz-notu.md (özet + açık sorular)
- /save-session "Faz N tamamlandı"

Tüm fazlar bitince:
- thesis/00-icindekiler.md → tez bölüm taslağı
- thesis/01-giris.md, 02-yontem.md, 03-bulgular.md, 04-tartisma.md, 05-sonuc.md
  taslakları
- reports/00-FINAL-SYNTHESIS.md → tüm fazların entegre özeti

[BAŞLAMA TALİMATI]
1. ADIM 1'i (Kontrol & Aktivasyon) yap
2. repo/ durumunu bana raporla
3. Klonlama gerekiyorsa, komutu hazırla — birlikte çalıştıralım
4. Sonra ADIM 2'ye (Repo Keşfi / Faz 0) geç
5. Sonra ADIM 3 — plan onayı için bana göster

Hazır mısın? Onayımı bekle, sonra başla.
```

---

## Devam Eden Oturumlar İçin (Faz N+1)

```
[YENİ OTURUM — Tez Asistanı, Faz N]

1. Bu klasörde 4 .md dosyasını oku:
   - 02-PROJECT-CLAUDE.md (kontrol dosyası)
   - 01-WORKFLOW-PLAN.md (faz N akışı)
   - 03-PHASE-DOC-TEMPLATE.md (şablon)
   - phases/README.md (önceki fazlar)

2. Önceki faz raporunu oku:
   - reports/faz-(N-1)-analiz-notu.md

3. Memory MCP sorgula:
   mcp__memory__search_nodes "Thesis Nuclear AI Project"

4. 06-FIGURE-TABLE-CATALOG.md ve 07-GLOSSARY-SYMBOLS.md'yi tara
   (önceki bilgi tekrarını önlemek için)

5. Faz N'in kapsamı:
   - phases/README.md'den faz N'in .py dosyaları
   - 01-WORKFLOW-PLAN.md'den faz N'in beklenen analiz adımları

6. Bana özet ver:
   - Önceki fazda ne yapıldı, açık kalan?
   - Bu fazın .py dosyaları
   - Önerilen analiz sırası

7. ONAY BEKLE, sonra başla.
```

---

## Hızlı Kullanım Senaryoları

### A) Tek bir .py dosyasını derinlemesine analiz et

```
Şu dosyayı incele: src/preprocess/normalize.py

- ECC code-explorer agent ile execution path
- python-reviewer agent ile kalite review
- comment-analyzer agent ile yorum kalitesi
- Tespit edilen formülleri 06-FIGURE-TABLE-CATALOG.md'ye ekle
- Kısa rapor: reports/code-deep-dive-normalize.md
```

### B) Tezin Yöntem bölümünü taslakla

```
phases/ klasöründeki tüm faz dokümanlarını oku.
Bunlardan tezimin "Yöntem" bölümünü taslakla:

- thesis/02-yontem.md
- Akış: önce faz akışı diyagramı, sonra her faz alt-bölüm olarak
- Akademik dil, atıf format: APA (varsayılan, sonra IEEE'ye çevirebiliriz)
- Bana göster, onay bekle
- Onay sonrası humanizer skill ile son temizlik (DİKKAT: akademik tonu koru)
```

### C) Belirli bir formülün tezdeki yeri

```
06-FIGURE-TABLE-CATALOG.md'de F-005 numaralı formül var.
Bu formül:
- Hangi fazda kullanılıyor?
- Tezin hangi bölümünde anlatılmalı?
- Türetimi tam mı, yoksa kaynak gerekiyor mu?
- LaTeX form'unda yazılmış mı?

Bana detaylı söyle.
```

### D) Eksik bir referansı bul

```
Repo'da kullanılan bir algoritma/kütüphane var ama kaynak gösterilmemiş.
Şu kodu incele: [dosya:satır]

ECC documentation-lookup + exa-search ile orijinal kaynağı bul.
07-GLOSSARY-SYMBOLS.md'ye ve faz dokümanına atıf olarak ekle.
```

### E) Tüm fazları sırasıyla özetle (Final Synthesis)

```
phases/ altındaki tüm fazları oku.
reports/00-FINAL-SYNTHESIS.md oluştur:

- Bir-paragraf executive summary (tezin Özet bölümü için)
- Faz akış diyagramı (mermaid)
- Her fazın 2-3 cümle özeti
- Sonuçlar ve katkılar listesi
- Sınırlamalar
- Gelecek çalışma önerileri
```

---

## Acil Komutlar

| Durum | Komut |
|-------|-------|
| Repo değişti | `cd repo && git pull origin "dev updates"` sonra ilgili faz docs'ını re-analyze |
| Yan soru | `/aside` |
| Hızlı checkpoint | `/checkpoint create "açıklama"` |
| Oturum kaydet | `/save-session "Faz N — durum"` |
| Önceki oturum | `/resume-session` |
| Token sıkıntısı | `/skill strategic-compact` |
| Kaynak doğrulama | exa-search MCP |
| Library docs | Context7 MCP |
| Repo dosya çekimi | GitHub MCP veya local `repo/` klasörü |

---

## Acil Durdurma

```
[ANALİZİ DURDUR]
1. Şu ana kadar olan bulguları phases/'a yaz (eksik olsa bile)
2. 06 ve 07'yi senkronize et
3. /save-session "Faz N kısmen — X kaldı"

Tekrar başlamak için: yeni oturumda "Devam Eden Oturumlar İçin" şablonunu kullan.
```

---

*Master Prompt v1.0 | 2026-05-02 | Thesis Toolkit*
