# PFAZ 03 — Analiz Notu
**Tarih:** 2026-05-03 | **Durum:** completed 100%

---

## Ozet

PFAZ 03, PFAZ 01'in urettigi veri kumeleri uzerinde 8 farkli ANFIS konfigurasyonunu
paralel olarak egitir. Takagi-Sugeno 1. dereceden ANFIS; Python tabanlı, MATLAB opsiyonel.
Onceki calisma turundan basariyla tamamlanmistir (completed 100%).

---

## Teknik Bulgular

### ANFIS Implementasyon

- TakagiSugenoANFIS sinifi: max_iter=300, patience=30, alpha=0.01
- 4 MF turu: Gaussian, GenBell (4. kuvvet), Ucgen, Yamuk
- Ic StandardScaler (PFAZ01 olceklemesinden bagimsiz)
- Hibrit ogrenme: LSE (kapalı form, ridge) + L-BFGS-B/LBFGS (gradyan)

### 8 Konfigurasyon

| CFG | Yontem | n_MF | MF Turu | Not |
|-----|--------|------|---------|-----|
| CFG001 | Grid | 2 | Gaussian | Temel referans |
| CFG002 | Grid | 2 | GenBell | 4. kuvvet bell |
| CFG003 | Grid | 2 | Ucgen | Sert sinirlar |
| CFG004 | Grid | 2 | Yamuk | Plato bolgesi |
| CFG005 | Grid | 3 | Gaussian | Adaptif n_mfs tetikler |
| CFG006 | SubClust | K-Means | Gaussian | radii=0.3 (ince kume) |
| CFG007 | SubClust | K-Means | Gaussian | radii=0.5 (orta kume) |
| CFG008 | SubClust | K-Means | Gaussian | radii=0.7 (genis kume) |

### Onemli Gozlemler

1. **SubClust fallback:** Python implementasyonu gercek subtractive clustering yerine
   KMeans kullanir. Radii parametresi k hesabini dogrudan etkilemez.
   genfis2 MATLAB koduna denk degil.

2. **Adaptif n_mfs:** CFG005 (3 MF) kucuk veri kumelerinde otomatik 2 MF'e duser.
   n_rules < max(4, n_train/3) kisiti. Buyuk feature setlerinde (n_inputs yuksek)
   kural sayisi patlamasi onlenir.

3. **Bell MF:** _bell fonksiyonu 4. kuvvet kullanir, standart gbellmf 2b kuvvet kullanir.
   Bu farklılık MF'in keskinligini degistirir; belgelenmiş bir tasarim tercihidir.

---

## Sonraki Adimlar

- [ ] PFAZ 04 (Bilinmeyen Cekirdek Tahminleri) analizi
- [ ] ANFIS modellerinin ML modelleriyle R2 karsilastirmasi (PFAZ 05/06)

---

*PFAZ 03 Analiz Notu | 2026-05-03*