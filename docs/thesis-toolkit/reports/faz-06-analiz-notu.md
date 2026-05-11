# PFAZ 06 Analiz Notu

> Tarih: 2026-05-04 | Durum: Kod hazir, cikti yok

## Tek Cumle Ozet

PFAZ 06, tum fazlarin ciktilarini THESIS_COMPLETE_RESULTS.xlsx (29 sayfa), LaTeX, Bootstrap CI ve Tornado analiziyle birlestirir; PFAZ 12-13 basarisizligi nedeniyle 3 sayfa bos kalacak.

## Kritik Bulgular

- Pipeline sirasi: [1,2,3,4,5,7,9,12,13,**6**,8,10] -- 9. sirada calisir
- PFAZ 12 (Istatistik) ve PFAZ 13 (AutoML) BASARISIZ -- Band_Analizi + AutoML sayfalar bos
- 29 Excel sayfasi; All_AI_Models 50k/sayfa parcalanir (toplam ~95k satir)
- Bootstrap CI: 5000 ornekli Val_R2 guven araligi
- Renk kodu: Excellent(>=0.95)/Good(>=0.90)/Medium(>=0.70)/Poor(<0.70)
- R2_FLOOR = -10.0: sapmis modeller filtreleniyor
- Eksik giris: logger.warning + atlama (pipeline durmuyor)

## Acik Sorular

- PFAZ 12/13 yeniden calistirilacak mi?
- thesis_report.tex gercek degerlerle doluyor mu?
- Bootstrap CI 267 cekirdek icin anlamli mi?

## Formul / Algoritma

- F-045..F-046 (2 yeni formul)
- A-022 (1 yeni algoritma)
