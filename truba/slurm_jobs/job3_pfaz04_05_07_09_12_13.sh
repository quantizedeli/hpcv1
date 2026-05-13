#!/bin/bash
# ============================================================
# Job 3: PFAZ 4,5,7,9,12,13 -- Tahmin + Analiz
# PFAZ 2+3 tamamlandiktan SONRA calistir.
# Gercek calisma sirasi: 4 -> 5 -> 7 -> 9 -> 12 -> 13
# Calistirma: sbatch truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh
# Beklenen sure: 6-10 saat
# ============================================================
#SBATCH -p orfoz
#SBATCH -A ahmacar
#SBATCH -J nucphys-pfaz-analiz
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 110
#SBATCH -C weka
#SBATCH --time=0-18:00:00
#SBATCH --output=/arf/scratch/ahmacar/hpcv1_outputs/logs/job3_analiz_%j.out
#SBATCH --error=/arf/scratch/ahmacar/hpcv1_outputs/logs/job3_analiz_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ahmetkemalacar@gmail.com

echo "===================================================="
echo " Job 3: PFAZ 4,5,7,9,12,13 -- Analiz Fazlari"
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

PROJECT_DIR="/arf/home/ahmacar/hpcv1"
OUTPUT_DIR="/arf/scratch/ahmacar/hpcv1_outputs"
mkdir -p "$OUTPUT_DIR/logs" \
         "$OUTPUT_DIR/unknown_predictions" \
         "$OUTPUT_DIR/cross_model_analysis" \
         "$OUTPUT_DIR/ensemble_results" \
         "$OUTPUT_DIR/aaa2_results" \
         "$OUTPUT_DIR/advanced_analytics" \
         "$OUTPUT_DIR/automl_results"

cd "$PROJECT_DIR" || { echo "[HATA] $PROJECT_DIR bulunamadi!"; exit 1; }

# Model kontrolu
if [ ! -d "$OUTPUT_DIR/trained_models" ] || [ -z "$(ls -A $OUTPUT_DIR/trained_models 2>/dev/null)" ]; then
    echo "[HATA] trained_models bos! Job 2 tamamlandi mi?"
    exit 1
fi

# Fazlari sirayla calistir -- main.py PIPELINE_EXECUTION_ORDER = [4,5,7,9,12,13]
for PFAZ in 4 5 7 9 12 13; do
    echo ""
    echo "[START] PFAZ $PFAZ basliyor -- $(date)"
    python3 -u main.py --pfaz $PFAZ 2>&1 | tee "$OUTPUT_DIR/logs/pfaz0${PFAZ}_${SLURM_JOB_ID}.log"
    EC=$?
    if [ $EC -ne 0 ]; then
        echo "[UYARI] PFAZ $PFAZ exit=$EC -- devam ediliyor"
    else
        echo "[OK] PFAZ $PFAZ tamamlandi"
    fi
done

echo "===================================================="
echo " Job 3 tamamlandi: $(date)"
echo "===================================================="
exit 0
