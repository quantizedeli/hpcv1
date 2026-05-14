# Superpowers — Tam Kapsamlı Rehber

> **Sürüm:** 5.0.7 (31 Mart 2026) | **Lisans:** MIT  
> **Yazar:** Jesse Vincent (jesse@fsck.com)  
> **Kaynak:** https://github.com/obra/superpowers  
> **Discord:** https://discord.gg/35wsABTejz  
> **Son Güncelleme:** 2026-05-01

---

## İçindekiler

1. [Hızlı Başlangıç Kartı](#hızlı-başlangıç-kartı)
2. [Plugin Anatomisi](#plugin-anatomisi)
3. [Kurulum](#kurulum)
4. [Slash Komutları Tam Referansı (3 komut — deprecated)](#slash-komutları-tam-referansı)
5. [Skills — Tam Katalog (14 skill)](#skills--tam-katalog)
6. [Agents — Tam Liste (1 agent)](#agents--tam-liste)
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
/plugin marketplace add obra/superpowers
/plugin install superpowers
/reload-plugins

# İlk komutun (komut yok — skill otomatik tetiklenir):
"Yeni bir özellik düşünüyorum: kullanıcı yönetimi sistemi"
# → brainstorming skill otomatik devreye girer
```

**Ne sunar:**
- 14 disiplin uygulayan skill — TDD, sistematik debug, brainstorming, kanıt-bazlı doğrulama
- 1 agent — code-reviewer (isolated context ile)
- SessionStart hook'u — `using-superpowers` skill'ini otomatik enjekte eder
- 8 platform desteği — Claude Code, Cursor, Codex, Copilot, Gemini, OpenCode, Windows, WSL

---

## Plugin Anatomisi

```
superpowers/5.0.7/
├── .claude-plugin/
│   ├── plugin.json              ← Plugin manifest
│   └── marketplace.json         ← Marketplace config
├── .codex-plugin/               ← Codex CLI plugin config
├── .cursor-plugin/              ← Cursor plugin config
├── .codex/                      ← Codex agent rolleri
├── .opencode/                   ← OpenCode entegrasyonu
├── agents/
│   └── code-reviewer.md         ← Tek agent
├── commands/
│   ├── brainstorm.md            ← DEPRECATED → brainstorming skill
│   ├── execute-plan.md          ← DEPRECATED → executing-plans skill
│   └── write-plan.md            ← DEPRECATED → writing-plans skill
├── skills/                      ← 14 skill (her birinde SKILL.md)
│   ├── brainstorming/
│   ├── dispatching-parallel-agents/
│   ├── executing-plans/
│   ├── finishing-a-development-branch/
│   ├── receiving-code-review/
│   ├── requesting-code-review/
│   ├── subagent-driven-development/
│   ├── systematic-debugging/
│   ├── test-driven-development/
│   ├── using-git-worktrees/
│   ├── using-superpowers/
│   ├── verification-before-completion/
│   ├── writing-plans/
│   └── writing-skills/
├── hooks/
│   ├── hooks.json               ← SessionStart hook config
│   ├── run-hook.cmd             ← Cross-platform polyglot wrapper
│   └── session-start            ← Bash script
├── AGENTS.md                    ← Codex/Codex CLI için
├── CLAUDE.md                    ← Katkı kuralları (94% PR red oranı)
├── GEMINI.md                    ← Gemini CLI için
├── gemini-extension.json        ← Gemini extension manifest
├── package.json                 ← Sıfır production dep
└── LICENSE                      ← MIT
```

---

## Kurulum

### Yöntem 1: Plugin Marketplace (Önerilen)

```bash
/plugin marketplace add obra/superpowers
/plugin install superpowers
/reload-plugins
```

### Yöntem 2: Manuel Klonlama

```bash
git clone https://github.com/obra/superpowers ~/.claude/plugins/superpowers
/reload-plugins
```

### Bağımlılıklar

| Bileşen | Gereksinim | Neden |
|---------|------------|-------|
| Claude Code | v1.0.33+ | `/plugin` komutu için |
| Bash | herhangi bir sürüm | Hook script'leri için |
| Git | herhangi bir sürüm | Repo işlemleri için |
| (Windows) Git for Windows | C:\Program Files\Git | run-hook.cmd için |

**Not:** Superpowers **sıfır production dependency** politikasıyla çalışır.

### Kaldırma

```bash
/plugin uninstall superpowers
# Manuel:
rm -rf ~/.claude/plugins/cache/superpowers-marketplace
```

---

## Slash Komutları Tam Referansı

> ⚠️ **Tüm 3 komut DEPRECATED — sonraki major sürümde kaldırılacak.**

| Komut | Durum | Yerine Kullan |
|-------|-------|--------------|
| `/brainstorm` | DEPRECATED | `brainstorming` skill (otomatik tetiklenir) |
| `/write-plan` | DEPRECATED | `writing-plans` skill |
| `/execute-plan` | DEPRECATED | `executing-plans` skill |

---

## Skills — Tam Katalog

Superpowers 14 skill sunar. Hepsi `skills/<ad>/SKILL.md` formatında.

### Skill Çağırma Mekanizması

> **"BİR SKİLL GÖREVİNE UYUYORSA KULLANMAK ZORUNDASIN. SEÇİMİN YOK."**

Öncelik sırası:
1. Kullanıcının açık talimatları (en yüksek)
2. Superpowers skill'leri (varsayılanları geçersiz kılar)
3. Claude'un varsayılan davranışı (en düşük)

---

### 1. `using-superpowers` — Skill Sistemi Giriş Noktası

| Alan | Değer |
|------|-------|
| **Tetikleyici** | SessionStart hook ile her oturumda otomatik enjekte |
| **Çağırma** | Otomatik (hook), manuel `/skill using-superpowers` |
| **Yetenekler** | Diğer skill'leri çağırma rehberi, öncelik sistemi |
| **Anti-pattern** | "Bu basit bir soru" diyerek skill kontrolü atlamak |

---

### 2. `brainstorming` — Tasarım Keşfi & Spec Oluşturma

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "düşünüyorum", "yapmak istiyorum", "yeni özellik", "let's make" — otomatik |
| **Ne Zaman Kullan** | Her geliştirme görevinden ÖNCE (zorunlu) |
| **Çıktı formatı** | `docs/superpowers/specs/YYYY-MM-DD-<konu>-design.md` |
| **Anti-pattern** | Tasarım onaylanmadan kod yazmak |

**9 Adım Süreç:**
1. Mevcut proje dosyalarını incele
2. Görsel mockup teklif et (uygunsa, ayrı mesaj)
3. Tek soru sor (tercihen çoktan seçmeli)
4. 2-3 yaklaşım öner (artı/eksi + tavsiye)
5. Tasarım sun (her bölümde onay al)
6. Spec yaz
7. Self-review (placeholder, çelişki, belirsizlik)
8. Kullanıcı onayını bekle
9. writing-plans skill'ini çağır

---

### 3. `writing-plans` — Uygulama Planı Oluşturma

| Alan | Değer |
|------|-------|
| **Tetikleyici** | brainstorming sonrası, "plan yaz" |
| **Çıktı formatı** | `docs/superpowers/plans/YYYY-MM-DD-<özellik>.md` |
| **Anti-pattern** | "TBD", placeholder kullanmak |

---

### 4. `executing-plans` — Yazılmış Planı Uygulama

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "planı uygula", plan dosyası mevcut |
| **3 Aşama** | Yükle & İncele → Görevleri Çalıştır → Tamamla |
| **Anti-pattern** | main/master üzerinde başlamak |

---

### 5. `subagent-driven-development` — Subagent Orkestrasyon

| Alan | Değer |
|------|-------|
| **Yetenekler** | Her görev için taze subagent + 2 aşamalı review |
| **Anti-pattern** | Review'ı atlamak |

---

### 6. `dispatching-parallel-agents` — Paralel Ajan Dağıtımı

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "paralel", birden fazla bağımsız hata/görev |
| **Ne Zaman KULLANMA** | Hatalar interconnected, tam sistem görünümü gerekli |

---

### 7. `test-driven-development` — Test Önce Geliştirme

**Demir Kural:** "Testi başarısız görmediysen, doğru şeyi test edip etmediğini bilemezsin."

- **RED** — Başarısız test yaz
- **GREEN** — Minimum kod yaz, test geçsin
- **REFACTOR** — Kodu temizle, testler hâlâ geçsin

---

### 8. `systematic-debugging` — Sistematik Hata Ayıklama

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "hata", "bug", "çalışmıyor" |
| **Anti-pattern** | Kök neden analizi olmadan düzeltmeye girişmek |

**4 Aşama:**
1. Kök Neden Araştırması
2. Kalıp Analizi
3. Hipotez & Test
4. Uygulama

3 başarısız girişim sonra: mimariyi sorgula.

---

### 9. `verification-before-completion` — Tamamlanmadan Önce Doğrulama

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "tamamlandı", "düzeltildi", "çalışıyor" iddiası — otomatik |
| **Anti-pattern** | "Muhtemelen", "sanırım", doğrulama olmadan claim |

**5 Adım:** Hangi komut iddiayı kanıtlar → Çalıştır → Oku → Destekliyor mu → İddiada bulun

---

### 10. `using-git-worktrees` — Git Worktree Yönetimi

| Alan | Değer |
|------|-------|
| **Tetikleyici** | "worktree", "izole çalışma alanı" |
| **Anti-pattern** | Dizin .gitignore'da değilken worktree oluşturmak |

---

### 11. `finishing-a-development-branch` — Geliştirme Dalını Tamamlama

**4 Seçenek Sun:** Yerel merge / PR oluştur / Branch'i tut / Sil (yazılı onay zorunlu)

---

### 12. `requesting-code-review` — Kod Review İsteme

**Yanıt Protokolü:** Kritik → hemen | Önemli → devam etmeden önce | Öneri → belgele

---

### 13. `receiving-code-review` — Kod Review Alma

**Temel Prensip:** "Doğrula, sonra uygula. Varsaymadan önce sor."
**Yasaklı İfadeler:** "Kesinlikle haklısın!", "Harika nokta!"

---

### 14. `writing-skills` — Yeni Skill Yazma

**TDD Skill Geliştirme:**
- RED — Skill OLMADAN baseline çalıştır
- GREEN — Minimum skill yaz
- REFACTOR — Loophole'ları kapat

---

## Agents — Tam Liste

### `code-reviewer`

```python
Agent({
  description: "Code review for auth module",
  subagent_type: "superpowers:code-reviewer",
  prompt: "Implementation: <what was built>\nRequirements: <spec>"
})
```

**Sorun Kategorileri:** Critical / Important / Suggestion

---

## Hooks Sistemi

SessionStart hook → `using-superpowers` skill içeriği context'e enjekte edilir.

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup|clear|compact",
      "hooks": [{"type": "command", "command": "run-hook.cmd session-start"}]
    }]
  }
}
```

`run-hook.cmd` — Cross-platform (Windows: cmd.exe → bash bulur; Unix: direkt çalışır)

---

## Skill Birleştirme — İş Akışı Zincirleri

### Zincir 1: Tam Geliştirme Döngüsü

```
"Yeni kullanıcı yönetimi sistemi yapmak istiyorum"
  → brainstorming → writing-plans → using-git-worktrees
  → executing-plans / subagent-driven-development
    (her görevde: TDD + verification + code-review)
  → finishing-a-development-branch
```

### Zincir 2: Bug Fix

```
systematic-debugging → TDD failing test → fix → verification → code-review
```

### Zincir 3: Paralel Test Failure

```
dispatching-parallel-agents (3 agent) → verification-before-completion → code-review
```

---

## Sorun Giderme

### Hook Hataları (Windows)

```cmd
cd %USERPROFILE%\.claude\plugins\cache\superpowers-marketplace\superpowers\5.0.7\hooks
run-hook.cmd session-start
```

### Skill Tetiklenmiyor

1. `/reload-plugins` ile reload deneyin
2. Manuel çağır: `/skill brainstorming`

### Code Reviewer Agent Çakışması

```python
Agent({ subagent_type: "superpowers:code-reviewer", ... })   # Superpowers
Agent({ subagent_type: "everything-claude-code:code-reviewer", ... })  # ECC
```

---

## Bakım & Güncelleme

```bash
/plugin update superpowers
```

### Sürüm Geçmişi

| Sürüm | Tarih | Değişiklikler |
|-------|-------|--------------|
| **5.0.7** | 31 Mar 2026 | Bootstrap first-user-message; Windows/WSL PID fix |
| **5.0.2** | Oca 2026 | Brainstorming server sıfır-bağımlılık |
| **5.0.0** | Aral 2025 | Skills tabanlı sistem, Copilot CLI desteği |

---

## Kaynaklar

- **GitHub:** https://github.com/obra/superpowers
- **Discord:** https://discord.gg/35wsABTejz
- **Lisans:** MIT

### İlgili Belgeler

- [INDEX.md](INDEX.md) — Ana indeks
- [everything-claude-code-rehber.md](everything-claude-code-rehber.md) — ECC mega-plugin
- [humanizer-rehber.md](humanizer-rehber.md) — AI yazı temizleme
- [academic-shield-rehber.md](academic-shield-rehber.md) — Türkçe akademik yazı

---

*Üretilme tarihi: 2026-05-01 | Superpowers v5.0.7*
