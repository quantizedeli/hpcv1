# Faz 01 Analiz Notu: Veri Kümesi Üretimi

> **Tarih:** 2026-05-02  
> **Durum:** Kaynak analizi tamamlandi  
> **Dokuman:** `phases/faz-01-veri-kumesi-uretimi.md`

---

## Özet

PFAZ 01, `data/aaa2.txt` dosyasindaki 267 cekirdegi alarak 7 fizik modulu uzerinden 44+ ozelige genisletir ve 848 varyant veri kumesi uretir. Tum alt-bilesanler `DatasetGenerationPipelineV2` tarafindan orkestre edilir.

---

## Temel Bulgular

### Mimari
- **Ana orkestrator:** `DatasetGenerationPipelineV2` — 9 bilesen sinifi
- **Fizik zenginlestirme:** `TheoreticalCalculationsManager` → 7 alt-modul sirali calistirir
- **Paralel eski sinif:** `DatasetGenerator` — aktif degil

### Veri Akisi
```
aaa2.txt (12 sutun) 
  → _load_raw_data 
  → _add_theoretical_calculations (44+ sutun)
  → _apply_qm_filtering (hedefe gore)
  → _perform_quality_control
  → _generate_all_datasets (848 iterasyon)
  → CSV + Excel + metadata.json
```

### Tanimlanan Formuller (F-001..F-020)

| Grup | Formuller |
|------|-----------|
| SEMF | F-001 (toplam BE), F-002..F-006 (5 terim), F-007 (BE/A) |
| Yaricap | F-008 (R = R0 * A^(1/3)) |
| Ayrilma enerjisi | F-009 (S_n), F-010 (S_p) |
| Kabuk | F-011 (sihirli karakter) |
| Deformasyon | F-012 (beta2'den), F-013 (Q0) |
| Schmidt | F-014, F-015 (j=l+/-1/2) |
| WS | F-016 (merkezi potansiyel) |
| Nilsson | F-017 (tek-parcacik enerjisi) |
| Aykirı deger | F-018 (IQR sinirlari) |
| Diger | F-019 (eslenme acigi), F-020 (B(E2) WU) |

### Tespit Edilen Bug'lar

| Bug | Konum | Etki | Sprint 2026-05-04 Durumu |
|-----|-------|------|--------------------------|
| `HBAR_C` import hatasi (BUG-02) | `woods_saxon.py:15` | `WoodsSaxonPotential` kullanılamaz | **DÜZELTİLDİ** — `constants.py`'e `HBAR_C=197.3269804` eklendi |
| Spin-yorunge parametreleri eksik (BUG-03) | `woods_saxon.py:73-75` | `V_so`, `r_so`, `a_so` -> KeyError riski | **DÜZELTİLDİ** — `WOODS_SAXON_PARAMS`'a `V_so=6.0, r_so=1.25, a_so=0.67` eklendi |
| `data_file_mat` key hatasi (BUG-04) | `pipeline_v2.py:1193` | Raporlama adiminda KeyError riski | **GEÇERSİZ** — MAT formatı kasıtlı kaldırılmış, tasarım kararı |
| Q=0 yanlis filtreleme (BUG-01) | `qm_filter_manager.py:153` | Gercek Q=0 cekirdekleri silinebilir | **GEÇERSİZ** — aaa2.txt dışı çekirdek kullanılmıyor, filtre kasıtlı |

> **Not:** PFAZ01 ve PFAZ02'nin BUG-02/03 düzeltmesiyle yeniden çalıştırılması gerekmektedir. WS özellikleri o zamana kadar sıfır/NaN olarak kalacaktır.

---

## Tez Katkisi

- **§2. Kuramsal Cerceve:** F-001..F-020 formüllerinin tamami bu fazdan alinacak
- **§3. Yontem:** A-001 (pipeline), A-002 (veri temizleme), A-004 (ornekleme), A-005 (zenginlestirme)
- **§3.1:** Veri kumesi isimlendirme semasi tablosu (T-003)
- **§3.2:** Fizik ozellik muhendisligi bilesen diyagrami (S-003)

---

## Tamamlama Kontrol Listesi

- [x] `phases/faz-01-veri-kumesi-uretimi.md` yazildi (17 bolum)
- [x] `phases/README.md` guncellendi (durum tamamlandi, tarih 2026-05-02)
- [x] `reports/faz-01-analiz-notu.md` yazildi
- [x] `06-FIGURE-TABLE-CATALOG.md` — F-001..F-020, A-001..A-005, S-002, S-003, T-002..T-004 eklenecek
- [x] `07-GLOSSARY-SYMBOLS.md` — yeni terimler eklenecek

---

*Faz 01 Analiz Notu v2.0 | 2026-05-03 (Guncelleme: olcekleme 4 yontem, ozellik kisaltma tablosu, SHAP siralamasi, veri kumesi agaci eklendi)*

