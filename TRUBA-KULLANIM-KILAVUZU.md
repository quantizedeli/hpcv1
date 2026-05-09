# TRUBA Kullanım Kılavuzu
## Nuclear Physics AI Pipeline v2.0.0 — nucdatav2-truba

**Hazırlayan:** Ahmet Kemal Acar  
**Güncelleme:** 2026-05-07  
**Sistem:** TRUBA — ULAKBİM Ulusal Yüksek Başarım Bilgisayarı  
**Destek:** `support@truba.gov.tr` | `https://portal.truba.gov.tr`

---

## İçindekiler

1. [TRUBA Nedir? — Hızlı Özet](#1-truba-nedir)
2. [Ön Koşullar — Hesap ve Erişim](#2-ön-koşullar)
3. [Dosya Transferi (Windows → TRUBA)](#3-dosya-transferi)
4. [TRUBA'da İlk Kurulum](#4-trubada-ilk-kurulum)
5. [Pipeline'ı Çalıştırma](#5-pipelineı-çalıştırma)
6. [SLURM Job Yönetimi](#6-slurm-job-yönetimi)
7. [İzleme ve Log Takibi](#7-i̇zleme-ve-log-takibi)
8. [Sonuçları Geri Alma (TRUBA → Windows)](#8-sonuçları-geri-alma)
9. [Partition Seçimi Rehberi](#9-partition-seçimi-rehberi)
10. [Sık Karşılaşılan Sorunlar](#10-sık-karşılaşılan-sorunlar)
11. [Faz Bazlı Çalıştırma Stratejisi](#11-faz-bazlı-çalıştırma-stratejisi)
12. [Komut Özet Tablosu](#12-komut-özet-tablosu)

---

## 1. TRUBA Nedir?

TRUBA (Türkiye Ulusal Yüksek Başarım Araştırma Merkezi), ULAKBİM tarafından işletilen Türkiye'nin ulusal süperbilgisayar altyapısıdır. Akademik araştırmacılara ücretsiz hesaplama kaynağı sağlar.

**Temel Özellikler:**
- **Giriş Sunucusu:** `levrek.ulakbim.gov.tr` (SSH, port 22)
- **Alternatif:** `172.16.11.1` (iç ağdan)
- **İş Yöneticisi:** SLURM (sbatch, squeue, scancel)
- **Depolama:**
  - `$HOME` → `/truba/home/<kullanıcı_adı>` (kalıcı, kota ~50GB)
  - `/arf/scratch/<kullanıcı_adı>` → Scratch (hızlı, geçici, kota ~10TB)
- **Partition'lar:**

| Partition | Donanım | Max Süre | Ne İçin |
|-----------|---------|----------|---------|
| `hamsi` | Intel Xeon, 40 çekirdek, 192GB RAM | 240 saat | CPU yoğun hesaplama ✅ ÖNERİLEN |
| `barbun` | Intel Xeon, 28 çekirdek, 128GB RAM | 240 saat | CPU, alternatif |
| `palamut` | GPU: Tesla V100 16GB + CPU | 240 saat | GPU gerektiren işler |
| `sardalya` | GPU: A100 + CPU | 240 saat | Büyük DNN/TF işleri |
| `levrek` | 1.5TB RAM CPU | 240 saat | Çok büyük bellekli işler |
| `mid1/mid2` | CPU | 24 saat | Orta ölçek |
| `short` | CPU | 1 saat | Test/debug |

---

## 2. Ön Koşullar

### 2.1 TRUBA Hesabı

1. **Portal:** `https://portal.truba.gov.tr` adresine git
2. **"Başvuru"** → **"Hesap Başvurusu"** seç
3. Kurumsal e-posta ile kayıt ol (üniversite e-postası zorunlu)
4. Başvuru onaylandıktan sonra `support@truba.gov.tr` adresine kullanıcı adı/şifre e-postası gelir
5. Onay süresi: 1-5 iş günü

### 2.2 Windows'ta SSH İstemcisi

**Seçenek 1 — Windows 11 yerleşik SSH (PowerShell):**
```powershell
# Kontrol et
ssh -V
# Yoksa yükle:
Add-WindowsCapability -Online -Name OpenSSH.Client*
```

**Seçenek 2 — MobaXterm (önerilir — SFTP + SSH tek uygulamada):**
- `https://mobaxterm.mobatek.net` adresinden ücretsiz sürümü indir
- SFTP arayüzü ile dosya sürükle-bırak

**Seçenek 3 — WinSCP (dosya transferi için):**
- `https://winscp.net` adresinden indir

---

## 3. Dosya Transferi (Windows → TRUBA)

### 3.1 İlk Transfer — SSH ile bağlan

PowerShell açın ve bağlanın:

```powershell
ssh <kullanici_adi>@levrek.ulakbim.gov.tr
```

> İlk bağlantıda "fingerprint" onayı sorar → `yes` yazın.
> Şifrenizi girin (terminal'de görünmez, normal).

### 3.2 TRUBA'da Dizin Oluştur

```bash
# TRUBA'da (SSH ile bağlı olduğunuzda)
mkdir -p ~/nucdatav2-truba
ls ~/
```

### 3.3 Dosyaları Gönder (scp ile)

PowerShell'i **yeni bir pencere**de açın (TRUBA bağlantısı açık kalsın):

```powershell
# nucdatav2-truba klasörünü TRUBA'ya gönder
# TÜMÜNÜ bir seferde:
scp -r "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba" <kullanici_adi>@levrek.ulakbim.gov.tr:~/

# SADECE kod (outputs hariç — zaten hariç tutuluyor):
scp -r "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba" <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/
```

> **Not:** İlk transferde tüm dosyalar gider. Sonraki güncellemelerde sadece değişen dosyaları gönderin.

### 3.4 Tek Dosya Güncellemesi

```powershell
# Sadece main.py güncelle
scp "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba\main.py" <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/

# Sadece config güncelle
scp "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba\config.json" <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/
```

### 3.5 MobaXterm ile Transfer (Kolayı)

1. MobaXterm aç → **"Session"** → **"SSH"**
2. Remote host: `levrek.ulakbim.gov.tr`
3. Kullanıcı adını gir → Bağlan
4. Sol panel otomatik SFTP açılır
5. Windows'ta `nucdatav2-truba` klasörünü sol panele sürükle-bırak ✅

### 3.6 Transfer Doğrulama

TRUBA'da (SSH bağlantısında):
```bash
cd ~/nucdatav2-truba
ls -la
wc -l data/aaa2.txt   # 268 satır olmalı (267 çekirdek + başlık)
python3 -c "import json; json.load(open('config.json')); print('config.json OK')"
```

---

## 4. TRUBA'da İlk Kurulum

SSH ile TRUBA'ya bağlı olduğunuzu varsayıyorum:

### 4.1 Otomatik Kurulum (setup_truba.sh)

```bash
cd ~/nucdatav2-truba
chmod +x setup_truba.sh
bash setup_truba.sh
```

Bu script:
- Python modülünü yükler
- `~/nucdatav2_env` sanal ortamını oluşturur
- `requirements-hpc.txt` paketlerini kurar
- Veri ve config dosyalarını doğrular
- Çıktı dizinlerini oluşturur
- İsteğe bağlı smoke test çalıştırır

### 4.2 Manuel Kurulum (adım adım)

```bash
# 1. Mevcut Python modüllerini listele
module avail 2>&1 | grep -i python

# 2. Python yükle (versiyon değişebilir — listeden seç)
module load centos7.9/comp/python/3.11.2

# 3. Sanal ortam oluştur
python3 -m venv ~/nucdatav2_env
source ~/nucdatav2_env/bin/activate

# 4. Paketleri yükle
pip install --upgrade pip
pip install -r requirements-hpc.txt

# 5. Kontrol
python3 -c "import numpy, pandas, sklearn, xgboost; print('Paketler OK')"

# 6. Dizinler
mkdir -p logs outputs/generated_datasets outputs/trained_models outputs/anfis_models \
         outputs/reports outputs/visualizations outputs/thesis outputs/ensemble_results \
         outputs/unknown_predictions outputs/cross_model_analysis outputs/aaa2_results
```

### 4.3 SLURM Script Konfigürasyonu

```bash
nano ~/nucdatav2-truba/truba_slurm_job.sh
```

Düzenlenmesi gereken satırlar:
```bash
#SBATCH --partition=hamsi          # Partition: hamsi (CPU) veya palamut (GPU)
#SBATCH --mail-user=ahmetkemalacar@gmail.com   # ✅ Zaten ayarlı

export THESIS_SUPERVISOR="Prof. Dr. [Danışman Adı]"   # ← Buraya danışman adını yaz
export THESIS_UNIVERSITY="Sakarya Üniversitesi"        # ← Kontrol et
```

---

## 5. Pipeline'ı Çalıştırma

> **ÖNEMLİ:** Login node'da hesaplama YAPMAYIN. İşleri daima `sbatch` ile gönderin.

### 5.1 Tüm Pipeline (Tavsiye Edilen Başlangıç)

```bash
cd ~/nucdatav2-truba

# Temiz başlangıç için status sıfırla
echo '{}' > pfaz_status.json

# Job gönder
sbatch truba_slurm_job.sh

# Cıktı: Submitted batch job 123456
# Bu job ID'yi not edin!
```

### 5.2 Tek Faz Çalıştırma

```bash
sbatch truba_slurm_job.sh --pfaz 1     # Sadece PFAZ 1 (dataset)
sbatch truba_slurm_job.sh --pfaz 2     # Sadece PFAZ 2 (AI eğitim)
sbatch truba_slurm_job.sh --pfaz 3     # Sadece PFAZ 3 (ANFIS)
sbatch truba_slurm_job.sh --pfaz 13    # Sadece PFAZ 13 (AutoML)
```

### 5.3 Belirli Faz Aralığı

```bash
sbatch truba_slurm_job.sh --run-all --start-from 5 --end-at 10
```

### 5.4 Resume (Kaldığı Yerden Devam)

```bash
sbatch truba_slurm_job.sh --pfaz 1 --mode resume
sbatch truba_slurm_job.sh --pfaz 2 --mode resume
```

### 5.5 Debug Modu (short partition, 1 saat)

Tam pipeline göndermeden önce test etmek için:

```bash
sbatch --partition=short --time=01:00:00 --cpus-per-task=4 --mem=16G \
    truba_slurm_job.sh --pfaz 1 --mode run
```

---

## 6. SLURM Job Yönetimi

### 6.1 Job Durumu

```bash
# Kendi job'larını listele
squeue -u $USER

# Belirli job
squeue -j 123456

# Tüm bilgiler
scontrol show job 123456
```

Durum kodları:
- `PD` → Pending (sıra bekliyor)
- `R` → Running (çalışıyor)
- `CG` → Completing (bitiyor)
- `F` → Failed (başarısız)
- `CD` → Completed (tamamlandı)

### 6.2 Job İptal

```bash
scancel 123456        # Belirli job
scancel -u $USER      # Tüm job'ların (dikkatli ol!)
```

### 6.3 Job Önceliği / Kalan Süre

```bash
squeue -u $USER -l    # Uzun format, başlangıç zamanı tahmini
sshare -u $USER       # Kullanım kotası
```

### 6.4 Kaynakları Görmek

```bash
sinfo                 # Tüm partitionlar ve durumları
sinfo -p hamsi        # Sadece hamsi partition
sinfo -o "%n %c %m %G %T"   # Node bilgileri (isim, CPU, RAM, GPU, durum)
```

---

## 7. İzleme ve Log Takibi

### 7.1 Gerçek Zamanlı Log

```bash
# Job çalışırken canlı log izle (job ID ile)
tail -f ~/nucdatav2-truba/logs/truba_123456.out

# Hata logu
tail -f ~/nucdatav2-truba/logs/truba_123456.err

# Son 50 satır
tail -50 ~/nucdatav2-truba/logs/truba_123456.out
```

### 7.2 PFAZ Durum Kontrolü

```bash
cd ~/nucdatav2-truba
python3 -c "
import json
s = json.load(open('pfaz_status.json'))
print('PFAZ Durum Özeti:')
for k, v in sorted(s.items()):
    status = v.get('status', '?')
    progress = v.get('progress', 0)
    print(f'  {k}: {status} — {progress}%')
"
```

### 7.3 Uyarı Özeti

```bash
python3 -c "
import json
try:
    with open('outputs/pipeline_warnings.json') as f:
        w = json.load(f)
    print(f'Toplam uyarı: {len(w)}')
    for item in w[-5:]:
        print(' -', item)
except FileNotFoundError:
    print('Henüz uyarı dosyası yok (pipeline başlamamış olabilir)')
"
```

### 7.4 Log Parser

```bash
python3 scripts/log_parser.py
```

---

## 8. Sonuçları Geri Alma (TRUBA → Windows)

### 8.1 Tüm Outputs'ı Çek (scp)

PowerShell'de (Windows'ta):

```powershell
# Tüm outputs/ dizinini çek
scp -r <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/outputs "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba\"

# Sadece Excel raporları
scp <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/outputs/reports/*.xlsx "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba\outputs\reports\"

# Sadece tez (LaTeX) dosyaları
scp -r <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/outputs/thesis "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba\outputs\"

# Sadece görselleştirmeler
scp -r <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/outputs/visualizations "C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba\outputs\"
```

### 8.2 Seçici Transfer (Büyük Dosyaları Filtrele)

```powershell
# Sadece .xlsx ve .tex dosyaları
scp "<kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/outputs/reports/*.xlsx" .

# Log dosyası
scp "<kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/logs/truba_123456.out" .
```

### 8.3 MobaXterm ile Çekme

1. SFTP panelinde `~/nucdatav2-truba/outputs/` dizinine git
2. İstediğin klasörü/dosyaları sağ tık → **"Download"** seç
3. Yerel Windows dizinine kaydeder ✅

### 8.4 Toplu Transfer İçin tar Kullan

```bash
# TRUBA'da — sıkıştır
cd ~/nucdatav2-truba
tar -czf outputs_results.tar.gz outputs/reports outputs/thesis outputs/visualizations
ls -lh outputs_results.tar.gz
```

```powershell
# Windows'ta — çek
scp <kullanici_adi>@levrek.ulakbim.gov.tr:~/nucdatav2-truba/outputs_results.tar.gz "C:\Users\Hakan Yakut\Desktop\ahmet\"
# Aç: 7-Zip ile veya PowerShell:
tar -xzf outputs_results.tar.gz
```

---

## 9. Partition Seçimi Rehberi

### Ne Zaman Hangi Partition?

| Durum | Partition | Örnek Komut |
|-------|-----------|-------------|
| Test / Debug (≤1 saat) | `short` | `#SBATCH --partition=short --time=01:00:00` |
| PFAZ 1 (dataset üretimi) | `hamsi` | `#SBATCH --partition=hamsi --cpus-per-task=40` |
| PFAZ 2 (AI eğitim, CPU) | `hamsi` | `#SBATCH --partition=hamsi --mem=128G` |
| PFAZ 2 (AI eğitim, GPU) | `palamut` | `#SBATCH --partition=palamut --gres=gpu:1` |
| PFAZ 3 (ANFIS) | `hamsi` | `#SBATCH --partition=hamsi --cpus-per-task=8` |
| PFAZ 7 (Ensemble) | `barbun` | `#SBATCH --partition=barbun` |
| PFAZ 9 (Monte Carlo) | `hamsi` | `#SBATCH --partition=hamsi --cpus-per-task=40` |
| PFAZ 13 (AutoML) | `hamsi` | `#SBATCH --partition=hamsi --time=24:00:00` |
| Tüm Pipeline | `hamsi` | `#SBATCH --partition=hamsi --time=48:00:00` |

### GPU Kullanım Kararı

GPU'yu yalnızca şu durumlarda aç:
- `config.json` → `pfaz02_ai_training.gpu.enabled = true`
- TensorFlow DNN modelleri eğitiliyorsa
- XGBoost v2.0+ `device: cuda` ayarlıysa

Aksi halde `hamsi` (CPU) çok daha erişilebilir ve genellikle daha hızlı kuyruk süresi.

---

## 10. Sık Karşılaşılan Sorunlar

### Problem: SSH bağlantısı reddediliyor

```
ssh: connect to host levrek.ulakbim.gov.tr port 22: Connection refused
```

**Çözüm:**
- Hesap onaylanmadıysa: `support@truba.gov.tr` adresine e-posta
- VPN gerekebilir: ULAKBİM VPN bilgisi için destek birimi
- Alternatif: `ssh <kullanici_adi>@172.16.11.1` (iç ağdan)

### Problem: Job başlamıyor (PD durumunda kalıyor)

```bash
squeue -j 123456
# REASON: Resources, Priority, ReqNodeNotAvail
```

**Çözüm:**
- `Resources` → Node boşalmasını bekle (normal)
- `Priority` → Düşük öncelik, bekle
- Daha az kaynak talep et:
  ```bash
  sbatch --cpus-per-task=8 --mem=32G truba_slurm_job.sh
  ```

### Problem: Job hemen FAILED

```bash
tail logs/truba_123456.err
```

Olası nedenler:
1. **Python modülü yüklenmemiş:**
   ```bash
   # truba_slurm_job.sh içinde module load satırını kontrol et
   module avail 2>&1 | grep python
   ```

2. **Sanal ortam bulunamadı:**
   ```bash
   bash setup_truba.sh  # Tekrar çalıştır
   ```

3. **Paket eksik:**
   ```bash
   source ~/nucdatav2_env/bin/activate
   pip install <eksik_paket>
   ```

4. **data/aaa2.txt yok:**
   ```bash
   ls data/aaa2.txt  # Kontrol et
   # Yoksa Windows'tan tekrar gönder
   ```

### Problem: Çok Uzun Süre Bekliyor

```bash
# Daha erişilebilir partition dene
sbatch --partition=mid1 truba_slurm_job.sh
# veya
sbatch --partition=barbun truba_slurm_job.sh
```

### Problem: Memory hatası (OOM)

```
slurmstepd: error: Exceeded step memory limit
```

**Çözüm:**
```bash
# Daha fazla RAM iste
#SBATCH --mem=192G
# veya levrek partition (1.5TB)
#SBATCH --partition=levrek
```

### Problem: pip install başarısız

```bash
# Ağ bağlantısı yoksa:
pip install --no-index --find-links=/arf/sw/lib/python3.11/site-packages -r requirements-hpc.txt
# veya conda kullan:
module load centos7.9/comp/python/anaconda3
conda create -n nucdatav2 python=3.11
conda activate nucdatav2
conda install numpy pandas scikit-learn
pip install xgboost lightgbm optuna
```

### Problem: PFAZ 1/2 "running" ama bitmiyor

pfaz_status.json'da donmuş durum var. Sıfırla:

```bash
python3 -c "
import json
s = json.load(open('pfaz_status.json'))
for k in s:
    if s[k].get('status') == 'running':
        s[k]['status'] = 'pending'
        print('Reset:', k)
json.dump(s, open('pfaz_status.json','w'), indent=2)
"
```

### Problem: TensorFlow GPU bulunamıyor

```bash
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
# [] çıkıyorsa GPU görünmüyor

# Kontrol:
module list  # cuda yüklü mü?
module load centos7.9/lib/cuda/12.1
echo $CUDA_VISIBLE_DEVICES
```

---

## 11. Faz Bazlı Çalıştırma Stratejisi

Pipeline'ı bütün çalıştırmak yerine faz faz ilerletmek hem güvenli hem de daha esnek.

### Önerilen Strateji

**Aşama 1 — Test (short partition, 1 saat):**
```bash
sbatch --partition=short --time=01:00:00 --cpus-per-task=4 --mem=16G \
    truba_slurm_job.sh --pfaz 1 --mode run
# Logları izle, hata yoksa devam et
```

**Aşama 2 — Dataset Üretimi (hamsi, 8-12 saat):**
```bash
# pfaz_status.json sıfırla
echo '{}' > pfaz_status.json
sbatch --partition=hamsi --time=12:00:00 truba_slurm_job.sh --pfaz 1 --mode run
# Tamamlanınca:
squeue -u $USER  # Job bitti mi?
ls outputs/generated_datasets/ | wc -l  # 848 dataset var mı?
```

**Aşama 3 — AI Eğitim (hamsi veya palamut, 24-48 saat):**
```bash
sbatch --partition=hamsi --time=48:00:00 truba_slurm_job.sh --pfaz 2 --mode run
# CPU ile: ~24-36 saat
# GPU ile (palamut): ~12-24 saat
```

**Aşama 4 — Kalan Fazlar (12-24 saat):**
```bash
sbatch --partition=hamsi --time=24:00:00 \
    truba_slurm_job.sh --run-all --start-from 3 --end-at 10
```

### Checkpoint ile Devam

Job kesilirse (timeout, node hatası):

```bash
# pfaz_status.json'a bak
python3 -c "
import json
s = json.load(open('pfaz_status.json'))
for k, v in s.items():
    print(k, v.get('status'))
"

# Yarım kalan fazı resume et
sbatch truba_slurm_job.sh --pfaz 2 --mode resume
```

---

## 12. Komut Özet Tablosu

### Temel SSH/SCP Komutları (Windows PowerShell)

```powershell
# Bağlan
ssh ahmet@levrek.ulakbim.gov.tr

# Dosya gönder
scp -r "C:\...\nucdatav2-truba" ahmet@levrek.ulakbim.gov.tr:~/

# Dosya çek (outputs)
scp -r ahmet@levrek.ulakbim.gov.tr:~/nucdatav2-truba/outputs "C:\...\nucdatav2-truba\"

# Tek dosya güncelle
scp "C:\...\main.py" ahmet@levrek.ulakbim.gov.tr:~/nucdatav2-truba/
```

### TRUBA İş Yönetimi (TRUBA SSH'de)

```bash
# Job gönder
sbatch truba_slurm_job.sh                     # Tüm pipeline
sbatch truba_slurm_job.sh --pfaz 2            # Tek faz

# İzle
squeue -u $USER                               # Job listesi
squeue -j 123456                              # Belirli job
tail -f logs/truba_123456.out                 # Log izle

# İptal
scancel 123456                                # Job iptal

# Sistem bilgisi
sinfo -p hamsi                                # Partition durumu
sshare -u $USER                              # Kullanım kotası

# Pipeline durumu
python3 -c "import json; [print(k,v.get('status')) for k,v in json.load(open('pfaz_status.json')).items()]"
```

### Kurulum Komutları (TRUBA SSH'de)

```bash
# Modül yükle
module purge
module load centos7.9/comp/python/3.11.2

# Ortam
source ~/nucdatav2_env/bin/activate           # Aktive et
bash setup_truba.sh                           # İlk kurulum

# Kontrol
python3 scripts/health_check.py
pytest tests/test_smoke -v
```

---

## Notlar ve İpuçları

1. **Login node'da hesaplama yapma** — sadece `sbatch` ile iş gönder. Login node'da uzun süreli Python çalıştırmak hesabının askıya alınmasına neden olabilir.

2. **$HOME kotası** — `/truba/home/$USER` genellikle 50GB. Büyük çıktılar için `/arf/scratch/$USER` kullan (geçici, periyodik temizlenir).

3. **job mail bildirim** — `#SBATCH --mail-type=END,FAIL` ile job bitince/başarısız olunca e-posta alırsın.

4. **pfaz_status.json** — Pipeline sürdürme mekanizması. Job kesilirse bunu sıfırlama (sadece failed olanları pending yap).

5. **Module listesi** — Kullanılabilir modüller sistemden sisteme değişir. Her zaman `module avail 2>&1 | grep -i python` ile kontrol et.

6. **TRUBA desteği** — Sorun için: `support@truba.gov.tr` veya `https://portal.truba.gov.tr`

---

*Nuclear Physics AI Pipeline v2.0.0 — TRUBA Kılavuzu*  
*Ahmet Kemal Acar | 2026-05-07*
