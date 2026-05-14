# Skills Klasörü — İndeks

> **Konum:** `C:\Users\Hakan Yakut\Desktop\ahmet\skillv1\skills\`  
> **Son Güncelleme:** 2026-05-07  
> **Ana İndeks:** [../INDEX.md](../INDEX.md)

---

## Rehber Dosyaları

| # | Dosya | Plugin | Durum | Kapsam |
|---|-------|--------|-------|--------|
| 1 | [everything-claude-code-rehber.md](everything-claude-code-rehber.md) | everything-claude-code 2.0.0-rc.1 | ✅ Kurulu | 182 skill, 48 agent, 68 komut |
| 2 | [superpowers-rehber.md](superpowers-rehber.md) | superpowers 5.0.7 | ✅ Kurulu | 14 skill, 1 agent, 3 komut |
| 3 | [ui-ux-pro-max-rehber.md](ui-ux-pro-max-rehber.md) | ui-ux-pro-max 2.5.0 | ✅ Kurulu | 7 skill, BM25 arama, 16 stack |
| 4 | [humanizer-rehber.md](humanizer-rehber.md) | humanizer 2.5.1 | ✅ Kurulu | 1 skill, 29 AI kalıbı |
| 5 | [anthropics-skills-rehber.md](anthropics-skills-rehber.md) | anthropics/skills | ❌ Kurulu değil | 17 skill — referans |
| 6 | [academic-shield-rehber.md](academic-shield-rehber.md) | academic-shield (custom) | ✅ Kurulu | Türkçe akademik yazı, AI detector bypass |
| 7 | [literature-review-rehber.md](literature-review-rehber.md) | literature-review (custom) | ✅ Kurulu | Çok dilli tarama, 30+ veritabanı, DOI zorunlu, 5 aşama |
| 8 | [academic-writing-pro-rehber.md](academic-writing-pro-rehber.md) | academic-writing-pro (custom) | ✅ Kurulu | 3 alan profili, LaTeX/DOCX, 5-rol pipeline, bypass |

---

## Hızlı Notlar

- **everything-claude-code** ve **superpowers** `code-reviewer` agent çakışması: prefix kullan
  - `superpowers:code-reviewer` — subagent sonrası
  - `everything-claude-code:code-reviewer` — genel kalite review
- **academic-shield** — [`academic-shield/SKILL.md`](../academic-shield/SKILL.md) ile yüklenir; SAÜ tez formatı + AI detector bypass
- **literature-review** — [`literature-review/SKILL.md`](../literature-review/SKILL.md) ile yüklenir; academic-shield ve academic-writing-pro tarafından ortak modül olarak kullanılır
- **academic-writing-pro** — [`academic-writing-pro/SKILL.md`](../academic-writing-pro/SKILL.md) ile yüklenir; 3 alan (Fen/Sosyal/Sağlık), LaTeX/DOCX çıktısı, 5-rol pipeline
- **anthropics-skills** — kurulmadı, ileride değerlendirmek için referans dosyası tutuldu

---

*[CLAUDE.md](../CLAUDE.md) · [PLAYBOOK.md](../PLAYBOOK.md) · [Ana İndeks](../INDEX.md)*
