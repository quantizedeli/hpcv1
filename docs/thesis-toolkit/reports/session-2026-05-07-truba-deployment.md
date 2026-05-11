# Oturum Raporu — 2026-05-07
## TRUBA Deployment Hazırlığı + İki Repo Klonu

**Oturum Tarihi:** 2026-05-07  
**Yapılan İşlemler:** Bug tarama, iki repo klonu, TRUBA kılavuzu, desktop config

---

## 1. Bug Tarama Sonuçları

Python Reviewer agent tüm kritik dosyaları inceledi:

| Bug ID | Dosya | Durum | Açıklama |
|--------|-------|-------|----------|
| BUG-02 | `core_modules/constants.py:44` | ✅ PASS | `HBAR_C = 197.3269804` tanımlı, `woods_saxon.py:15` doğru import ediyor |
| BUG-31 | `pfaz12_advanced_analytics/__init__.py:32-51` | ✅ PASS | `NuclearBandAnalyzer` try/except ImportError bloğu ile graceful fallback var |
| BUG-32 | `pfaz13_automl/automl_retraining_loop.py:40-60` | ✅ PASS | IndentationError giderilmiş, satırlar temiz |
| BUG-01 | `pfaz01_dataset_generation/qm_filter_manager.py:153,181` | ⚠️ AÇIK | Q=0 kürsel çekirdekler hala filtreleniyor; önceki oturumda "tasarım kararı" denildi ama kod değişmedi |
| — | `main.py:1751-1754` | ✅ PASS | `input()` → `sys.stdin.isatty()` ve `HPC_MODE` env var ile korumalı |
| — | `pfaz10_master_integration.py:2283-2293` | ✅ PASS | `_interactive` flag ile korumalı |
| — | `pfaz10_thesis_orchestrator.py:1371` | ✅ DÜZELTİLDİ | `/mnt/project` hardcoded yol → `os.environ.get('PROJECT_DIR')` veya `os.getcwd()` tabanlı dinamik yol |
| — | `pfaz_status.json` | ⚠️ DONMUŞ | PFAZ 01, 02, 10 "running" ama son güncelleme tarihleri çok eski (Mart-Nisan) → sıfırlandı |
| — | Bare `except:` | ✅ PASS | Hiç tipsiz except yok |
| — | Hardcoded /mnt/ (dataset_generation_pipeline_v2.py:1331) | ⚠️ UYARI | Aktif `main()` içinde ama fallback var; demo mode devreye giriyor |

**Ek Not:** `constants_v1.1.0.py` dosyası hala mevcut; aktif pipeline `constants.py` kullanıyor, bu eski dosya kafa karıştırıcı ve bakım riski. İleride silinebilir.

---

## 2. Oluşturulan Repolar

### nucdatav2-truba (HPC — Tam Pipeline)

**Konum:** `C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-truba`  
**Kaynak:** `skillv1/thesis-nuclear-ai/repo` → robocopy (git, pycache, outputs hariç, 284 dosya)

| Yeni / Değiştirilen Dosya | İçerik |
|---------------------------|--------|
| `truba_slurm_job.sh` | TRUBA SLURM script: `hamsi`/`palamut` partition, `HPC_MODE=1`, `OMP_NUM_THREADS=1`, e-posta bildirimi |
| `setup_truba.sh` | İlk kurulum scripti: modül yükle, venv oluştur, paket kur, kontrol et |
| `TRUBA-KULLANIM-KILAVUZU.md` | 12 bölüm kılavuz (hesap, SSH, scp, kurulum, sbatch, log, çıktı alma, sorun giderme) |
| `pfaz_status.json` | Tüm fazlar `pending` sıfırlandı |
| `pfaz10_thesis_orchestrator.py:1369-1374` | `/mnt/project` → `$PROJECT_DIR` env var tabanlı dinamik yol |

**Config:** Orijinal `config.json` (tam 848 dataset, 50 konfigürasyon, tüm modeller)

### nucdatav2-desktop (Hafif — Desktop)

**Konum:** `C:\Users\Hakan Yakut\Desktop\ahmet\nucdatav2-desktop`  
**Kaynak:** Aynı kaynak, aynı 284 dosya

| Yeni / Değiştirilen Dosya | İçerik |
|---------------------------|--------|
| `config_desktop.json` | Hafifletilmiş config: 3 boyut (100/150/267), 3 model (RF/XGB/DNN), 10 konfigürasyon, n=50 MC |
| `run_desktop.bat` | Windows çift tıkla çalıştırma scripti |
| `README_DESKTOP.md` | Desktop vs TRUBA fark tablosu, kurulum, çalıştırma komutları |
| `pfaz_status.json` | PFAZ 01 `pending` sıfırlandı |

---

## 3. TRUBA Sistem Bilgileri

| Bilgi | Değer |
|-------|-------|
| Giriş sunucusu | `levrek.ulakbim.gov.tr` (SSH, port 22) |
| Ana partition (CPU) | `hamsi` — 40 çekirdek, 192GB RAM, Intel Xeon |
| GPU partition | `palamut` — NVIDIA Tesla V100 16GB |
| Yüksek bellek | `levrek` — 1.5TB RAM |
| Test partition | `short` — max 1 saat |
| Depolama | `$HOME` (~50GB kalıcı) + `/arf/scratch/$USER` (geçici, hızlı) |
| İş yöneticisi | SLURM (`sbatch`, `squeue`, `scancel`) |
| Python modülü | `centos7.9/comp/python/3.11.2` (kontrol için: `module avail | grep python`) |
| Başvuru | `https://portal.truba.gov.tr` |

---

## 4. Pipeline Durum Karşılaştırması

| PFAZ | Kaynak Repo Durumu | nucdatav2-truba Durumu | nucdatav2-desktop Durumu |
|------|--------------------|------------------------|--------------------------|
| 01 | running (donmuş, Nisan) | pending | pending |
| 02 | running (donmuş, Nisan) | pending | pending |
| 03-09 | completed | pending (sıfırlandı) | pending |
| 10 | running (donmuş, Mart) | pending | pending |
| 11 | skipped | skipped | skipped |
| 12 | failed | pending | pending |
| 13 | failed | pending | pending |

> Not: TRUBA'da tüm fazlar sıfırlı başlayacak. Desktop'ta `config_desktop.json` ile çalışacak.

---

## 5. Sıradaki Adımlar

1. **TRUBA hesabı yok ise:** `https://portal.truba.gov.tr` başvuru (1-5 iş günü onay)
2. **Dosya transferi:** `scp -r "...\nucdatav2-truba" <kullanici>@levrek.ulakbim.gov.tr:~/`
3. **Kurulum:** `bash setup_truba.sh`
4. **SLURM script güncelle:** Danışman adı, GPU tercihi, partition seçimi
5. **Test job:** `sbatch --partition=short --time=01:00:00 truba_slurm_job.sh --pfaz 1`
6. **Tam pipeline:** `sbatch truba_slurm_job.sh`

---

## 6. Bekleyen Kararlar

| Karar | Bağlam |
|-------|--------|
| **BUG-01: Q=0 kürsel çekirdekler** | `qm_filter_manager.py:153` — filtre baki. Q=0 fiziksel olarak geçerli (küresel çekirdek). Filtreden çıkarmak istiyorsan söyle, düzeltirim. |
| **GPU mu CPU mu?** | `truba_slurm_job.sh`'da `palamut` (GPU) veya `hamsi` (CPU) seçimi. Tavsiye: önce `hamsi` ile test et. |
| **Desktop'ta hangi config?** | `config_desktop.json` varsayılan. Çalıştırırken `--config config_desktop.json` gibi argüman gerekmez, manuel seçim yapman gerekebilir. Bunu entegre etmemi istersen yapabilirim. |
| **PFAZ 01-02 yeniden eğitim** | TRUBA'da temiz çalıştırıldığında BUG-02 (HBAR_C) düzeltmesi etkili olacak ve WS özellikleri artık doğru hesaplanacak. |

---

*Hazırlayan: Claude Code | 2026-05-07*  
*Referans: pipeline-hatalari.md, HPC_DEPLOYMENT_CHECKLIST.md, V10_QA_REREVIEW_REPORT.md*
