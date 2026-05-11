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

**Uygulama sırası:** Sprint 1 → Sprint 2 → Sprint 3 — HEPSİ TAMAMLANDI

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
