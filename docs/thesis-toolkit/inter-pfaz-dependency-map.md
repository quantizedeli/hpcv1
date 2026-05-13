# Inter-PFAZ Bağımlılık Haritası

**Tarih:** 2026-05-13 (Sprint 10 sonu denetimi)
**Kapsam:** main.py + her PFAZ modülünün gerçek okuma/yazma davranışı

Bu belge `Kemal'in "faz 3 PFAZ 2 sonuçlarını mı kullanıyor?"` sorusundan doğdu. Cevap kısa: **kullanıyor ama main.py'den explicit aktarılmıyor, modül içinde sibling-path inference ile arıyor.** Bu pattern 3 yerde tekrarlanıyor ve mimari risk.

## Bağımlılık Matrisi

| Faz | Bağımlı Olduğu Fazlar | Path Aktarım Yöntemi | Risk |
|-----|----------------------|----------------------|------|
| 1 | — | yok | — |
| 2 | 1 | `datasets_dir=pfaz_outputs[1]` explicit | düşük |
| 3 | 1, **2** | datasets_dir explicit, **PFAZ2 sibling-inference** | **ORTA** |
| 4 | 1, 2, 3 | tüm 3 path explicit | düşük |
| 5 | 2, 3 | tüm 2 path explicit | düşük |
| 6 | 2, 3, 9, 13 | tüm 4 path explicit | düşük |
| 7 | 1, 2, 3 | tüm 3 path explicit | düşük |
| 8 | **6** | **PFAZ6 sibling-inference** (`_find_reports_dir`) | **ORTA** |
| 9 | 1, 2, **3** | PFAZ1+PFAZ2 explicit, **PFAZ3 sibling-inference** | **YÜKSEK** (BUG-73) |
| 10 | tüm fazlar (tez compilation) | `pfaz_outputs={k: str(v)...}` TÜM PATH explicit | **DOĞRU PATTERN** ✓ |
| 11 | — | permanent skip | — |
| 12 | 2 | `ai_models_dir=pfaz_outputs[2]` explicit | düşük |
| 13 | 1, 2, 3, 4, 9, 12 | mixed (Sprint 10 BUG-65 ile düzeltildi) | düşük |

## PIPELINE_EXECUTION_ORDER Doğrulaması

```
order = [1, 2, 3, 4, 5, 7, 9, 12, 13, 6, 8, 10, 11]
```

Her fazın çalıştırma sırasındaki tüm bağımlılıkları öncesinde tamamlanmış mı? **Evet, 13/13 OK** — sıralama mantıklı, hiçbir faz öncesinden tamamlanmamış bir bağımlılık üzerinde çalışmıyor.

| Sıra | Faz | Önceden tamamlanması gereken | Durum |
|------|-----|------------------------------|-------|
| 0 | 1 | — | OK |
| 1 | 2 | [1] | OK |
| 2 | 3 | [1, 2] | OK |
| 3 | 4 | [1, 2, 3] | OK |
| 4 | 5 | [2, 3] | OK |
| 5 | 7 | [1, 2, 3] | OK |
| 6 | 9 | [1, 2, 3] | OK |
| 7 | 12 | [2] | OK |
| 8 | 13 | [1, 2, 3, 4, 9, 12] | OK |
| 9 | 6 | [2, 3, 9, 13] | OK |
| 10 | 8 | [6] | OK (sup. çalışınca) |
| 11 | 10 | tüm fazlar | OK |
| 12 | 11 | skip | — |

## Path Inference Pattern'i (Mimari Risk)

42 yerde `self.output_dir.parent / 'name'` veya `self.output_dir.parent.parent / 'outputs' / 'name'` kalıbı kullanılıyor. Bu **kırılgan**:

- `output_dir` yapısı değişirse kırılır
- Hardcoded klasör adı (`'trained_models'`, `'anfis_models'`, `'generated_datasets'`) `pfaz_outputs` map ile senkron olmazsa kırılır
- Test ortamında farklı path yapısı kullanılırsa kırılır

### Risk Sıralı Liste

**YÜKSEK — BUG-73 [Sprint 11 adayı]:**
- `pfaz_modules/pfaz09_aaa2_monte_carlo/aaa2_control_group_complete_v4.py:617`
  ```python
  anfis_models_dir = self.trained_models_dir.parent / 'anfis_models'
  ```
  main.py `anfis_models_dir` argümanını PFAZ9 constructor'a hiç geçirmiyor. Modül kendi başına buluyor. Eğer çıktı klasör yapısı değişirse (örn. ANFIS results ayrı bir mount'a yazılırsa) PFAZ9 top-50 model seçiminin ANFIS yarısı **sessizce eksik** kalır.

**ORTA:**
- `pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py:1191`
  ```python
  _ai_results_dir = self.output_dir.parent / 'trained_models'
  if not _ai_results_dir.exists():
      _ai_results_dir = self.output_dir.parent.parent / 'trained_models'
  ```
  ANFIS Dataset Selector PFAZ2'yi 2 fallback ile arıyor. TRUBA'da yol 1 doğru çözülüyor → çalışır. Ama main.py'den explicit aktarılmalı.

- `pfaz_modules/pfaz08_visualization/visualization_master_system.py:1368`
  ```python
  candidates = [
      self.output_dir.parent / 'reports',
      self.output_dir.parent.parent / 'outputs' / 'reports',
  ]
  ```
  PFAZ8 PFAZ6 `final_summary.json` arıyor. TRUBA'da yol 1 doğru.

## Sprint 10'da Düzeltilenler (BUG-65/66/67)

- BUG-65: PFAZ13 dataset path → sibling-inference doğru hale getirildi (`pfaz_outputs[1] / name`)
- BUG-66: PFAZ13 metadata-aware CSV okuma — header/kolon adı standartlığı sağlandı

## Sprint 11 Adayları (BUG-73 + Mimari)

1. **BUG-73 fix**: main.py PFAZ9 constructor'a `anfis_models_dir=str(self.pfaz_outputs[3])` ekle. Modülde de constructor'a parametre tanımı.
2. **PFAZ3 selector path**: ANFISParallelTrainerV2.__init__'e `ai_results_dir` parametresi ekle, main.py explicit aktarsın.
3. **PFAZ8 reports dir**: MasterVisualizationSystem.__init__'e `reports_dir` parametresi ekle.
4. **Genel pattern**: `_find_*` veya `output_dir.parent / 'X'` arayan tüm 42 nokta — fonksiyonel test yaz, env-bağımsız hale getir.

## Doğrulama Komutu

Yeni sprint sonu kontrolü:

```bash
# Path inference sayısı azaldı mı?
grep -rn "output_dir\.parent" pfaz_modules/*/*.py | grep -v test_ | wc -l
# Sprint 10 sonu: 42
# Sprint 11 hedef: < 30
```

---

*Sprint 10 ek inceleme | Inter-PFAZ bağımlılık denetimi*
