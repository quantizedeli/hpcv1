# Bug Analiz Notu — WS Import ve Spin-Yörünge

> **Tarih:** 2026-05-03  
> **Durum:** Çalışan PC'ye etkisi analiz edildi

---

## Bug 1: HBAR_C Import Hatası

**Konum:** `woods_saxon.py:15`  
```python
from core_modules.constants import HBAR_C  # constants.py'de TANIMLI DEĞİL
```

**Gerçek durum:**
- `constants.py`'de HBAR_C eksik
- `theoretical_calculations_manager.py:25` kendi içinde tanımlıyor: `HBAR_C = 197.3269804`
- WS modülü import aşamasında çöküyor, `_AVAILABLE=False` oluyor
- Program çökmüyor: try/except yakalar

**Çalışan PC etkisi:**
- WS potansiyel özellikleri = 0 veya NaN (tüm 267 çekirdek için aynı)
- SEMF, Schmidt, deformasyon, kabuk modeli: TAMAM, etkilenmiyor
- Tree modeller (RF, XGBoost) bu sıfır-varyans kolonu otomatik görmezden gelir
- **SONUÇ: Veri tutarlı, ama WS bilgisi yok. Bitirip dokümante et.**

**Düzeltme (sonraki çalıştırma için):**
`core_modules/constants.py`'e ekle:
```python
HBAR_C = 197.3269804  # MeV·fm (ℏc)
```

---

## Bug 2: Spin-Yörünge Parametreleri Eksik

**Konum:** `woods_saxon.py:73-75`  
**Durum:** Bug 1 WS'yi import aşamasında blokluyor → Bug 2 hiç tetiklenmiyor bu çalıştırmada.

**Bug 1 düzeltilince ortaya çıkar:**
```python
V_so = self.params['V_so']   # KeyError: 'V_so' not in WOODS_SAXON_PARAMS
```

**Düzeltme:**
`constants.py`'deki `WOODS_SAXON_PARAMS`'a ekle:
```python
WOODS_SAXON_PARAMS = {
    'V0': 51.0,   'r0': 1.25, 'a': 0.67,
    'V_so': 7.5,  'r_so': 1.25, 'a_so': 0.67   # ← EKLENECEk
}
```
Önem: Orta. Sadece spin-yörünge terimini etkiler.

---

## Bug 3: MAT Dosyası Anahtar Hatası

**Konum:** `pipeline_v2.py:1193`  
**Durum:** Kullanıcı MAT eğitimini kaldırdı. Kod kalmış ama tetiklenmiyor.  
**Etki:** Düşük öncelik — sadece MAT path raporlanırken KeyError verir.

---

## Düzeltme Sırası (sonraki çalıştırma öncesi)

1. `constants.py`'e HBAR_C ekle → Bug 1 çözülür
2. `WOODS_SAXON_PARAMS`'a V_so/r_so/a_so ekle → Bug 2 çözülür
3. `qm_filter_manager.py:153` Q=0 mantığını düzelt → Bug 4 (en kritik, QM modelleri etkiler)
4. Bug 3 kodu temizle veya koy → düşük öncelik

---

## Sprint 2026-05-04 — Uygulanan Düzeltmeler

> Bu bölüm 2026-05-04 tarihinde sprint sırasında uygulanan düzeltmeleri belgelemektedir.

### Bug 1 (HBAR_C) — DÜZELTİLDİ ✓
`core_modules/constants.py`'e eklendi:
```python
HBAR_C = 197.3269804  # MeV·fm (ℏc)
```
`woods_saxon.py` artık bu sabiti başarıyla import edebilir. WS özellikleri bir sonraki PFAZ01 çalıştırmasında doğru hesaplanacak.

### Bug 2 (Spin-Yörünge Parametreleri) — DÜZELTİLDİ ✓
`WOODS_SAXON_PARAMS` güncellendi. Dikkat: bu dosyada V_so=7.5 yazıyordu, ancak literatür referansı baz alınarak **V_so=6.0** kullanıldı:
```python
WOODS_SAXON_PARAMS = {
    'V0': 51.0, 'r0': 1.25, 'a': 0.67,
    'V_so': 6.0, 'r_so': 1.25, 'a_so': 0.67   # ← EKLENDİ
}
```

### Bug 3 (MAT Anahtar Hatası) — GEÇERSİZ (tasarım kararı)
`pipeline_v2.py:1193` MAT formatı kasıtlı olarak kaldırılmış. Kod kalıntısıdır, bug değil. Tez notuna alındı.

### Bug 4 (Q=0 Filtreleme) — GEÇERSİZ (tasarım kararı)
`qm_filter_manager.py:153` Q=0 filtresi kasıtlıdır — aaa2.txt dışındaki çekirdekler zaten kullanılmıyor. Değişiklik gerekmez.

---

## Sprint 4-13 — Eski "Bug N" Numaralandırması ile Resmi BUG-ID Eşleme

Bu dosyada kullanılan eski "Bug 1/2/3/4" numaraları sonradan resmi BUG-ID sistemine geçirildi. Aşağıdaki tablo eşleştirmeyi gösterir:

| Eski No | Resmi BUG-ID | Sprint | Durum |
|---------|--------------|--------|-------|
| Bug 1 (HBAR_C) | **BUG-02** | Sprint 4 (2026-05-04) | DÜZELTİLDİ |
| Bug 2 (V_so) | **BUG-03** | Sprint 4 (2026-05-04) | DÜZELTİLDİ (V_so=6.0) |
| Bug 3 (MAT KeyError) | BUG-12 (geçersiz) | — | GEÇERSİZ (tasarım) |
| Bug 4 (Q=0 filtre) | BUG-01 (geçersiz) | — | GEÇERSİZ (tasarım) |

---

## Sprint 4-13 — Bu Dosyaya Eklenen Yeni Buglar (Özet)

Bu dosya yalnızca Sprint 4 öncesi tespit edilen 4 bug'ı kapsıyordu. Sprint 4-13 sonrası toplam BUG sayısı **99**'a ulaştı. Detaylar için ana kaynak:

- **`docs/thesis-toolkit/pipeline-hatalari.md`** — Tam bug katalog (BUG-01..99)
- **`docs/thesis-toolkit/CLAUDE.md`** — Sprint özetleri
- **`docs/thesis-toolkit/sprints/sprint-XX-*.md`** — Her sprint için detaylı bug analizi

### Önemli Sprint 4-13 Bug'ları (Bu Dosya İle İlgili)

| BUG-ID | Konu | Sprint | Durum |
|--------|------|--------|-------|
| BUG-31 | NuclearBandAnalyzer alias | Sprint 4 | DÜZELTİLDİ |
| BUG-32 | automl IndentationError | Sprint 4 | DÜZELTİLDİ |
| BUG-38 | MC n_bootstrap=100 yetersiz | Sprint 4+8 | DÜZELTİLDİ (1000) |
| BUG-47/48 | TRUBA-CRITICAL hardcoded sys.path | Sprint 7 | DÜZELTİLDİ |
| BUG-53 | Optuna TF clear_session eksik | Sprint 7 | DÜZELTİLDİ |
| BUG-62 | CV gate gerçekten aktif değildi | Sprint 8 | DÜZELTİLDİ |
| BUG-85 | PIPESTATUS Slurm exit code | Sprint 13 | DÜZELTİLDİ |

### Kapatma Tablosu Sync Notu

Sprint 4 sonrası "DÜZELTİLDİ ✓" işaretli bug'lar (Bug 1/2) **kapatılma tarihleri**:
- **Bug 1 (BUG-02) HBAR_C:** Kapatıldı 2026-05-04 (Sprint 4 patch)
- **Bug 2 (BUG-03) V_so:** Kapatıldı 2026-05-04 (Sprint 4 patch)

Bu eşleme `docs/thesis-toolkit/CLAUDE.md` "Known Critical Bugs" tablosu ile senkronize tutulmalıdır (KURAL 31 -- Single Source of Truth).

---

*Sprint 4-13 güncelleme: 2026-05-14*
