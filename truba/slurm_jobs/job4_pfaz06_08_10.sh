#!/bin/bash
# ============================================================
# Job 4: PFAZ 6,8,10 -- Raporlama + Gorsellestirme + Tez
# Job 3 tamamlandiktan SONRA calistir.
# Gercek calisma sirasi: 6 -> 8 -> 10
# NOT: PFAZ 6 tum diger fazlarin ciktisini bekler (9. sirada calisir)
# Calistirma: sbatch truba/slurm_jobs/job4_pfaz06_08_10.sh
# Beklenen sure: 3-5 saat
# ============================================================
#SBATCH -p orfoz
#SBATCH -A ahmacar
#SBATCH -J nucphys-pfaz-rapor
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 112
#SBATCH -C weka
#SBATCH --time=0-10:00:00
#SBATCH --output=/arf/scratch/ahmacar/hpcv1_outputs/logs/job4_rapor_%j.out
#SBATCH --error=/arf/scratch/ahmacar/hpcv1_outputs/logs/job4_rapor_%j.err
#SBATCH --chdir=/arf/scratch/ahmacar/hpcv1_outputs
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ahmetkemalacar@gmail.com

echo "===================================================="
echo " Job 4: PFAZ 6,8,10 -- Rapor + Gorsel + Tez"
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
export THESIS_COMPILE_PDF=n

PROJECT_DIR="${PROJECT_DIR:-/arf/home/ahmacar/hpcv1}"  # BUG-89: env override
OUTPUT_DIR="${OUTPUT_DIR:-/arf/scratch/ahmacar/hpcv1_outputs}"  # BUG-89: env override
mkdir -p "$OUTPUT_DIR/logs" \
         "$OUTPUT_DIR/reports" \
         "$OUTPUT_DIR/visualizations" \
         "$OUTPUT_DIR/thesis"

cd "$PROJECT_DIR" || { echo "[HATA] $PROJECT_DIR bulunamadi!"; exit 1; }

FAIL=0
for PFAZ in 6 8 10; do
    echo ""
    echo "[START] PFAZ $PFAZ basliyor -- $(date)"
    python3 -u main.py --pfaz $PFAZ 2>&1 | tee "$OUTPUT_DIR/logs/pfaz0${PFAZ}_${SLURM_JOB_ID}.log"
    EC=${PIPESTATUS[0]}
    if [ $EC -ne 0 ]; then
        echo "[UYARI] PFAZ $PFAZ exit=$EC -- job basarisiz isaretlenecek"
        FAIL=1
    else
        echo "[OK] PFAZ $PFAZ tamamlandi"
    fi
done

# Sonuclari zip'le -- indirmesi kolay olsun
echo ""
echo "[ZIP] Ciktilar arsivleniyor..."
cd "$OUTPUT_DIR"
zip -r "results_job4_${SLURM_JOB_ID}.zip" reports/ visualizations/ thesis/ \
    2>&1 | tail -3
echo "[ZIP] Tamamlandi: results_job4_${SLURM_JOB_ID}.zip"

# Tum ciktilari da zip'le
zip -r "all_outputs_${SLURM_JOB_ID}.zip" . \
    --exclude "*.zip" \
    2>&1 | tail -3
echo "[ZIP] Tum ciktilar: all_outputs_${SLURM_JOB_ID}.zip"

echo ""
echo "===================================================="
echo " Pipeline TAMAMLANDI: $(date) | FAIL=$FAIL"
echo " Indirmek icin (PowerShell):"
echo " scp ahmacar@172.16.6.11:$OUTPUT_DIR/all_outputs_${SLURM_JOB_ID}.zip ."
echo "===================================================="
# BUG-68 FIX: Onceden kosulsuz 'exit 0' idi.
exit $FAIL
