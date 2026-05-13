#!/bin/bash
# ============================================================
# Job 2: PFAZ 2+3 -- AI Egitimi + ANFIS Egitimi
# PFAZ 1 tamamlandiktan SONRA calistir.
# Calistirma: sbatch truba/slurm_jobs/job2_pfaz02_03.sh
# Beklenen sure: 8-15 saat
# ============================================================
#SBATCH -p orfoz
#SBATCH -A ahmacar
#SBATCH -J nucphys-pfaz0203
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 110
#SBATCH -C weka
#SBATCH --time=1-00:00:00
#SBATCH --output=/arf/scratch/ahmacar/hpcv1_outputs/logs/job2_pfaz0203_%j.out
#SBATCH --error=/arf/scratch/ahmacar/hpcv1_outputs/logs/job2_pfaz0203_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ahmetkemalacar@gmail.com

echo "===================================================="
echo " Job 2: PFAZ 2+3 -- AI + ANFIS Egitimi"
echo " Job ID    : $SLURM_JOB_ID"
echo " Node      : $SLURMD_NODENAME"
echo " Baslangic : $(date)"
echo "===================================================="

module purge
module load apps/truba-ai/cpu-2024.0
echo "[OK] Python: $(python3 --version)"

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=""
export TF_CPP_MIN_LOG_LEVEL=3
export HPC_MODE=1
export _PFAZ_PARALLEL_ACTIVE=0

PROJECT_DIR="/arf/home/ahmacar/hpcv1"
OUTPUT_DIR="/arf/scratch/ahmacar/hpcv1_outputs"
mkdir -p "$OUTPUT_DIR/logs" "$OUTPUT_DIR/trained_models" "$OUTPUT_DIR/anfis_models"

cd "$PROJECT_DIR" || { echo "[HATA] $PROJECT_DIR bulunamadi!"; exit 1; }

# PFAZ 1 cikti kontrolu
if [ ! -d "$OUTPUT_DIR/generated_datasets" ] || [ -z "$(ls -A $OUTPUT_DIR/generated_datasets 2>/dev/null)" ]; then
    echo "[HATA] generated_datasets bos! PFAZ 1 tamamlandi mi?"
    exit 1
fi

echo "[START] PFAZ 2 basliyor -- $(date)"
python3 -u main.py --pfaz 2 2>&1 | tee "$OUTPUT_DIR/logs/pfaz02_${SLURM_JOB_ID}.log"
EXIT_PFAZ2=$?
echo "[PFAZ2] Exit: $EXIT_PFAZ2 -- $(date)"

echo "[START] PFAZ 3 basliyor -- $(date)"
python3 -u main.py --pfaz 3 2>&1 | tee "$OUTPUT_DIR/logs/pfaz03_${SLURM_JOB_ID}.log"
EXIT_PFAZ3=$?
echo "[PFAZ3] Exit: $EXIT_PFAZ3 -- $(date)"

# Birisi basarisiz olsa da devam
EXIT_CODE=$(( EXIT_PFAZ2 + EXIT_PFAZ3 ))

echo "===================================================="
echo " Job 2 tamamlandi: $(date)"
echo " PFAZ2: $EXIT_PFAZ2 | PFAZ3: $EXIT_PFAZ3"
echo "===================================================="
exit $EXIT_CODE
