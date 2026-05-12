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
