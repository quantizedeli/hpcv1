# Fizik Özellik Justifikasyonları — Neden Bu 44+ Özellik?

> **Amaç:** Her özelliğin fiziksel gerekçesini ve tezdeki rolünü belgelemek  
> **Tarih:** 2026-05-03

---

## 1. Ham Özellikler (aaa2.txt'den)

### 1.1 Z (Proton Sayısı), N (Nötron Sayısı), A (Kütle Numarası)

**Neden bu üçü temel?**
Nükleer fizikteki her özellik sonuçta Z ve N'in fonksiyonudur. A = Z + N bağımlı değişken olmasına rağmen ayrıca eklenir çünkü:
- Kütle bağımlı davranış (büyük A'da SEMF daha iyi çalışır) bağımsız yakalanabilir
- Model, A üzerinden kütle ölçeğini daha kolay öğrenir

### 1.2 Deneysel MM ve QM (hedef değerler)

Mevcut deneysel ölçümler hem eğitim hedefleri hem de model doğrulaması için kullanılır. 267 çekirdeğin tamamının MM ve QM ölçümü yoktur — bu durum PFAZ 04'ün (bilinmeyen çekirdek tahmini) varoluş nedenidir.

---

## 2. SEMF Türetilmiş Özellikler (F-001..F-007)

### 2.1 Toplam Bağlanma Enerjisi: BE(A,Z)

```
BE = a_v·A - a_s·A^(2/3) - a_c·Z(Z-1)/A^(1/3) - a_a·(N-Z)²/A + δ(A,Z)
```

**Neden MM/QM tahmini için?**
Bağlanma enerjisi nükleer doygunluk, yüzey katkısı ve asimetri koşullarını özetler. Bu koşullar dolaylı olarak nükleonların yörünge yapısını belirler — yörünge yapısı ise MM'yi doğrudan, QM'yi ise deformasyon üzerinden etkiler. Korelasyon direkt olmasa da BE, tek parçacık enerji düzeylerinin dolaylı bir işareti olarak kullanılır.

### 2.2 SEMF Birimleri (a_v terimi, a_s terimi, a_c terimi, a_a terimi, δ)

Her terimin ayrı özellik olarak eklenmesi, modele SEMF'in hangi bileşeninin tahmin için ne kadar önemli olduğunu öğrenme fırsatı tanır. Örneğin:
- **a_a terimi (asimetri):** N≠Z çekirdeklerde çok büyük → isospin efekti → MM üzerine doğrudan etki
- **δ terimi (çiftlenme):** Çift-çift vs tek-tek nükleon farkını kodlar → Schmidt değeri farkının kaynağı

### 2.3 Nükleon Başına Bağlanma Enerjisi: BE/A

BE/A, bağlanma gücünün yoğunluğunu ölçer ve doygunluk bölgesini (A~60) açıkça işaretler. Model, BE/A ≈ 8.7 MeV bölgesindeki çekirdeklerin farklı davrandığını öğrenebilir.

---

## 3. Yarıçap ve Boyut Özellikleri (F-008)

### 3.1 R = R₀·A^(1/3), R₀ = 1.2 fm

**Fiziksel gerekçe:**
Nükleer yarıçap, hem kuadrupol momentin hem de çiftlenme etkileşiminin (pairing) büyüklüğünü etkiler. Q = (2/5)·Z·R²·β₂ bağıntısı nedeniyle R doğrudan QM hesabına girer. Ayrıca Woods-Saxon potansiyelinin etkili derinliği yarıçapla ölçeklenir.

---

## 4. Ayrılma Enerjileri (F-009, F-010)

### 4.1 Nötron Ayrılma Enerjisi S_n ve Proton Ayrılma Enerjisi S_p

```
S_n(Z,N) = BE(Z,N) - BE(Z,N-1)
S_p(Z,N) = BE(Z,N) - BE(Z-1,N)
```

**Neden kritik?**
S_n ve S_p, son nükleonun ne kadar gevşek bağlı olduğunu ölçer. Manyetik moment büyük ölçüde son (tek) nükleonun spin durumuna bağlıdır; bu nükleon ne kadar "dışarıda" ise single-particle davranışı o kadar belirgindir. Ayrıca S_n/S_p'deki ani düşüş, kabuk kapanmasının en güvenilir göstergesidir.

---

## 5. Kabuk Model Özellikleri (F-011)

### 5.1 magic_character, Z_magic_dist, N_magic_dist

**Neden bu üç özellik?**

Sihirli sayılar (2, 8, 20, 28, 50, 82, 126) nükleer özelliklerin ani değişim noktalarıdır. ML modeli, bu noktaları kendi başına bulamaz çünkü:

1. Z=82 ile Z=83 arasındaki fark sayısal olarak yalnızca 1'dir
2. Ama fiziksel olarak aradaki fark dev boyuttadır (kapalı vs açık kabuk)
3. Modelin bu farkı öğrenmesi için söylenmesi gerekir

magic_character = 1 (Z veya N sihirli) bu bağlamı verir.
Z_magic_dist ve N_magic_dist ise ne kadar uzakta olduğunu söyler.

---

## 6. Deformasyon Özellikleri (F-012, F-013)

### 6.1 Kuadrupol Deformasyon Parametresi β₂

```
β₂ = (√(5π)/3) · Q₀ / (Z·R²)
```

**Neden hem β₂ hem de ham Q₀?**
β₂ normalleştirilmiş bir deformasyon ölçüsüdür — farklı kütle bölgelerindeki çekirdeklerin karşılaştırılmasına izin verir. Ham Q₀ ise mutlak büyüklüğü kodlar. Model her ikisinden farklı bilgi çıkarabilir.

**QM tahmini için neden kritik?**
Kuadrupol moment doğrudan çekirdeğin deformasyonuna bağlıdır:
- β₂ = 0: küresel çekirdek, Q = 0 (kapalı kabuk)
- β₂ > 0: prolate (uzun eksen boyunca uzamış), Q > 0
- β₂ < 0: oblate (yassılaşmış), Q < 0

Bu işaret bilgisi tez sonuçlarında model doğruluğunu değerlendirmek için kritiktir.

---

## 7. Schmidt Momentleri (F-014, F-015)

### 7.1 Schmidt Manyetik Momenti (μ_Schmidt)

```
μ_Schmidt(j=l+1/2) = (j-1/2)·g_l + (1/2)·g_s
μ_Schmidt(j=l-1/2) = [j·(j+3/2)·g_l - (1/2)·g_s] / (j+1)
```

**Neden ML modeline girdi olarak?**
Schmidt değeri teorik üst/alt sınırları tanımlar. Deneysel momentler genellikle Schmidt değerinin belirli bir oranındadır. Bu oran (quenching faktörü) yaklaşık 0.6-0.8 civarındadır. ML modeli:
1. Schmidt değerini referans alarak kaba tahmini öğrenir
2. Ardından quenching ve kolektif efektleri ayrıca öğrenir

Bu iki adımlı öğrenme, yalnızca ham Z ve N kullanmaktan önemli ölçüde daha verimlidir.

---

## 8. Woods-Saxon Potansiyeli (F-016)

```
V_WS(r) = -V₀ / (1 + exp((r-R)/a))
V₀ = 51.0 MeV, R = r₀·A^(1/3), r₀ = 1.25 fm, a = 0.67 fm
```

**Neden basit harmonik osilator yerine?**
Harmonik osilator nükleer potansiyelini fazla idealleştirir: gerçekte nükleer yüzey difüzdür (a ≠ 0) ve yüzey difüzlüğü tek-parçacık enerji düzeylerini değiştirir. Nilsson modelinin Woods-Saxon potansiyeline dayalı versiyonu, tek-parçacık düzeylerini daha doğru verir.

---

## 9. Nilsson Tek-Parçacık Enerjileri (F-017)

```
H_Nilsson = ℏω₀[-∇² + r²] - 2κ(l·s) - κμl²
ω₀ = 41/A^(1/3) MeV, κ = 0.05, μ = 0.60
```

**Neden MM tahmini için zorunlu?**
Manyetik moment hesabı için hangi yörüngede (l, j) olduğunu bilmek şarttır. Nilsson modeli, deformasyon ve spin-yörünge etkileşimini birlikte ele alarak tek-parçacık durumlarını gerçekçi biçimde hesaplar. Bu enerji değerleri, modelin hangi kuantum durumunun aktif olduğunu "tahmin" etmesine yardım eder.

---

## 10. Çiftlenme Açığı ve Kolektif Özellikler

### 10.1 Çiftlenme Açığı Δ

```
Δ(Z,N) = (1/2)[BE(Z,N+1) + BE(Z,N-1) - 2·BE(Z,N)]
```

**Neden önemli?**
Çiftlenme efekti, çift-çift çekirdeklerde μ=0 olmasını sağlar (çift protonlar/nötronlar spin sıfırı çiftler oluşturur). Bu çiftlenme açığı özelliği, modelin tek-nükleon çekirdeklerini çift-nükleon çekirdeklerinden ayırt etmesine yardımcı olur.

### 10.2 B(E2) Geçiş Olasılığı (Weisskopf birimi)

```
B(E2; 0→2) [W.u.] = (5/16π) · (e·Q₀)² / (Weisskopf_normalization)
```

B(E2), kolektif kuadrupol hareketi ölçer ve β₂ ile doğrudan bağlantılıdır. Bu değer, QM tahmini için dolaylı doğrulama özelliği sağlar.

---

## Özellik Grupları Özeti

| Grup | Özellikler | Hedef | Gerekçe |
|------|------------|-------|---------|
| Ham | Z, N, A | Her ikisi | Temel tanımlayıcılar |
| SEMF | BE, 5 terim, δ, BE/A | Her ikisi | Kütle ölçeği ve asimetri |
| Yarıçap | R | QM öncelikli | Q-β₂ bağıntısı |
| Ayrılma | S_n, S_p | Her ikisi | Son nükleon gevşekliği |
| Kabuk | magic_character, Z/N_magic_dist | Her ikisi | Ani değişim tespiti |
| Deformasyon | β₂, Q₀ | QM öncelikli | Doğrudan QM bağıntısı |
| Schmidt | μ_Schmidt, Q_Schmidt | Her ikisi | Teorik referans |
| WS | V_WS | MM öncelikli | Orbital enerji ölçeği |
| Nilsson | ε_nilsson | MM öncelikli | Tek-parçacık durumu |
| Çiftlenme | Δ, eslenme_acigi | Her ikisi | Çift-teklik farkı |
| Kolektif | B(E2) WU | QM öncelikli | Kolektif hareket ölçeği |

---

*Araştırma notu — 2026-05-03*
*Bu notlar PFAZ 01 Bölüm 7 (Formüller) ve Bölüm 10 (Uygulama) yazımında kullanılacak*

---

## Sprint 4-13 Güncellemeleri (2026-05-11 → 2026-05-14)

### Woods-Saxon Aktif (Sprint 4 BUG-02/03)

**Önemli güncelleme:** Bu dokümanın §8 (Woods-Saxon) bölümünde "WS henüz çalışmıyor" notu artık geçersiz. Sprint 4'te BUG-02 (HBAR_C eksik) ve BUG-03 (V_so/r_so/a_so eksik) düzeltildi:

- `core_modules/constants.py:44` — `HBAR_C = 197.3269804` eklendi
- `core_modules/constants.py:72-74` — `WOODS_SAXON_PARAMS` literatür değerleri: `V_so=6.0` (literatür baz alındı; eski belge "V_so=7.5" hatalı), `r_so=1.25`, `a_so=0.67`
- TRUBA yeniden çalıştırma ile WS özellikleri (V_ws_center, V_ws_so, epsilon_WS) gerçek değer alacak

§8 metnine "Sprint 4 sonrası WS aktif" notu eklenmeli. Özet tabloda WS satırı **aktif (post-BUG-02)** olarak işaretlendi.

### Sprint 13 PFAZ12 BandAnalyzer ile Empirik Doğrulama

Sprint 11+12 BUG-80 ile aktif edilen BandAnalyzer artık her fizik özelliğinin **kabuk kapanması bölgelerindeki dağılımını** ölçüyor:

- Magic group (Z veya N sihirli ±3): MM/QM dağılımı ayrı raporlanır
- Non-magic group: kontrol grubu
- KS test p-value ile ayrı dağılımlar mı sorusu yanıtlanır

Bu çıktı `outputs/advanced_analytics/band_analysis/` altında. Tezde "Bölüm 4: Bulgular" için bu veriler **fizik özelliklerinin gerekliliğini empirik olarak kanıtlar** (S-002 sorusunun yanıtı).

### Nilsson Hâlâ Kapalı (2026-05-08 Karar)

Nilsson modeli %34 NaN üretiyor (deforme çekirdek olmayan küresel çekirdekler için), küçük dataset'lerde orantısız veri kaybı. Karar `tez-yazim-not-defteri.md` 2026-05-08 günlüğünde:

> "Nilsson özellikleri mevcut pipeline'da KAPALI tutulur. Nilsson sadece yüksek deformasyon bölgesi analizleri için (ileride ayrı çalışma) aktif edilebilir."

Bu, §9 (Nilsson) bölümünün geçerliliğini değiştirmez; yalnızca **uygulama kapsamı dışı** notu eklenmeli.

---

*Sprint 4-13 güncelleme: 2026-05-14*
