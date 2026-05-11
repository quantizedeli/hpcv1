# FAZ-12 Analiz Notu: Ileri Istatistiksel Analitik

> **Proje:** Nuclear Physics AI Project v2.0.0
> **Analiz Tarihi:** 2026-05-04
> **Kaynak Dosya:** phases/faz-12-ileri-analitik.md

---

## Ozet

PFAZ 12, model karsilastirmasi icin kapsamli istatistiksel test portfoyu + nükleer veri örüntü analizi sunar.
7 dosya, ~4370 satir; 6 sinif.

**Durum:** ~~FAILED~~ **KOD HAZIR** -- BUG-31 DUZELTILDI 2026-05-09 (NuclearBandAnalyzer alias eklendi). Henuz calistirilmadi; PFAZ02 bittikten sonra calistir.
**Sprint 2026-05-04:** BUG-31 duzeltildi -- `__init__.py` guncellendi (sinif adi uyumsuzlugu da 2026-05-09'da duzeltildi)

---

## Siniflar

| Sinif | Satir | Ozet |
|-------|-------|------|
| StatisticalTestingSuite | 688 | 6 test + etki buyuklugu |
| AdvancedSensitivityAnalysis | 646 | Sobol/Morris/Tornado |
| NuclearPatternAnalyzer | 789 | Izotop zinciri + magic number |
| NuclearBandAnalyzer | 1174 | Bant + kutle bolgesi (BUG-31: export eksik) |
| BootstrapConfidenceIntervals | 586 | n=5000 CI |
| BayesianModelComparison | 450 | Bayes Factor + ROPE |

## Bulunan Buglar

| ID | Oncelik | Sorun | Sprint 2026-05-04 Durumu |
|----|---------|-------|--------------------------|
| BUG-31 | [ORTA] | NuclearBandAnalyzer __init__ export eksik | **DÜZELTİLDİ** — `NuclearBandAnalyzer` ve `NuclearPatternAnalyzer` `__init__.py`'e eklendi |
| BUG-36 | [BILGI] | Progress=0 baslatma hatasi belirsiz | Tez notu — statsmodels/SALib kurulumu yeni PC'de dogrulanmali |

## Kritik Etkiler

- PFAZ06: Band_Analizi sayfasi bos
- PFAZ09: Analysis_5..15 sayfalarindan 11'i bos  
- PFAZ08: ST12-A/B grafikleri uretilemiyor

## Onerilen Eylemler

1. PFAZ12 isolation test: `python main.py --pfaz 12 --mode run` ve hata mesajini logla
2. BUG-31 fix: 3 satir __init__.py guncelleme
3. statsmodels + SALib kurulumunu dogrula

*faz-12-analiz-notu.md v1.0 | 2026-05-04*
