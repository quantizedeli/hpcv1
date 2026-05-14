# Sprint Planı — Nuclear Physics AI Pipeline
## Sohbet: 2026-05-07/08 Log Analizi Sonrası

> **Durum:** Sprint dosyaları hazır. Yeni sohbette çalıştırılacak.
> **Bağlam:** `sprints/` klasörü — her sprint kendi .md dosyasında.
> **Ön Koşul:** Bu dosyayı ve ilgili sprint dosyasını yeni sohbet başında oku.

---

## Sprint Genel Bakış

| Sprint | Dosya | Konu | Öncelik | Durum |
|--------|-------|------|---------|-------|
| Sprint 1 | `sprint-01-dual-r2-filtresi.md` | Çift R² filtresi + CV fold adaptif | KRITIK | **TAMAMLANDI** 2026-05-08 |
| Sprint 2 | `sprint-02-config-temizlik.md` | Config sync + Robust/N75 kaldırma | YUKSEK | **TAMAMLANDI** 2026-05-09 |
| Sprint 3 | `sprint-03-belge-sync.md` | Faz belgeleri + pipeline-hatalari.md sync | ORTA | **TAMAMLANDI** 2026-05-09 |
| Sprint 4 | `sprint-04-truba-hazirlik.md` | TRUBA hazırlık + BUG-02/03/31/32/38/39/20 fix | YUKSEK | **TAMAMLANDI** 2026-05-11 |
| Sprint 5 | `sprint-05-inter-pfaz-audit.md` | Inter-PFAZ data flow audit (KURAL 19) + BUG-42..46 | YUKSEK | **TAMAMLANDI** 2026-05-11 |
| Sprint 6 | `sprint-06-8-kategori-tarama.md` | 8 kategori paralel agent taraması — 15 yeni bug (BUG-47..61) | ORTA | **TAMAMLANDI** 2026-05-12 |
| Sprint 7 | `sprint-07-bug-fixes.md` | BUG-47..61 fix: 15 bug, 14 dosya, 16 satir kod | YUKSEK | **TAMAMLANDI** 2026-05-12 |
| Sprint 8 | `sprint-08-missing-fixes.md` | BUG-62/63/64 -- Sprint 1/2/4 eksik fix'ler + CV gate gercek implementasyon | KRITIK | **TAMAMLANDI** 2026-05-12 |
| Sprint 9A | `sprint-09-v10-sync.md` | v10 sync: Sprint 7+8 fix'leri, CV gate, max_train_cv_gap=0.6 | YUKSEK | **TAMAMLANDI** 2026-05-13 |
| Sprint 9B | `sprint-09-truba.md` | TRUBA: 4 job script (weka flag, 110CPU, n_workers=100, zip) | YUKSEK | **TAMAMLANDI** 2026-05-13 |
| Sprint 10 | `sprint-10-qa-fixes.md` | TRUBA QA raporu + inter-PFAZ denetim (BUG-65..74) | KRITIK | **TAMAMLANDI** 2026-05-13 |
| Sprint 11+12 | `sprint-11-12-final-truba-ready.md` | Cikti tamligi + TRUBA 2025-12-15 kurali (BUG-75..84): PFAZ3/6/8/9/12 path explicit, training_configs_50.json, submit_all.sh, PFAZ8 helper-based, BandAnalyzer, -c 110->112 | KRITIK | **TAMAMLANDI** 2026-05-13 |
| Sprint 13 | `sprint-13-final.md` | Codex audit + tez plani (BUG-85..99): PIPESTATUS fix, run_all RuntimeError, optuna/lightgbm REQUIRED, strict_truba, PFAZ2 fail→PFAZ3 skip, MC random_state, RobustnessTester aktif, PFAZ12 BootstrapCI+ANFIS, PFAZ5 AI_vs_ANFIS sheet, automl_trials_details.xlsx, KURAL 29-33 | KRITIK | **TAMAMLANDI** 2026-05-14 |

**Uygulama sırası:** Sprint 1-13 TAMAMLANDI. **TRUBA AKMAYA HAZIR.** Acik adaylar (TRUBA sonrasi): v10 sync (BUG-65..99, notlar `docs/thesis-toolkit/v10-todo.md`), PFAZ10 rewrite (Sprint 14 plan: `sprint-14-pfaz10-rewrite-plan.md`), tez sonrasi PFAZ11.

---

## Sprint 4 ve 5 Eklenme Notu (2026-05-11)

Sprint 4 ve 5 başlangıçta SPRINT-PLAN.md'de yer almıyordu çünkü retrospektif
olarak (yapıldıktan sonra) belgelendi:

- **Sprint 4** = v10 reposundaki commit `3d61faa` (2026-05-11 22:53)
  *"feat: Sprint 1-4 -- Dual R2 filtresi, bug fix'ler, TRUBA hazirlik"*
  içeriğinden sentezlendi. TRUBA hazırlık + Sprint 1-3'te kalan bug temizliği.

- **Sprint 5** = Kemal'in talebi üzerine Claude tarafından yapılan
  Inter-PFAZ data flow audit oturumu. KURAL 19 doğdu. 5 yeni bug
  (BUG-42..46) tespit edildi (başlangıçta yanlışlıkla BUG-13..17 numarası
  kullanıldı, sonra düzeltildi).

Sprint 6 başlangıçta tanımlanmadı çünkü Sprint 5'in 8 kategori taraması
(hardcoded path, optional imports, sheet name, n_jobs, silent failures,
encoding, memory leak, doc iddialari) henüz yapılmamıştı.

---

## Bu Oturumda Tamamlanan İşler (2026-05-07/08)

### Kod Düzeltmeleri
- [x] BUG-39: `overfitting_detector.py` — `analyze_training_metrics` metodu eklendi
- [x] BUG-40: `automl_anfis_optimizer.py:538` + `automl_retraining_loop.py:583` — `anfis_core` import yolu düzeltildi
- [x] BUG-41: `config_desktop.json` — "Physics" geçersiz feature set kaldırıldı, null ile değiştirildi

### Config Güncellemeleri
- [x] `config_desktop.json` — Robust scaling kaldırıldı, N=75 kaldırıldı
- [x] `config_desktop.json` — feature_sets: null (hedef-bazlı otomatik, 14 MM + 15 QM set)
- [x] `config_desktop.json` — Scenarios: [S70] (desktop hızı)
- [x] `config_desktop.json` — ANFIS: 4 config + n_datasets_per_target: 20 (placeholder)
- [x] `config_desktop.json` — Sampling: [Random, Stratified] eklendi
- [x] `config_desktop.json` — r2_min_threshold: 0.5, cv_folds: 3, BNN/PINN kaldırıldı

### Belge Güncellemeleri
- [x] `tez-yazim-not-defteri.md` v1.6 — Nilsson, Robust, N=75, Stratified, Dual R², ANFIS 16 config notları
- [x] `memory/pipeline_bugs.md` — BUG-40, BUG-41 eklendi, toplam: 41
- [x] `memory/phases_progress.md` — 2026-05-08 güncellemesi

### Yeni Bulgular (Orphan Scan — tüm fazlar)
- 40+ metod çağrısı incelendi → sorunsuz
- 1 kritik eksik modül: `anfis_core.py` (BUG-40 — düzeltildi)
- 1 geçersiz config değeri: "Physics" (BUG-41 — düzeltildi)
- `ANFISDatasetSelector` → **AKTİF EDİLDİ** (`anfis_parallel_trainer_v2.py:1170`, Top=50 Mid=50 Low=100)
- `configurations` alanı hiç okunmuyor (hardcoded PILOT_IDS — tasarım kararı, belgelendi)
- `ANFIS_MAX_INPUTS = 5` — tüm TARGET_RECOMMENDED_SETS geçiyor (doğrulandı)
- PINN mevcut haliyle işlevsiz (bounds ±20, veri ±7 → ceza hiç çalışmıyor) → Sprint 4 adayı
- Transfer Learning + GNN → ertelendi (memory/project_deferred_features.md)
- BUG-02 (HBAR_C) → CLAUDE.md güncellendi: 2026-05-04'te düzeltilmişti

### Faz Belgeleri Güncellendi (Bu Oturumda)
- [x] `phases/faz-01-veri-kumesi-uretimi.md` — Robust kaldırma + N=75 kaldırma karar notları
- [x] `phases/faz-03-anfis-egitimi.md` — Bölüm 11: ANFISDatasetSelector AKTİF, PILOT_IDS, CFG_ adlandırma
- [x] `sprints/sprint-02-config-temizlik.md` — 3c: configurations not, 3d: ANFISDatasetSelector TAMAMLANDI
- [x] `sprints/sprint-03-belge-sync.md` — Adım 4b: faz-03 güncelleme talimatları eklendi
- [x] `CLAUDE.md` — BUG-02 "düzeltilmedi" → "DÜZELTİLDİ 2026-05-04"
- [x] `claude-hatalarim-ve-dersler.md` — KURAL 15 (config okuma), KURAL 16 (CLAUDE.md + memory dahil)
- [x] `memory/project_deferred_features.md` — Transfer Learning, PINN geliştirme, GNN erteleme
- [x] `sprints/sprint-00-oturum-ozeti.md` — Sprint sonu smoke test adımları eklendi

---

## Bekleyen Sprint Görevleri

### Sprint 1 — Çift R² Filtresi (KOD DEĞİŞİKLİĞİ)
**Neden önemli:** Şu an val_R2 ≥ 0.5 filtresi var ama CV R² kontrolü yok.
Train_R2=0.99 ama CV_R2=-0.31 olan modeller kaydediliyor → aşırı uyum problemi.
**Fix:** `parallel_ai_trainer.py` refactor — model kayıt akışını yeniden yapılandır.

### Sprint 2 — Config Senkronizasyonu
**Neden önemli:** `config.json` (TRUBA) ve `nucdatav2-truba/` hâlâ Robust scaling ve N=75 içeriyor.
**Fix:** Tüm config dosyaları aynı ilkeleri uygulamalı.

### Sprint 3 — Belge Senkronizasyonu
**Neden önemli:** `pipeline-hatalari.md` (kök dizin) hafif güncel değil.
Faz belgeleri (phases/) Dual R² filtresi metodolojisini içermiyor.
**Fix:** İlgili belgelere bu oturumun bulgularını ekle.

---

## Referans: Bu Proje Skill Kullanımı

Yeni sohbette sprint başlatmadan önce şunları oku:
- `guide/MASTER-SKILL-GUIDE.md` — hangi skill ne zaman kullanılır
- `guide/AGENT-DECISION.md` — subagent ne zaman çağrılır

Sprint kod değişikliklerinde:
- Bug fix → `systematic-debugging` skill (superpowers) otomatik tetiklenir
- Kod yazdıktan sonra → `verification-before-completion` (superpowers)
- Büyük değişiklik → `everything-claude-code:python-reviewer` (agent)
