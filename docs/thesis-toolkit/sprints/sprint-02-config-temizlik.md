# Sprint 2 — Config Senkronizasyonu + Robust/N75 Kaldırma
## Durum: BEKLIYOR | Öncelik: YUKSEK

> **Bu sprint neden var:**
> `nucdatav2-desktop/config_desktop.json` güncellendi (2026-05-08) ama
> `repo/config.json` (TRUBA ana config) hâlâ Robust scaling ve N=75 içeriyor.
> Tüm config dosyaları aynı ilkeleri uygulamalı.
>
> **Sprint 1 tamamlandıktan sonra çalıştır** (config.json'a Sprint 1'in threshold'ları da girecek).

---

## Hedef

Tüm config dosyalarında tutarsızlıkları gider:
1. Robust scaling → tüm config'lerden kaldır
2. Dataset boyut N=75 → tüm config'lerden kaldır
3. ANFIS `dataset_sizes_filter` → kod desteği ekle (config'de var, kod'da yok)
4. `nucdatav2-truba/` config varsa → güncelle

---

## Etkilenen Dosyalar

| Dosya | Değişiklik |
|-------|------------|
| `repo/config.json` | Robust kaldır, N=75 kaldır, notlar ekle |
| `nucdatav2-truba/config_truba.json` | Varsa aynı kaldırmaları yap |
| `repo/pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py` | `dataset_sizes_filter` okuma kodu ekle |

---

## Adım 1: `repo/config.json` Güncelleme

### 1a. Robust Scaling Kaldırma

`pfaz01_dataset_generation.scalings` listesini bul:
```json
"scalings": ["NoScaling", "Standard", "Robust", "MinMax"]
```
Robust'u kaldır:
```json
"scalings": ["NoScaling", "Standard", "MinMax"],
"_scaling_notes": {
  "NoScaling": "Agac tabanli modeller icin ideal",
  "Standard": "DNN ve genel icin en iyi",
  "MinMax": "TRUBA kapsamli tarama icin",
  "Robust": "KALDIRILDI — QM target icin sistematik basarisizlik (R2 < 0, WARN-03)"
}
```

### 1b. Dataset N=75 Kaldırma

`pfaz01_dataset_generation.dataset_sizes` listesini bul:
```json
"dataset_sizes": [75, 100, 150, 200, 267]
```
75'i kaldır:
```json
"dataset_sizes": [100, 150, 200, 267],
"_size_notes": {
  "75": "KALDIRILDI — DNN_MIN_SAMPLES=80 ihlali + 5-fold CV fold basi ~12 ornek",
  "100": "KULLAN — hizli egitim, iyi performans",
  ...
}
```

### 1c. Sprint 1 Threshold'larını Kontrol Et
Sprint 1 `cv_r2_min_threshold` ve `max_train_cv_gap` eklediyse, `config.json`'da da olduğundan emin ol.

## Adım 2: TRUBA Config Kontrolü

```bash
ls "c:/Users/Hakan Yakut/Desktop/ahmet/nucdatav2-truba/" 2>/dev/null | head -5
```

Varsa ve config dosyası içeriyorsa: `config_truba.json`'a aynı kaldırmaları uygula.

## Adım 3: ANFIS Dataset Seçim Mekanizması — Durum Tespiti

**Önemli keşif (2026-05-08):** `ANFISDatasetSelector` (PFAZ2 R²-bazlı seçim)
`anfis_parallel_trainer_v2.py:1427`'de devre dışı bırakılmış.
Şu an ANFIS, PFAZ1 çıktı dizinindeki TÜM ANFIS-feasible datasetleri kullanıyor.
Tek filtre: `ANFIS_MAX_INPUTS` (giriş sayısı limiti).

### 3a. Mevcut Durumu Doğrula
```bash
grep -n "ANFISDatasetSelector\|deactivated" repo/pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py | head -5
```
**Beklenen:** `ANFISDatasetSelector: deactivated` mesajı görünmeli.

### 3b. Bu Sprint'te Yapılacak (Hafif)

ANFIS dataset sayısını kontrol etmenin mevcut yolu: `configurations` listesini kısaltmak.
Desktop config'de `n_datasets_per_target: 20` var — bu bir placeholder.
ANFISDatasetSelector ileride aktif edildiğinde devreye girecek.

**Bu sprint'te bu adımda değişiklik YOK.** Belgeleme yeterli.

### 3d. ANFISDatasetSelector Aktivasyonu — TAMAMLANDI (2026-05-08)

`anfis_parallel_trainer_v2.py`'ye `discover_datasets()` sonrasına ANFISDatasetSelector
entegre edildi. Parametreler: **Top=50, Mid=50, Low=100** (toplam 200/target).

Aktivasyon mantığı:
- `training_summary.xlsx` (PFAZ2 çıktısı) varsa → seçim yapar
- Yoksa → tüm datasetler kullanılır (fallback — PFAZ2 henüz tamamlanmamış?)

Değiştirilen satır aralığı: ~1167-1210 (discover_datasets sonrası)

### 3c. KRITIK Keşif: `configurations` Alanı Kod Tarafından Okunmuyor (2026-05-08)

`config_desktop.json` ve `config.json` içindeki `pfaz03_anfis_training.configurations` listesi
**anfis_parallel_trainer_v2.py tarafından hiç okunmuyor.**

Gerçek davranış:
```python
# anfis_parallel_trainer_v2.py:1171-1172 — hardcoded
PILOT_IDS = {'CFG_Grid_2MF_Trap', 'CFG_Grid_2MF_Bell',
             'CFG_Grid_2MF_Gauss', 'CFG_Grid_2MF_Tri'}

# train_all_anfis_parallel(self, n_configs: int = 10)
# → n_configs parametresi config'den DEĞİL, main.py'den geliyor
```

Bu nedenle config'deki `["Grid_2MF_Gauss", "Grid_2MF_Tri", "SubClust_R05", "SubClust_R07"]`
listesi tamamen görmezden gelinir.

**Bu sprint'te yapılacak:** `config.json` ve `config_desktop.json`'a `_configurations_note` ekle:
```json
"_configurations_note": "DIKKAT: Bu liste kod tarafından okunmuyor. PILOT_IDS hafif kodlanmis (anfis_parallel_trainer_v2.py:1172). Aktif konfigurasyonlar: CFG_Grid_2MF_Trap/Bell/Gauss/Tri. n_configs parametresi config'den degil main.py'den gelir."
```

**Kod değişikliği YOK** — bu tasarım kararı (3-phase pilot strategy). Belgeleme yeterli.

---

## Doğrulama Adımları

### Test 1: Config JSON Geçerliliği
```bash
cd repo/
python -c "
import json
cfg = json.load(open('config.json'))
sizes = cfg['pfaz01_dataset_generation']['dataset_sizes']
scalings = cfg['pfaz01_dataset_generation']['scalings']
assert 75 not in sizes, 'N=75 hala var!'
assert 'Robust' not in scalings, 'Robust hala var!'
print('[OK] Config temiz — N=75 ve Robust kaldırıldı')
print(f'  Sizes: {sizes}')
print(f'  Scalings: {scalings}')
"
```
**Beklenen çıktı:** `[OK] Config temiz`

### Test 2: ANFIS Deactivated Durumu Doğrulama
```bash
grep -c "deactivated" repo/pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py
```
**Beklenen çıktı:** 1 (ANFISDatasetSelector devre dışı notu var)

### Test 3: Desktop Config Tutarlılığı
```bash
cd repo/
python -c "
import json
desk = json.load(open('../nucdatav2-desktop/config_desktop.json'))
main = json.load(open('config.json'))
print('Desktop scenarios:', desk['pfaz01_dataset_generation']['scenarios'])
print('Desktop feature_sets:', desk['pfaz01_dataset_generation']['feature_sets'])
print('Desktop ANFIS configs:', desk['pfaz03_anfis_training']['configurations'])
print('Desktop ANFIS filter:', desk['pfaz03_anfis_training']['dataset_sizes_filter'])
print('[OK] Desktop config okunabilir')
"
```
**Beklenen çıktı:** `[OK] Desktop config okunabilir`, scenarios=['S70'], feature_sets=None

### Test 4: Import Kontrolü
```bash
cd repo/
python -c "
from pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 import DatasetGenerationPipelineV2
from pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 import ANFISParallelTrainerV2
print('[OK] Tum importlar basarili')
"
```

---

## Sprint Tamamlanma Kriterleri

```
[ ] repo/config.json — Robust kaldırıldı
[ ] repo/config.json — N=75 kaldırıldı
[ ] TRUBA config — Varsa aynı kaldırmalar yapıldı
[ ] ANFISDatasetSelector durumu belgelendi (deaktif, n_datasets_per_target placeholder)
[ ] Test 1: Config temiz GEÇTI
[ ] Test 2: ANFIS deactivated doğrulandı GEÇTI
[ ] Test 3: Desktop config okunabilir GEÇTI
[ ] Test 4: Import GEÇTI
[ ] Yeni bug veya hata yok
```

---

## Sprint Sonrası Zorunlu Belge Güncellemeleri

1. **`phases/faz-01-veri-kumesi-uretimi.md`**
   - "Scaling Stratejisi" bölümüne Robust kaldırma gerekçesi ekle (WARN-03)
   - "Dataset Boyutları" bölümüne N=75 kaldırma gerekçesi ekle

2. **`tez-yazim-not-defteri.md`**
   - Karar Günlüğü: `| 2026-05-08 | Robust scaling ve N=75 tum config'lerden kaldirildi |`

3. **`pipeline-hatalari.md`** (kök dizin)
   - WARN-03: "TRUBA config'de de düzeltildi" notunu ekle

4. **`memory/phases_progress.md`**
   - Tarih ve sprint durumunu güncelle

---

## Skill Kullanımı — Bu Sprint İçin

```
Config değişikliklerinde:
→ Sadece Read + Edit araçları — Agent/Skill gerekmez

Kod değişikliği (ANFIS filter) için:
→ verification-before-completion (superpowers) — test çalıştırmadan "tamam" deme

JSON geçerlilik sorununda:
→ python -c "import json; json.load(open('config.json'))" hata vermeli
```

---

## Notlar

- `repo/config.json` çok büyük olabilir. Sections olarak oku (limit parametresi kullan).
- TRUBA dizini: `c:/Users/Hakan Yakut/Desktop/ahmet/nucdatav2-truba/`
- `nucdatav2-truba/` yoksa veya config yoksa bu adımı atla.
- ANFIS filter kodu eklenirken mevcut kodu bozmamak kritik — minimal değişiklik.
