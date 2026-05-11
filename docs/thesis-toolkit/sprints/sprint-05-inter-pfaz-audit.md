# Sprint 5 — Inter-PFAZ Veri Akışı Audit
## Durum: TAMAMLANDI 2026-05-11 | Öncelik: YÜKSEK

> **Bu sprint neden var:**
> Sprint 1-4 tamamlandı, kod fix'leri yapıldı, `py_compile` ve `import` testleri
> geçti. Ancak pipeline gerçek çalıştırıldığında (PC, 2026-05-04, Elif K) PFAZ 06,
> 08, 10 hala `pending` kaldı, PFAZ 13 `failed`. Sebep: **PFAZ'lar arası veri
> akışında sessiz uyumsuzluklar** — statik testler ile asla yakalanamayan tipte.
>
> **Tetikleyen olay:** Kullanıcı Kemal "selectorda hangi R² kullanılıyor, kolon adı
> uyumlu mu?" sorusunu sordu. Audit sonucu PFAZ 02 → PFAZ 03/08 arasında kolon
> adı drift'i tespit edildi.
>
> **Bağlam dosyaları:**
> - `pc error.md` — gerçek run log (PFAZ 06, 08, 10, 13 sorunları)
> - `claude-hatalarim-ve-dersler.md` KURAL 18 + KURAL 19 — yöntem
> - `phases/faz-03-anfis-egitimi.md` §11.1 — selector niyet beyanı
> - `sprints/SPRINT-PLAN.md` — sprint zinciri

---

## Hedef

**KURAL 19 (yeni eklenen)**: Inter-PFAZ data flow audit.

Tüm PFAZ'lar arası veri alış-verişi (yazılan dosya, okunan dosya, kolon adı,
dosya adı, config key) sistematik taranır ve uyumsuzluklar tespit edilir.

Yöntem:
1. Tüm `to_excel`/`to_csv`/`json.dump` çağrılarını listele
2. Tüm `read_excel`/`read_csv`/`json.load` çağrılarını listele
3. Yazılan dosya adı = okunan dosya adı? (orphan reads)
4. Kolon adı tutarlılığı (`R2_test` vs `Test_R2`, vb.)
5. Config flat (`pfaz0X_*`) vs nested (`pfaz_config[id]`) okuma

---

## Tespit Edilen Bug'lar (BUG-42..BUG-46)

### BUG-42 [YÜKSEK] PFAZ 08 Dashboard Kolon Adı Uyumsuzluğu

**Bulgu:** `model_comparison_dashboard.py` 15+ yerde `df['R2_test']`,
`df['RMSE_test']` arıyor. PFAZ 02 `parallel_ai_trainer.py:1648`
`Test_R2`/`Test_RMSE` yazıyor. KeyError → PFAZ 08 sessizce `pending`.

**Etki:** PC error.md'de PFAZ 08 pending kalma sebebi tam burası.

**Fix:** `load_results()` içine `_normalize_columns()` helper eklendi.
Yükleme sırasında kolon adları dashboard'un beklediği isimlere çevriliyor.
Geri uyumluluk korundu.

**Dosya:** `pfaz_modules/pfaz08_visualization/model_comparison_dashboard.py`

---

### BUG-43 [YÜKSEK] main.py Flat Config Key'leri Çoğu PFAZ'da Okumuyor

**Bulgu:** `config.json`'da hem flat (`pfaz02_ai_training`) hem nested
(`pfaz_config[2]`) key'ler var. main.py'da yalnızca **PFAZ 02** her ikisini
de okuyordu. PFAZ 01, 03-13 sadece nested okuyordu. Sonuç: kullanıcının
config.json'a yazdığı `pfaz03_anfis_training.use_matlab=true` gibi ayarlar
sessizce **ignore** ediliyordu.

**Etki:** TRUBA için yapılan ayarlar (GPU off, n_workers, MATLAB) etkisiz
kalıyordu.

**Fix:** `_get_pfaz_config(pfaz_id)` helper eklendi. 7 PFAZ'da
`config = self.config['pfaz_config'][pfaz_id]` →
`config = self._get_pfaz_config(pfaz_id)` rename. Hibrit flat+nested,
flat öncelikli.

**Dosya:** `main.py` sat. 478, 586, 665, 781, 826, 1015, 1321

---

### BUG-44 [ORTA] Dataset Sizes — `267` int vs `'ALL'` str

**Bulgu:** `config.json` `dataset_sizes=[100, 150, 200, 267]` (int) ama
`dataset_generation_pipeline_v2.py:154` `NOANOMALY_SIZES = {150, 200, 'ALL'}`
(str). Set match başarısız: `267 in {150, 200, 'ALL'}` → `False`.

**Etki:** 267 (= ALL) boyutu için NoAnomaly varyantı üretilmiyordu.

**Fix:** `_FULL_SET_MARKERS = {'ALL', 267, None}` ve `_is_full_set()` helper
eklendi. NOANOMALY_SIZES `{150, 200, 267, 'ALL'}` olarak genişletildi.
4 farklı yerdeki `if n_nuclei == 'ALL'` kontrolü helper'a yönlendirildi.

**Dosya:** `pfaz_modules/pfaz01_dataset_generation/dataset_generation_pipeline_v2.py`

---

### BUG-45 [ORTA] ANFISDatasetSelector — Kod ile Belge Drift

**Bulgu:** `docs/thesis-toolkit/phases/faz-03-anfis-egitimi.md §11.1`:
> "ANFISDatasetSelector — AKTİF (2026-05-08)
> Kota: Top=50, Mid=50, Low=100"

Kodda (`anfis_parallel_trainer_v2.py:1427-1428`):
```python
# ANFISDatasetSelector: deactivated — ANFIS 3-phase strategy covers all datasets
logger.info("[INFO] ANFISDatasetSelector: deactivated (3-phase pilot strategy active)")
```

**Klasik KURAL 18 vakası.** Belge ileri-dönük niyeti not almış, kod aktive
edilmemiş. ANFIS tüm 848 dataset üzerinde çalışmaya devam ediyordu.

**Fix:** Selector `train_all_anfis_parallel` başında, `discover_datasets()`
sonrası aktive edildi:
- Top tier (R²_test ≥ 0.90): 50 dataset
- Mid tier (0.80–0.90): 50 dataset
- **Low tier** (R²_test < 0.80): **100 dataset** ← "ML başarısız → ANFIS dene"
- Toplam: 200 dataset/target

Graceful fallback: FileNotFoundError, ImportError, Exception durumlarında
tüm datasetler kullanılır.

**Dosya:** `pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py`

---

### BUG-46 [YÜKSEK] training_summary — Üç Farklı Dosya Adı

**Bulgu:** PFAZ 02 yazıyor: `training_results_summary.xlsx`. PFAZ 03 selector
arıyor: `training_summary.xlsx`. PFAZ 08 visualizer da `training_summary.xlsx`
arıyor.

**Etki:** Selector aktif edilirse FileNotFoundError. PFAZ 08 viz de "summary
bulunamadı" diyerek atlıyordu.

**Fix:**
- PFAZ 02: İki dosya yaz (`training_summary.xlsx` + `training_results_summary.xlsx`)
- PFAZ 03 selector: Fallback chain (training_summary → training_results_summary → ai_training_summary)
- PFAZ 03 selector kolon adları da normalize edildi (`R2_test` vs `Test_R2`)

**Dosyalar:**
- `pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py` sat. 1657
- `pfaz_modules/pfaz03_anfis_training/anfis_dataset_selector.py` sat. 66+

---

## Tamamlama: BUG-38 Sınıf Default'ları

**Bulgu:** Sprint 4'te BUG-38 belge olarak "DUZELTILDI" işaretliydi (Sprint 1-4
commit'inde DEFAULT_MC_CONFIG 100→1000). Ancak KURAL 18 doğrulaması:

```python
# BootstrapSimulator (sat. 194):
def __init__(self, n_bootstrap: int = 100, ...):  # hala 100!

# NoiseSimulator (sat. 288):
def __init__(self, ..., n_samples_per_level: int = 100, ...):  # hala 100!
```

Sınıf doğrudan çağrılırsa hala 100 kullanıyordu.

**Fix:** Sınıf default'ları da 100 → 1000.

**Dosya:** `pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py`

---

## Bonus: BUG-32 Mirror (Dinamik Test Sayesinde)

**Yakalama yöntemi:** Sprint 5 sonunda `pytest tests/test_integration` çalıştırıldı.
Statik test (`py_compile`) geçmişti, ama integration test:

```
File "pfaz6_final_reporting.py", line 1267
    sys = None
IndentationError: unexpected indent
```

Sprint 4'te BUG-32 yalnızca `automl_retraining_loop.py`'da düzeltilmiş. Aynı
pattern `pfaz6_final_reporting.py:1264-1268`'de hala mevcuttu, PFAZ 06 ve
PFAZ 12 import zincirini bozuyordu.

**Fix:** 5 anlamsız satır silindi. PFAZ 06 ve PFAZ 12 import edilebilir oldu.

**Bu, KURAL 19'un dinamik test bölümünün ne kadar değerli olduğunu kanıtladı.**

---

## Akademik Katkılar (Tez §3.4 için)

### 1. Dual R² Mimari Katmanlılığı
- PFAZ 02: Dual R² filtresi (Shang 2023, Utama 2016) overfit'i eler
- PFAZ 03 Selector: Temizlenmiş listeden tek R²_test ile tabakalı seçim
- **Tez argümanı:** Aynı kontrol iki katmanda tekrarlanmasına gerek yok;
  arşitektürel ayrım metodolojik şeffaflık sağlıyor.

### 2. Adaptive Quota Redistribution
- Selector kotaları (Top=50, Mid=50, Low=100) eğer dolmazsa round-robin
  ile artık kapasiteye dağıtılır.
- "Top tier boş kalırsa ne olur?" senaryosu **zaten kod tarafından çözülmüş**.
- **Tez argümanı:** Hedef seçim sayısı (200 dataset/hedef) mevcut model
  dağılımı ne olursa olsun garanti altında.

---

## Yeni Kurallar (claude-hatalarim-ve-dersler.md'ye eklendi)

### KURAL 19: Inter-PFAZ Data Flow Audit

Major değişiklik sonrası **5 grep komutu seti** ile sistematik kontrol:
1. Yazılan dosyalar
2. Okunan dosyalar
3. Dosya adı tutarlılığı (orphan reads)
4. Kolon adı tutarlılığı
5. Config flat vs nested

**Statik vs dinamik test farkı:**

| Test Tipi | Kategori | Yakalar |
|-----------|----------|---------|
| `py_compile` | Statik | Syntax error |
| `import test` | Statik | ImportError |
| Unit test | Statik+Dinamik | Modül içi hatalar |
| Inter-PFAZ audit | Statik | Kolon/dosya adı drift |
| **pytest tests/test_smoke** | **Dinamik** | **Runtime davranış** |

**Sonuç:** Statik testler **gerekli ama yetersiz**. Dinamik test (pytest)
de çalıştırılmalı.

### KURAL 6 (sonradan eklendi, BUG numara çakışması üzerine)

Yeni bug numarası vermeden önce:
```bash
grep -oE "^### BUG-[0-9]+" pipeline-hatalari.md | sort -V | tail -3
```
ile son numarayı doğrula. **Sprint 5'te ben bu kuralı ihmal ettim**, BUG-13..17
çakıştı, BUG-42..46 olarak yeniden numaralandırıldı (commit `4c32820`).

---

## Test ve Doğrulama

### Smoke Test (sandbox)
```
pytest tests/test_smoke -v
==================== 8 passed in 4.86s ====================
```

### Integration Test (sandbox)
```
pytest tests/test_integration -v
==================== 38 passed, 5 failed ====================
```
5 fail: opsiyonel paket eksiği (tqdm, keras, statsmodels) — TRUBA'da çözülecek.

---

## Sprint 5 → Sprint 6 Geçişi

Sprint 5'te 5 bug daha bulundu, ancak **8 kategori daha tarama yapılmadı**:
- Hardcoded path (Linux/Windows)
- Optional imports try/except
- Excel sheet name 31 char
- n_jobs nested parallelism
- Silent exception swallowing
- Encoding UTF-8
- Memory leak (TF/Torch)
- Doc iddiaları vs gerçek artifact

Bu 8 kategori **Sprint 6**'da Claude Code paralel agent'larıyla tarancak
(F1 prompt hazır, `outputs/01_F1_AGENT_PROMPT.md`).

---

## Etkilenen Dosyalar (Final Liste)

```
Kod:
  - main.py (BUG-43)
  - pfaz_modules/pfaz01_dataset_generation/dataset_generation_pipeline_v2.py (BUG-44)
  - pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py (BUG-46)
  - pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py (BUG-45)
  - pfaz_modules/pfaz03_anfis_training/anfis_dataset_selector.py (BUG-46)
  - pfaz_modules/pfaz06_final_reporting/pfaz6_final_reporting.py (BUG-32 mirror)
  - pfaz_modules/pfaz08_visualization/model_comparison_dashboard.py (BUG-42)
  - pfaz_modules/pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py (BUG-38 tamamlama)

Doc:
  - docs/thesis-toolkit/pipeline-hatalari.md
  - docs/thesis-toolkit/tez-yazim-not-defteri.md
  - docs/thesis-toolkit/claude-hatalarim-ve-dersler.md
```

---

## Referanslar

- **Sprint 4 retrospektif belge** — `sprints/sprint-04-truba-hazirlik.md`
- **KURAL 18, 19** — `claude-hatalarim-ve-dersler.md`
- **pc error.md** — gerçek run log
- **Sprint 5 commits** — `21a82a9` … `e7614c2` (hpcv1 truba-fixes branch)
- **BUG numara çakışması düzeltme** — commit `4c32820` (Sprint 6 hazırlık)

---

*Sprint 5 v1.0 | 2026-05-11 | Inter-PFAZ Data Flow Audit (KURAL 19 uygulaması)*
