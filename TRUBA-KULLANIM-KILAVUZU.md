# TRUBA Kullanim Kilavuzu — Nuclear Physics AI Pipeline
## Kullanici: ahmacar | Sistem: ARF Kumesi | Tarih: 2026-05-13

> Bu kilavuz Sprint 9B ile gercek TRUBA bilgileriyle guncellendi.
> Eski kilavuzdaki yanlis bilgiler (levrek1, centos7.9, hamsi,
> venv kurulumu, pip install) duzeltildi.

---

## 1. Baglanma (OpenVPN Zorunlu)

### Onkosul
OpenVPN bagli olmasi gerekiyor. Bagliysan devam et.

### SSH Komutu (Windows PowerShell veya Terminal)
```powershell
ssh ahmacar@levrek.ulakbim.gov.tr
```
TRUBA sifren sorulur. Ilk baglantiginda "yes" yaz.

---

## 2. Dosya Transferi

### Proje klasorunu yukle (Windows PowerShell)
```powershell
# Tum proje
scp -r C:\Users\<Kullanici>\Desktop\hpcv1 ahmacar@levrek.ulakbim.gov.tr:~/

# Sadece guncel dosyalar
scp main.py config.json ahmacar@levrek.ulakbim.gov.tr:~/hpcv1/

# aaa2.txt veri dosyasi
scp data\aaa2.txt ahmacar@levrek.ulakbim.gov.tr:~/hpcv1/data/
```

### Sonuclari indir
```powershell
scp -r ahmacar@levrek.ulakbim.gov.tr:~/hpcv1/outputs C:\Users\<Kullanici>\Desktop\
```

---

## 3. TRUBA'da Ilk Kurulum (bir kez yapilir)

```bash
# 1. SSH ile baglan
ssh ahmacar@levrek.ulakbim.gov.tr

# 2. Proje dizinine gec
cd ~/hpcv1

# 3. Kurulum scriptini calistir (modul kontrolu + dizin olusturma)
bash setup_truba.sh

# 4. Smoke test (opsiyonel)
module load apps/truba-ai/cpu-2024.0
python3 -c "import numpy, pandas, sklearn, xgboost; print('OK')"
```

---

## 4. Job Gondermek

### Tek komut (tum pipeline)
```bash
sbatch truba_slurm_job.sh
```

### Faz faz gondermek (onerilir -- hata izolasyonu)
```bash
sbatch truba_slurm_job.sh --pfaz 1    # Dataset uretimi
sbatch truba_slurm_job.sh --pfaz 2    # AI egitim
sbatch truba_slurm_job.sh --pfaz 3    # ANFIS egitim
# ... vs.
```

---

## 5. Job Izleme

```bash
squeue -u ahmacar                     # Aktif job'lar
squeue -u ahmacar -l                  # Detayli durum

tail -f logs/truba_<JOB_ID>.out       # Canli log
cat logs/truba_<JOB_ID>.err          # Hata logu

scancel <JOB_ID>                      # Job iptal
sinfo -p orfoz                        # Partition durumu
```

---

## 6. Partition ve Modul Bilgisi

| Partition | Tip | Cekirdek | RAM | Maks Sure |
|-----------|-----|----------|-----|-----------|
| **orfoz** | CPU | 110 | 256GB | 3 gun (SECILEN) |
| hamsi | CPU | 54 | 384GB | 3 gun |
| barbun-cuda | GPU P100 | 16+ | - | proje gerekli |
| akya-cuda | GPU V100 | 16+ | - | proje gerekli |

**Modul:** 
- numpy, pandas, scikit-learn, xgboost, lightgbm, tensorflow, optuna,
  scipy, matplotlib, joblib ve daha fazlasi dahil
- pip install YAPMA -- modul yeterli

**MATLAB:**  (ANFIS backend icin)

---

## 7. Tahmini Sure (orfoz, 55 cekirdek)

| Faz | Sure | Notlar |
|-----|------|--------|
| PFAZ 1: Dataset | ~2 saat | 267 cekirdek, 20+ dataset |
| PFAZ 2: AI Egitim | ~15-20 saat | 50 config x hedef x dataset |
| PFAZ 3: ANFIS | ~8-10 saat | MATLAB backend ile |
| PFAZ 4-7: Analiz | ~5-8 saat | Topluluk, capraz model vs. |
| PFAZ 8-10: Rapor/Tez | ~3-5 saat | Excel, LaTeX, PDF |
| **Toplam** | **~35-45 saat** | Faz faz 5 ayri job onerilen |

Cekirdek-saat tuketim tahmini: ~2000-3000 (YL kotasinin ~%1-1.5)

---

## 8. Calisma Dizinleri

```
~/hpcv1/                    # Proje koku (kalici, HOME ~50GB)
~/hpcv1/data/aaa2.txt       # Veri dosyasi (ZORUNLU)
~/hpcv1/logs/               # Slurm log dosyalari
~/hpcv1/outputs/            # Tum ciktilar

/arf/scratch/ahmacar/       # Gecici scratch (buyuk dosyalar, hizli I/O)
                            # Uzun sure saklanmaz -- sonuclari HOME'a kopyala
```

---

## 9. Sik Karsilasilan Hatalar

| Hata | Sebep | Cozum |
|------|-------|-------|
|  | Modul adi yanlis |  |
|  | Account eksik |  ekle |
|  | Bellek asimi |  dene |
|  | Sure asimi |  artir veya faz bol |
| Import error | pip install yapildi |  |

---

*TRUBA-KULLANIM-KILAVUZU.md v2.0 | 2026-05-13 | Sprint 9B*
*Guncelleme: gercek modul (apps/truba-ai/cpu-2024.0), partition (orfoz),*
*SSH adresi (levrek.ulakbim.gov.tr), pip install uyarisi eklendi*
