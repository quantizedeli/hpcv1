# TRUBA Submit Checklist -- Sprint 15+16 Sonrasi

**Tarih:** 2026-05-20
**Tez teslim:** 22 Mayis 2026 (2 gun)
**Tahmini sure:** ~2 saat (toplam pipeline)
**Onceki kosu:** Sprint 14, Job-5779758, 65 saat (2 timeout). Sprint 15 sonrasi 250x azalma.

---

## ON KOSULLAR

- [ ] Sprint 15+16 commit'leri local'de var:
  ```
  Beklenen son 4 commit:
    HEAD~3  docs(sprint15)        b50d296
    HEAD~2  fix(sprint15)         cd1f4b5
    HEAD~1  config(sprint15)      dc9e8e0
    HEAD    sprint16-final        <yeni hash>
  ```
- [ ] TRUBA VPN aktif (172.16.6.11 erisilebilir)
- [ ] TRUBA hesabin aktif (ahmacar)

---

## ADIM 1 -- VS Code'da Push (lokal -> github)

```bash
cd Desktop/hpcv1
git log --oneline -5
```

Eger Sprint 15+16 commit'leri varsa:

```bash
git push -u origin sprint16-final
```

Branch henuz push edilmedi ise yeni branch acilir, github'da kontrol edebilirsin.

**Beklenen cikti:** Branch yuklendi, "Compare & pull request" linki gozukur.

---

## ADIM 2 -- TRUBA'ya Baglan

```bash
ssh ahmacar@172.16.6.11
```

**Beklenen:** Login node prompt: `[ahmacar@arf-ui1 ~]$`

Eger "Connection refused" alirsan: TRUBA VPN'i kontrol et.

---

## ADIM 3 -- TRUBA'da Mevcut Durumu Kontrol Et

```bash
cd /arf/scratch/ahmacar/hpcv1_outputs
ls -la
```

**Beklenen:** Eski klasorler gozukur:
- `generated_datasets/` (1468 dataset, Sprint 14 sonrasi)
- `outputs/trained_models/` (6615 PKL, 61283 metrics)
- `outputs/trained_anfis_models/` (varsa)

```bash
# Sprint 14 oncesi eski verileri say
find generated_datasets -maxdepth 1 -type d | wc -l
find outputs/trained_models -name "*.pkl" | wc -l
find outputs/trained_models -name "metrics_*.json" | wc -l
```

Bu sayilari not al -- tezsel feature ablation analizinde lazim olabilir.

---

## ADIM 4 -- ESKI VERILERI ARSIVLE (KRITIK -- KURAL 37)

Eski 61283 metrics dosyasi **feature ablation kaniti**. SILME, arsivle.

```bash
mkdir -p archive

# 1. Generated datasets arsivle (~5-15 GB)
echo "[$(date)] generated_datasets arsivleniyor..."
tar czf archive/generated_datasets_PRE_SPRINT15.tar.gz generated_datasets/ 2>&1 | tail -3
ls -lah archive/generated_datasets_PRE_SPRINT15.tar.gz

# 2. Trained models arsivle (~5-10 GB)
echo "[$(date)] trained_models arsivleniyor..."
tar czf archive/trained_models_PRE_SPRINT15.tar.gz outputs/trained_models/ 2>&1 | tail -3
ls -lah archive/trained_models_PRE_SPRINT15.tar.gz

# 3. ANFIS varsa
if [ -d outputs/trained_anfis_models ]; then
  tar czf archive/trained_anfis_models_PRE_SPRINT15.tar.gz outputs/trained_anfis_models/ 2>&1 | tail -3
fi
```

Bu adim 5-15 dakika surebilir (boyuta gore).

---

## ADIM 5 -- ESKI KLASORLERI YEDEK ISIMLERLE TASI

```bash
# Silmek yerine yan klasore tasi -- yedek + temiz baslangic
mv generated_datasets generated_datasets_PRE_SPRINT15
mv outputs/trained_models outputs/trained_models_PRE_SPRINT15
[ -d outputs/trained_anfis_models ] && mv outputs/trained_anfis_models outputs/trained_anfis_models_PRE_SPRINT15

ls -la | grep PRE_SPRINT15
```

**Beklenen:** Eski klasorler `_PRE_SPRINT15` ekiyle, yeni klasorler yok (PFAZ1 uretecek).

---

## ADIM 6 -- Kod Guncelle

```bash
cd /arf/home/ahmacar/hpcv1
git status
git fetch origin
git checkout sprint16-final
git pull origin sprint16-final
git log --oneline -5
```

**Beklenen:** Son 4 commit (Sprint 15+16) gozukur.

---

## ADIM 7 -- Config Dogrula

```bash
# config.json Sprint 15 anahtarlari dogru mu?
python3 -c "
import json
with open('config.json') as f: c = json.load(f)
p2 = c['pfaz02_ai_training']
print('models:', p2['models'])
print('n_configurations:', p2['n_configurations'])
print('training_config_path:', p2['training_config_path'])
print('allowed_feature_sets (len):', len(p2['allowed_feature_sets']))
print('allowed_scenarios:', p2['allowed_scenarios'])
print('allowed_anomaly_modes:', p2['allowed_anomaly_modes'])
print('allowed_scalings:', p2['allowed_scalings'])
"
```

**Beklenen cikti:**
```
models: ['RF', 'XGBoost']
n_configurations: 20
training_config_path: training_configs_20.json
allowed_feature_sets (len): 9
allowed_scenarios: ['S80']
allowed_anomaly_modes: ['vanilla']
allowed_scalings: ['NoScaling']
```

Eger farkliysa: `git pull` tekrarla, branch dogru mu kontrol et.

---

## ADIM 8 -- training_configs_20.json Mevcut mu?

```bash
ls -la pfaz_modules/pfaz02_ai_training/training_configs_20.json
python3 -c "
import json
with open('pfaz_modules/pfaz02_ai_training/training_configs_20.json') as f: d = json.load(f)
print('Toplam config:', len(d['configs']))
prefixes = {c['id'].split('_')[0] for c in d['configs']}
print('Prefix\'ler:', prefixes)
rf = sum(1 for c in d['configs'] if c['id'].startswith('RF_'))
xgb = sum(1 for c in d['configs'] if c['id'].startswith('XGB_'))
print(f'RF={rf}, XGB={xgb}')
"
```

**Beklenen:**
```
Toplam config: 20
Prefix'ler: {'XGB', 'RF'}
RF=11, XGB=9
```

---

## ADIM 9 -- Pipeline Status Sifirla

```bash
# Eski pfaz_status.json varsa sil (yeniden baslangic icin)
if [ -f pfaz_status.json ]; then
  echo "pfaz_status.json mevcut, yedek alip silinecek:"
  cp pfaz_status.json pfaz_status.json.bak_$(date +%Y%m%d)
  rm pfaz_status.json
fi
```

---

## ADIM 10 -- Slurm Script Dogrula

```bash
cd truba/slurm_jobs
ls -la
cat job1_pfaz01.sh | head -20
```

Onemli flag'leri kontrol et:
- [ ] `#SBATCH -C weka` (ZORUNLU)
- [ ] `#SBATCH -A ahmacar` (ZORUNLU)
- [ ] `#SBATCH -p orfoz` 
- [ ] `#SBATCH -c 112` (Sprint 12: 56/112 katlari zorunlu)
- [ ] `#SBATCH --chdir=/arf/scratch/ahmacar/hpcv1_outputs` (Sprint 13)

Eger eksikse `git pull` tekrarla. Hala eksikse Claude'a soracaksin.

---

## ADIM 11 -- Submit

```bash
cd /arf/home/ahmacar/hpcv1
chmod +x truba/slurm_jobs/*.sh setup_truba.sh
bash setup_truba.sh
./truba/slurm_jobs/submit_all.sh
```

**Beklenen:** 4 job kuyruga eklenir:
```
Submitted batch job <JOB1_ID> (pfaz01)
Submitted batch job <JOB2_ID> (pfaz02+03, --dependency=afterok:JOB1)
Submitted batch job <JOB3_ID> (pfaz04..12, --dependency=afterok:JOB2)
Submitted batch job <JOB4_ID> (pfaz13+final, --dependency=afterok:JOB3)
```

Job ID'leri **not al**.

---

## ADIM 12 -- Job'lari Izle

```bash
squeue -u ahmacar
```

Beklenen statusler:
- `PD` (pending, kuyrukta bekliyor)
- `R` (running)
- Sonra: jobs disappear from queue (done)

Detayli takip:
```bash
sacct -u ahmacar --format=JobID,JobName,State,Elapsed,ExitCode -j <JOB_ID>
```

---

## ADIM 13 -- Job1 (PFAZ1) Cikti Kontrol (~5 dk sonra)

```bash
ls /arf/scratch/ahmacar/hpcv1_outputs/generated_datasets | head
ls /arf/scratch/ahmacar/hpcv1_outputs/generated_datasets | wc -l
```

**Beklenen:** ~36 dataset (9 FS x 2 sampling x 2 boyut).

Eger 1468 dataset gorursen: `allowed_feature_sets` filtresi calismadi -- config.json'a tekrar bak.

---

## ADIM 14 -- Job2 (PFAZ2+PFAZ3) Izleme (~30-60 dk)

```bash
# Anlik durum
squeue -u ahmacar -j <JOB2_ID>

# Aktif model sayisi (canli)
find /arf/scratch/ahmacar/hpcv1_outputs/outputs/trained_models -name "*.pkl" 2>/dev/null | wc -l
find /arf/scratch/ahmacar/hpcv1_outputs/outputs/trained_models -name "completed.json" 2>/dev/null | wc -l
```

**Beklenen tamamlamada:**
- ~1440 PKL ya da kalite-red toplam ~1440 completed.json (Sprint 15 BUG-101 fix sayesinde)
- ~36 dataset altinda RF + XGB klasorleri

---

## ADIM 15 -- Job3-4 (PFAZ4-12) Tamamlanmasi (~30 dk)

```bash
squeue -u ahmacar
# Job3 + Job4 sira ile calisir

# Final cikti
ls /arf/scratch/ahmacar/hpcv1_outputs/outputs/reports/ | head
ls /arf/scratch/ahmacar/hpcv1_outputs/outputs/visualizations/ | head -10
```

**Beklenen:** `MASTER_NUCLEAR_AI_REPORT.xlsx` raporu, tez verisi hazir.

---

## SORUN DURUMUNDA

### Job timeout
```bash
sacct -u ahmacar --format=JobID,State,Elapsed,ExitCode -j <JOB_ID>
```
`TIMEOUT` gorursen:
1. Hangi PFAZ'da kaldi: log dosyasini oku
2. `pfaz_status.json` kontrol et
3. Resume modunda yeniden submit et:
   ```bash
   sbatch truba/slurm_jobs/job2_pfaz02_03.sh  # Sprint 15 BUG-101 fix calisir, resume guvenli
   ```

### Job FAIL (ExitCode != 0)
```bash
cat /arf/scratch/ahmacar/hpcv1_outputs/logs/main_<son>.log | tail -100
```
Hata mesajini Claude'a getir, beraber bakacagiz.

### Kaynak yetersizlik (memory/disk)
```bash
df -h /arf/scratch
# Disk dolduysa: eski archive/ klasorunu sika
```

---

## TAMAMLANDIGINDA

- [ ] Job1, Job2, Job3, Job4 hepsi `COMPLETED` (ExitCode 0)
- [ ] `MASTER_NUCLEAR_AI_REPORT.xlsx` mevcut
- [ ] `outputs/visualizations/` doluyor
- [ ] `outputs/thesis/` LaTeX dosyalari uretildi
- [ ] PFAZ10 LaTeX -> PDF derlemesi calisti

Sonra tez metnine veriyi entegre et:
- `MASTER_NUCLEAR_AI_REPORT.xlsx`'in ilgili sheet'lerinden ortalama R², en iyi model satirlari
- `outputs/visualizations/` altindan PNG'leri tez bolumlerine
- `tez-yazim-not-defteri.md` Sprint 15 bolumune **gercek sonuc** sayilarini ekle

---

*TRUBA Submit Checklist | Sprint 15+16 sonrasi | 2026-05-20*
