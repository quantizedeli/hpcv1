# Humanizer — Tam Kapsamlı Rehber

> **Sürüm:** 2.5.1 | **Lisans:** MIT  
> **Yazar:** Blader  
> **Kaynak:** https://github.com/blader/humanizer  
> **Yıldız:** 16.7K  
> **Uyumluluk:** Claude Code, OpenCode  
> **Son Güncelleme:** 2026-05-02

---

## İçindekiler

1. [Hızlı Başlangıç Kartı](#hızlı-başlangıç-kartı)
2. [Plugin Anatomisi](#plugin-anatomisi)
3. [Kurulum](#kurulum)
4. [Slash Komutları](#slash-komutları)
5. [Skill — `humanizer` Detayı](#skill--humanizer-detayı)
6. [Agents](#agents)
7. [Hooks](#hooks)
8. [Scripts & CLI Tools](#scripts--cli-tools)
9. [Config Dosyaları](#config-dosyaları)
10. [MCP Servers](#mcp-servers)
11. [29 AI Yazı Kalıbı — Tam Liste](#29-ai-yazı-kalıbı--tam-liste)
12. [İşlem Süreci (2 Tur Denetim)](#i̇şlem-süreci-2-tur-denetim)
13. [Kişilik & Ruh Katmak](#kişilik--ruh-katmak)
14. [Tam Örnek](#tam-örnek)
15. [Skill Birleştirme — İş Akışı Zincirleri](#skill-birleştirme--iş-akışı-zincirleri)
16. [Sorun Giderme](#sorun-giderme)
17. [Gerçek Dünya Senaryoları](#gerçek-dünya-senaryoları)
18. [Bakım & Güncelleme](#bakım--güncelleme)
19. [Kaynaklar](#kaynaklar)

---

## Hızlı Başlangıç Kartı

```bash
# 30 saniyede aktif:
git clone https://github.com/blader/humanizer ~/.claude/skills/humanizer
/reload-plugins

# İlk komutun:
/humanizer
# Sonra:
"Humanize this: [metin]"
```

**Ne sunar:**
- 1 skill — 29 AI yazı kalıbı tespiti + temizliği
- Wikipedia "Signs of AI writing" rehberinden türetilmiş
- 2 turlu denetim sistemi (RED → GREEN sürecine benzer)
- Ses tonu kalibrasyonu (kişisel yazı örneği ile)

---

## Plugin Anatomisi

```
~/.claude/skills/humanizer/
├── SKILL.md            ← Skill tanımı (frontmatter + 29 kalıp + örnekler)
├── README.md           ← Kullanıcı dokümantasyonu (özet pattern tablosu)
├── WARP.md             ← WARP IDE için ek rehberlik
└── LICENSE             ← MIT
```

**Source of Truth:** `SKILL.md` — Hem tanım hem talimat. README.md insan tüketimi için özetlenmiş.

---

## Kurulum

### Yöntem 1: Doğrudan Klonlama (Önerilen)

Marketplace formatında değil — direkt skill klasörüne klonlanır:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/blader/humanizer ~/.claude/skills/humanizer
/reload-plugins
```

### Yöntem 2: Manuel Kopyalama (Sadece SKILL.md)

```bash
mkdir -p ~/.claude/skills/humanizer
curl -o ~/.claude/skills/humanizer/SKILL.md \
  https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md
/reload-plugins
```

### Yöntem 3: OpenCode

```bash
mkdir -p ~/.config/opencode/skills/humanizer
git clone https://github.com/blader/humanizer ~/.config/opencode/skills/humanizer
```

> **Not:** OpenCode hem `~/.config/opencode/skills/` hem de Claude'un `~/.claude/skills/` klasörünü tarar — uyumluluk için.

### Bağımlılıklar

| Bileşen | Gereksinim |
|---------|------------|
| Claude Code | v1.0.33+ |
| Git | klonlama için |

**Sıfır production dependency** — sadece markdown.

### Doğrulama

```bash
# Skill yüklü mü?
ls ~/.claude/skills/humanizer/SKILL.md

# Frontmatter doğru mu?
head -25 ~/.claude/skills/humanizer/SKILL.md

# Aktif çalışıyor mu?
/humanizer
```

### Kaldırma

```bash
rm -rf ~/.claude/skills/humanizer
/reload-plugins
```

### Güncelleme

```bash
cd ~/.claude/skills/humanizer
git pull
/reload-plugins
```

---

## Slash Komutları

`/humanizer` — Skill'i manuel tetikleme. Skill `description` alanı üzerinden otomatik de tetiklenir (kullanıcı "humanize", "AI writing", "make this sound human" gibi ifadelerle).

---

## Skill — `humanizer` Detayı

### Tam Frontmatter

```yaml
---
name: humanizer
version: 2.5.1
description: |
  Remove signs of AI-generated writing from text. Use when editing or reviewing
  text to make it sound more natural and human-written. Based on Wikipedia's
  comprehensive "Signs of AI writing" guide. Detects and fixes patterns including:
  inflated symbolism, promotional language, superficial -ing analyses, vague
  attributions, em dash overuse, rule of three, AI vocabulary words, passive
  voice, negative parallelisms, and filler phrases.
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---
```

### Skill Profili

| Alan | Değer |
|------|-------|
| **Ad** | `humanizer` |
| **Sürüm** | 2.5.1 |
| **Tetikleyici (otomatik)** | "humanize", "make this sound human", "remove AI writing", "natural", "AI-sounding text" |
| **Tetikleyici (manuel)** | `/humanizer` |
| **Ne Zaman Kullan** | Metni yayına hazırlamadan önce, AI üretimi içeriği insanlaştırmak için |
| **Ne Zaman KULLANMA** | Teknik kod commenti, API dokümantasyonu, aşırı casual chat |
| **Çağırma** | Otomatik (anahtar kelime) veya `/humanizer` |
| **Yetenekler** | 29 AI kalıbı tespiti, ses kalibrasyonu, 2 tur denetim |
| **Bağımlılıklar** | Yok — standalone |
| **Allowed Tools** | Read, Write, Edit, Grep, Glob, AskUserQuestion |
| **Çıktı formatı** | 1) Taslak rewrite, 2) Kalan AI tells, 3) Final rewrite, 4) değişiklik özeti |
| **Anti-pattern** | Sadece kalıp kaldırmak (ruhsuz olur), aşırı kişisel ton zorlamak |

---

## Agents

Humanizer **agent sağlamaz** — saf skill.

---

## Hooks

Humanizer **hook kullanmaz** — pre-flight kontrolü, context injection yok.

---

## Scripts & CLI Tools

Humanizer **script sağlamaz** — saf markdown skill. Tüm mantık `SKILL.md` içindeki talimatlardadır.

---

## Config Dosyaları

### Frontmatter (`SKILL.md`)

```yaml
---
name: humanizer
version: 2.5.1
description: ...
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---
```

**v2.5.1'de eklenen:** Pattern 13 — Passive voice and subjectless fragments

### Plugin manifest YOK

`plugin.json` veya `marketplace.json` yok — sadece manuel klonlama çalışır.

---

## MCP Servers

Humanizer **MCP server sağlamaz** veya kullanmaz.

---

## 29 AI Yazı Kalıbı — Tam Liste

### İçerik Kalıpları (1-6)

#### 1. Anlam, Miras ve Geniş Trend Şişirme

**İzlenecek kelimeler:** `stands/serves as`, `is a testament/reminder`, `vital/significant/crucial/pivotal/key role/moment`, `underscores/highlights its importance/significance`, `reflects broader`, `symbolizing its ongoing/enduring/lasting`, `contributing to the`, `setting the stage for`, `marking/shaping the`, `represents/marks a shift`, `key turning point`, `evolving landscape`, `focal point`, `indelible mark`, `deeply rooted`

**Sorun:** LLM, rastgele unsurları daha geniş bir konuya katkıda bulunuyor gibi göstererek önem şişirir.

**Önce:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.

**Sonra:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

#### 2. Önem ve Medya Kapsamı Vurgusu

**İzlenecek:** `independent coverage`, `local/regional/national media outlets`, `written by a leading expert`, `active social media presence`

**Önce:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**Sonra:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

#### 3. -ing Ekli Yüzeysel Analizler

**İzlenecek:** `highlighting/underscoring/emphasizing...`, `ensuring...`, `reflecting/symbolizing...`, `contributing to...`, `cultivating/fostering...`, `encompassing...`, `showcasing...`

**Sorun:** AI chatbot'ları cümlelere sahte derinlik için present participle ekler.

**Önce:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**Sonra:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

---

#### 4. Tanıtım ve Reklam Dili

**İzlenecek:** `boasts a`, `vibrant`, `rich (mecazi)`, `profound`, `enhancing its`, `showcasing`, `exemplifies`, `commitment to`, `natural beauty`, `nestled`, `in the heart of`, `groundbreaking`, `renowned`, `breathtaking`, `must-visit`, `stunning`

**Önce:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**Sonra:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

#### 5. Belirsiz Atıflar ve Muğlak Kelimeler

**İzlenecek:** `Industry reports`, `Observers have cited`, `Experts argue`, `Some critics argue`, `several sources/publications`

**Önce:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**Sonra:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

#### 6. Kalıplaşmış "Zorluklar ve Gelecek Beklentileri"

**İzlenecek:** `Despite its... faces several challenges...`, `Despite these challenges`, `Challenges and Legacy`, `Future Outlook`

**Önce:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive.

**Sonra:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

### Dil & Dilbilgisi Kalıpları (7-13)

#### 7. AI Kelime Dağarcığı

**Yüksek frekans AI kelimeleri:**
`Actually`, `additionally`, `align with`, `crucial`, `delve`, `emphasizing`, `enduring`, `enhance`, `fostering`, `garner`, `highlight (verb)`, `interplay`, `intricate/intricacies`, `key (adjective)`, `landscape (abstract noun)`, `pivotal`, `showcase`, `tapestry (abstract noun)`, `testament`, `underscore (verb)`, `valuable`, `vibrant`

**Sorun:** Bu kelimeler 2023 sonrası metinlerde çok daha sık görünür ve genellikle birlikte kullanılır.

**Önce:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated.

**Sonra:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

#### 8. is/are Yerine Süslü Yapılar (Copula Avoidance)

**İzlenecek:** `serves as/stands as/marks/represents [a]`, `boasts/features/offers [a]`

**Önce:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**Sonra:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

#### 9. Negatif Paralelizm ve Kuyruk Olumsuzlama

**Sorun:** "Not only...but..." veya "It's not just about..." yapıları aşırı kullanılır.

**Önce:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**Sonra:**
> The heavy beat adds to the aggressive tone.

---

#### 10. Üçler Kuralı Aşırı Kullanımı

**Önce:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**Sonra:**
> The event includes talks and panels. There's also time for informal networking between sessions.

---

#### 11. Zarif Varyasyon (Synonym Cycling)

**Sorun:** AI'ın repetition-penalty kodu aşırı eş anlamlı ikame üretir.

**Önce:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**Sonra:**
> The protagonist faces many challenges but eventually triumphs and returns home.

---

#### 12. Sahte Aralıklar (False Ranges)

**Sorun:** "from X to Y" yapısı X ve Y anlamlı bir ölçekte değilken kullanılır.

**Önce:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**Sonra:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

#### 13. Edilgen Çatı ve Öznesi Olmayan Parçalar

**Sorun:** LLM aktörü gizler veya özneyi düşürür: "No configuration file needed."

**Önce:**
> No configuration file needed. The results are preserved automatically.

**Sonra:**
> You do not need a configuration file. The system preserves the results automatically.

---

### Stil Kalıpları (14-19)

#### 14. Em Tire (—) Aşırı Kullanımı

**Önce:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**Sonra:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

---

#### 15. Bold Aşırı Kullanımı

**Önce:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**Sonra:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

---

#### 16. Inline-Header Vertical Lists

**Sorun:** AI çıktıları kalın başlık + iki nokta ile başlayan liste ögeleri.

**Önce:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**Sonra:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

#### 17. Title Case Başlıklar

**Önce:**
> ## Strategic Negotiations And Global Partnerships

**Sonra:**
> ## Strategic negotiations and global partnerships

---

#### 18. Emoji Süslemeleri

**Önce:**
> 🚀 **Launch Phase:** The product launches in Q3

**Sonra:**
> The product launches in Q3.

---

#### 19. Kıvrımlı Tırnak (Curly Quotes)

**Sorun:** ChatGPT kıvrımlı tırnak kullanır, düz tırnak yerine — her iki format da okunabilir ama kıvrımlı tırnak AI izine işaret eder.

---

### İletişim Kalıpları (20-22)

#### 20. Chatbot Artifaktları

**İzlenecek:** `I hope this helps`, `Of course!`, `Certainly!`, `You're absolutely right!`, `Would you like...`, `let me know`, `here is a...`

**Önce:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**Sonra:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

---

#### 21. Knowledge-Cutoff Disclaimers

**İzlenecek:** `as of [date]`, `Up to my last training update`, `While specific details are limited/scarce...`, `based on available information...`

**Önce:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**Sonra:**
> The company was founded in 1994, according to its registration documents.

---

#### 22. Pohpohlama / Sycophantic Ton

**Önce:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**Sonra:**
> The economic factors you mentioned are relevant here.

---

### Dolgu & Belirsizleştirme (23-29)

#### 23. Filler İfadeler

| Önce | Sonra |
|------|-------|
| `In order to achieve this goal` | `To achieve this` |
| `Due to the fact that it was raining` | `Because it was raining` |
| `At this point in time` | `Now` |
| `In the event that you need help` | `If you need help` |
| `The system has the ability to process` | `The system can process` |
| `It is important to note that the data shows` | `The data shows` |

---

#### 24. Aşırı Hedging

**Önce:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**Sonra:**
> The policy may affect outcomes.

---

#### 25. Jenerik Olumlu Sonuçlar

**Önce:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence.

**Sonra:**
> The company plans to open two more locations next year.

---

#### 26. Tireli Kelime Çifti Aşırı Kullanımı

**İzlenecek:** `third-party`, `cross-functional`, `client-facing`, `data-driven`, `decision-making`, `well-known`, `high-quality`, `real-time`, `long-term`, `end-to-end`

**Önce:**
> The cross-functional team delivered a high-quality, data-driven report on our client-facing tools.

**Sonra:**
> The cross functional team delivered a high quality, data driven report on our client facing tools.

---

#### 27. İkna Edici Otorite Kalıpları

**İzlenecek:** `The real question is`, `at its core`, `in reality`, `what really matters`, `fundamentally`, `the deeper issue`, `the heart of the matter`

**Önce:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.

**Sonra:**
> The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.

---

#### 28. Sinyal Verme ve Duyurular

**İzlenecek:** `Let's dive in`, `let's explore`, `let's break this down`, `here's what you need to know`, `now let's look at`, `without further ado`

**Önce:**
> Let's dive into how caching works in Next.js. Here's what you need to know.

**Sonra:**
> Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.

---

#### 29. Parçalı Başlıklar

**Sorun:** Başlığı yeniden ifade eden tek satırlık paragraf.

**Önce:**
```
## Performance

Speed matters.

When users hit a slow page, they leave.
```

**Sonra:**
```
## Performance

When users hit a slow page, they leave.
```

---

## İşlem Süreci (2 Tur Denetim)

```
1. Giriş metnini dikkatlice oku
2. 29 kalıbın tamamını tespit et
3. Her sorunlu bölümü yeniden yaz:
   - Sesli okunduğunda doğal mı?
   - Cümle yapısı doğal değişiyor mu?
   - Belirsiz iddialar yerine spesifik detay var mı?
   - Bağlam için uygun ton korunuyor mu?
   - Basit yapılar (is/are/has) uygun yerlerde kullanılıyor mu?

4. TASLAK rewrite sun

5. Tur 2 — Self-eleştiri:
   "Bu metin neden hâlâ açıkça AI üretimi?"
   → Kalan tells'i kısa bullet'larla yaz

6. Tur 2 — Düzeltme:
   "Şimdi açıkça AI üretimi olmaktan çıkar."
   → Final versiyonu sun

7. (Opsiyonel) Yapılan değişikliklerin kısa özeti
```

### Çıktı Formatı

```
## Draft Rewrite
[Taslak metin]

## What makes the below so obviously AI generated?
- [Kalan tell 1]
- [Kalan tell 2]

## Final Rewrite
[Nihai metin]

## Changes Made (Optional)
- [Değişiklik 1]
```

---

## Kişilik & Ruh Katmak

Sadece kalıpları kaldırmak yarısı — ruhsuz yazı da AI gibi görünür.

### Ruhsuz Yazının Belirtileri

- Her cümle aynı uzunluk ve yapıda
- Görüş yok, tarafsız raporlama
- Uygun olduğunda birinci şahıs yok
- Mizah, keskinlik, kişilik yok

### Nasıl Ses Katılır

| Teknik | Açıklama |
|--------|----------|
| **Görüş belirt** | "Bununla nasıl hissedeceğimi gerçekten bilmiyorum" |
| **Ritim değiştir** | Kısa vurucu cümleler. Sonra uzun olanlar. |
| **Karmaşıklığı kabul et** | "Bu etkileyici ama aynı zamanda biraz rahatsız edici" |
| **"Ben" kullan** | "Bunu düşünmeye devam ediyorum..." gerçek bir insan signal'i |
| **Biraz dağınıklık bırak** | Tangent, parantez, yarım düşünce → insansaldır |
| **Duygular hakkında özgül ol** | "Bu endişe verici" yerine somut sahne tasvir et |

---

## Tam Örnek

**Önce (AI sesli):**
> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools—nestled at the intersection of research and practice—are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> - 💡 **Speed:** Code generation is significantly faster, reducing friction.
> - 🚀 **Quality:** Output quality has been enhanced through improved training.
>
> In conclusion, the future looks bright. Let me know if you'd like me to expand on any section!

**Taslak Rewrite:**
> AI coding assistants speed up some tasks. The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped paying attention.

**What makes the below so obviously AI generated?**
- The rhythm is still a bit too tidy
- The closer leans a touch slogan-y

**Final Rewrite:**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value.

---

## Skill Birleştirme — İş Akışı Zincirleri

### Zincir 1: Blog Yazma + Humanize

```
1. ECC: article-writing skill → uzun form içerik
2. ECC: brand-voice skill → ses tonu profili
3. humanizer → 29 kalıbı temizle + ses ekle
4. (Manuel) Yayına gönder
```

### Zincir 2: Sosyal Medya İçerik

```
1. ECC: content-engine → X/LinkedIn için içerik
2. humanizer → her platform için ayrı tur
3. ECC: crosspost → platform-spesifik adapt
```

### Zincir 3: Ses Kalibrasyonlu Üretim

```
KULLANICI: "Bu konuda yazı yaz [konu]. İşte benim yazı stilim: [örnek]"
1. humanizer → örneği analiz et (cümle uzunluğu, kelime seviyesi)
2. ECC: article-writing → kalıba uygun yaz
3. humanizer → yine kontrol + temizlik
```

---

## Sorun Giderme

### `/humanizer` komutu çalışmıyor

```bash
ls ~/.claude/skills/humanizer/SKILL.md
/reload-plugins
```

### Skill marketplace add ile yüklenmiyor

**Sebep:** Repo plugin marketplace formatında değil — `.claude-plugin/marketplace.json` yok.

**Çözüm:** Direkt klonla (yöntem 1).

### Sonuç çok kuru / robotik

Kişisel yazı örneği sağla:

```
Humanize this text. Here's a sample of my writing for voice matching:
[2-3 paragraph kişisel yazı]

[Humanize edilecek metin]
```

---

## Gerçek Dünya Senaryoları

### Senaryo 1: Newsletter

```
1. ECC: article-writing → ilk taslak
2. humanizer (sample ile) → temizlik
3. Manuel review → yayın
```

### Senaryo 2: Blog Postu

```
1. ECC: deep-research → konu araştırması
2. ECC: article-writing → 1500 kelime taslak
3. humanizer → AI tells temizliği
4. ECC: seo skill → meta description
```

### Senaryo 3: Akademik Yazı

```
1. ECC: article-writing → akademik draft
2. humanizer → AI tells'i temizle, akademik ton koru
3. Manual peer review
```

---

## Bakım & Güncelleme

```bash
cd ~/.claude/skills/humanizer
git pull
/reload-plugins
```

### Sürüm Geçmişi

| Sürüm | Değişiklik |
|-------|-----------|
| **2.5.1** | Pattern 13 eklendi (passive voice, subjectless fragments) |
| 2.5.0 | 25 → 29 pattern (rule of three, hyphenated pairs, persuasive authority, signposting) |
| 2.0.0 | Voice calibration özelliği |
| 1.x | İlk sürüm — 20 pattern |

---

## Kaynaklar

- **GitHub:** https://github.com/blader/humanizer
- **Wikipedia kaynak:** [Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- **Lisans:** MIT

### İlgili Belgeler

- [INDEX.md](INDEX.md) — Ana indeks
- [everything-claude-code-rehber.md](everything-claude-code-rehber.md) — ECC mega-plugin
- [superpowers-rehber.md](superpowers-rehber.md) — Geliştirme metodolojisi
- [ui-ux-pro-max-rehber.md](ui-ux-pro-max-rehber.md) — UI/UX tasarım

---

*Üretilme tarihi: 2026-05-02 | Humanizer v2.5.1*
