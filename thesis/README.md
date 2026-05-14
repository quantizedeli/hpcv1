# Thesis — Tez Bölüm Indeksi

> **Bu klasör:** PhD tezinin bölüm bölüm Markdown taslaklarını barındırır.

> **Doluluk:** ⏳ Tüm fazlar (`phases/`) tamamlanınca bu klasör doldurulur.

> **Final çıktı:** Markdown → Pandoc → tez.pdf

---

## Tez Bölüm Listesi

| # | Bölüm Başlığı | Dosya | Durum | Hedef Sayfa | Kaynak Fazlar |
|---|---------------|-------|-------|-------------|---------------|
| 0 | İçindekiler | `00-icindekiler.md` | ⏳ | - | (otomatik) |
| 1 | Giriş | `01-giris.md` | ⏳ | 8-12 | Faz 0 + literatür |
| 2 | Kuramsal Çerçeve | `02-kuramsal-cerceve.md` | ⏳ | 15-25 | Manuel + literatür |
| 3 | Yöntem | `03-yontem.md` | ⏳ | 25-40 | Tüm fazlar |
| 4 | Uygulama ve Deneysel Kurulum | `04-uygulama.md` | ⏳ | 8-15 | Faz 7 + repo config |
| 5 | Bulgular | `05-bulgular.md` | ⏳ | 15-25 | Faz çıktıları |
| 6 | Tartışma | `06-tartisma.md` | ⏳ | 8-15 | Cross-faz |
| 7 | Sonuç ve Öneriler | `07-sonuc.md` | ⏳ | 5-8 | Final synthesis |
| 8 | Kaynakça | `08-kaynakca.md` | ⏳ | - | (BibTeX) |
| 9 | Ekler | `09-ekler.md` | ⏳ | - | Repo, hyperparam, ek görsel |

**Durum:**
- ⏳ Beklemede
- 🔄 Devam ediyor
- ✅ Tamamlandı (danışman onayı bekliyor)
- ✔ Onaylandı

---

## Tez Bölüm Sırası ve Mantığı

`../04-THESIS-WRITING-GUIDE.md`'deki yapı şablonunu izler:

```
ÖZET (TR + EN) — En son yazılır
ÖNSÖZ — Tüm tez bittikten sonra
İÇİNDEKİLER — Otomatik (Pandoc)
ŞEKİLLER LİSTESİ — 06-FIGURE-TABLE-CATALOG.md'den
TABLOLAR LİSTESİ — 06-FIGURE-TABLE-CATALOG.md'den
SİMGELER VE KISALTMALAR — 07-GLOSSARY-SYMBOLS.md'den

1. GİRİŞ
2. KURAMSAL ÇERÇEVE
3. YÖNTEM
4. UYGULAMA
5. BULGULAR
6. TARTIŞMA
7. SONUÇ
KAYNAKÇA
EKLER
```

---

## Faz → Tez Bölüm Eşleştirmesi

| Tez Bölümü | Kaynak Faz / Doküman |
|------------|---------------------|
| 1.1 Problem Tanımı | (Manuel — kullanıcı yazar) |
| 1.2 Amaç | `00-MASTER-PROMPT.md` projesi |
| 1.3 Katkılar | `reports/00-FINAL-SYNTHESIS.md` |
| 1.4 Düzen | `phases/README.md` |
| 2. Kuramsal Çerçeve | (Manuel literatür) |
| 3.1 Genel Mimari | `phases/README.md` + Şekil S-001 |
| 3.2-3.N Faz alt bölümleri | `phases/faz-NN-...md` |
| 4.1 Veri Kümesi | İlgili faz dokümanı |
| 4.2 Donanım/Yazılım | repo'daki requirements.txt |
| 4.3 Hiperparametreler | Tablo T-002 |
| 4.4 Metrikler | `04-THESIS-WRITING-GUIDE.md` + Faz son aşama |
| 5. Bulgular | Tüm fazların §14 bölümleri |
| 6. Tartışma | Faz §13 + cross-analiz |
| 7. Sonuç | `reports/00-FINAL-SYNTHESIS.md` |

---

## Yazım Sırası Önerisi

```
1. 03-yontem.md    (faz dokümanlarından otomatik derlenir)
2. 04-uygulama.md  (deneysel kurulum)
3. 05-bulgular.md  (sonuçlar)
4. 06-tartisma.md  (yorumlar)
5. 07-sonuc.md     (özet + gelecek çalışma)
6. 02-kuramsal-cerceve.md  (manuel literatür)
7. 01-giris.md     (Bulgular bilince yazılır)
8. ÖZET (TR + EN)  (tüm tez bittikten sonra)
9. ÖNSÖZ           (en son)
```

**Mantık:** Bilgiyi "ortadan dışarı" yazmak — Yöntem ve Bulgular hâlâ taze, sonra Tartışma yorumla, sonra Giriş "ne sorunu çözdüğümüzü" gerçekten bildiğinde yaz.

---

## Pandoc ile PDF Üretimi

```bash
cd thesis/

pandoc \
  -F pandoc-crossref \
  --citeproc \
  --csl=apa.csl \
  --bibliography=08-kaynakca.bib \
  --pdf-engine=xelatex \
  -V lang=tr \
  -V mainfont="Times New Roman" \
  -V geometry:margin=2.5cm \
  -V linestretch=1.5 \
  -V toc=true \
  -V toc-depth=3 \
  -V numbersections=true \
  -o tez.pdf \
  00-icindekiler.md \
  01-giris.md \
  02-kuramsal-cerceve.md \
  03-yontem.md \
  04-uygulama.md \
  05-bulgular.md \
  06-tartisma.md \
  07-sonuc.md \
  08-kaynakca.md \
  09-ekler.md
```

> **Not:** Üniversitenin tez şablonu varsa (.docx veya .tex), Pandoc çıktısını ona göre dönüştür.

---

## Bölüm Yazma Kılavuzu

Her bölüm yazıldığında:

1. **`../04-THESIS-WRITING-GUIDE.md`'yi yeniden oku**
2. **Atıflar:** APA 7 varsayılan
3. **Formüller:** LaTeX, numaralı, değişkenler tanımlı
4. **Şekil/Tablo:** `../06-FIGURE-TABLE-CATALOG.md` ID ile
5. **Kısaltma:** İlk geçişte tam ad
6. **Sembol:** `../07-GLOSSARY-SYMBOLS.md` ile uyumlu
7. **humanizer:** SADECE final pass, akademik ton koruyarak
8. **Plagiarism check:** Turnitin/iThenticate

---

## Bölüm Tamamlama Kontrol Listesi

- [ ] Tüm formüller LaTeX, numaralı, değişkenleri tanımlı
- [ ] Tüm şekil/tablolar caption'lı, numaralı, metinde referans
- [ ] Atıf formatı tutarlı
- [ ] Kaynakça'da olmayan atıf yok
- [ ] Kısaltma ilk geçişte tam ad
- [ ] Belirsiz ifade yok
- [ ] Spekülatif iddia yok
- [ ] Türkçe yazım denetimi yapıldı
- [ ] Bu README'de bölüm satırı güncellendi

---

## Figures Klasörü (Önerilen)

```
thesis/
├── 00-icindekiler.md
├── 01-giris.md
├── ...
├── figures/
│   ├── S-001-mimari.svg
│   ├── S-002-faz-1-akis.svg
│   ├── S-003-konfuzyon-matris.png
│   └── ...
└── kaynakca.bib
```

`../06-FIGURE-TABLE-CATALOG.md`'deki S-NNN ID'leri ile bu klasördeki dosyalar eşleşmeli.

---

## Sonraki Adım

Henüz hiç tez bölümü yazılmadı. Sırayla:

1. ✅ Faz dokümanları tamamlanmış olmalı (`phases/`)
2. ✅ `06-FIGURE-TABLE-CATALOG.md` dolu olmalı
3. ✅ `07-GLOSSARY-SYMBOLS.md` dolu olmalı
4. ✅ `reports/00-FINAL-SYNTHESIS.md` yazılmış olmalı
5. ⏳ İlk bölüm: `03-yontem.md` (faz dokümanlarından derlenir)

İlk bölüm prompt'u:

```
phases/ klasöründeki tüm faz dokümanlarını oku.
Bunlardan tezimin "3. YÖNTEM" bölümünü Markdown olarak taslakla.

- Dosya: thesis/03-yontem.md
- Yapı: 04-THESIS-WRITING-GUIDE.md'deki şablona göre
- Atıf format: APA 7
- Akademik Türkçe (uygulanmıştır, gerçekleştirilmiştir)
- Formül: LaTeX, numaralı, değişken tanımlı
- Şekil/Tablo: 06-CATALOG'tan ID ile referans
- Kısaltma: İlk geçişte tam ad

Bana göster, onayımı bekle.
Onay sonrası humanizer skill ile son temizlik yap (akademik tonu koruyarak).
```

---

*thesis/README.md v0.1 | Son güncelleme: 2026-05-02*
