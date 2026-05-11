# PFAZ 04 -- Analiz Notu
**Tarih:** 2026-05-03 | **Durum:** completed 100%

## Ozet

PFAZ 04, PFAZ 02 ve PFAZ 03'ten gelen egitilmis modelleri test.csv uzerinde degerlendirir.
Test seti = 'bilinmeyen cekirdekler' (egitimde hic kullanilmadi).
3 ana sinif: UnknownNucleiPredictor, SingleNucleusPredictor, GeneralizationAnalyzer.

## Teknik Bulgular

- **Degradasyon:** Val_R2 - Test_R2; nukleer gecis bolgeleri ve magic number cevrelerinde yuksek
- **GS:** Test_R2 / Val_R2 * 100; ideal >= 95%
- **Consensus:** Top-25 modelin ortalamasi; standart sapma belirsizlik gostergesi
- **Feature enrichment:** Yalnizca Z ve N ile 44+ ozellik otomatik turetilir
- **7-sayfali Excel:** All_Results, Best_Per_Dataset, Degradation, AI_vs_ANFIS, 2xPivot, Per-Nucleus

## Onemli Gozlem

val_r2 okunmasi ic-ic sozluk: m.get('val',{}).get('r2')
Bu yapinin PFAZ02 metrics JSON'u ile uyumlu olmasi kritik.
Uyumsuzlukta val_r2=None -> degradation=None -> Degradation_Analysis sayfasi bos.

---
*PFAZ 04 Analiz Notu | 2026-05-03*
