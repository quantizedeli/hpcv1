#!/bin/bash
# ============================================================
# TRUBA İlk Kurulum Scripti — nucdatav2-truba
# Kullanım: bash setup_truba.sh
# ============================================================
# Bu script TRUBA login node'unda BİR KEZ çalıştırılır.
# Sonraki çalıştırmalarda sadece sbatch truba_slurm_job.sh yeterli.
# ============================================================

set -e  # Hata varsa dur

echo "============================================================"
echo " nucdatav2 TRUBA Kurulum Scripti"
echo " Tarih: $(date)"
echo "============================================================"

# ---- 1. Modülleri yükle ----
echo ""
echo "[1/6] Modüller yükleniyor..."
module purge
module load centos7.9/comp/python/3.11.2 2>/dev/null || \
    module load centos7.3/comp/python/3.6.5 2>/dev/null || {
    echo "[UYARI] Python modülü bulunamadı. Mevcut Python modülleri:"
    module avail 2>&1 | grep -i python | head -20
    echo ""
    echo "Yukarıdaki listeden uygun modülü setup_truba.sh içinde güncelleyin."
    exit 1
}
echo "[OK] Python: $(python3 --version)"

# ---- 2. Sanal ortam ----
echo ""
echo "[2/6] Sanal ortam kuruluyor..."
VENV_PATH="$HOME/nucdatav2_env"
if [ -d "$VENV_PATH" ]; then
    echo "[INFO] Mevcut ortam bulundu: $VENV_PATH"
    echo "       Silip yeniden kurmak için: rm -rf $VENV_PATH && bash setup_truba.sh"
else
    python3 -m venv "$VENV_PATH"
    echo "[OK] Sanal ortam: $VENV_PATH"
fi
source "$VENV_PATH/bin/activate"
pip install --upgrade pip --quiet
echo "[OK] pip güncel"

# ---- 3. Paketler ----
echo ""
echo "[3/6] Python paketleri kuruluyor (requirements-hpc.txt)..."
pip install -r requirements-hpc.txt 2>&1 | tail -5
echo "[OK] Paketler kuruldu"

# ---- 4. Kritik paket kontrolü ----
echo ""
echo "[4/6] Kritik paket kontrolü..."
python3 -c "
pkgs = ['numpy', 'pandas', 'sklearn', 'xgboost', 'lightgbm',
        'tensorflow', 'optuna', 'scipy', 'matplotlib', 'joblib']
missing = []
for p in pkgs:
    try:
        __import__(p)
        print(f'  [OK] {p}')
    except ImportError:
        print(f'  [EKSIK] {p}')
        missing.append(p)
if missing:
    print(f'[HATA] Eksik paketler: {missing}')
    exit(1)
else:
    print('[OK] Tüm kritik paketler mevcut')
"

# ---- 5. Veri ve config kontrolü ----
echo ""
echo "[5/6] Veri ve konfigürasyon kontrolü..."
if [ -f "data/aaa2.txt" ]; then
    NUCLEI=$(wc -l < data/aaa2.txt)
    echo "[OK] data/aaa2.txt mevcut ($NUCLEI satır)"
else
    echo "[HATA] data/aaa2.txt bulunamadı!"
    echo "       Dosyayı transfer etmeyi unutmuş olabilirsiniz."
    exit 1
fi

python3 -c "import json; json.load(open('config.json')); print('[OK] config.json geçerli JSON')"
python3 -c "import json; json.load(open('pfaz_status.json')); print('[OK] pfaz_status.json geçerli JSON')" 2>/dev/null || \
    python3 -c "open('pfaz_status.json','w').write('{}'); print('[OK] pfaz_status.json oluşturuldu')"

# ---- 6. Çıktı dizinleri ----
echo ""
echo "[6/6] Çıktı dizinleri oluşturuluyor..."
mkdir -p logs
mkdir -p outputs/generated_datasets outputs/trained_models outputs/anfis_models \
         outputs/reports outputs/visualizations outputs/thesis outputs/ensemble_results \
         outputs/unknown_predictions outputs/cross_model_analysis outputs/aaa2_results \
         outputs/automl_results outputs/advanced_analytics
echo "[OK] Dizinler hazır"

# ---- Smoke test (isteğe bağlı) ----
echo ""
echo "Smoke test çalıştırmak ister misiniz? (ön kontrol — ~30 saniye)"
echo "Evet için Enter, atlamak için 'n' yazın:"
read -r SMOKE_ANSWER
if [[ "$SMOKE_ANSWER" != "n" ]]; then
    echo "[TEST] Smoke testler çalıştırılıyor..."
    python3 -m pytest tests/test_smoke -v --tb=short 2>&1 | tail -20
fi

# ---- Özet ----
echo ""
echo "============================================================"
echo " KURULUM TAMAMLANDI!"
echo ""
echo " Sonraki adımlar:"
echo " 1. truba_slurm_job.sh dosyasını düzenleyin:"
echo "    - SBATCH --partition= (hamsi/palamut/barbun)"
echo "    - THESIS_SUPERVISOR, THESIS_UNIVERSITY"
echo "    - GPU kullanıyorsanız gres satırını açın"
echo ""
echo " 2. Job gönderin:"
echo "    sbatch truba_slurm_job.sh"
echo ""
echo " 3. İzleyin:"
echo "    squeue -u $USER"
echo "    tail -f logs/truba_<JOB_ID>.out"
echo "============================================================"
