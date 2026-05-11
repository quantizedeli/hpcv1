# PFAZ 01 Final Rapor: Veri Kümesi Üretimi — Derin Analiz Özeti

> **Tarih:** 2026-05-03  
> **Sürüm:** v2.0 (Derin Akademik Revizyon sonrası)  
> **Belge:** `phases/faz-01-veri-kumesi-uretimi.md` (35.7 KB, 782 satır)  
> **DOCX:** `phases/faz-01-veri-kumesi-uretimi.docx` (52.2 KB)

---

## Özet

PFAZ 01, `data/aaa2.txt` dosyasındaki 267 çekirdeği alarak yedi fizik modülü üzerinden 44+ özelliğe genişletir ve 848 farklı veri kümesi üretir. Bu faz, tüm sonraki fazların (PFAZ 02-13) veri tabanını kurar.

**Bu revizyonun kapsamı:** İlk versiyon temel mimariyi belgelemiş ama her kararın gerekçesini vermemişti. v2.0 revizyonu beş araştırma dosyası (`research/` dizini) üretilmesi ardından şu soruların tamamını yanıtlar:
- Neden tam olarak bu 44+ özellik?
- Neden S70 ve S80, başka senaryo değil?
- Neden IQR=3.0, standart 1.5 değil?
- Neden bu ML modelleri bu problem için seçildi?
- Ani değişim (shell closure) neden özel özellikler gerektiriyor?

---

## Üretilen Dosyalar

| Dosya | Boyut | İçerik |
|-------|-------|--------|
| `phases/faz-01-veri-kumesi-uretimi.md` | 35.7 KB | 17 bölüm, derin akademik dokümantasyon |
| `phases/faz-01-veri-kumesi-uretimi.docx` | 52.2 KB | DOCX formatı (python-docx ile üretildi) |
| `research/fizik-ozellik-justifikasyonlari.md` | ~12 KB | Her özelliğin fiziksel gerekçesi |
| `research/ml-model-secim-gerekceleri.md` | ~10 KB | 7 modelin bu problem için seçim nedenleri |
| `research/ani-degisim-arastirmasi.md` | ~8 KB | Shell closure discontinuity araştırması |
| `research/istatistik-justifikasyonlari.md` | ~9 KB | S70/S80, IQR, örnekleme gerekçeleri |
| `research/acik-sorular.md` | ~7 KB | Yanıtlanması gereken 10 açık soru |
| `tez-yazim-not-defteri.md` | ~5 KB | Tez yazım sürecinin canlı not defteri |
| `scripts/md_to_docx.py` | ~3 KB | Markdown→DOCX dönüşüm scripti |

---

## Anahtar Bulgular

### Fizik Kararları

**SEMF terimleri ayrı özellik olarak:** Her SEMF terimi ($a_v$, $a_s$, $a_c$, $a_a$, $\delta$) bağımsız özellik olarak eklendi. Bunun nedeni, modelin hangi fiziksel katkının tahmin üzerinde daha belirleyici olduğunu ayrı ayrı öğrenmesine izin vermektir. Toplam BE tek bir özellik olsaydı bu bilgi kaybolurdu.

**Schmidt momentleri:** Model, ham Z/N'den tahmin yerine teorik referans değerinden ne kadar saptığını öğrenir. Bu yaklaşım quenching faktörünü ve kolektif efektleri dolaylı yoldan yakalar.

**Ani değişim özellikleri:** `magic_character`, `Z_magic_dist`, `N_magic_dist` olmadan ML modeli, kabuk kapanmalarındaki süreksizliği öğrenemez. Bu özellikler, eğitim kümesinde az temsil edilen sihirli çekirdekler için sistematik hata kaynağını ortadan kaldırır.

### Veri Tasarım Kararları

| Karar | Tercih | Gerekçe |
|-------|--------|---------|
| Bölme senaryosu | S70 + S80 | Küçük veri kümesi stabilitesi |
| Anomali IQR eşiği | 3.0 | Sihirli çekirdek değerlerini korur |
| IF contamination | 0.08 | ~21 şüpheli kayıt üst sınırı |
| NoAnomaly | Yalnızca 150/200/ALL | Küçük boyutta çok veri kaybı riski |
| DNN min örnek | 80 | Overfit sınırı |

### Tespit Edilen Buglar (Düzeltme Önceliği)

| Öncelik | Bug | Etki |
|---------|-----|------|
| Yüksek | Q=0 filtresi yanlış (`qm_filter_manager.py:153`) | QM modelleri kapalı kabuk çekirdeklerini kaybeder |
| Yüksek | HBAR_C eksik (`woods_saxon.py:15`) | WS potansiyeli hesaplanamıyor |
| Orta | Spin-yörünge params eksik (`woods_saxon.py:73-75`) | KeyError riski |
| Düşük | data_file_mat anahtar hatası (`pipeline_v2.py:1193`) | Raporlamada hata |

### Modül Bağlantı Sorunu

`DataEnricher` sınıfı pipeline'a bağlı değildir. Bu sınıfın işlevi netleştirilmeli ve gerekiyorsa `TheoreticalCalculationsManager`'a entegre edilmelidir.

---

## Tamamlama Kontrol Listesi

- [x] `phases/faz-01-veri-kumesi-uretimi.md` v2.0 yazıldı (17 bölüm, 35.7 KB)
- [x] `phases/faz-01-veri-kumesi-uretimi.docx` üretildi (52.2 KB)
- [x] `research/` dizini oluşturuldu (5 araştırma dosyası)
- [x] `tez-yazim-not-defteri.md` oluşturuldu
- [x] `scripts/md_to_docx.py` oluşturuldu ve test edildi
- [x] Memory sistemi kuruldu (MEMORY.md + 5 bellek dosyası)
- [x] `phases/README.md` — PFAZ 01 durumu ✅ (önceki oturumda güncellendi)
- [ ] `06-FIGURE-TABLE-CATALOG.md` — v2.0'dan yeni eklemeler (mevcut v0.3 güncel sayılır)
- [ ] `07-GLOSSARY-SYMBOLS.md` — ek kısaltmalar kontrolü
- [ ] Bug fix takibi: 4 bug için PFAZ_DEVELOPMENT_NOTES.md'ye ekleme

---

## Sonraki Adım: PFAZ 02 Analizi

PFAZ 02 (`ParallelAITrainer`) analizi için öneri:
- `pfaz_modules/pfaz02_ai_training/` kaynak kodu incelenmeli
- 6 model × 50 konfigürasyon eğitiminin nasıl parallelize edildiği
- 5-fold CV stratejisi ve hyperparameter arama uzayı
- GPU kullanımı ve DNN_MIN_SAMPLES kısıtının PFAZ 02'ye yansıması

---

*PFAZ 01 Final Rapor v2.0 | 2026-05-03*
