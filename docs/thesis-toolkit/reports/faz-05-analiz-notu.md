# PFAZ 05 Analiz Notu

> Tarih: 2026-05-04 | Durum: Tamamlandi

## Tek Cumle Ozet

PFAZ 05, AI ve ANFIS modellerini ortak cekirdek kesiti uzerinde Good/Medium/Poor kategorilerine ayirarak model uyumunu quantifiye eder ve BestModelSelector ile cok kriterli model secimine olanak saglar.

## Temel Bulgular

- 5 sinif, 7 kaynak dosya: CrossModelEvaluator, CrossModelAnalysisPipeline,
  BestModelSelector, IsotopeChainAnalyzer, OptimizerComparisonReporter
- Good/Medium/Poor sinirlar: error<0.1/R2>0.90, error<0.5/R2>0.70, diger
- Agreement score: 1/(1+std_error) -- yuksek std = dusuk uzlasma = yuksek belirsizlik
- BestModelSelector agirlik: accuracy(%35)+speed(%20)+efficiency(%15)+stability(%15)+gen(%15)
- IsotopeChainAnalyzer: SDI=delta/sigma, esik=1.5, sihirli sayi korelasyonu
- Durum: pfaz_status.json completed 100% (2026-04-02)

## Acik Sorular

- Poor / Degradation ortusme durumu dogrulanmali
- BUG-10 val_r2 ic sozluk riski BMS generalization girdisini etkiliyor mu?
- SDI>1.5 kac cekirdek flaglendi? Sihirli sayi korelasyon orani?
- ANFIS vs ML agreement simetrisi?

## Formul / Algoritma Sayimi

- Formuller: F-040..F-044 (5 yeni formul)
- Algoritmalar: A-019..A-021 (3 yeni algoritma)

