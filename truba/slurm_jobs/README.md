# TRUBA Slurm Job Scriptleri

Bu klasordeki scriptler TRUBA ARF kumesinde calistirilir.
Gercek sistem bilgileriyle yazilmistir (2026-05-13 dogrulama).

## Sistem Bilgileri (Dogrulanmis)

| Parametre | Deger |
|-----------|-------|
| SSH | `ahmacar@172.16.6.11` (VPN/PuTTY) |
| Login node | `arf-ui1` |
| Partition | `orfoz` |
| ZORUNLU flag | `#SBATCH -C weka` |
| Max CPU | 110 (112 degil -- 2 cekirdek IO icin ayrilmis) |
| n_workers | 100 |
| Modul | `apps/truba-ai/cpu-2024.0` |
| Kod dizini | `/arf/home/ahmacar/hpcv1/` |
| Cikti dizini | `/arf/scratch/ahmacar/hpcv1_outputs/` |

## Calistirma Sirasi (ZORUNLU -- atlama)

```bash
# Adim 1: Once her scripte calistirma izni ver
chmod +x truba/slurm_jobs/*.sh

# Adim 2: Sirayla gonder -- onceki job BITMEDEN sonrakini gonderme
sbatch truba/slurm_jobs/job1_pfaz01.sh

# Job 1 bittikten sonra (mail gelir):
sbatch truba/slurm_jobs/job2_pfaz02_03.sh

# Job 2 bittikten sonra:
sbatch truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh

# Job 3 bittikten sonra:
sbatch truba/slurm_jobs/job4_pfaz06_08_10.sh
```

## Job Izleme

```bash
squeue -u ahmacar              # aktif joblar
squeue -u ahmacar -l           # detayli
tail -f /arf/scratch/ahmacar/hpcv1_outputs/logs/job1_pfaz01_<JOBID>.out
scancel <JOBID>                # iptal
```

## Sonuclari Indirme (PowerShell)

Job 4 bittikten sonra zip olusur:
```powershell
scp ahmacar@172.16.6.11:/arf/scratch/ahmacar/hpcv1_outputs/all_outputs_<JOBID>.zip C:\Users\HakanYakut\Desktop\
```

## Faz Sirasi (main.py PIPELINE_EXECUTION_ORDER)

```
[1] -> [2,3] -> [4,5,7,9,12,13] -> [6,8,10]
```
PFAZ 6 (raporlama) ve 8 (gorsel) en sona -- diger tum fazlarin ciktisini bekler.
PFAZ 11 disabled. PFAZ 13 (AutoML) Job 3'te.
