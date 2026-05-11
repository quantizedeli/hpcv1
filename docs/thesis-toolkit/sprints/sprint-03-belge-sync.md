# Sprint 3 — Belge Senkronizasyonu
## Durum: BEKLIYOR | Öncelik: ORTA

> **Bu sprint neden var:**
> Sprint 1 ve 2 kod değişiklikleri yaptı. Bu sprint sadece belgeleri günceller.
> Kod değişikliği yoktur — yalnızca .md dosyaları.
>
> **Sprint 1 ve Sprint 2 tamamlandıktan sonra çalıştır.**

---

## Hedef

Bu oturumda (2026-05-07/08) yapılan tüm değişiklikleri ilgili belgelere yansıt:
1. `pipeline-hatalari.md` — BUG durumlarını güncelle
2. `faz-degerlendirme-notlari.md` — yeni bulgular ekle
3. `phases/faz-02-yapay-zeka-egitimi.md` — Dual R² metodolojisi ekle
4. `phases/faz-01-veri-kumesi-uretimi.md` — Scaling/boyut kararları ekle
5. `phases/README.md` — Sprint sonrası genel durum güncelle

---

## Etkilenen Dosyalar

| Dosya | Ne Eklenir |
|-------|-----------|
| `pipeline-hatalari.md` | BUG-39..41 durumları, WARN-03..05 |
| `faz-degerlendirme-notlari.md` | 2026-05-08 oturumu bulguları |
| `phases/faz-01-veri-kumesi-uretimi.md` | Robust removal, N=75 removal, Nilsson NaN |
| `phases/faz-02-yapay-zeka-egitimi.md` | Dual R², CV fold adaptif, log analizi bulguları |
| `phases/faz-03-anfis-egitimi.md` | ANFISDatasetSelector sleeping orphan, ANFIS_MAX_INPUTS=5, configurations alanı okunmuyor |
| `phases/README.md` | Sprint özeti, BUG sayısı güncelle |

---

## Adım 1: `pipeline-hatalari.md` Güncelle

Kök dizindeki `pipeline-hatalari.md` dosyasını oku.
BUG-39, BUG-40, BUG-41 satırlarını bul ve "DUZELTILDI" olarak işaretle.
WARN-03, WARN-04, WARN-05 satırlarını ekle (yoksa).

Eklenecek özet tablo:
```
| BUG-39 | PFAZ 02 | overfitting_detector.py | analyze_training_metrics eksikti | DUZELTILDI 2026-05-07 |
| BUG-40 | PFAZ 13 | automl_anfis_optimizer.py | anfis_core import yanlıştı | DUZELTILDI 2026-05-08 |
| BUG-41 | Config  | config_desktop.json | "Physics" feature set geçersizdi | DUZELTILDI 2026-05-08 |
| WARN-03 | Config | config_desktop.json | Robust scaling QM için R2<0 | KALDIRILDI 2026-05-08 |
| WARN-04 | PFAZ 02 | model_validator.py | N<150 fold başına ~17 örnek | TEZ NOTU |
| WARN-05 | PFAZ 02 | parallel_ai_trainer.py | 15 örnekli val set yanıltıcı olabilir | TEZ NOTU |
```

## Adım 2: `faz-degerlendirme-notlari.md` Güncelle

Bu dosya BOLUM A-M yapısında. En sona yeni bölüm ekle:

```markdown
## BOLUM N — Log Analizi ve Sprint 2026-05-07/08 Bulgulari

**Tarih:** 2026-05-08
**Kaynak:** `old logs/main_20260430_184414.log.*` (eski PC, ~7 gün çalışma)

### Kritik Bulgular

1. **446,400 toplam iş = model eğitim turu** (dataset değil)
   - 848 dataset × ~527 model config = 446,400 eğitim
   - PFAZ 2 tek başına ~12.7 gün (eski PC'de)

2. **En iyi konfigürasyon:**
   - QM_100_S70_B2EMCBEA_NoScaling_Stratified + XGBoost → val R²=0.84
   - Genel kural: XGBoost > RF >= DNN

3. **Sistematik başarısızlıklar:**
   - Robust scaling + QM hedefi → tüm R²<0 → KALDIRILDI
   - N=75 → DNN_MIN_SAMPLES=80 ihlali + yetersiz CV → KALDIRILDI
   - Nilsson NaN = %34 → KAPALI

4. **Yeni Düzeltilen Buglar:**
   - BUG-39: analyze_training_metrics eksikti
   - BUG-40: anfis_core.py yok → import hatası
   - BUG-41: "Physics" feature set tanımsız

### Desktop Config Son Hali (v2.0.1)
- feature_sets: null (14 MM + 15 QM = 29 hedef-bazlı set)
- scenarios: [S70]
- scalings: [NoScaling, Standard]
- sizes: [100, 150, 267]
- sampling: [Random, Stratified]
- ANFIS: 4 config, filter=[100, 150]
- Tahmini dataset sayısı: ~450 (NoAnomaly dahil)
```

## Adım 3: `phases/faz-02-yapay-zeka-egitimi.md` Güncelle

"Değerlendirme Kriterleri" veya "Model Kayıt Akışı" bölümünü bul.
Şu içeriği ekle:

```markdown
### Çift R² Filtresi (Sprint 1 — 2026-05-08)

**Gerekçe:** Log analizi (2026-04-30) train_R2=0.9967 ama cv_R2=-0.31 olan modellerin
kaydedildiğini gösterdi. Tek val_R2 filtresi 15 örneklik doğrulama seti üzerinden
hesaplandığından yanıltıcı olabilir.

**Yeni Kriter:**
- val_R2 ≥ 0.5 (mevcut)
- cv_R2 ≥ 0.0 (yeni: en az ortalamadan iyi)
- gap = train_R2 - cv_R2 < 0.5 (yeni: aşırı uyum kontrolü)

**Literatür Desteği:**
- Shang et al. (2022): train-test gap >0.2-0.3 aşırı uyum sinyali
- Utama et al. (2016): nükleer özellik ML'de CV zorunlu
- Genel ML: cv_R2 < 0 → model anlamsız (ortalamadan kötü)

**Tez Notu:** Çift filtrenin istatistiksel gerekçesi Metodoloji bölümü §3.5'e girmeli.
```

## Adım 4: `phases/faz-01-veri-kumesi-uretimi.md` Güncelle

"Scaling Stratejisi" bölümüne ekle:
```
**Robust Scaling — Kaldırma Kararı (2026-05-08):**
Eski PC log analizi: QM hedefiyle Robust scaling %100 R²<0 sonuç veriyor.
IQR normalleştirmesi simetrik olmayan QM dağılımıyla uyumsuz.
WARN-03 olarak belgelendi. Tüm config dosyalarından kaldırıldı.
```

"Dataset Boyutları" bölümüne ekle:
```
**N=75 — Kaldırma Kararı (2026-05-08):**
DNN_MIN_SAMPLES=80 nedeniyle N=75 setlerde DNN çalışmıyor.
5-fold CV'de fold başına ~12 örnek → istatistiksel açıdan güvenilmez.
Minimum boyut N=100 olarak belirlendi.
```

"Nilsson Modeli" bölümüne ekle (yoksa oluştur):
```
**Nilsson NaN — Kapalı Tutma Kararı (2026-05-08):**
267 çekirdekten 68'inde (%34) Nilsson özellikleri NaN döndürüyor.
Yalnızca deformasyonlu çekirdekler için hesaplanabiliyor (Beta_2≠0).
Küçük dataset boyutlarında orantısız veri kaybı — kapalı bırakıldı.
```

## Adım 4b: `phases/faz-03-anfis-egitimi.md` Güncelle (2026-05-08 keşifleri)

"Veri Seti Seçimi" veya "Mimari" bölümünü bul. Şu içeriği ekle:

```markdown
### Sleeping Orphan: ANFISDatasetSelector (2026-05-08)

`anfis_dataset_selector.py` içindeki `ANFISDatasetSelector` sınıfı
PFAZ2 R² sonuçlarına göre dataset seçimi yapacak şekilde tasarlanmış
(Top ≥0.90 / Mid 0.80-0.90 / Low <0.80 katmanları), **ancak
`anfis_parallel_trainer_v2.py:1427` itibarıyla devre dışı bırakılmış.**

Mevcut davranış: PFAZ1 çıktısındaki TÜM ANFIS-feasible datasetler kullanılır.
Tek filtre: `ANFIS_MAX_INPUTS = 5` (giriş özellik sayısı limiti, satır 1042).
`TARGET_RECOMMENDED_SETS` içindeki tüm setler ≤5 giriş içerdiğinden hepsi geçer.

### Config `configurations` Alanı Okunmuyor (2026-05-08)

`config.json` ve `config_desktop.json` içindeki
`pfaz03_anfis_training.configurations` listesi kod tarafından **hiç okunmuyor.**
Gerçek davranış hardcoded `PILOT_IDS` kümesine dayanır:
```
PILOT_IDS = {CFG_Grid_2MF_Trap, CFG_Grid_2MF_Bell, CFG_Grid_2MF_Gauss, CFG_Grid_2MF_Tri}
```
3-phase pilot strategy (Wave 1 PILOT → Wave 2 ADVANCED) aktif olduğundan
config listesi yalnızca dokümantasyon amacıyla var. Kod değişikliği gerekmiyor.

### ANFIS Eğitim Config Adlandırması Tutarsızlığı

`anfis_config_manager.py`: `Grid_2MF_Gauss`, `Grid_2MF_Tri`, ...
`anfis_parallel_trainer_v2.py` PILOT_IDS: `CFG_Grid_2MF_Gauss`, `CFG_Grid_2MF_Tri`, ...

`CFG_` öneki fark eder. `anfis_config_manager.py::get_config_by_name()` bu prefix'e
göre lookup yapar. Bu tasarım kararı — tutarsızlık değil, katmanlı yapı.
```

## Adım 5: `phases/README.md` Güncelle

Sprint özeti tablosu ekle:
```
| Sprint 1 | 2026-05-08 | Çift R² filtresi | parallel_ai_trainer.py refactor |
| Sprint 2 | 2026-05-08 | Config senkronizasyonu | Robust/N75 kaldırma |
| Sprint 3 | 2026-05-08 | Belge senkronizasyonu | Bu sprint |
```

BUG sayısını güncelle: Toplam 41 (15 düzeltildi, 4 geçersiz, 22 bekliyor/tez notu)

---

## Doğrulama Adımları

### Kontrol 1: pipeline-hatalari.md BUG-40 var mı?
```bash
grep "BUG-40" "c:/Users/Hakan Yakut/Desktop/ahmet/skillv1/thesis-nuclear-ai/pipeline-hatalari.md"
```
**Beklenen:** BUG-40 satırı görünmeli.

### Kontrol 2: faz-02 belgesinde "Çift R² Filtresi" var mı?
```bash
grep -c "Çift R" "c:/Users/Hakan Yakut/Desktop/ahmet/skillv1/thesis-nuclear-ai/phases/faz-02-yapay-zeka-egitimi.md"
```
**Beklenen:** 1 veya daha fazla.

### Kontrol 3: faz-01 belgesinde Robust kaldırma var mı?
```bash
grep -c "Robust.*Kaldırma\|Kaldırma.*Robust" "c:/Users/Hakan Yakut/Desktop/ahmet/skillv1/thesis-nuclear-ai/phases/faz-01-veri-kumesi-uretimi.md"
```
**Beklenen:** 1 veya daha fazla.

---

## Sprint Tamamlanma Kriterleri

```
[ ] pipeline-hatalari.md — BUG-39, 40, 41 ve WARN-03..05 var
[ ] faz-degerlendirme-notlari.md — BOLUM N eklendi
[ ] phases/faz-02-yapay-zeka-egitimi.md — Çift R² bölümü eklendi
[ ] phases/faz-01-veri-kumesi-uretimi.md — Robust + N75 + Nilsson notları eklendi
[ ] phases/README.md — Sprint özeti ve BUG sayısı güncellendi
[ ] Kontrol 1: GEÇTI
[ ] Kontrol 2: GEÇTI
[ ] Kontrol 3: GEÇTI
[ ] Yeni bug veya hata yok
```

---

## Sprint Sonrası (Tüm Sprintler Tamamlandı)

Tüm 3 sprint tamamlandığında:

1. `sprints/SPRINT-PLAN.md` güncelle — tüm sprint'leri TAMAMLANDI olarak işaretle
2. `memory/phases_progress.md` güncelle — son durum
3. `tez-yazim-not-defteri.md` Karar Günlüğü — sprint özeti ekle

---

## Skill Kullanımı — Bu Sprint İçin

```
Sadece belge güncellemeleri:
→ Read + Edit araçları yeterli
→ Agent veya Skill gerekmez

Uzun .md dosyalarında bölüm bulma:
→ Grep ile bölüm başlığı ara, sonra Read ile offset/limit kullan

"Bölüm bulunamadı" durumunda:
→ Oluştur (Write yerine dosya sonuna Edit ile ekle)
```

---

## Notlar

- Belge güncellemeleri sırasında mevcut içeriği silme — ekle
- "BOLUM N" faz-degerlendirme-notlari.md'de en son bölüm olacak
- phases/ dosyaları 20-40KB olabilir — önce Grep ile bölüm bul, sonra Read ile o bölümü oku
- `pipeline-hatalari.md` (kök dizin) ≠ `memory/pipeline_bugs.md` (bellek dosyası) — ikisi ayrı
