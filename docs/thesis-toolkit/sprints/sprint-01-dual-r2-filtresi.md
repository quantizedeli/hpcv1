# Sprint 1 — Çift R² Filtresi + CV Fold Adaptif
## Durum: BEKLIYOR | Öncelik: KRITİK

> **Bu sprint neden var:**
> Log analizi (2026-05-07): train_R2=0.9967 ama cv_R2=-0.31 olan XGBoost modelleri
> kaydedildi. Mevcut `val_R2 >= 0.5` filtresi yetersiz — aşırı uyumu yakalamıyor.
>
> **Bağlam dosyaları:**
> - `reports/old-log-analysis-2026-05-07.md` — bulgular
> - `tez-yazim-not-defteri.md` Bölüm "Çift R2 Filtresi" — metodoloji kararı
> - `sprints/SPRINT-PLAN.md` — genel plan

---

## Hedef

`parallel_ai_trainer.py`'de model kayıt akışını yeniden yapılandır:
1. Model eğitildikten sonra val_R2 kontrol et (mevcut)
2. CV çalıştır (mevcut ama model kayıttan SONRA)
3. CV R2 ve gap kontrol et (yeni — model kayıttan ÖNCE olmalı)

### Yeni Filtre Kriterleri
```
val_R2  >= 0.5  (mevcut — koru)
cv_R2   >= 0.0  (yeni — en az ortalamadan iyi)
gap     <  0.5  (yeni — train_R2 - cv_R2 farkı)
```

---

## Etkilenen Dosyalar

| Dosya | Satır | Değişiklik |
|-------|-------|------------|
| `repo/pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py` | ~1327-1420 | Model kayıt akışı yeniden yapılandırma |
| `repo/config.json` | `pfaz02_ai_training` bölümü | `cv_r2_min_threshold` ve `max_train_cv_gap` ekle |
| `nucdatav2-desktop/config_desktop.json` | `pfaz02_ai_training` bölümü | Aynı threshold'ları ekle |

---

## Adım Adım Uygulama

### Adım 1: `config.json` — Yeni Threshold'lar Ekle

`repo/config.json` dosyasında `pfaz02_ai_training` bölümünü bul.
`r2_min_threshold` satırının yanına ekle:

```json
"r2_min_threshold": 0.5,
"cv_r2_min_threshold": 0.0,
"max_train_cv_gap": 0.6,
"_dual_r2_note": "Literatur destegi: Shang et al. 2022, Utama et al. 2016. cv_R2 >= 0 = en az ortalamadan iyi. gap < 0.6 = aşırı uyum sınırı."
```

### Adım 2: `config_desktop.json` — Aynı Threshold'ları Ekle

`nucdatav2-desktop/config_desktop.json` → `pfaz02_ai_training` bölümüne ekle:
```json
"cv_r2_min_threshold": 0.0,
"max_train_cv_gap": 0.6
```

### Adım 3: `parallel_ai_trainer.py` — Model Kayıt Akışını Yeniden Yapılandır

**Mevcut akış (yanlış sıra):**
```
1. Modeli eğit
2. val_R2 kontrol et → geçerliyse KAYDET
3. CV çalıştır (kayıt sonrası — geç kalıyor)
4. Aşırı uyum tespiti
```

**Hedef akış (doğru sıra):**
```
1. Modeli eğit
2. val_R2 >= 0.5? → hayırsa at
3. CV çalıştır (3-fold N<150, 5-fold N≥150)
4. cv_R2 >= cv_r2_min_threshold? → hayırsa at (kaydetme)
5. gap < max_train_cv_gap? → hayırsa at
6. Tüm kriterler geçtiyse → KAYDET
```

**Kod değişikliği yeri:** `parallel_ai_trainer.py` satır ~1327-1420 arası.

`_save_model_if_good` veya benzeri metodu bul. CV'yi kayıt öncesine taşı.

Config'ten yeni threshold'ları oku:
```python
cv_r2_min = self.config.get('pfaz02_ai_training', {}).get('cv_r2_min_threshold', 0.0)
max_gap = self.config.get('pfaz02_ai_training', {}).get('max_train_cv_gap', 0.5)
```

Log mesajları ekle (sessiz ret olmadığından emin ol):
```python
logger.info(f"[DUAL_FILTER] val_R2={val_r2:.3f} cv_R2={cv_r2:.3f} gap={gap:.3f} -> {'KABUL' if passed else 'RET'}")
```

### Adım 4: CV Fold Adaptif (Bonus — eğer zaman varsa)

`config.json` ve `config_desktop.json`'da:
```json
"cv_folds": 3,
"cv_folds_large_n": 5,
"cv_large_n_threshold": 150
```

`parallel_ai_trainer.py`'de:
```python
n_folds = cv_folds_large if train_size >= cv_large_n_threshold else cv_folds
```

---

## Doğrulama Adımları

Sprint tamamlandıktan sonra bu testleri çalıştır:

### Test 1: Config JSON Geçerliliği
```bash
cd repo/
python -c "import json; cfg = json.load(open('../nucdatav2-desktop/config_desktop.json')); print('cv_r2:', cfg['pfaz02_ai_training']['cv_r2_min_threshold'])"
```
**Beklenen çıktı:** `cv_r2: 0.0`

### Test 2: Kod Import Kontrolü
```bash
cd repo/
python -c "from pfaz_modules.pfaz02_ai_training.parallel_ai_trainer import ParallelAITrainer; print('[OK] Import basarili')"
```
**Beklenen çıktı:** `[OK] Import basarili`

### Test 3: Smoke Test
```bash
cd repo/
pytest tests/test_smoke/ -v -k "trainer or config" 2>&1 | tail -20
```
**Beklenen çıktı:** Tüm testler geçmeli, FAILED satırı olmamalı.

### Test 4: Dual Filtre Log Kontrolü
Küçük bir test çalıştırma sonrası log'da şunu ara:
```bash
grep "DUAL_FILTER" logs/main_*.log | tail -10
```
**Beklenen çıktı:** KABUL/RET mesajları görünmeli.

---

## Sprint Tamamlanma Kriterleri

Sprint **tamamlandı** sayılır ancak ve ancak:

```
[ ] config.json — cv_r2_min_threshold ve max_train_cv_gap eklendi
[ ] config_desktop.json — aynı threshold'lar eklendi
[ ] parallel_ai_trainer.py — CV kayıt öncesine taşındı
[ ] Test 1: JSON geçerliliği GEÇTI
[ ] Test 2: Import GEÇTI
[ ] Test 3: Smoke test GEÇTI (0 FAILED)
[ ] Test 4: Log'da DUAL_FILTER mesajları görünüyor
[ ] Yeni bug veya hata yok
```

---

## Sprint Sonrası Zorunlu Belge Güncellemeleri

Sprint tamamlanınca şu belgeleri güncelle (atlamak yasak):

1. **`phases/faz-02-yapay-zeka-egitimi.md`**
   - "Değerlendirme Kriterleri" bölümüne Çift R² filtresi metodolojisini ekle
   - Literatür: Shang et al. 2022, Utama et al. 2016

2. **`tez-yazim-not-defteri.md`**
   - "Karar Günlüğü" tablosuna ekle: `| 2026-05-08 | Çift R² filtresi uygulandı | log analizi: aşırı uyum tespiti için val_R2 tek başına yetersiz |`

3. **`pipeline-hatalari.md`** (kök dizinde)
   - İlgili satırı güncelle: bu iyileştirme uygulandı olarak işaretle

4. **`memory/pipeline_bugs.md`**
   - WARN-05 satırını güncelle: "TEZ NOTU → UYGULAMAYA ALINDI (Sprint 1)"

---

## Skill Kullanımı — Bu Sprint İçin

```
Kod değişikliği başlamadan önce:
→ systematic-debugging (superpowers) — mevcut akışı anlamak için

Kod yazarken:
→ python-reviewer agent (ECC) — değişiklik tamamlanınca review için
  Agent({ subagent_type: "everything-claude-code:python-reviewer", ... })

Tamamlama iddiasından önce:
→ verification-before-completion (superpowers) — kanıt olmadan "tamam" demek yasak

Büyük refactor ise:
→ tdd-workflow (superpowers) — önce test yaz (RED), sonra fix (GREEN)
```

---

## Notlar

- `parallel_ai_trainer.py` uzun bir dosya (~2000+ satır). Doğru metodu bulmak için grep:
  ```bash
  grep -n "r2_min\|val_r2\|save_model\|_save_if" repo/pfaz_modules/pfaz02_ai_training/parallel_ai_trainer.py | head -30
  ```
- Değişiklik minimal olmalı — geniş refactor yapma, sadece akış sırası ve yeni kontrol ekle
- `train_R2` değeri CV'den ÖNCE mevcut (model eğitim metriklerinden geliyor)
- CV zaten çalışıyor, sadece sıralama ve karar noktası değişiyor

---

## Sprint 8 Duzeltme Notu -- BUG-62 (2026-05-12)

**Durum:** Sprint 1 belgede TAMAMLANDI yaziyordu ama CV gate hic calismiyordu.

**Sorun:** `ParallelAITrainer.__init__` imzasinda `cv_r2_min_threshold`,
`max_train_cv_gap`, `cv_folds`, `cv_folds_large_n`, `cv_large_n_threshold`
parametreleri YOKTU. main.py 5 parametreyi geciriyordu ama constructor kabul
etmiyordu -- hepsi sessizce yok sayildi. (Bkz. KURAL 22)

**Fix (commit 2f1e594):**
- Constructor imzasina 5 parametre eklendi
- DUAL_FILTER blogu model kaydinin ONCESINE tasinmasi (Sprint 1'in asil amaci)
- Adaptif fold aktif: N<150 -> 3-fold, N>=150 -> 5-fold
- [DUAL_FILTER] KABUL/RET log mesajlari eklendi
- max_train_cv_gap: 0.6 (Sprint 8 karari, bkz. sprint-08-missing-fixes.md)

*Sprint 1 v2.0 | 2026-05-12 | BUG-62 ile gercek implementasyon tamamlandi*
