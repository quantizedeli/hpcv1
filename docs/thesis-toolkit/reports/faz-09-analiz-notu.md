# FAZ-09 Analiz Notu: Monte Carlo Belirsizlik Analizi

> **Proje:** Nuclear Physics AI Project v2.0.0
> **Analiz Tarihi:** 2026-05-04
> **Analist:** Claude Code (Ahmet Kemal Acar arastirmasi)
> **Kaynak Dosyasi:** phases/faz-09-monte-carlo.md

---

## Ozet

PFAZ 09, tezdeki belirsizlik katmanini olusturur. Iki sinif -- AAA2ControlGroupAnalyzerComplete (1046 satir) ve MonteCarloSimulationSystem (1259 satir) -- birlikte 267 cekirdek icin 95% CI uretir ve Top-10 model uzerinde 5 farkli MC teknigi uygular.

**Kod durumu:** Tamamlandi (2026-04-04, pfaz_status.json: completed)
**Gercek cikti:** YOK -- PFAZ02 hala calisuyor, top-50 model henuz hazir degil.

---

## Teknik Bulgular

### Mimari
- **Katman 1:** Top-50 model secimi (AI + ANFIS), 267 cekirdek ensemble CI
- **Katman 2:** Top-10 model, 5 MC teknigi (MCDropout, Bootstrap, Noise, FeatureDropout, EnsembleUncertainty)
- **CI yontemi:** Percentile [P_2.5, P_97.5] -- normal dagilim varsayimi yok (dogru secim)

### Performans Parametreleri
| Parametre | Deger |
|-----------|-------|
| n_models (K1) | 50 |
| n_models (K2) | 10 |
| n_bootstrap | 100 (onerilen: 1000) |
| n_mc_dropout | 100 |
| Noise seviyeleri | 5 x 100 |
| Feature dropout | 3 x 500 |
| Paralel is | n_jobs=8 |

### Excel Ciktisi
- `AAA2_Complete_MM.xlsx` ve `AAA2_Complete_QM.xlsx`
- 4 ana sayfa: Predictions, Uncertainty, PerModel_Top25, Model_Ranking
- 11 bos analiz sayfasi (PFAZ12 FAILED)

### PFAZ08 Baglantisi
MC9-A (Std haritasi), MC9-B (CV dagilimi), MC9-C (CI genisligi scatter) grafikleri
PFAZ08 ikinci gecisinde bu Excel dosyalarindan besleniyor.

---

## Bulunan Buglar (7 yeni: BUG-24..30)

| ID | Oncelik | Sorun | Sprint 2026-05-04 Durumu |
|----|---------|-------|--------------------------|
| BUG-24 | [ORTA] | Bootstrap n=100 kucuk; CI guvenilir degil | Tez notu — yeniden egitimde arttirilacak |
| BUG-25 | [ORTA] | Feature uyumsuzlugunda sessiz model atlama | Tez notu — loglama sinirlamasi |
| BUG-26 | [DUSUK] | MC Dropout DNN-only sinirlamasi | Tez notu — mimari karar |
| BUG-27 | [ORTA] | BUG-02 (WS) PFAZ09'u da etkiliyor | BUG-02 duzeltildi; PFAZ09 yeniden calistirinca kapanacak |
| BUG-28 | [DUSUK] | Analysis_5..15 PFAZ12 bagimlisi | BUG-31 duzeltildi; PFAZ12 artik import edilebilir |
| BUG-29 | [DUSUK] | n_jobs=8 hardcoded | **DÜZELTİLDİ** — `min(8, os.cpu_count())` kullaniliyor |
| BUG-30 | [DUSUK] | consensus_threshold hedef-bagimsiz | **DÜZELTİLDİ** — MM/QM ayrimi icin yorum satiri eklendi |

---

## Guclu Yonler

1. Iki katmanli MC mimarisi: genis kapsam (K1) + derin analiz (K2)
2. Per-model feature set -- metadata.json'dan otomatik okuma
3. 5 farkli belirsizlik kaynagi -- cok boyutlu analiz
4. Percentile CI -- dogru istatistiksel tercih

---

## Kritik Dikkat Noktalari

1. **n_bootstrap=100 yetersiz:** Tezde belirtilmeli; fix oncelikli.
2. **Sessiz model atlama:** 50 model yerine daha az kullaniliyor olabilir; loglama iyilestirilmeli.
3. **WS bug zinciri:** BUG-02 duzeltilmeden PFAZ09 WS-agirlikli modellerin CI'si kirli.
4. **PFAZ12 bagimliligi:** Analysis bolumleri bos; bunu tez istatistik bolumuyle nasil dolduracagiz?

---

## Onerilen Eylemler

1. **Simdi:** Bu analiz notu ile devam et, PFAZ12/13 belgelemeye gec.
2. **PFAZ02 bittikten sonra:** BUG-24 fix (n_bootstrap=1000) + PFAZ09 yeniden calistir.
3. **BUG-02 fix sonrasi:** Tum pipeline (01->09) yeniden calistir.

---

*faz-09-analiz-notu.md v1.0 | 2026-05-04*
