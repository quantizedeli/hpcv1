#!/bin/bash
# ============================================================================
# Sprint 11 BUG-78: SLURM --dependency=afterok chain
# Sprint 12: Production-ready -- log dizini ve cikti dogrulama
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

# logs dizini hazirla (PFAZ8 LogAnalyticsViz arar)
OUTPUT_DIR="/arf/scratch/ahmacar/hpcv1_outputs"
mkdir -p "$OUTPUT_DIR/logs"

echo "===================================================="
echo " TRUBA Pipeline Submit (afterok chain)"
echo " Tarih: $(date)"
echo " User: $(whoami)"
echo " Output: $OUTPUT_DIR"
echo "===================================================="

# Job 1: PFAZ01
JID1=$(sbatch --parsable truba/slurm_jobs/job1_pfaz01.sh)
echo "[SUBMIT] Job 1 (PFAZ01)            -> $JID1"

# Job 2: PFAZ02-03 (afterok Job 1)
JID2=$(sbatch --parsable --dependency=afterok:$JID1 truba/slurm_jobs/job2_pfaz02_03.sh)
echo "[SUBMIT] Job 2 (PFAZ02-03)         -> $JID2 (afterok:$JID1)"

# Job 3: PFAZ04/05/07/09/12/13 (afterok Job 2)
JID3=$(sbatch --parsable --dependency=afterok:$JID2 truba/slurm_jobs/job3_pfaz04_05_07_09_12_13.sh)
echo "[SUBMIT] Job 3 (PFAZ04-13)         -> $JID3 (afterok:$JID2)"

# Job 4: PFAZ06/08/10 (afterok Job 3)
JID4=$(sbatch --parsable --dependency=afterok:$JID3 truba/slurm_jobs/job4_pfaz06_08_10.sh)
echo "[SUBMIT] Job 4 (PFAZ06/08/10)      -> $JID4 (afterok:$JID3)"

echo ""
echo "===================================================="
echo " TUM JOB'LAR GONDERILDI"
echo "===================================================="
echo " Job 1: $JID1 (PFAZ01)"
echo " Job 2: $JID2 (PFAZ02-03,  afterok:$JID1)"
echo " Job 3: $JID3 (PFAZ04-13,  afterok:$JID2)"
echo " Job 4: $JID4 (PFAZ06/08/10, afterok:$JID3)"
echo "===================================================="
echo ""
echo " Izleme:"
echo "   squeue -u $(whoami)"
echo "   sacct -j $JID1,$JID2,$JID3,$JID4 --format=JobID,State,ExitCode,Elapsed"
echo ""
echo " Bir job basarisiz olursa sonrakiler OTOMATIK iptal olur."
echo " Manuel iptal: scancel $JID1 $JID2 $JID3 $JID4"
echo ""
