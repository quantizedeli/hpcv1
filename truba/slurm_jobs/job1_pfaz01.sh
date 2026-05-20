#!/bin/bash
# ============================================================
# Job 1: PFAZ 1 -- Dataset Uretimi
# Calistirma: sbatch truba/slurm_jobs/job1_pfaz01.sh
# Beklenen sure: 2-3 saat
# ============================================================
#SBATCH -p orfoz
#SBATCH -A ahmacar
#SBATCH -J nucphys-pfaz01
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 112
#SBATCH -C weka
#SBATCH --time=0-06:00:00
#SBATCH --output=/arf/scratch/ahmacar/hpcv1_outputs/logs/job1_pfaz01_%j.out
#SBATCH --error=/arf/scratch/ahmacar/hpcv1_outputs/logs/job1_pfaz01_%j.err
#SBATCH --chdir=/arf/scratch/ahmacar/hpcv1_outputs
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ahmetkemalacar@gmail.com

echo "===================================================="
echo " Job 1: PFAZ 1 -- Dataset Uretimi"
echo " Job ID    : $SLURM_JOB_ID"
echo " Node      : $SLURMD_NODENAME"
echo " Baslangic : $(date)"
echo "===================================================="

# Modul
module purge
module load apps/truba-ai/cpu-2024.0
echo "[OK] Python: $(python3 --version)"

# Paralellik
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=""
export TF_CPP_MIN_LOG_LEVEL=3
export HPC_MODE=1

# Dizinler
PROJECT_DIR="${PROJECT_DIR:-/arf/home/ahmacar/hpcv1}"  # BUG-89: env override
OUTPUT_DIR="${OUTPUT_DIR:-/arf/scratch/ahmacar/hpcv1_outputs}"  # BUG-89: env override
mkdir -p "$OUTPUT_DIR/logs" "$OUTPUT_DIR/generated_datasets"

cd "$PROJECT_DIR" || { echo "[HATA] $PROJECT_DIR bulunamadi!"; exit 1; }
echo "[OK] Proje dizini: $(pwd)"

# Veri kontrolu
ls -lh data/aaa2.txt 2>/dev/null || { echo "[HATA] data/aaa2.txt eksik!"; exit 1; }

# Run
echo "[START] PFAZ 1 basliyor -- $(date)"
python3 -u main.py --pfaz 1 2>&1 | tee "$OUTPUT_DIR/logs/pfaz01_${SLURM_JOB_ID}.log"
EXIT_CODE=${PIPESTATUS[0]}  # BUG-85: $? would capture tee exit, not python exit

echo "===================================================="
echo " Job 1 tamamlandi: $(date) | Exit: $EXIT_CODE"
echo "===================================================="
exit $EXIT_CODE
