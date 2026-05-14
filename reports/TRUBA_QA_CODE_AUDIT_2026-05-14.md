# TRUBA QA Kod Denetim Raporu

Tarih: 2026-05-14  
Repo yerel dizin: `c:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba`  
Branch: `sprint6-scan-results`  
Onceki rapor: `reports/TRUBA_QA_CODE_AUDIT_2026-05-13.md`

## Kapsam

Bu denetim onceki TRUBA QA raporunun tekrar kontrolunu, Sprint 10/11/12 patch izlerinin etkisini, Slurm exit-code davranisini, PFAZ orkestrasyonunu, dependency kontrollerini ve tez/reproducibility rehberleriyle uyumu kapsar.

Ek olarak okunan rehber klasorleri:

- `docs/thesis-toolkit/guide`: `MASTER-SKILL-GUIDE.md`, `AGENT-DECISION.md`, `SKILL-COMBOS.md`
- `skills`: `INDEX.md` ve 8 rehber dosyasi

Bu rehberlerden bu denetimde kullanilan ana cerceve: Python ML code review, silent-failure hunting, verification-before-completion, TRUBA/HPC calistirilabilirlik, akademik reproducibility.

## Calistirilan Dogrulamalar

```powershell
git status --short --branch
python -m pytest tests/test_smoke tests/test_integration/test_module_imports.py -q --tb=short -p no:cacheprovider
python main.py --check-deps
python -c "import optuna, lightgbm, catboost; ..."
```

Sonuc:

- Aktif branch: `sprint6-scan-results`
- Smoke/import testleri: `32 passed`
- `main.py --check-deps`: 13 temel paket mevcut
- Yerel ortamda `catboost` eksik; komut `ModuleNotFoundError: No module named 'catboost'` ile durdu
- `requests` tarafinda lokal uyarı goruldu: `urllib3` / `chardet` / `charset_normalizer` uyumsuzlugu

Not: Uzun sureli PFAZ kosulari lokal calistirilmadi. TRUBA moduluyle birebir paket durumu lokal ortamdan farkli olabilir.

## Genel Sonuc

Onceki rapordaki kritik maddelerin onemli bir kismi repo icinde duzeltilmis:

- PFAZ13 dataset path map'i artik `generated_datasets/{dataset}` tarafina gidiyor.
- PFAZ13 headerless CSV + `metadata.json` okuma destegi eklenmis.
- `config.json` top-level `"data_file": "data/aaa2.txt"` ile hizalanmis.
- HPC worker limiti `HPC_MODE=1` icin `n - 2` olacak sekilde guncellenmis.
- Job 3 ve Job 4 faz hatalarini artik `FAIL` ile non-zero exit'e tasiyor.
- `training_configs_50.json` artik repo icinde var.
- `submit_all.sh` `afterok` zinciri kuruyor.

Buna ragmen TRUBA icin hala duzeltilmesi gereken iki kritik risk var:

1. Job 1, Job 2 ve tek parca `truba_slurm_job.sh` `python | tee` sonrasi `$?` kullaniyor; Bash'te bu `python` degil `tee` exit kodudur.
2. `main.py --run-all` non-interactive/HPC modda faz hatalarini yakalayip devam ediyor ve finalde exception firlatmiyor; tek parca Slurm job basarisiz faza ragmen basarili gorunebilir.

## Kritik Bulgular

### 1. Job 1, Job 2 ve tek parca job Python hatasini Slurm'a tasimayabilir

Dosyalar:

- `truba/slurm_jobs/job1_pfaz01.sh:54-55`
- `truba/slurm_jobs/job2_pfaz02_03.sh:54-60`
- `truba_slurm_job.sh:89-94`

Kod deseni:

```bash
python3 -u main.py --pfaz 1 2>&1 | tee "$OUTPUT_DIR/logs/pfaz01_${SLURM_JOB_ID}.log"
EXIT_CODE=$?
```

Bash'te `pipefail` yoksa `$?` pipeline'in son komutu olan `tee` icin doner. `python3` fail olsa bile `tee` basariliysa exit `0` olabilir.

Etkisi:

- Job 1 veya Job 2 gercekte kirilsa bile `submit_all.sh` icindeki `afterok` zinciri sonraki job'u baslatabilir.
- `sacct` ve mail bildirimi yaniltici olur.
- Job 2'de PFAZ2/PFAZ3 hatasi maskelenirse Job 3 eksik model ciktilariyla baslayabilir.

Oneri:

Job 3/4'teki desen Job 1/2 ve tek parca job'a da uygulanmali:

```bash
python3 -u main.py --pfaz 1 2>&1 | tee "$OUTPUT_DIR/logs/pfaz01_${SLURM_JOB_ID}.log"
EXIT_CODE=${PIPESTATUS[0]}
```

Alternatif olarak dosya basina `set -o pipefail` eklenebilir; yine de `PIPESTATUS[0]` daha acik.

### 2. `main.py --run-all` faz hatalarini basarili process exit'e cevirebilir

Dosya: `main.py`

Ilgili noktalar:

- `main.py:1762`: `run_all_pfaz`
- `main.py:1860-1867`: faz exception yakalaniyor, HPC/non-interactive modda devam ediliyor
- `main.py:1910`: `return results`
- `main.py:2259`: CLI `--run-all` sonucu kontrol etmiyor

Davranis:

Tek tek `--pfaz N` calistirmada faz method exception firlatirsa `main()` en sonda `sys.exit(1)` yapabilir. Fakat `--run-all` icinde faz exception'i yakalaniyor; HPC modda sadece warning yazilip devam ediliyor. Sonunda `run_all_pfaz` normal donuyor.

Etkisi:

- Tek parca `truba_slurm_job.sh` icin en riskli yol budur.
- PFAZ2/PFAZ13 gibi ara fazlar kirilsa bile process exit `0` olabilir.
- Final output eksik veya kismi oldugu halde Slurm job basarili gorunebilir.

Oneri:

`run_all_pfaz` icinde `failed_phases` listesi tutulmali. HPC/non-interactive modda devam edilebilir, fakat sonda failure varsa:

```python
if failed_phases:
    raise RuntimeError(f"Failed PFAZ phases: {failed_phases}")
```

Eger "devam et ama exit 0" bilincli isteniyorsa CLI'a ayri `--continue-on-error` bayragi eklenmeli.

### 3. Dependency check PFAZ2/PFAZ13 kritik paketlerini kapsamiyor

Dosyalar:

- `main.py:64-83`: `AutoInstaller.REQUIRED_PACKAGES`
- `requirements.txt:15-24`
- `requirements-hpc.txt:20-29`
- `pfaz_modules/pfaz13_automl/automl_optimizer.py:12-19`
- `pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py:68-84`

`python main.py --check-deps` su an 13 temel paketi kontrol ediyor, fakat `optuna`, `lightgbm`, `catboost` bu listede yok. Requirements dosyalarinda ise bu paketler var.

Yerel dogrulama:

```text
ModuleNotFoundError: No module named 'catboost'
```

Etkisi:

- PFAZ13 `optuna` yoksa `status: skipped` donuyor ama faz tamamlanmis gibi isaretleniyor.
- PFAZ2 LightGBM/CatBoost yoksa ilgili model aileleri sessizce devre disi kalabilir.
- `--check-deps` "Tum kutuphaneler mevcut" dedigi halde TRUBA kosusunda beklenen model/AutoML kapsami azalabilir.

Oneri:

`AutoInstaller.REQUIRED_PACKAGES` en azindan su paketleri de kontrol etmeli:

```python
'lightgbm': 'lightgbm',
'optuna': 'optuna',
```

`catboost` TRUBA'da opsiyonel kalacaksa `--check-deps --strict` veya raporda "optional missing" olarak ayrilmali. Config'te `CatBoost` etkin oldugu icin su an tamamen opsiyonel saymak tutarsiz.

### 4. PFAZ13 `skipped` durumlarini process failure'a cevirmiyor

Dosya: `main.py`

Ilgili noktalar:

- `main.py:1310-1313`: `optuna` yoksa `status_manager` completed yapiliyor ve `{'status': 'skipped'}` donuyor
- `main.py:1501-1503`: `skipped_no_pfaz2_results` / `skipped_no_datasets`
- `main.py:1517-1519`: yine `completed` olarak isaretleniyor

Sprint 10'da status acik raporlanmis; bu iyi. Ancak Slurm/CLI seviyesinde bu durum hala basarili kabul ediliyor.

Etkisi:

- PFAZ13 bilimsel olarak uretilmemis olsa bile Job 3 `exit 0` alabilir.
- PFAZ6 final raporu AutoML bolumunu eksik/kismi alir.

Oneri:

PFAZ13 icin kabul edilebilir minimum basari kriteri tanimlanmali. Ornegin:

- `optuna` yoksa hard failure
- `best_by_target` bos ise hard failure
- `automl_results` bos ise hard failure
- `targets_optimized` beklenen hedefleri kapsamiyorsa warning veya failure

TRUBA final kosusunda bu kriterler `config.json` ile `strict_truba: true` gibi kontrol edilebilir.

## Orta Seviye Bulgular

### 5. `run_complete_pipeline.py` hala guncel paket yapisiyla uyumsuz

Dosya: `run_complete_pipeline.py`

Eski import path'leri hala mevcut:

- `dataset_generation.dataset_generator`
- `ai_training.model_trainer`
- `anfis_training.anfis_operator`
- `visualization.visualization_system`
- `reporting.reporting_system`

Etkisi:

- Yanlislikla calistirilirse erken kirilir.
- README veya aliskanlikla bu dosya kullanilirsa TRUBA job kaybi olur.

Oneri:

Dosyanin en ustune hard stop eklenmeli:

```python
raise SystemExit("Deprecated: use main.py or truba/slurm_jobs/submit_all.sh")
```

Ya da guncel `pfaz_modules/...` import yapisina tasinmali.

### 6. Split job path'leri hala sabit `/arf/home/ahmacar/hpcv1`

Dosyalar:

- `truba/slurm_jobs/job1_pfaz01.sh`
- `truba/slurm_jobs/job2_pfaz02_03.sh`
- `truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh`
- `truba/slurm_jobs/job4_pfaz06_08_10.sh`

Split job'lar:

```bash
PROJECT_DIR="/arf/home/ahmacar/hpcv1"
OUTPUT_DIR="/arf/scratch/ahmacar/hpcv1_outputs"
```

Tek parca job ise `SLURM_SUBMIT_DIR` kullaniyor. Bu bilincli olabilir ama deployment varsayimini sertlestiriyor.

Oneri:

`PROJECT_DIR="${PROJECT_DIR:-/arf/home/ahmacar/hpcv1}"` ve `OUTPUT_DIR="${OUTPUT_DIR:-/arf/scratch/ahmacar/hpcv1_outputs}"` desenine gecilmeli. Boylece varsayilan korunur, farkli klon dizini icin env override mumkun olur.

### 7. `config.json` icinde `data.input_file` eski degerde kaliyor

Dosya: `config.json`

- Top-level: `"data_file": "data/aaa2.txt"` dogru.
- Nested: `"data": { "input_file": "aaa2.txt" }` eski.

Ana PFAZ akisi top-level `data_file` okudugu icin kritik degil. Ancak `automl_retraining_loop.py` config fallback'inde nested `data.input_file` okuyor. `run_pfaz_13` explicit `_aaa2_path` verdigi icin mevcut ana akista sorun beklenmiyor.

Oneri:

Dokuman/kod drift'ini azaltmak icin nested alan da `"input_file": "aaa2.txt"` yerine `"input_file": "aaa2.txt"` + `paths.data_dir=data` ile acik tutulmali veya tamamen top-level `data_file` tek kaynak yapilmali.

### 8. Yerel dependency ortaminda `requests` uyumsuzluk uyarisi var

`pytest` ve `--check-deps` sirasinda:

```text
RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.4.3)/charset_normalizer (3.4.3) doesn't match a supported version
```

Etkisi:

- Bu proje ana akista network agirlikli gorunmuyor, bu yuzden TRUBA icin kritik degil.
- Yine de reprodukcibilite raporunda lokal ortam kirliligi olarak not edilmeli.

Oneri:

TRUBA'da module/venv temizse sorun olmayabilir. Lokal dogrulama icin `pip check` calistirilip requirements pin'leri gozden gecirilmeli.

## Onceki Rapor Bulgularinin Guncel Durumu

| Onceki bulgu | Durum | Kanit |
|---|---|---|
| PFAZ13 dataset path hatasi | Duzeltilmis | `main.py:1331-1332` |
| Job 3/4 kosulsuz `exit 0` | Duzeltilmis | `job3: FAIL`, `job4: FAIL` |
| `run_complete_pipeline.py` eski import | Devam ediyor | Eski importlar halen var |
| Worker sayisi config/kod uyumsuzlugu | Buyuk olcude duzeltilmis | `GPUManager.optimal_workers`, `HPC_MODE=1 -> n-2` |
| Tek parca vs split path farki | Devam ediyor | Split job sabit path, tek parca `SLURM_SUBMIT_DIR` |
| Veri path uyumsuzlugu | Ana akista duzeltilmis | top-level `data_file: data/aaa2.txt` |
| `training_configs_50.json` yok | Duzeltilmis | Dosya repo icinde mevcut |

## Olumlu Kontroller

- `submit_all.sh` `afterok` zinciri kuruyor.
- Job 3/4 `PIPESTATUS[0]` kullaniyor.
- `HPC_MODE=1` ile worker kullanimi TRUBA kaynaklarina uyarlanmis.
- `PFAZ11` otomatik skip kalmis; CPU batch hedefi icin uygun.
- `THESIS_COMPILE_PDF=n` Job 4'te set ediliyor; LaTeX toolchain eksikliginden job kirilma riski azaltilmis.
- Smoke/import testleri geciyor: `32 passed`.
- `config.json` top-level data path'i `data/aaa2.txt`.

## TRUBA Oncesi Zorunlu Checklist

1. Job 1, Job 2 ve `truba_slurm_job.sh` icin `$?` yerine `${PIPESTATUS[0]}` kullan.
2. `main.py --run-all` icinde faz hatasi varsa finalde non-zero process exit uret.
3. `--check-deps` kapsamına `optuna`, `lightgbm` ve config etkinse `catboost` ekle.
4. PFAZ13 `skipped` durumlarini TRUBA strict modda hard failure yap.
5. `run_complete_pipeline.py` dosyasini deprecated hard-stop ile isaretle veya guncelle.

## Onerilen TRUBA Calistirma

Tek parca job yerine split zincir tercih edilmeli:

```bash
cd /arf/home/ahmacar/hpcv1
bash setup_truba.sh
bash truba/slurm_jobs/submit_all.sh
```

Ilk duzeltmeler yapilmadan `submit_all.sh` da tam guvenli degil; Job 1/2 pipeline exit kodu maskelenirse `afterok` yaniltici olabilir.

## Nihai Degerlendirme

Repo onceki rapora gore belirgin sekilde daha TRUBA-ready durumda. Ancak "Slurm basarili gorundu ama icerik eksik" riskinin iki ana kaynagi hala duruyor: pipe exit kodlari ve `--run-all` hata yutma davranisi. Bunlar duzeltilmeden uzun TRUBA kosusu baslatilmamali.
