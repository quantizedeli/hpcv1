#!/bin/bash
# ============================================================
# Nuclear Physics AI Pipeline — TRUBA ARF Slurm Job Script
# Kullanici : ahmacar (YL ogrencisi, GPU hakki YOK)
# Sistem    : TRUBA ARF Kumesi, RockyLinux 9.2
# Partition : orfoz (CPU-only, 110 cekirdek/node, 256GB RAM)
# Modul     : apps/truba-ai/cpu-2024.0 (pip install YAPMA)
# SSH       : ssh ahmacar@levrek.ulakbim.gov.tr
#
# Kullanim:
#   sbatch truba_slurm_job.sh              # Tum pipeline
#   sbatch truba_slurm_job.sh --pfaz 1    # Sadece PFAZ 1
#   sbatch truba_slurm_job.sh --pfaz 2    # Sadece PFAZ 2
#   sbatch truba_slurm_job.sh --run-all   # Tum fazlar sirali
# ============================================================

#SBATCH --job-name=nucphys-ai
#SBATCH --account=ahmacar
#SBATCH --partition=orfoz
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=55
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --output=logs/truba_%j.out
#SBATCH --error=logs/truba_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ahmetkemalacar@gmail.com

echo "========================================================"
echo " Nuclear Physics AI Pipeline"
echo " Job ID    : $SLURM_JOB_ID"
echo " Node      : $SLURMD_NODENAME"
echo " CPUs      : $SLURM_CPUS_PER_TASK"
echo " Partition : $SLURM_JOB_PARTITION"
echo " Baslangic : $(date)"
echo "========================================================"

# ---- Modul yukle ----
module purge
module load apps/truba-ai/cpu-2024.0
# MATLAB ANFIS backend icin: module load apps/matlab/r2025b
echo "[OK] Modul: apps/truba-ai/cpu-2024.0"
echo "[OK] Python: $(python3 --version)"

# ---- Ic ice paralellik engeli (ZORUNLU) ----
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export BLAS_NUM_THREADS=1
export _PFAZ_PARALLEL_ACTIVE=0

# ---- CPU-only: GPU devre disi ----
export CUDA_VISIBLE_DEVICES=""
export TF_CPP_MIN_LOG_LEVEL=3

# ---- HPC modu ----
export HPC_MODE=1
export PARALLEL_TRAINING=1
export PROJECT_DIR="$SLURM_SUBMIT_DIR"

# ---- Tez metadata ----
export THESIS_AUTHOR="Ahmet Kemal Acar"
export THESIS_SUPERVISOR="Prof. Dr. [Danisman Adi]"
export THESIS_UNIVERSITY="Sakarya Universitesi"
export THESIS_DEPARTMENT="Fizik"
export THESIS_COMPILE_PDF="n"

# ---- Proje dizini ----
cd "$SLURM_SUBMIT_DIR" || { echo "[HATA] Submit dizinine gecilemedi"; exit 1; }
echo "[OK] Calisma dizini: $(pwd)"

# ---- Cikti dizinleri ----
mkdir -p logs
mkdir -p outputs/generated_datasets outputs/trained_models outputs/anfis_models \
         outputs/reports outputs/visualizations outputs/thesis \
         outputs/ensemble_results outputs/unknown_predictions \
         outputs/cross_model_analysis outputs/aaa2_results \
         outputs/automl_results outputs/advanced_analytics

# ---- On kontrol ----
echo "[CHECK] Veri: $(ls -lh data/aaa2.txt 2>/dev/null || echo 'EKSIK!')"
python3 -c "import numpy, pandas, sklearn, xgboost; print('[CHECK] Kritik paketler OK')"

# ---- Pipeline ----
echo "[START] $(date)"
if [ $# -gt 0 ]; then
    python3 -u main.py "$@" 2>&1 | tee "logs/run_${SLURM_JOB_ID}.log"
else
    python3 -u main.py --run-all 2>&1 | tee "logs/run_${SLURM_JOB_ID}.log"
fi
# BUG-85: capture python exit, not tee exit. $? after pipe returns last cmd (tee).
EXIT_CODE=${PIPESTATUS[0]}
echo "========================================================"
echo " Job $SLURM_JOB_ID tamamlandi -- $(date) -- Exit: $EXIT_CODE"
echo "========================================================"
exit $EXIT_CODE
