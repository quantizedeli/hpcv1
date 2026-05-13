# Sprint 10 — TRUBA QA Raporu Düzeltmeleri
**Tarih:** 2026-05-13
**Durum:** TAMAMLANDI
**Branch:** `sprint10-qa-report-fixes`
**Tetikleyici:** Kemal'in `nucdatav2-truba` lokal kopyasında çıkardığı statik QA raporu

---

## Bağlam

Kemal bağımsız bir statik QA taraması yaptı (`sprint6-scan-results` branch, yerel `nucdatav2-truba/` kopya). Raporu 7 bulgu ile geri getirdi: 3 kritik (PFAZ13 path, Job 3/4 exit, eski script), 4 orta seviye (worker, path stratejisi, data_file, training_configs_50.json).

Sprint 10 görevi: bulguları doğrula, ek bulgu varsa ekle, kod ve dokümanları senkron et.

---

## Doğrulama Süreci

Tüm 7 raporu bulgusu bağımsız doğrulandı:

| Bulgu | Doğrulama Yöntemi | Sonuç |
|-------|-------------------|-------|
| 1: PFAZ13 path | `sed main.py:1290-1345`, `pfaz_outputs` map analizi | DOGRULANDI |
| 2: Job 3/4 exit | `tail truba/slurm_jobs/*.sh` | DOGRULANDI |
| 3: run_complete_pipeline | `grep "from " imports`, dir comparison | DOGRULANDI |
| 4: Worker tutarsızlık | `gpu_manager.py:180-200`, config.json:82 | DOGRULANDI + ek bulgu |
| 5: Path stratejisi | `grep SLURM_SUBMIT_DIR vs PROJECT_DIR` | DOGRULANDI |
| 6: data_file | `python3 -c "json.load(config)" → top-level kontrol` | DOGRULANDI |
| 7: training_configs_50.json | `find . -name "*.json"`, fallback grep | DOGRULANDI |

## Claude'un Ekstra Bulguları (Rapor Atladı)

### Ek A — BUG-66: PFAZ13 metadata-aware CSV okuma yok
Rapor sadece path düzeltmeyi önerdi. Path düzelse bile PFAZ13 hâlâ çöker — çünkü PFAZ1 headerless CSV yazıyor, PFAZ2 metadata.json'dan kolon adları alıyor, ama PFAZ13 default `pd.read_csv(train_csv)` kullanıyor.

**Fonksiyonel test:**
```
Eski yöntem  -> 'MAGNETIC MOMENT [µ]' bulundu: False
Yeni yöntem -> 'MAGNETIC MOMENT [µ]' bulundu: True
```

### Ek B — Slurm dependency chain yok
`afterok` chain yok — README "Job 3 bittikten sonra Job 4'ü gönder" diyor. Kullanıcı `sacct`/mail'e güveniyor → exit 0 yanıltıcılığı (BUG-68) gerçek risk.

### Ek C — BUG-70: HPC_MODE worker limiti gerçek performans kaybı
Rapor "config notu güncellenmeli" dedi. Asıl sorun farklı: TRUBA 110-cpu → kod 16 worker → kaynak %14 kullanım → koşu 7x uzar → 3-gün limit riski. HPC_MODE flag'i gpu_manager.py'de hiç kontrol edilmiyordu.

## Sprint 10 Bug Listesi (BUG-65..72)

| Bug | Seviye | Dosya | Açıklama |
|-----|--------|-------|----------|
| BUG-65 | KRITIK | main.py:1305 | PFAZ13 dataset path -> generated_datasets/{name} |
| BUG-66 | KRITIK | main.py:1336 | PFAZ13 metadata-aware CSV okuma (eklendi) |
| BUG-67 | ORTA | main.py:1470 | PFAZ13 bos AutoML acik status (`skipped_no_*`) |
| BUG-68 | KRITIK | truba/slurm_jobs/job3.sh, job4.sh | exit 0 -> exit $FAIL + ${PIPESTATUS[0]} |
| BUG-69 | ORTA | run_complete_pipeline.py | Deprecated guard (sys.exit(2)) |
| BUG-70 | KRITIK | utils/gpu_manager.py:181-199 | HPC_MODE=1 ise n-2 worker |
| BUG-71 | ORTA | config.json | Top-level data_file: data/aaa2.txt |
| BUG-72 | DUSUK | config.json | parallel_training._note guncellendi |

## Doğrulama Sonuçları

- `py_compile main.py` → OK
- `py_compile utils/gpu_manager.py` → OK
- `py_compile run_complete_pipeline.py` → OK
- `json.load(config.json)` → OK
- `bash -n job3*.sh` → OK
- `bash -n job4*.sh` → OK
- pytest tests/test_smoke → 8 passed
- PFAZ13 fonksiyonel mini-test → CSV doğru okundu, kolonlar bulundu

## Etkilenen Dosyalar

| Dosya | Değişiklik | Bug |
|-------|-----------|-----|
| main.py | PFAZ13 path + metadata-aware CSV + status | BUG-65, 66, 67 |
| utils/gpu_manager.py | HPC_MODE branş | BUG-70 |
| run_complete_pipeline.py | Deprecated guard | BUG-69 |
| config.json | data_file + worker notları | BUG-71, 72 |
| truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh | FAIL + PIPESTATUS + exit $FAIL | BUG-68 |
| truba/slurm_jobs/job4_pfaz06_08_10.sh | FAIL + PIPESTATUS + exit $FAIL | BUG-68 |
| docs/thesis-toolkit/pipeline-hatalari.md | BUG-65..72 dokümantasyon | doc |
| docs/thesis-toolkit/sprints/SPRINT-PLAN.md | Sprint 10 satırı | doc |
| docs/thesis-toolkit/sprints/sprint-10-qa-fixes.md | Bu dosya | doc |
| docs/thesis-toolkit/tez-yazim-not-defteri.md | Sprint 10 özeti | doc |
| docs/thesis-toolkit/claude-hatalarim-ve-dersler.md | KURAL 26, 27 | doc |
| docs/thesis-toolkit/CLAUDE.md | Pipeline status güncelle | doc |



## PFAZ11 Hakkinda Karar (2026-05-13)

Kemal: "Faz11 i kullanmiyoruz daha sonra."

PFAZ11 (Production Deployment) zaten kod seviyesinde **kalici skip** durumunda:
- `run_pfaz_11()` her cagrildiginda `status='skipped'` doner (main.py:1057)
- `run_all_phases()` icinde PFAZ11 otomatik `mode='pass'` zorlanir (main.py:1758)
- Inter-PFAZ bagimlilik tablosunda PFAZ11'i kullanan baska faz YOK

Bu karar Sprint 10'da degismedi -- mevcut davranis korundu. PFAZ11 dosyalari ve modulu repo'da kalir ama pipeline'da otomatik atlanir. Proje sonrasi (tez sonrasi) tekrar acilmasi planlaniyor (`run_pfaz_11` reason field: "PFAZ11 deferred per user request - will be implemented after project completion").

**TRUBA icin etkisi yok:** Slurm scriptleri PFAZ11'i listesinde tutmuyor (Job 1-4 PFAZ1-10/12/13'u kapsiyor). PFAZ11 koda ait kalir ama execution graph'tan disaridadir.

## Açık Olanlar (Sprint 10'da KAPSAM DIŞI)

- **training_configs_50.json üretimi** (raporun 7. bulgusu): Şimdilik default config fallback kabul. Tez için deterministiklik isteniyorsa seed'li üretim eklenmeli (Sprint 11 adayı).
- **Slurm `--dependency=afterok` chain**: Sprint 10'da manuel sıralı zincir korundu. Otomatik chain için ayrı sprint planı gerekli (Sprint 11 adayı).
- **v10 sync**: Sprint 10 fix'leri v10'a henüz taşınmadı. BUG-65/66/67 sadece hpcv1'de var (PFAZ13 v10'da farklı durumda mı kontrol edilmeli). Sprint 11A v10 sync.

## TRUBA'ya Almadan Önce Final Kontrol Listesi

ZORUNLU (Sprint 10'da kapatıldı):
- [x] PFAZ13 dataset path düzeltildi
- [x] PFAZ13 metadata-aware CSV okuma eklendi
- [x] Job 3/4 exit kodu propagation
- [x] HPC_MODE worker limiti (108 worker)
- [x] data_file top-level config
- [x] run_complete_pipeline.py guard

YAPILMASI ONERILEN (Sprint 10'da kapalı değil):
- [ ] training_configs_50.json deterministik üretim
- [ ] Slurm --dependency=afterok chain
- [ ] v10 sync (BUG-65..72)

## Patch

`sprint10-qa-fixes.patch` — Kemal Desktop\hpcv1\ klasörüne koyar, sonra:
```powershell
git checkout truba-fixes
git am sprint10-qa-fixes.patch
git push origin truba-fixes
```

---

*Sprint 10 v1.0 | 2026-05-13 | TRUBA QA raporu + 3 ek bulgu | 8 bug fix*
