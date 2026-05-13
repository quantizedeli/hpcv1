# Sprint 9B -- TRUBA Script Guncelleme (2026-05-13)
## Durum: TAMAMLANDI

### Neden Guncellendi

Mevcut `truba_slurm_job.sh` ve `setup_truba.sh` tahmine dayali yazilmisti.
Sohbet arsivi analizi ile gercek TRUBA bilgileri belirlendi:

| Alan | Eski (yanlis) | Yeni (dogru) |
|------|--------------|--------------|
| SSH adresi | levrek1.yonetim.truba.gov.tr | levrek.ulakbim.gov.tr |
| Partition | hamsi | orfoz |
| Modul | centos7.9/comp/python/3.11.2 | apps/truba-ai/cpu-2024.0 |
| venv kurulumu | python -m venv + pip install | GEREKSIZ -- modul yeterli |
| GPU | --gres=gpu:1 aktif | CUDA_VISIBLE_DEVICES="" (YL'de GPU yok) |
| Account | Eksikti | --account=ahmacar ZORUNLU |

### Degistirilen Dosyalar

1. `truba_slurm_job.sh` -- gercek partition/modul/account ile yeniden yazildi
2. `setup_truba.sh` -- venv kaldirildi, gercek modul ile guncellendi
3. `TRUBA-KULLANIM-KILAVUZU.md` -- v2.0 olarak yeniden yazildi

### TRUBA Bilgileri (dogrulanmis)

- SSH: `ssh ahmacar@levrek.ulakbim.gov.tr` (OpenVPN zorunlu)
- Partition: orfoz (CPU, 110 cekirdek/node, 256GB RAM, max 3 gun)
- Modul: `apps/truba-ai/cpu-2024.0` (numpy/pandas/sklearn/xgboost/tf/optuna dahil)
- MATLAB: `apps/matlab/r2025b` (ANFIS backend)
- Scratch: `/arf/scratch/ahmacar`
- --account=ahmacar SBATCH direktifinde ZORUNLU

### Kaynaklar

TRUBA sohbet arsivi (2026-05-11): chat/7c091386-4c94-4428-a969-97027aa20b29
TRUBA belgeleri: docs.truba.gov.tr

*Sprint 9B v1.0 | 2026-05-13*

---

## Sprint 9B Tamamlama (2026-05-13 -- Gercek Sistem Bilgileriyle)

Kemal'in PuTTY ekran goruntuleri ve sinfo/module avail ciktilari ile
tum bilgiler dogrulandi. Asagidaki duzeltmeler yapildi:

### Dogrulanan Bilgiler

| Parametre | Onceki Tahmin | Gercek Deger |
|-----------|--------------|--------------|
| SSH | levrek.ulakbim.gov.tr | **172.16.6.11** (VPN ic IP) |
| Login node | levrek | **arf-ui1** |
| Baglanti araci | PowerShell | **PuTTY** |
| Max CPU | 112 | **110** (2 cekirdek IO icin ayrilmis) |
| Zorunlu flag | Yoktu! | **#SBATCH -C weka** |
| n_workers | 55 | **100** |
| MATLAB | Kullanilacak | **Disabled** (matlabws 0/0 saat) |
| orfoz durumu | Kapali (eski duyuru) | **ACIK** (sinfo: up) |

### Yeni Dosyalar

- `truba/slurm_jobs/job1_pfaz01.sh`
- `truba/slurm_jobs/job2_pfaz02_03.sh`
- `truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh`
- `truba/slurm_jobs/job4_pfaz06_08_10.sh`
- `truba/slurm_jobs/README.md`

### config.json Degisiklikleri

- `matlab_engine.enabled: false`
- `n_workers: 100` (pfaz02 ve pfaz03)
- `output_dir: /arf/scratch/ahmacar/hpcv1_outputs`

### Zip ile Indirme

Job 4 sonu otomatik zip olusturur. PowerShell ile:
```
scp ahmacar@172.16.6.11:/arf/scratch/ahmacar/hpcv1_outputs/all_outputs_<JOBID>.zip .
```

*Sprint 9B v2.0 | 2026-05-13 | Gercek sistem bilgileriyle tamamlandi*
