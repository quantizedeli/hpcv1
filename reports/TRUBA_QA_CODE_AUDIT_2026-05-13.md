# TRUBA QA Kod Denetim Raporu

Tarih: 2026-05-13  
Repo: `https://github.com/quantizedeli/hpcv1.git`  
Branch: `sprint6-scan-results`  
Yerel dizin: `c:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba`

## Kapsam

Bu rapor TRUBA'ya almadan önce kodun ve çalıştırma akışının statik QA incelemesini kapsar. İnceleme özellikle şu başlıklara odaklandı:

- `main.py` orkestratörü ve PFAZ 1-13 bağlantıları
- TRUBA/SLURM betikleri
- `config.json`, `requirements*.txt`, veri ve çıktı path varsayımları
- Fazlar arası dosya bağımlılıkları
- Import/smoke test seviyesi doğrulama

## Doğrulanan Komutlar

```powershell
git status --short --branch
git remote -v
python -m pytest tests/test_smoke tests/test_integration/test_module_imports.py -q --tb=short -p no:cacheprovider
python main.py --check-deps
```

Sonuç:

- Aktif branch: `sprint6-scan-results`
- Remote: `origin https://github.com/quantizedeli/hpcv1.git`
- Smoke/import testleri: `32 passed`
- `main.py --check-deps`: lokal Python ortamında gerekli 13 temel paket mevcut

Not: Testler yalnızca import ve temel sanity seviyesindedir. Uzun süreli PFAZ koşuları lokal olarak çalıştırılmadı.

## Genel Sonuç

Repo TRUBA için ana hatlarıyla hazırlanmış durumda; `main.py` güncel orkestratör olarak kullanılmalı. `config.json` çıktıları `/arf/scratch/ahmacar/hpcv1_outputs` altına yönlendiriyor ve split job dosyaları da aynı scratch yolunu kontrol ediyor.

Ancak TRUBA'ya göndermeden önce düzeltilmesi veya bilinçli kabul edilmesi gereken birkaç risk var. En önemlileri:

1. PFAZ13 ilk AutoML geçişi yanlış dataset path'i okuyor; optimizasyon sessizce boş geçebilir.
2. Job 3 ve Job 4 hata alsa bile `exit 0` ile başarılı görünebilir.
3. `run_complete_pipeline.py` güncel paket yapısıyla uyumsuz eski import path'leri içeriyor; kullanılmamalı.
4. `config.json` içinde 100 worker yazmasına rağmen kod PFAZ2/PFAZ3 worker sayısını `GPUManager` üst sınırlarıyla 16/20 civarında sınırlar.

## Kritik Bulgular

### 1. PFAZ13 Dataset Path Hatası

Dosya: `main.py`

İlgili noktalar:

- `main.py:1305`: `ds_dir = metrics_file.parent.parent.parent`
- `main.py:1328`: `train_csv = ds_path / 'train.csv'`
- `main.py:1336`: `train_df = pd.read_csv(train_csv)`

PFAZ2 model sonuç yapısı şu şekilde:

```text
trained_models/{dataset}/{model_type}/{config}/metrics_*.json
```

`metrics_file.parent.parent.parent` bu nedenle `trained_models/{dataset}` dizinine gider. Fakat `train.csv` ve `val.csv` gerçek dataset ağacında, yani `generated_datasets/{dataset}` altında bulunur. Bu yüzden PFAZ13'ün ilk AutoML optimizasyon bloğu çoğu koşuda:

```text
[PFAZ13] CSV bulunamadi: ...
```

ile geçilir ve `automl_summary.json` boş kalabilir.

Etkisi:

- PFAZ13 job exit olarak başarılı görünebilir.
- AutoML raporunda hedef optimize edilmemiş olabilir.
- PFAZ6 final raporu PFAZ13 iyileştirmelerini eksik alabilir.

Öneri:

`ds_dir` şu mantıkla `generated_datasets` tarafına map edilmeli:

```python
trained_ds_dir = metrics_file.parent.parent.parent
ds_dir = self.pfaz_outputs[1] / trained_ds_dir.name
```

Ayrıca PFAZ13 sonunda `best_by_target` varsa ama `automl_results` boşsa warning yerine hata ya da en azından `status: skipped_no_datasets` döndürülmeli.

### 2. Job 3 ve Job 4 Hataları Başarılı Exit Koduyla Gizliyor

Dosyalar:

- `truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh`
- `truba/slurm_jobs/job4_pfaz06_08_10.sh`

İlgili noktalar:

- `job3_pfaz04_05_07_09_12_13.sh:60`: faz döngüsü
- `job3_pfaz04_05_07_09_12_13.sh:75`: `exit 0`
- `job4_pfaz06_08_10.sh:52`: faz döngüsü
- `job4_pfaz06_08_10.sh:84`: `exit 0`

Bu betikler fazlardan biri hata verse bile Slurm'a başarılı job sonucu döndürür. TRUBA'da `sacct`, mail bildirimi veya zincir job kullanılırsa gerçek hata gizlenir.

Etkisi:

- Job tamamlandı maili yanıltıcı olabilir.
- PFAZ6/8/10 çıktıları eksik olduğu halde final zip üretilebilir.
- Sonraki iş adımları başarısız fazları fark etmeden devam edebilir.

Öneri:

Her fazın exit kodu bir toplam ya da flag değişkenine yazılmalı ve sonda başarısızlık varsa non-zero dönülmeli:

```bash
FAIL=0
...
if [ $EC -ne 0 ]; then
  FAIL=1
fi
...
exit $FAIL
```

### 3. `run_complete_pipeline.py` Güncel Paket Yapısıyla Uyumsuz

Dosya: `run_complete_pipeline.py`

İlgili noktalar:

- `run_complete_pipeline.py:154`: `from dataset_generation.dataset_generator import DatasetGenerator`
- `run_complete_pipeline.py:175`: `from ai_training.model_trainer import ModelTrainingPipeline`
- `run_complete_pipeline.py:196`: `from anfis_training.anfis_operator import ANFISTrainer`
- `run_complete_pipeline.py:222`: `from visualization.visualization_system import VisualizationManager`
- `run_complete_pipeline.py:241`: `from reporting.reporting_system import ReportingManager`

Bu import path'leri mevcut repo yapısıyla eşleşmiyor. Güncel modüller `pfaz_modules/...`, `visualization_modules/...`, `physics_modules/...` altında.

Etkisi:

- TRUBA'da yanlışlıkla `python run_complete_pipeline.py` çalıştırılırsa erken kırılır.
- Dokümantasyon veya alışkanlıkla eski script kullanılırsa gereksiz job kaybı olur.

Öneri:

TRUBA için yalnızca şu giriş noktaları kullanılmalı:

```bash
python3 -u main.py --run-all
python3 -u main.py --pfaz 1
sbatch truba_slurm_job.sh
sbatch truba/slurm_jobs/job1_pfaz01.sh
```

`run_complete_pipeline.py` ya güncellenmeli ya da üstüne "deprecated, kullanmayın" uyarısı konmalı.

## Orta Seviye Bulgular

### 4. Worker Sayısı Config ile Kod Arasında Tutarsız

Dosyalar:

- `config.json`
- `main.py`
- `utils/gpu_manager.py`

İlgili noktalar:

- `config.json:80`: PFAZ2 `n_workers: 100`
- `config.json:107`: PFAZ3 `n_workers: 100`
- `main.py:593`: PFAZ2 worker sayısı `GPUManager.optimal_workers('ai')`
- `main.py:675`: PFAZ3 worker sayısı `GPUManager.optimal_workers('anfis')`
- `utils/gpu_manager.py:186`: AI worker üst sınırı 16
- `utils/gpu_manager.py:192`: ANFIS worker üst sınırı 20

`config.json` 100 worker hedefliyor ama kod bunu doğrudan kullanmıyor. `orfoz` için `#SBATCH -c 110` ayrılmış olsa da PFAZ2 yaklaşık en fazla 16, PFAZ3 yaklaşık en fazla 20 worker kullanacak.

Etkisi:

- Çalışma güvenli ama beklenen TRUBA hızlanması alınmayabilir.
- Kullanıcı config'e bakarak 100 paralel eğitim bekleyebilir.

Öneri:

Bu bilinçli bir güvenlik limitiyse `config.json` notu güncellenmeli. Gerçekten 100 worker isteniyorsa `GPUManager.optimal_workers()` TRUBA/HPC modunda farklı limit kullanacak şekilde düzenlenmeli.

### 5. Tek Parça `truba_slurm_job.sh` ile Split Job Akışı Farklı Davranıyor

Dosyalar:

- `truba_slurm_job.sh`
- `truba/slurm_jobs/*.sh`

`truba_slurm_job.sh` submit dizinine göre çalışıyor:

```bash
cd "$SLURM_SUBMIT_DIR"
python3 -u main.py --run-all
```

Split job dosyaları ise sabit path kullanıyor:

```bash
PROJECT_DIR="/arf/home/ahmacar/hpcv1"
OUTPUT_DIR="/arf/scratch/ahmacar/hpcv1_outputs"
```

Etkisi:

- Repo TRUBA'da farklı dizine klonlanırsa split job'lar kırılır.
- Tek parça job submit edildiği dizinden çalışır, split job sabit dizin ister.

Öneri:

TRUBA'da repo kesin olarak `/arf/home/ahmacar/hpcv1` altında tutulmalı veya split job dosyaları `SLURM_SUBMIT_DIR` / env değişkeni destekleyecek şekilde güncellenmeli.

### 6. Veri Path Varsayımları İki Yerde Farklı

Dosyalar:

- `config.json`
- `main.py`
- `truba_slurm_job.sh`
- `truba/slurm_jobs/job1_pfaz01.sh`

Job dosyaları `data/aaa2.txt` kontrol ediyor. `main.py` ise top-level `data_file` olmadığı için varsayılan olarak root `aaa2.txt` kullanıyor:

- `main.py:479`: `data_file = self.config.get('data_file', 'aaa2.txt')`
- `main.py:481-482`: relative path proje root altına bağlanıyor

Bu yerel repoda hem `aaa2.txt` hem `data/aaa2.txt` olduğu için sorun görünmüyor.

Etkisi:

- TRUBA transferinde sadece `data/aaa2.txt` gider, root `aaa2.txt` gitmezse PFAZ1 kırılır.
- Job ön kontrolü geçer ama Python tarafı farklı dosyayı arar.

Öneri:

`config.json` içine top-level şu alan eklenmeli:

```json
"data_file": "data/aaa2.txt"
```

ya da job kontrolleri root `aaa2.txt` ile hizalanmalı.

### 7. PFAZ2 Training Config Dosyası Yok, Kod Default Üretiyor

Dosya: `main.py`

İlgili nokta:

- `main.py:600`: `pfaz_modules/pfaz02_ai_training/training_configs_50.json`

Bu dosya repoda yok. `ParallelAITrainer` bunu hata yapmadan default config üreterek tolere ediyor.

Etkisi:

- Koşu kırılmaz.
- Fakat beklenen 50 konfigürasyonun versiyonlanmış, deterministik içeriği repo içinde görünmüyor.

Öneri:

Eğer tez/rapor için aynı konfigürasyonların tekrar üretilebilir olması önemliyse `training_configs_50.json` dosyası repo içinde üretilip commitlenmeli ya da default üretim seed/config çıktısı rapora eklenmeli.

## Olumlu Kontroller

- `main.py` CLI yapısı TRUBA için uygun: `--pfaz`, `--run-all`, `--start-from`, `--end-at`, `--mode`, `--check-deps` mevcut.
- `HPC_MODE` ve `SLURM_JOB_ID` kontrolü var; HPC ortamında otomatik pip install denemiyor.
- `PIPELINE_EXECUTION_ORDER = [1, 2, 3, 4, 5, 7, 9, 12, 13, 6, 8, 10, 11]` faz bağımlılıkları açısından mantıklı. PFAZ6 ve PFAZ10 raporlama/tez fazları geçe alınmış.
- PFAZ11 production/docker kalıcı olarak skip ediliyor; TRUBA CPU batch işi için uygun.
- CPU-only job ayarları doğru yönde: `CUDA_VISIBLE_DEVICES=""`, BLAS thread env'leri `1`, `HPC_MODE=1`.
- `config.json` output path'i scratch alanına yönlenmiş: `/arf/scratch/ahmacar/hpcv1_outputs`.
- PFAZ1 çıktıları `AAA2_enriched_all_nuclei.csv/xlsx`, split `train.csv/val.csv/test.csv` ve `metadata.json` üretme mantığıyla PFAZ2'nin beklediği yapıya uyumlu.
- PFAZ2 headerless CSV + `metadata.json` okuma desteğine sahip.
- PFAZ9, PFAZ1'in `AAA2_enriched_all_nuclei.csv` çıktısını bekliyor; path mantığı `config.json` output root ile uyumlu.
- PFAZ6'ya PFAZ9 ve PFAZ13 output dizinleri explicit aktarılıyor.
- Smoke/import testleri geçti: `32 passed`.

## TRUBA Çalıştırma Öncesi Kontrol Listesi

Zorunlu:

- PFAZ13 dataset path hatasını düzelt.
- Job 3 ve Job 4 final `exit 0` davranışını non-zero hata dönecek şekilde değiştir.
- TRUBA'ya root `aaa2.txt` ve `data/aaa2.txt` birlikte gittiğini doğrula veya `data_file: data/aaa2.txt` ile hizala.
- `run_complete_pipeline.py` kullanılmayacaksa açıkça deprecated işaretle.

Önerilen:

- `config.json` worker notlarını gerçek kod davranışıyla hizala.
- Split job dosyalarında `PROJECT_DIR` ve `OUTPUT_DIR` sabitlerini tek yerde env ile yönet.
- PFAZ13 sonunda boş AutoML sonucu üretildiyse job'u warning-only bırakma; raporda açık durum kodu yaz.
- `training_configs_50.json` yokluğu bilinçli ise default config üretim seed'ini rapora yazdır.

TRUBA'da önerilen sıralı split akış:

```bash
cd /arf/home/ahmacar/hpcv1
bash setup_truba.sh
sbatch truba/slurm_jobs/job1_pfaz01.sh
sbatch truba/slurm_jobs/job2_pfaz02_03.sh
sbatch truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh
sbatch truba/slurm_jobs/job4_pfaz06_08_10.sh
```

Her job sonrası minimum kontrol:

```bash
sacct -j <JOB_ID> --format=JobID,State,ExitCode,Elapsed,MaxRSS
tail -100 /arf/scratch/ahmacar/hpcv1_outputs/logs/<ilgili_log>
find /arf/scratch/ahmacar/hpcv1_outputs -maxdepth 2 -type f | wc -l
```

## Nihai Değerlendirme

Bu haliyle repo TRUBA'ya alınabilir ama "hata ve eksik olmasın" hedefi için yukarıdaki kritik 3 madde düzeltilmeden uzun job başlatılmamalı. Özellikle PFAZ13 ve job exit kodları düzeltilmezse Slurm tarafında başarılı görünen ama içerik olarak eksik bir final üretme riski var.

