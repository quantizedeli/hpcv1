# Sprint 7 — BUG-47..BUG-61 Fix Planı
**Hedef Tarih:** 2026-05-12 veya sonraki oturum  
**Dal:** truba-fixes (veya sprint7-bug-fixes)  
**Durum:** BEKLIYOR

---

## Hedef

Sprint 6'da bulunan 15 bug'u öncelik sırasıyla düzelt.  
Önce TRUBA-CRITICAL (TRUBA'da pipeline çalışmaz), sonra CRITICAL (memory leak / data loss),
sonra YUKSEK (yanlış sonuç / orphan read).

---

## Öncelik Sırası

### ADIM 1 — TRUBA-CRITICAL (önce bunlar)

#### BUG-47: real_data_integration_manager.py hardcoded paths
**Dosya:** `analysis_modules/real_data_integration_manager.py:28-29`
```python
# KALDIR:
sys.path.insert(0, '/home/claude')
sys.path.insert(0, '/mnt/user-data/outputs')

# YERİNE:
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```
**Kontrol:** `from pathlib import Path` import var mı? Yoksa başa ekle.

#### BUG-48: visualization_integration.py hardcoded path
**Dosya:** `visualization_modules/visualization_integration.py:31`
```python
# KALDIR:
sys.path.insert(0, '/mnt/user-data/outputs')

# YERİNE:
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

---

### ADIM 2 — KRITIK (memory leak / import fail)

#### BUG-49: advanced_models_extended.py — torch hard import
**Dosya:** `pfaz_modules/pfaz02_ai_training/advanced_models_extended.py:16-20`
```python
# ÖNCE (hard import):
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# SONRA:
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    from torch.utils.data import TensorDataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    nn = None
    F = None
    optim = None
    TensorDataset = None
    DataLoader = None
    TORCH_AVAILABLE = False
```
**Ek:** Dosyada TORCH_AVAILABLE kullanılan yerlere `if not TORCH_AVAILABLE: raise RuntimeError(...)` ekle.

#### BUG-53: hyperparameter_tuner + automl — finally/clear_session eksik
**Dosyalar:**
- `pfaz_modules/pfaz02_ai_training/hyperparameter_tuner.py:423,436`
- `pfaz_modules/pfaz13_automl/automl_optimizer.py:289`
- `pfaz_modules/pfaz13_automl/automl_hyperparameter_optimizer.py:276`

Her `model.fit(...)` çağrısının etrafına:
```python
try:
    model.fit(X_train, y_train, ...)
    # ... evaluate ...
finally:
    try:
        import tensorflow as tf
        tf.keras.backend.clear_session()
    except Exception:
        pass
    import gc
    gc.collect()
```

#### BUG-55: automl_retraining_loop.py:211 — silent fail (dataset load)
**Dosya:** `pfaz_modules/pfaz13_automl/automl_retraining_loop.py:211`
```python
# ÖNCE:
except Exception:
    pass

# SONRA:
except Exception as e:
    get_tracker().warn(f"[AutoML] Dataset yukleme hatasi: {e}")
    continue
```

---

### ADIM 3 — YUKSEK

#### BUG-50: tqdm hard import (PFAZ9)
**Dosyalar:**
- `pfaz09_aaa2_monte_carlo/aaa2_control_group_complete_v4.py:29`
- `pfaz09_aaa2_monte_carlo/monte_carlo_simulation_system.py:31`
```python
# ÖNCE:
from tqdm import tqdm

# SONRA:
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    tqdm = None
    TQDM_AVAILABLE = False
```
Kullanılan yerlerde: `if TQDM_AVAILABLE: for x in tqdm(items): ...` else `for x in items: ...`

#### BUG-51: visualization_master_system.py — orphan sheet read
**Dosya:** `pfaz_modules/pfaz08_visualization/visualization_master_system.py:1492`
```python
# ÖNCE:
sheet_name='Robustness_CV_Results'

# SONRA:
sheet_name='Robustness_CV'
```
**Doğrulama:** `pfaz06_final_reporting/comprehensive_excel_reporter.py`'deki yazım adının
`'Robustness_CV'` olduğunu grep ile teyit et.

#### BUG-52: comprehensive_excel_reporter.py — sheet truncation eksik
**Dosya:** `pfaz_modules/pfaz06_final_reporting/comprehensive_excel_reporter.py:210,223`
```python
# ÖNCE:
sheet_name = f'{target}_Sonuclar'
sheet_name = f'{config_id}_Detay'

# SONRA:
sheet_name = f'{target}_Sonuclar'[:31]
sheet_name = f'{config_id}_Detay'[:31]
```

#### BUG-56: automl_retraining_loop.py:305 — silent fail (config read)
```python
except Exception as e:
    get_tracker().warn(f"[AutoML] Config okuma hatasi: {e}")
    continue
```

#### BUG-57: automl_retraining_loop.py:758 — silent fail (report write)
```python
except Exception as e:
    get_tracker().warn(f"[AutoML] Rapor yazma hatasi: {e}")
```

#### BUG-54: stacking_ensemble.py:312 — finally/clear_session eksik
Aynı BUG-53 pattern'i uygula.

---

### ADIM 4 — ORTA / TASARIM (isteğe bağlı)

#### BUG-58/59/60: Dokümantasyon düzeltmeleri
- `CLAUDE.md:100` — "29-sheet" → "18-sheet" (PFAZ 6 ComprehensiveExcelReporter gerçek değeri)
- `CLAUDE.md:101` — "70+ chart types" iddiasını doğrula veya kaldır
- `PFAZ_DEVELOPMENT_NOTES.md` — "stacking R²=0.9794" PFAZ 7'ye taşı

#### BUG-61: QA_PROJECT_STATUS_REPORT.md — "bare except: 0" güncelle
Sprint 6 bölümü eklendi (zaten yapıldı).

---

## Doğrulama Adımları

Sprint 7 bitince:
```bash
# 1) Syntax check
python -c "import py_compile; [py_compile.compile(f) for f in [
    'analysis_modules/real_data_integration_manager.py',
    'visualization_modules/visualization_integration.py',
    'pfaz_modules/pfaz02_ai_training/advanced_models_extended.py',
    'pfaz_modules/pfaz02_ai_training/hyperparameter_tuner.py',
    'pfaz_modules/pfaz13_automl/automl_retraining_loop.py'
]]"

# 2) Hardcoded path kalmadı mı?
grep -rn "'/home/\|'/mnt/" --include="*.py" analysis_modules/ visualization_modules/

# 3) Smoke test
pytest tests/test_smoke/ -v
```

---

## Belgeler (Sprint 7 bitince güncellenmeli)

- [ ] `pipeline-hatalari.md` — BUG-47..61 durumları DUZELTILDI yapılacak
- [ ] `CLAUDE.md` — BUG-58/59 dokümantasyon düzeltmeleri
- [ ] `SPRINT-PLAN.md` — Sprint 7 TAMAMLANDI
- [ ] `QA_PROJECT_STATUS_REPORT.md` — Sprint 7 bölümü eklenmeli
- [ ] `tez-yazim-not-defteri.md` — Sprint 7 özeti

---

*Sprint 7 planı | 2026-05-12 | BUG-47..61 öncelikli fix*
