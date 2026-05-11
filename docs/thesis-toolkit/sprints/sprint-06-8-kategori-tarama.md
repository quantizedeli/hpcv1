# Sprint 6 — 8 Kategori Kapsamlı Tarama
**Tarih:** 2026-05-12  
**Dal:** truba-fixes → sprint6-scan-results  
**Commit:** 65a6174  
**Durum:** TAMAMLANDI

---

## Hedef

Pipeline genelinde 8 farklı hata kategorisinde sistematik bug taraması.
Her kategori için ayrı bir subagent paralel çalıştırıldı (8 ajan, background=True).

---

## 8 Kategori ve Agent Sonuçları

| Ajan | Kategori | Bulgular |
|------|----------|---------|
| Agent 1 | Hardcoded paths (C:\\, /mnt/, /home/, sys.path literal) | 2 TRUBA-CRITICAL |
| Agent 2 | Optional imports — try/except eksik + _AVAILABLE flag yok | 2 KRITIK |
| Agent 3 | Excel sheet names > 31 char veya truncation eksik | 2 YUKSEK |
| Agent 4 | n_jobs=-1 nested ThreadPool/ProcessPool context | 0 (temiz) |
| Agent 5 | Silent exception swallowing (bare except, except: pass) | 3 KRITIK/YUKSEK |
| Agent 6 | open() encoding='utf-8' eksik | 0 (temiz — önceki QA kapsamış) |
| Agent 7 | TF/Torch model.fit() finally/clear_session/gc eksik | 2 KRITIK |
| Agent 8 | Dokümantasyon iddiası vs gerçek çıktı sayısı | 4 TASARIM/ORTA |

---

## Bulunan Buglar (BUG-47 .. BUG-61)

| BUG # | Öncelik | Dosya | Açıklama |
|-------|---------|-------|----------|
| BUG-47 | TRUBA-CRITICAL | `analysis_modules/real_data_integration_manager.py:28-29` | `sys.path.insert(0, '/home/claude')` + `'/mnt/user-data/outputs'` hardcoded |
| BUG-48 | TRUBA-CRITICAL | `visualization_modules/visualization_integration.py:31` | `sys.path.insert(0, '/mnt/user-data/outputs')` hardcoded |
| BUG-49 | KRITIK | `pfaz_modules/pfaz02_ai_training/advanced_models_extended.py:16-20` | torch import 5 satır — try/except yok, TORCH_AVAILABLE flag yok |
| BUG-50 | YUKSEK | `pfaz09_aaa2_monte_carlo/aaa2_control_group_complete_v4.py:29` + `monte_carlo_simulation_system.py:31` | `from tqdm import tqdm` — try/except yok |
| BUG-51 | YUKSEK | `pfaz08_visualization/visualization_master_system.py:1492` | Sheet adı `'Robustness_CV_Results'` ama PFAZ6 `'Robustness_CV'` yazıyor — orphan read |
| BUG-52 | YUKSEK | `pfaz06_final_reporting/comprehensive_excel_reporter.py:210,223` | `f'{target}_Sonuclar'` ve `f'{config_id}_Detay'` — dinamik şablon, `[:31]` truncation yok |
| BUG-53 | KRITIK | `pfaz02_ai_training/hyperparameter_tuner.py:423,436` + `pfaz13_automl/automl_optimizer.py:289` + `automl_hyperparameter_optimizer.py:276` | model.fit() sonrası finally/clear_session/gc.collect eksik — memory leak |
| BUG-54 | ORTA | `pfaz07_ensemble/stacking_ensemble.py:312` | stacking MLP fit — finally/clear_session yok |
| BUG-55 | KRITIK | `pfaz13_automl/automl_retraining_loop.py:211` | `except Exception: pass` — dataset yükleme hatası sessizce yutulur |
| BUG-56 | YUKSEK | `pfaz13_automl/automl_retraining_loop.py:305` | `except Exception: pass` — config okuma hatası sessizce yutulur |
| BUG-57 | YUKSEK | `pfaz13_automl/automl_retraining_loop.py:758` | `except Exception: pass` — rapor yazma hatası sessizce yutulur |
| BUG-58 | TASARIM | `CLAUDE.md:100` | "29-sheet Excel" iddiası — gerçekte 18 sheet (PFAZ 6 ComprehensiveExcelReporter) |
| BUG-59 | TASARIM | `CLAUDE.md:101` | "70+ chart types" — saydırılabilir plot sayısı 52, 70+ iddia abartılı |
| BUG-60 | ORTA | `PFAZ_DEVELOPMENT_NOTES.md` | PFAZ 13 "AutoML stacking R²=0.9794" iddiası — bu PFAZ 7 ensemble sonucu, yanlış faza atfedilmiş |
| BUG-61 | TASARIM | `QA_PROJECT_STATUS_REPORT.md` | "Bare except remaining: 0" iddiası — Sprint 6 Agent 5 BUG-55/56/57 buldu |

---

## Özet İstatistikler

| Öncelik | Adet |
|---------|------|
| TRUBA-CRITICAL | 2 |
| KRITIK | 3 |
| YUKSEK | 4 |
| ORTA | 2 |
| TASARIM | 4 |
| **Toplam** | **15** |

Temiz kategoriler (0 bug): n_jobs nested (Ajan 4), open() encoding (Ajan 6)

---

## Metodoloji Notu

Bu sprint **KURAL 20**'yi uyguladı: 8 agent tek mesajda paralel background=True ile
başlatıldı. ~8 dakikada tüm scan tamamlandı (seriyal olsaydı ~40 dk).

Her agent:
1. Kendi kategorisi için 100+ Python dosyayı grep ile taradı
2. Bulguları öncelik sıralamasıyla raporladı
3. Fix önerisi ile birlikte sundu

---

## Tamamlanan Dosya Güncellemeleri

- [x] `pipeline-hatalari.md` — BUG-47..BUG-61 blokları eklendi
- [x] `tez-yazim-not-defteri.md` — v2.3 Sprint 6 özeti eklendi
- [x] `claude-hatalarim-ve-dersler.md` — KURAL 20 + KURAL 21 eklendi
- [x] `SPRINT-PLAN.md` — Sprint 6 TAMAMLANDI, Sprint 7 satırı eklendi
- [x] `sprint-06-8-kategori-tarama.md` — Bu dosya
- [x] `sprint-07-bug-fixes.md` — Sprint 7 planı oluşturuldu
- [x] `QA_PROJECT_STATUS_REPORT.md` — Sprint 6 bölümü eklendi
- [x] `QA_WIRING_REPORT.md` — Sprint 6 wiring bulguları eklendi

---

*Sprint 6 tamamlandı | 15 yeni bug (BUG-47..BUG-61) | 2026-05-12*
