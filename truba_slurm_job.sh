#!/bin/bash
# ============================================================
# Nuclear Physics AI Pipeline v2.0.0 — TRUBA SLURM Job Script
# Hazırlayan: Ahmet Kemal Acar
# Hedef Sistem: TRUBA (ULAKBİM Ulusal Yüksek Başarım Bilgisayarı)
#
# Kullanım:
#   sbatch truba_slurm_job.sh              # Tüm pipeline
#   sbatch truba_slurm_job.sh --pfaz 2    # Tek faz
#   sbatch truba_slurm_job.sh --run-all   # Tüm fazlar sırayla
# ============================================================

# ---- SLURM direktifleri ----
#SBATCH --job-name=nucdatav2
#SBATCH --output=logs/truba_%j.out
#SBATCH --error=logs/truba_%j.err
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --mem=192G
#SBATCH --partition=hamsi
# GPU için: --partition=palamut --gres=gpu:1 (aşağıdaki satırı aç)
##SBATCH --partition=palamut
##SBATCH --gres=gpu:1
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=ahmetkemalacar@gmail.com

# ---- TRUBA Partition Rehberi ----
# hamsi   → CPU (40 çekirdek/node, Intel Xeon, 192GB RAM)  [ÖNERİLEN başlangıç]
# barbun  → CPU (28 çekirdek/node, 128GB RAM)              [alternatif CPU]
# palamut → GPU (NVIDIA Tesla V100 16GB)                   [DNN/XGBoost GPU için]
# levrek  → Yüksek bellekli CPU (1.5TB RAM)               [büyük dataset için]
# sardalya→ Yeni GPU partition (A100 var ise)              [TF2 + büyük DNN için]
# mid1/mid2→ Orta süre CPU (max 24h)                      [orta ölçek]
# short   → Kısa CPU (max 1h)                             [test/debug için]

echo "========================================================"
echo " TRUBA Nuclear AI Pipeline Başlıyor"
echo " Job ID    : $SLURM_JOB_ID"
echo " Job Name  : $SLURM_JOB_NAME"
echo " Node      : $SLURMD_NODENAME"
echo " CPUs      : $SLURM_CPUS_PER_TASK"
echo " Partition : $SLURM_JOB_PARTITION"
echo " Başlangıç : $(date)"
echo "========================================================"

# ---- Modülleri yükle ----
module purge
module load centos7.9/comp/python/3.11.2    # Python 3.11
# GPU partition kullanıyorsan aç:
##module load centos7.9/lib/cuda/12.1
##module load centos7.9/comp/gcc/12.2.0

# NOT: TRUBA modül listesi için "module avail" veya "module avail python" komutunu çalıştır.
# Eğer python/3.11.2 bulunamazsa: module avail 2>&1 | grep -i python

echo "[OK] Modüller yüklendi"

# ---- Sanal ortam ----
VENV_PATH="$HOME/nucdatav2_env"
PROJECT_DIR="$SLURM_SUBMIT_DIR"

if [ ! -d "$VENV_PATH" ]; then
    echo "[SETUP] Sanal ortam oluşturuluyor: $VENV_PATH"
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip --quiet
    pip install -r requirements-hpc.txt --quiet
    echo "[OK] Paketler kuruldu"
else
    source "$VENV_PATH/bin/activate"
    echo "[OK] Sanal ortam aktive edildi: $VENV_PATH"
fi

# ---- İç içe paralellik engeli (ZORUNLU — crash önler) ----
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export BLAS_NUM_THREADS=1

# ---- GPU ayarları (palamut/sardalya partition için) ----
export TF_CPP_MIN_LOG_LEVEL=2
export TF_FORCE_GPU_ALLOW_GROWTH=true
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}

# ---- HPC/non-interactive mod ----
export HPC_MODE=1
export PARALLEL_TRAINING=1
export PROJECT_DIR="$PROJECT_DIR"

# ---- Tez metadata (PFAZ 10 için — değiştir) ----
export THESIS_AUTHOR="Ahmet Kemal Acar"
export THESIS_SUPERVISOR="Prof. Dr. [Danışman Adı]"
export THESIS_UNIVERSITY="Sakarya Üniversitesi"
export THESIS_DEPARTMENT="Fizik"
export THESIS_COMPILE_PDF="n"

# ---- Scratch dizini (isteğe bağlı — büyük ara çıktılar için) ----
# SCRATCH=${TMPDIR:-${SCRATCH:-/arf/scratch/$USER}}
# WORK_DIR="$SCRATCH/nucdatav2_$SLURM_JOB_ID"
# mkdir -p "$WORK_DIR"
# echo "[INFO] Scratch: $WORK_DIR"

# ---- Proje dizinine geç ----
cd "$PROJECT_DIR" || { echo "[HATA] Proje dizinine geçilemedi: $PROJECT_DIR"; exit 1; }
echo "[OK] Çalışma dizini: $(pwd)"

# ---- Çıktı dizinleri ----
mkdir -p logs
mkdir -p outputs/generated_datasets outputs/trained_models outputs/anfis_models \
         outputs/reports outputs/visualizations outputs/thesis outputs/ensemble_results \
         outputs/unknown_predictions outputs/cross_model_analysis outputs/aaa2_results \
         outputs/automl_results outputs/advanced_analytics

# ---- Ön kontrol ----
echo "[CHECK] Python: $(python3 --version)"
echo "[CHECK] Veri dosyası: $(ls -lh data/aaa2.txt 2>/dev/null || echo 'EKSIK!')"
python3 -c "import numpy, pandas, sklearn, xgboost; print('[CHECK] Kritik paketler OK')"

# ---- Pipeline çalıştır ----
echo ""
echo "[START] Pipeline başlıyor — $(date)"

if [ $# -gt 0 ]; then
    # Argüman varsa doğrudan ilet (--pfaz 2, --run-all, vb.)
    python3 -u main.py "$@" 2>&1 | tee "logs/run_$SLURM_JOB_ID.log"
else
    # Varsayılan: tüm pipeline
    python3 -u main.py --run-all 2>&1 | tee "logs/run_$SLURM_JOB_ID.log"
fi

EXIT_CODE=$?

echo ""
echo "========================================================"
echo " Job $SLURM_JOB_ID tamamlandı — $(date)"
echo " Çıkış kodu: $EXIT_CODE"
echo "========================================================"

# ---- PFAZ durum özeti ----
python3 -c "
import json, sys
try:
    s = json.load(open('pfaz_status.json'))
    print('\nPFAZ Durum Özeti:')
    for k, v in sorted(s.items()):
        status = v.get('status', '?')
        progress = v.get('progress', '?')
        print(f'  {k}: {status} ({progress}%)')
except Exception as e:
    print(f'Status dosyası okunamadı: {e}')
"

exit $EXIT_CODE
