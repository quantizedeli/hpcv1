# Sprint 15 — TRUBA Kriz Yonetimi ve Iyilestirme

**Tarih:** 2026-05-19/20
**Branch:** `sprint15-truba-kriz`
**Onceki:** Sprint 14 (PFAZ10 rewrite tamam, master'da)
**Sonraki onerilen:** Sprint 17 (BUG-109/110 mimari refactor — tez sonrasi)

---

## Sprint Hedefi

TRUBA Job2 iki kere timeout (24 saat, sonra 3 gun) sonrasi tam denetim. Krizin uc katmani:
1. **Resume BUG** — reddedilen ~54000 model her resume tekrar egitiliyor
2. **Dizin tutarsizligi** — `SVR/RF_018/` gibi model_type × config caprazlamasi
3. **Model kalitesi** — geometrik ortalama test_R²=0.001; %93 model reddedildi

Sprint hedefleri:
- Kok nedeni KOD ile dogrula (KURAL 32)
- Kalite haritasi cikar — feature/model/scenario/anomaly bazli
- Veriye dayali iyilestirme stratejisi (KURAL 40)
- BUG-101..108 fix + KURAL 34..40 belgelendir
- Tez cercevesini "R²>0.96" iddiasindan "feature secimi + kucuk-veri sinirlari" anlatisina cevir

---

## 1. Teshis Akisi (KURAL 34 — Once Teshis)

### Adim 1: TRUBA veri kontrolu
```
PKL:                6615  (kaydedilen model)
COMPLETED.json:     5731  (resume'un gordugu)
METRICS:           61283  (denenen toplam is)
DATASETS:           1468  (uretilen)
```

**Cikarim:** 61283 - 6615 = 54668 model reddedilip checkpoint yazmamis (BUG-101).
884 model PKL var ama completed.json yok — eski koşu artigi, kritik degil.

### Adim 2: Kok neden — kod denetimi
```
$ grep -nE "success=False|completed\.json" parallel_ai_trainer.py
1281: checkpoint_file = job.output_dir / 'completed.json'   # OKUMA
1346: ...  success=False  (POOR)                             # YAZMA YOK
1368: ...  success=False  (DIVERGED)                         # YAZMA YOK
1423: ...  success=False  (dual cv RET)                      # YAZMA YOK
1438: ...  success=False  (dual gap RET)                     # YAZMA YOK
1507: with open(... / 'completed.json', 'w')                 # SADECE BASARILI
1530: ...  success=False  (exception)                        # YAZMA YOK
```

5 erken-cikis yolundan 4'u kalite filtresi (deterministik), 1'i exception (geçici). 4 yolda checkpoint yazilmiyor — fix gerekli. Exception yolu KARARI: yazma (geçici hata tekrar denensin, B kararı).

### Adim 3: Yerel reprodüksiyon (QM_150_S70_AZNNP datasetiyle)
```
Train_R²=0.86 Val_R²=0.47 Test_R²=-0.54
DummyRegressor (sabit ortalama) Test_R²=-0.25 → RF DummyRegressor'dan KOTU
5-fold CV ortalama: -0.42 → asiri uyum kanıtı
```

Kok neden iki katmanli:
- **Feature seti zayif:** AZNNP = [A,Z,Nn,Np]. QM icin SHAP'ta B2E ikinci sirada (%18.3); AZNNP'de B2E YOK.
- **Kucuk veri + dagilim kaymasi:** 105 train, train QM ort 0.57, test ort 0.10.

---

## 2. Kalite Haritasi (KURAL 40 — Veri-Bazli Kucultme)

61283 metrics dosyasi tarandi (TRUBA'da `/arf/home/ahmacar/kalite_haritasi.py`).

### Feature Seti Siralamasi (test_R²)
**IYI (eğit) — 9 set:**
- AZB2EMCS (n=1992, ort 0.348, >0.8: **337**)
- AZSB2E (n=4482, >0.8: 179)
- AZS (n=3984, ort 0.344, >0.8: 147)
- ZB2EMCS (n=3515, >0.8: 79)
- AZSMC (n=2241, ort 0.383, >0.8: 41)
- AZSMCB2E, AZSMCBEPA, AZSBEPA, AZSNNNP (orta-iyi)

**COP (elimine) — 15 set:** ZNNPMC (-0.65), AMCBEPA (-0.27, hic >0.5 yok), AZNNP, AZB2EMC, NNPMC, ZB2EMC, AZB2E, AZNNPMC, AZMCBEPA, B2EMCBEA, AZB2EBEA, AZB2EMCBEA, ASMC (sinirda), AZBEPA, AZMC.

**Niceliksel ortuk:** B2E + Spin = iyi; ikisi yoksa cop. SHAP siralamasiyla birebir uyumlu.

### Hedef (Target)
- MM: ort 0.187, >0.8: 83
- QM: ort -0.132, >0.8: **700** (yuksek varyans: iyi setlerde cok iyi, kotu setlerde cok kotu)

### Model Tipi
- XGB (n=18459, ort 0.016, >0.8: 297)
- RF (n=24374, ort 0.006, >0.8: 343)
- **DNN** (n=18450, ort **-0.020**, >0.8: 143) — EN KOTU, en yavaş → ÇIKARILACAK

### Senaryo (S70 vs S80, iyi 9 FS'de)
- S80 (n=9740, ort 0.224, >0.8: 450)
- S70 (n=13197, ort 0.154, >0.8: 333)
- **QM/S70 ort -0.20, QM/S80 ort +0.17** → S70 elimine

### Anomaly modu (KARSI-SEZGISEL BULGU)
- vanilla (n=10985, ort 0.262, >0.8: **728**)
- NoAnomaly (n=11952, ort 0.111, >0.8: **55**)

**13× fark!** Anomali cikarmak performansi dusurur. **Yorum:** Nukleer "anomaliler" istatistiksel degil fiziksel sinyallerdir (sihirli sayilar, deformasyon gecisleri, izomerikler) — cikarmak rejim sinirlarini siliyor.

### Sampling
Random vs Stratified — marjinal fark. Ikisi de tut.

### Scaling
NoScaling 0.046 / Standard -0.001 / MinMax -0.043 — marjinal. NoScaling tut, digerleri elimine.

### Config (iyi 9 FS'de)
Top-20 config: 9 XGB + 11 RF (DNN'ler altta). En iyi config (XGB_021=0.265) ile en kotu RF/XGB (XGB_027=0.194) farki 0.07 — anlamsiz. Top-20 ortalamasi 0.226, genel 0.221.

---

## 3. Iyilestirme Kararlari (Kullanici Onayli, Veriye Dayali)

| # | Boyut | Karar | Veri Gerekceси |
|---|-------|-------|----------------|
| 1 | Feature setleri | 24 → 9 (iyi) | Cop 15 set test_R²>0 uretemiyor |
| 2 | Senaryo | S70+S80 → **S80** | QM/S70 -0.20 vs S80 +0.17 |
| 3 | Anomaly | vanilla+NoAnomaly → **vanilla** | 728 vs 55 model >0.8 (13×) |
| 4 | Boyut | 100/150/ALL → **150+ALL** | 100 yetersiz, ALL referans |
| 5 | Sampling | Random + Stratified | Marjinal fark, ikisi de tezde |
| 6 | Scaling | 3 → **NoScaling** | Marjinal, hafif iyi |
| 7 | Model | RF+XGB+LGB+CB+SVR+DNN → **RF+XGB** | DNN ort -0.02, digerleri BUG-104 |
| 8 | Config | 50 → **20** (top RF/XGB) | Config farki 0.07 (marjinal) |
| 9 | PFAZ3 esikleri | DEGISMEZ | Adaptive redistribution zaten en iyi 50'yi aliyor |
| 10 | Exception checkpoint | **YAZMA** (B) | Geçici hata tekrar denensin |
| 11 | PFAZ1 mudahale | **(α) yeniden uret** | Temiz, kapsam config'den |
| 12 | Eski datasetler | **(II) arsivle** | Feature ablation icin kullanilacak |

**Is hacmi:** 9 FS × 1 senaryo × 1 anomaly × 2 sampling × 1 scaling × 2 boyut = **36 dataset**. 36 × 2 model × 20 config = **1440 AI is + ~100 ANFIS is**. 110 worker × 250s ort = **~1 saat** koşu. (Onceki 65 saat → 1 saat = 65× hizlanma)

---

## 4. ANFIS Giris Sayisi Tasarim Karari (KURAL 36)

Grid-ANFIS kural sayisi = MF^giris:
| Giris | 2 MF | 3 MF | 105 ornekle? |
|-------|------|------|-------------|
| 3 | 8 | 27 | OK |
| 4 | 16 | 81 | Sinirda |
| 5 | 32 | **243** | IMKANSIZ |

**Cozum:** AI ve ANFIS farkli feature setleri kullanir:
- AI (RF/XGB): 5-giris zengin setler (AZB2EMCS, ZB2EMCS, AZSMCB2E, AZSMCBEPA) — agac modelleri yuksek boyuttan etkilenmez
- ANFIS 3-giris: AZS, AZSMC (tum 8 config OK)
- ANFIS 4-giris: AZSB2E, AZSBEPA, AZSNNNP — SADECE subclust 3 config (CFG006-008, kural sayisi veriden cikiyor)
- ANFIS 5-giris setler: SKIP

ANFIS toplam is: ~100 (PFAZ2 cok daha cabuk biter, ANFIS bekleme yok).

---

## 5. Bug ve Kural Ozeti

### Yeni Bug (10 toplam)
- **8 fix:** BUG-101..108 (Sprint 15)
- **2 ertelendi:** BUG-109, BUG-110 (Sprint 17 onerilen)

### Yeni Kural (7 toplam)
KURAL 34..40 — `claude-hatalarim-ve-dersler.md`'de detayli.
- **KURAL 34:** Kriz aninda once teshis (TRUBA verisi olmadan koşma)
- **KURAL 35:** Checkpoint felsefesi (basarili mi degil denendi mi)
- **KURAL 36:** AI/ANFIS feature seti ayriligi
- **KURAL 37:** Negatif sonuc tez katkisi
- **KURAL 38:** Memory niyet != kod davranisi
- **KURAL 39:** Inter-PFAZ tarama (QA_PLAYBOOK Bolum 3)
- **KURAL 40:** Veri-bazli kucultme

---

## 6. Tezsel Bulgular (tez-yazim-not-defteri.md'ye islendi)

10 niceliksel bulgu. Hepsi veri kaynakli (61283 metrics):
1. Feature secimi belirleyici, hiperparametre marjinal
2. B2E QM icin kritik (SHAP %18.3)
3. Spin MM icin kritik (SHAP %18.7)
4. Kucuk-veride DNN < RF/XGB
5. **Anomali cikarmak performansi dusurur** (728 vs 55, karsi-sezgisel, tezsel katki)
6. S80 > S70, QM'de ucurum
7. ANFIS kural patlamasi → AI/ANFIS feature seti ayrımı
8. Dual-R² filtresi calisiyor
9. Hiperparametre alani genis ama dar etkili
10. R²>0.96 hedefi ulasilamaz, R²>0.85 alt bolge literatur kiyasinda rekabetci

**Tez cercevesi degisikligi:** "Yuksek dogruluk" iddiasi → "feature secimi + kucuk-veri sinirlari" anlatisi. Daha savunulabilir, daha bilimsel olarak dogru.

---

## 7. Uygulama Planı

### Patch 1: docs.patch (BU PATCH)
- `pipeline-hatalari.md`: BUG-101..110
- `claude-hatalarim-ve-dersler.md`: KURAL 34..40
- `tez-yazim-not-defteri.md`: Sprint 15 eki (10 bulgu)
- `phases/faz-01..03.md`: yeni kapsam
- `phases/faz-05/06/08/09.md`: BUG-105/106/108 notlari
- `inter-pfaz-dependency-map.md`: ANFIS formatlari + BUG-108
- `sprints/sprint-15-truba-kriz-ve-iyilestirme.md`: bu dosya
- `sprints/SPRINT-PLAN.md`: Sprint 14+15 satir
- `CLAUDE.md`: kapsam degişiklikleri

### Patch 2: code-fix.patch (Adim 2'de hazirlanacak)
- `parallel_ai_trainer.py`: BUG-101 (_save_checkpoint), BUG-103 (model_type×config filtre), BUG-104 (config.json'dan model_types)
- `anfis_parallel_trainer_v2.py`: BUG-102, ANFIS giris kisitlamasi (3-giriş tüm config, 4-giriş subclust, 5-giriş skip)
- `monte_carlo_simulation_system.py`: BUG-108 (.pkl yolu)
- `faz5_complete_cross_model.py`: DEAD_CODE_NOTE header
- `pfaz_modules/pfaz08_visualization/*.py`: BUG-106 dinamik model listesi
- Yerel test scriptleri (Test 1-7)

### Patch 3: config.patch (Adim 3'te hazirlanacak)
- `config.json`: pfaz01 (9 FS, S80, vanilla, NoScaling, 150+ALL), pfaz02 (RF+XGB, n_configs=20)
- `training_configs_20.json`: top-20 RF/XGB config (yeni dosya)
- Slurm script suresi notu

### Adim 4: TRUBA yeniden koşu (patchler uygulandiktan sonra)
- Eski datasetleri arsivle (II)
- PFAZ1 yeniden (~5 dk)
- PFAZ2 + PFAZ3 (~1 saat)
- PFAZ4..12 (~30 dk)
- **Toplam ~2 saat** (Sprint 14'teki tahmin 25-48 saat → şimdi 2 saat = 12-24× hizlanma)

---

## 8. Acik Sorular / Riskler

1. **22 Mayis kesin son.** Yeni iş hacmi ile bu rahatlikla sigar (~2 saat koşu). Risk: patch uygulamasi sirasinda yeni bug bulunursa.
2. **R²>0.96 hedefi ulasilamaz** — danismanla konusulmali (tez sonuc bolumunde).
3. **BUG-111 (ANFIS multi-target list assumption)** — Sprint 15 koşusunda MM_QM joint target var mi? Şu plan tek-target (MM, QM ayri) — risk kapali.
4. **PFAZ9 BUG-108 fix calisir mi?** Yerel test eklenecek (Test 8).
5. **Sprint 17 onerisi** — Kullanici onayli mi? Tez sonrasi mimari refactor planlandi (BUG-109/110). Sprint 17 kararı kullanici verecek.

---

*Sprint 15 raporu | TRUBA kriz yonetimi (BUG-101..108) + 7 yeni KURAL + 10 tezsel bulgu | 2026-05-20*
