# QA Mühendisi Oyun Kitabı — Cross-Project Rehber

**Versiyon:** 1.0  
**Tarih:** 2026-05-14  
**Kaynak:** hpcv1 Nuclear Physics AI Pipeline, Sprint 1-13 deneyimleri  
**Kapsam:** HPC/ML pipeline projeleri, ama prensipler genel geçer

---

## Bu Kitap Ne İçin?

Sprint 1-13 boyunca 99 bug yakalandı. Çoğu benzer kategorilere düşüyordu.
Bu kitap, aynı kategorilerdeki bugları gelecekte **daha erken** yakalamak için
sistematik bir QA süreci tanımlar. Herhangi bir ML pipeline projesinde kullanılabilir.

---

## Bölüm 1: HPC/Slurm Exit Code Zinciri

### Kontrol Listesi

```bash
# 1. Pipe + tee pattern — $? YANLIŞ, ${PIPESTATUS[0]} DOĞRU
python3 main.py 2>&1 | tee log.txt
EXIT=$?              # YANLIŞ: tee exit'i
EXIT=${PIPESTATUS[0]} # DOĞRU: python exit'i

# 2. Her Slurm job script için kontrol:
grep -n '\$?' job*.sh | grep -v PIPESTATUS
# Çıktı varsa → düzelt

# 3. afterok zinciri gerçekten kırılıyor mu?
# Test: job1'i kasıtlı fail et, job2 başlamamalı
```

### Kural

> Bash'te `cmd1 | cmd2; echo $?` → `cmd2`'nin exit'i. `cmd1` fail etse bile 0 döner.
> HPC'de bu = sessiz veri kaybı + yanıltıcı sacct raporu.

---

## Bölüm 2: Python Silent Failure Avı

### Pattern 1: Exception yutma

```python
# KÖTÜ — HPC modda hata kaybolur
except Exception as e:
    logger.warning(f"devam ediliyor: {e}")
    continue

# İYİ — hatayı kaydet, sonunda RuntimeError
failed_phases = []
except Exception as e:
    failed_phases.append(phase_id)
    logger.error(...)

if failed_phases:
    raise RuntimeError(f"Başarısız fazlar: {failed_phases}")
```

### Pattern 2: `skipped` = `completed` yanılgısı

```python
# KÖTÜ
self.status_manager.update_pfaz(id, 'completed', 100)
return {'status': 'skipped'}

# İYİ — strict mode'da RuntimeError
if skipped and strict_mode and HPC:
    raise RuntimeError(f"PFAZ{id} atlanamaz: {reason}")
```

### Tarama Komutu

```bash
# Sessiz devam eden except bloklarını bul
grep -n "except.*:" main.py | grep -v "raise\|sys.exit\|RuntimeError" | head -20
```

---

## Bölüm 3: Inter-Module Veri Akışı Denetimi

### Altın Kural

> "PFAZ_A çıktısı = PFAZ_B girdisi" ise, sütun adları birebir eşleşmeli.
> Bu eşleşmeyi **test et**, varsayma.

### Denetim Scripti

```python
# inter_pfaz_audit.py -- her sprint sonunda çalıştır
import pandas as pd
from pathlib import Path

def check_column_exists(file_path, required_columns, context):
    df = pd.read_excel(file_path)
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        print(f"[FAIL] {context}: Eksik sütunlar: {missing}")
        print(f"       Mevcut: {list(df.columns)[:10]}")
    else:
        print(f"[OK] {context}: {required_columns}")

# PFAZ2 → PFAZ3 kontrol
check_column_exists(
    'outputs/trained_models/training_summary.xlsx',
    ['Target', 'Val_R2', 'Dataset_Name'],  # PFAZ3'ün beklediği
    'PFAZ2→PFAZ3'
)
```

### Yaygın Tuzaklar

| Tuzak | Örnek | Fix |
|-------|-------|-----|
| Sütun adı tutarsızlığı | `Test_R2` vs `R2_test` | SSoT: bir dosyada tanımla, diğeri okusun |
| Path hardcode | `/arf/home/ahmacar/...` | `${DIR:-/default/path}` env override |
| Sibling inference | `output_dir.parent / 'anfis_models'` | Constructor parametresi zorunlu yap |

---

## Bölüm 4: Dependency Kontrol Sistemi

### Minimal Kontrol

```python
REQUIRED = {'numpy', 'pandas', 'scikit-learn', 'scipy', 'optuna', 'lightgbm'}
OPTIONAL = {'catboost', 'SALib'}

def check_deps():
    missing_req = []
    for pkg in REQUIRED:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing_req.append(pkg)
    
    if missing_req:
        sys.exit(f"[FAIL] Eksik zorunlu paketler: {missing_req}")
    
    for pkg in OPTIONAL:
        try:
            importlib.import_module(pkg)
            print(f"[OK-OPT] {pkg}")
        except ImportError:
            print(f"[SKIP-OPT] {pkg} -- opsiyonel, devam")
```

### Kural

> Bir faz X paketini gerektiriyorsa, X `REQUIRED_PACKAGES`'ta olmalı.
> `--check-deps` çalıştırınca gerçekten hazır olup olmadığı anlaşılmalı.

---

## Bölüm 5: Dead Code Yönetimi

### Dead Code Nedir?

Yazılmış, içe aktarılmayan, hiç çağrılmayan kod. Bakım yükü + yanıltıcı özellik listesi.

### Tespit

```bash
# Modülün gerçekten import edilip edilmediğini kontrol et
grep -rn "from pfaz_modules.pfaz12.*import BootstrapCI" . --include="*.py"
# Çıktı yoksa → dead code

# Alternatif: Python ile
python3 -c "
import ast, sys
tree = ast.parse(open('main.py').read())
imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
print([ast.dump(i) for i in imports if 'bootstrap' in ast.dump(i).lower()])
"
```

### Yönetim Kararları

| Karar | Ne zaman | Nasıl |
|-------|----------|-------|
| Aktive et | Teze değer katıyor, <1 saat sürer | import ekle, main.py'de çağır |
| Dead note | Uzun sürer veya dep eksik | Dosya başına `# DEAD_CODE_NOTE (BUG-XX): ...` |
| Sil | Tamamen gereksiz | `git rm`, commit mesajında açıkla |

---

## Bölüm 6: Reproducibility Kontrol Listesi

```
[ ] Her random işlemde random_state=42 var mı? (np.random.seed, sklearn, torch)
[ ] Model kayıt yolları deterministik mi? (timestamp değil, config_id bazlı)
[ ] Training config JSON'da mı? (hardcode değil)
[ ] Veri okuma sırası sabit mi? (glob sonuçları sort() ile?)
[ ] Test/train split seed'li mi?
```

---

## Bölüm 7: Sprint QA Rutini (Her Sprint Sonunda)

### 5 Dakika Kontrol

```bash
# 1. Syntax
python3 -m py_compile main.py && echo "[OK] main.py"

# 2. Bash syntax
bash -n truba/slurm_jobs/*.sh && echo "[OK] Bash scripts"

# 3. PIPESTATUS kontrol
grep -n '\$?' truba/slurm_jobs/*.sh | grep -v PIPESTATUS && echo "[WARN] Bak"

# 4. Yeni except blokları — yutan var mı?
git diff HEAD~1 -- "*.py" | grep "^+" | grep "except" | grep -v "raise\|sys.exit"

# 5. Inter-PFAZ sütun adları — son değişen dosyalarda yeni to_excel/to_csv var mı?
git diff HEAD~1 -- "*.py" | grep "to_excel\|to_csv" | head -10
```

### 30 Dakika Denetim

```bash
# Inter-PFAZ tam audit
grep -rn "to_excel\|to_csv" pfaz_modules/ | grep -v "^Binary\|test\|#" > /tmp/writes.txt
grep -rn "read_excel\|read_csv" pfaz_modules/ | grep -v "^Binary\|test\|#" > /tmp/reads.txt
# Writes vs reads: her write'ın bir read karşılığı var mı? Sütun adları aynı mı?
```

---

## Bölüm 8: Yaygın Bug Kategorileri ve Önleme

| Kategori | Sık Görülen | Önleme |
|----------|-------------|--------|
| **Exit code** | `$?` pipe sonrası | `${PIPESTATUS[0]}` standart yap |
| **Silent fail** | HPC modda exception yutma | `failed_list` + `RuntimeError` pattern |
| **Dep check** | Kritik paket REQUIRED'da yok | `--check-deps` çalıştır, eksiği ekle |
| **Inter-PFAZ** | Sütun adı uyuşmazlığı | Mini integration test yaz |
| **Reproducibility** | random_state eksik | Kural: her stochastic op seed'li |
| **Dead code** | Import edilmeyen modül | Her PR'da dead code taraması |
| **Path hardcode** | `/arf/home/ahmacar/...` | Env var + default pattern |
| **Strict mode** | skipped=completed yanılgısı | HPC'de strict flag + RuntimeError |
| **ANFIS eksik** | AI-only istatistik | Her raporlama modülünde ANFIS verisi kontrol et |

---

## Bölüm 9: Hızlı Referans — Bu Projede Öğrenilenler

### KURAL 32 — VARSAYIM YASAĞI

"Muhtemelen X'tir" diyorsam → dur, grep/view ile kanıtla.

### KURAL 30 — Runtime Simulation

Kod yazarken 3 senaryo simüle et:
1. Happy path — her şey OK
2. Tek nokta fail — ortada bir şey bozulursa ne olur?
3. Pipe/zincir fail — Bash pipe, Slurm afterok zinciri gerçekten kırılıyor mu?

### KURAL 33 — Cross-Layer Chain

`Python return` → `sys.exit` → `Bash $?` → `Slurm ExitCode` → `afterok`
Bir katmanı düzeltince alttaki/üstteki katmanları da kontrol et.

---

*Bu kitap hpcv1 Sprint 1-13 deneyimlerinden damıtıldı. Her yeni projede başlangıç noktası olarak kullan.*
