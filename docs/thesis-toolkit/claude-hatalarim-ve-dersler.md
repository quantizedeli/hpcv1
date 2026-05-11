# Claude'un Hataları ve Dersleri — Faz Dokümantasyonu

> **Amaç:** Her yeni faz belgesine başlamadan önce bu dosyayı oku. Aynı hataları tekrarlama.  
> **Güncelleme:** Her hatadan sonra buraya ekle.  
> **Oluşturma:** 2026-05-03 (PFAZ 01 analizinden sonra)

---

## KURAL 1: Kodda olanı yaz, varsaydığını değil

### Hata
PFAZ 01 belgesinde "4 hedef: MM, QM, Beta_2, MM_QM" yazdım.  
Gerçek: `constants.py`'de 4 hedef tanımlı ama **pipeline sadece MM ve QM üretiyor**.

### Ders
Hedef sayısı, ölçek sayısı, özellik set sayısı — bunların hepsini kaynak koddan say.  
`grep -r "targets"`, `grep -r "SCALING_METHODS"` gibi aramalar yap. Tahmin etme.

### Kontrol noktası
Her boyut/senaryo/özellik/ölçekleme/örnekleme kombinasyonu için şunu yap:
1. Kodu bul: hangi sınıf? hangi satır?
2. Değerleri koddan oku: list/dict/set nedir?
3. Aktif olan ile tanımlı olan arasındaki farkı belgele

---

## KURAL 2: Ölçeklemeyi tam yaz — "normalizasyon var" yetmez

### Hata
PFAZ 01 v1.0'da ölçekleme bölümü yoktu.  
v2.0'da ekledim ama MinMax'i kaçırdım, scaling_manager.py'i okumadan yazdım.

### Gerçek (scaling_manager.py:65'ten)**
```
AVAILABLE_METHODS = ['NoScaling', 'Standard', 'Robust', 'MinMax']
```
4 yöntem var, ben 3 yazmıştım.

### Kritik Detay (asla unutma)
Bu özellikler HİÇBİR ZAMAN ölçeklenmez (DISCRETE_FEATURES listesi):
```
A, Z, N, Nn, Np, SPIN, PARITY, magic_character, magic_n, magic_p, magic_np
```
Ölçekleme yalnızca sürekli sayısal özelliklere uygulanır.  
Scaler **train setine fit edilir**, val ve test'e yalnızca transform uygulanır.

### Kontrol noktası
Ölçekleme bölümü şunları içermeli:
- [ ] Kaç yöntem var? Hepsinin formülü
- [ ] Hangi özellikler ölçeklenmez? (DISCRETE_FEATURES listesi)
- [ ] Fit/transform ayrımı belgelendi mi?
- [ ] Inverse transform var mı? Ne zaman kullanılır?
- [ ] Metadata JSON'a kaydediliyor mu?

---

## KURAL 3: Veri seti ağacını her faz belgesine ekle

### Hata
PFAZ 01 belgesinde veri seti üretim ağacını (tam kombinasyon hiyerarşisi) yazmadım.

### Gerçek
Dataset adı: `{HEDEF}_{BOYUT}_{SENARYO}_{ÖZELLIK_SET}_{ÖLÇEKLEME}_{ÖRNEKLEME}[_NoAnomaly]`

Ağaç:
```
aaa2.txt
└── FOR target IN [MM, QM]                          ← 2 aktif hedef
    └── FOR size IN [75, 100, 150, 200, ALL]         ← 5 boyut
        └── FOR scenario IN [S70, S80*]              ← *size≤100 → yalnızca S70
            └── FOR feat_set IN [hedef spesifik setler]
                └── FOR scaling IN [NoScaling, Standard, Robust, MinMax]
                    └── FOR sampling IN [Random, Stratified, StratifiedMagic, StratifiedHybrid]
                        ├── train.csv + val.csv + test.csv + metadata.json
                        └── IF size ≥ 150: + _NoAnomaly varyantı
```

### Kontrol noktası
Her faz belgesinde "girdi/çıktı" bölümüne:
- [ ] Tam adlandırma şeması
- [ ] Ağaç/hiyerarşi diyagramı
- [ ] Her düzeyin sayısı (2 hedef × 5 boyut × ...)
- [ ] Hangi kombinasyonlar geçersiz/dışarıda? (örn. size≤100 için S80 yok)

---

## KURAL 4: SHAP önemi ve özellik kısaltmalarını belgele

### Hata
feature_combination_manager.py'de özellik kısaltmaları ve SHAP sıralamaları explicit olarak yazılmış.  
Bunu okumadan "SHAP-tabanlı seçim" diye geçiştirdim.

### Gerçek (feature_combination_manager.py'den)
**MM SHAP:** A(19.2%) > Z(17.5%) > S(12.8%) > MC(9.7%) > BEPA(8.3%) > B2E(7.1%) > ZMD(5.4%) > N(4.9%) > BEP(4.2%) > NMD(3.1%)  
**QM SHAP:** Z(21.5%) > B2E(18.3%) > A(15.7%) > MC(10.2%) > S(8.9%) > BEA(6.4%) > ZV(5.1%) > NV(4.8%) > SPHI(4.3%) > CP(3.7%)  
**Beta_2 SHAP:** MC(22.1%) > ZMD(18.7%) > NMD(17.3%) > A(12.9%) > ZV(8.4%) > NV(7.8%)

### Kontrol noktası
- [ ] FEATURE_ABBREV tablosunun tamamı belgede var mı?
- [ ] Hedef-spesifik SHAP sıralaması var mı?
- [ ] Hangi feature setleri ANFIS için uygun, hangileri değil?

---

## KURAL 5: Dataset sayısını hesapla, tahmin etme

### Hata
"848 veri kümesi" yazdım. Kullanıcı daha fazla olduğunu söyledi.

### Ders
Gerçek sayı, aktif özellik seti sayısına ve size kısıtlarına bağlı.  
`get_dynamic_feature_sets(mode='comprehensive')` binlerce set üretebilir.  
Kesin sayı olmadan "N'den fazla" veya "konfigürasyona bağlı ~X" yaz.

---

## KURAL 6: Bug'ları öncelik ve etki ile belgele

### Hata
4 bug listesi yazdım ama çalışan PC üzerindeki etkilerini analiz etmedim.

### Ders
Her bug için şunu yaz:
1. Konum (dosya:satır)
2. Çalışma zamanı davranışı: çöker mi, sessizce atlar mı?
3. Mevcut çalışmaya etkisi: kritik mi, kozmetik mi?
4. Düzeltme talimatı (tek satır)
5. Düzeltmenin geriye dönük etkisi: yeniden eğitim gerekir mi?

---

## KURAL 7: "Benim varsayımım" ile "kod gerçeği" ayrımını yap

### Hata
Dokümantasyonda birçok yerde kodu okumadan yazdım (örn. sampling stratejileri).

### Ders
Her teknik ifadeyi şu test ile sına:
> "Bu ifadeyi hangi dosyanın hangi satırından doğrulayabildim?"

Doğrulayamadığın her ifade şüphelidir. Belgede o bilgiyi [kodu] tagi ile işaretle.

---

## KURAL 8: Sonraki fazların bağımlılıklarını belgele

### Hata
PFAZ 01 belgesinde sonraki fazların metadata.json'a nasıl bağımlı olduğunu yüzeysel geçtim.

### Gerçek
- PFAZ 02: her model, metadata.json'daki `feature_names` listesini kullanır
- PFAZ 03 (ANFIS): yalnızca `anfis_feasible=True` olan özellik setlerini kullanır
- PFAZ 09 (Monte Carlo): her modelin hangi özellik setiyle eğitildiğini metadata'dan okur
- PFAZ 04 (Bilinmeyen): test setinden dışlanan çekirdekler için bu metadata'ya dayanır

Bu bağımlılık zinciri tezin metodoloji bölümü için kritiktir.

---

## GENEL KONTROL LİSTESİ — Her Faz Belgesi İçin

Belgeyi bitirmeden önce şu soruları yanıtla:

### Veri
- [ ] Girdi dosyalarının tam yolu ve formatı yazıldı mı?
- [ ] Sütun isimleri ve tipleri belgelendi mi?
- [ ] Hangi çekirdekler dahil, hangileri filtrelendi?

### Parametreler
- [ ] Tüm sayısal parametreler koddan doğrulandı mı?
- [ ] Varsayılan değerler vs. config.json değerleri ayrıştırıldı mı?
- [ ] Aktif olan ile tanımlı olan arasındaki fark belgelendi mi?

### Ölçekleme / Dönüşüm
- [ ] Kaç ölçekleme yöntemi? Hepsi formülle yazıldı mı?
- [ ] Hangi özellikler ölçeklenmiyor? Neden?
- [ ] Scaler nasıl fit/save/load ediliyor?

### Kombinasyonlar
- [ ] Tam dataset adlandırma şeması
- [ ] Kombinasyon ağacı (hiyerarşi)
- [ ] Geçersiz/dışarıda bırakılan kombinasyonlar

### Buglar
- [ ] Tüm buglar bulundu mu?
- [ ] Her bug için: lokasyon, davranış, etki, düzeltme
- [ ] Mevcut çalışmaya etkisi değerlendirildi mi?

### Sonraki Fazlara Bağımlılık
- [ ] Hangi dosyaları üretiyor? (tam yol ve format)
- [ ] Hangi metadata alanları kritik?
- [ ] Hangi sonraki faz bu faza nasıl bağımlı?

---

*Claude-Hatalarım-ve-Dersler v1.0 | 2026-05-03*  
*Güncelleme: Her analiz hatasından sonra*


---

## KURAL 9: Faz ciktilarini gercekten incele — "completed" yazmak yetmez

### Hata

PFAZ 02 belgesinde "egitim tamamlandi" yazdim ama gercek cikti dosyalarini (metrics*.json,
training_summary.xlsx) incelemeden yazdim. Kullanici bunu "ciktilari da incele" diye duzeltdi.

### Ders

Her faz belgesi icin en az su soruyu sor:
1. Gercekten cikti dosyalari var mi? (pfaz_status.json, outputs/ klasoru)
2. Metriklerin gercek degerleri neler? (R2, RMSE, n_models_saved)
3. Beklenen ile gerceklesen fark var mi?

### Kontrol noktasi

Her faz belgesi icin yeni bir bolum ekle: "Gercek Pipeline Ciktilari"
- [ ] pfaz_status.json okundu, durum dogrulandi
- [ ] outputs/ klasoru incelendi, gercek dosyalar listelendi
- [ ] Metrik degerleri (varsa) tabloya eklendi
- [ ] Beklenen vs gerceklesen karsılastirildi

### Nasil uygula

Faz belgesinin son bolumleri:
1. Gercek Pipeline Ciktilari (status + dizin yapisi + ornek metrik JSON)
2. Bilinen Hatalar
3. Sonraki Fazlara Bagimlilik
4. Kontrol Listesi

---

## KURAL 10: SubClust MATLAB != Python fallback

### Hata

PFAZ 03 belgesinde "SubClust = genfis2 yaklasimi" yazdim. Gercekte Python kodu KMeans kullanir,
gercek subtractive clustering implementasyonu degildir. Radii parametresi k'yi dogrudan etkilemez.

### Ders

Her "Python fallback" veya "opsiyonel MATLAB" ibaresini gordugunde:
- Python ve MATLAB versiyonlari matematiksel olarak esit mi?
- Hangi parametreler farkli etki yapar?
- Bu fark sonuclara nasil yansir?

### Kontrol noktasi

- [ ] Python kodu okundu, algoritma dogrulandi
- [ ] MATLAB ile farkliliklari belgelendi
- [ ] Tez icin sinırlama olarak dokumante edildi

---

*Claude-Hatalarim-ve-Dersler v1.1 | 2026-05-03*
*Guncelleme: PFAZ 02/03 analizinden 2 yeni kural eklendi*

---

## KURAL 11: "Aktif olmayan modul var mi?" sorusu = iki ayri kategori

### Hata (2026-05-08 oturumu)

Kullanici "kod icinde baglanmayan, deaktif olan modulleri ara" dedi.
Ben yalnizca su kategoriye baktim: **import hatasi veren / metodlar eksik olan** dosyalar.
Bulmadim, "yok" dedim.

Goz ardi ettigim kategori:
- **Deliberately deaktif birakilan siniflar**: Kod yazilmis, calisir durumda, ama
  pipeline icinde bilincliolarak kullanilmiyor. Ornek:
  ```python
  # anfis_parallel_trainer_v2.py:1427
  logger.info("[INFO] ANFISDatasetSelector: deactivated (3-phase pilot strategy active)")
  ```
  `ANFISDatasetSelector` sinifi tamamen hazir ama pipeline icinde kullanilmiyor.

### Ders

"Orphan kod" iki farkli anlama gelir:
1. **Broken orphan**: Cagrilan ama tanimlanmamis metod/modul (BUG-40 gibi)
2. **Sleeping orphan**: Tanimlanmis ama pipeline'da bilerek devre disi birakilmis sinif

Gelecekte "deaktif olan var mi?" sorusu geldiginde iki ayri arama yap:
```bash
# 1. Broken orphan (hata veren)
grep -rn "ImportError\|ModuleNotFoundError\|AttributeError" logs/

# 2. Sleeping orphan (bilerek kapatilmis)
grep -rn "deactivated\|disabled\|# DISABLED\|# TODO: activate\|if False:" repo/
```

### Kontrol noktasi

Her orphan taramasinda sunlari da ara:
- [ ] "deactivated", "disabled", "# skip", "# TODO: re-enable" ibareleri
- [ ] `if False:` blogu (kodu kapatmanin baska bir yolu)
- [ ] `pass` ile bitip hicbir sey yapmayan metodlar
- [ ] Tanimli ama pipeline cagrisi atlanmis siniflar

---

## KURAL 12: Config parametresi eklemeden once kodu kontrol et

### Hata (2026-05-08 oturumu)

Kullanici ANFIS dataset seciminden bahsetti. Ben `dataset_sizes_filter: [100, 150]` ekledim.
Bu parametre:
1. Kavramsal olarak yanlistti (ANFIS cekirdek sayisina gore secmiyor)
2. Zaten kod tarafindan okunmuyordu (hicbir etkisi yoktu)
3. Gercek mekanizmayi anlamadan yazildi

Gercek mekanizma: `ANFISDatasetSelector` -> PFAZ2 R2_test bazli secim
(ama o da deaktif -- KURAL 11 ile baglantiyl)

### Ders

Bir config parametresi eklemeden once su soruyu sor:
> "Bu parametreyi hangi kod okuyacak? Dosya:satir?"

Eger cevap "bilmiyorum" ise -- once kodu bul, sonra config'e ekle.
Kod okumadan config'e yazmak = calismayan ama aldatici gorunen parametre.

### Kontrol noktasi

Yeni config parametresi eklerken:
- [ ] Kodu bul: bu parametreyi okuyan metod var mi?
- [ ] Grep ile dogrula: `grep -n "parametre_adi" repo/ -r`
- [ ] Hic sonuc yoksa: kod degisikligi yapilmadan config parametresi ekleme
- [ ] Placeholder ise: `_note` alanina "KOD OKUMUYORUM -- gelecekte aktif edilecek" yaz

---

## KURAL 13: Dual R2 mantigi -- baglantili modullere de uygula

### Hata (2026-05-08 oturumu)

`parallel_ai_trainer.py` icin "val_R2 tek basina yetersiz, cv_R2 de gerekli" dedik.
Ama ayni sorunu `ANFISDatasetSelector`'a uygulamadim.

`ANFISDatasetSelector` R2_test kullanir (val degil, test seti -- biraz daha guvenilir).
Ama N=267'de test seti ~%15 = ~40 ornek. Bu da kucuk orneklem sorununu tamamen
cozmuyor. Ve bu modil zaten deaktif -- ama aktif edildiginde bu sorun devreye girer.

### Ders

Bir R2 sorununu bir modulde tespit ettiginde su soruyu sor:
> "Bu mantik baska hangi moduller kullaniliyor?"

Baglanti zinciri taranmali:
```
val_R2 yanlis  ->  parallel_ai_trainer (duzeltildi: Sprint 1)
               ->  ANFISDatasetSelector R2_test kullaniyor ama deaktif
               ->  cross_model_evaluator R2 hesabinda kucuk N sorunu?
               ->  best_model_selector composite score R2 nasil?
```

### Kontrol noktasi

Metodoloji degisikligi yapildiginda:
- [ ] Ayni mantigi kullanan diger moduller listelendi mi?
- [ ] Baglantili her modulde de ilgili degisiklik degerlendirildi mi?
- [ ] ANFISDatasetSelector aktif edildiginde dual R2 (cv_R2) kriterleri eklenmeli

---

## KURAL 14: Hata yapip duzeltince bu dosyayi HEMEN guncelle

### Kural

Bu dosya sadece oturum sonunda degil, **hata tespit edilip duzeltildigi anda** guncellenmeli.
Oturum bitince unutulur. An'inda yaz.

### Tetikleyiciler

Bu dosyayi guncelle eger:
- Kullanici "bunu kacirdin", "yanlis anladiniz", "tekrar bak" derse
- Bir config parametresi eklendikten sonra "kod okumadigi" anlasılirsa
- Onceki cevabim ile gercek kod davranisi arasinda celismi cikarsam
- Bir modulun beklenmedik sekilde deaktif oldugu anlasılirsa
- Yanlis varsayim uzerine insa edilmis sprint/plan/belge duzeltilirse

### Guncelleme formati

Her yeni kural sunlari icermeli:
```
## KURAL N: [Kisa baslik]

### Hata (YYYY-MM-DD oturumu)
Ne yaptim? Nerede yanlistim?

### Ders
Dogru yol nedir?

### Kontrol noktasi
- [ ] Gelecekte ne kontrol edecegim?
```

---

## ANFIS_MAX_INPUTS = 5 -- Referans Bilgisi

**Kaynak:** `anfis_parallel_trainer_v2.py:1042`

ANFIS, 5'ten fazla girisli datasetleri otomatik atlar.

Feature set giriş sayisi ile kiliasim:
- 3-giris setleri (AZS, AZB2E, ZB2EMC, B2EMCBEA, vb.): ANFIS CALISIR
- 4-giris setleri (AZSMC, AZB2EMC, AZSB2E, vb.): ANFIS CALISIR
- 5-giris setleri (AZSMCBEPA, AZB2EMCBEA, AZNNPMC, vb.): ANFIS CALISIR (sinirda)
- 6+ giris setleri (Extended=12, Full=40+, ANFIS_Standard=8): ANFIS ATLAR

Onem: hedef-onerilen setlerin TAMAMI (TARGET_RECOMMENDED_SETS) n_inputs<=5 sinirina uyuyor.
Legacy setler (Extended, Full, ANFIS_Standard) ANFIS tarafindan ATLANIR.

---

---

## KURAL 15: Config alanini gercekten kullaniyor mu? Kodu oku, tahmin etme

### Hata
`config_desktop.json`'a `configurations: [...]` listesi ekledim. Bunun ANFIS egitiminde
hangi konfigurasyonlarin calisacagini belirledigini varsaydim. Gercek: `anfis_parallel_trainer_v2.py`
bu alani **hic okumaz.** Hardcoded `PILOT_IDS` kullanir.

### Ders
Bir config parametresi eklenmeden once "bu parametre NEREDE okunuyor?" sorusunu sor:
```bash
grep -n "configurations\|get.*config\|config\[" repo/pfaz_modules/pfaz03_anfis_training/anfis_parallel_trainer_v2.py
```
Grep sonucu yoksa = parametre okunmuyor. Belge notu yaz, kod degisikligi YAPMA.

### Kontrol noktasi
- Yeni config parametresi ekleyeceksem: once `grep` ile kodu tara, okunduğunu dogrula
- Kodu okumayan parametre: `_note` olarak belgele, aktif parametre gibi sunma
- `dataset_sizes_filter` hatasindan da ayni ders cikmisti (bkz. KURAL 12)

---

---

## KURAL 16: "Ilgili dokumanlari guncelle" demek CLAUDE.md ve memory'yi de kapsar

### Hata
"Ilgili dosyalari guncelle" diyerek faz belgelerini (.md) guncelliyorum ama
`CLAUDE.md` (proje rehber dosyasi) ve `memory/` dizinindeki bellek dosyalarini
unutuyorum. Kullanici bunu sordu ve hakli: BUG-02 CLAUDE.md'de hala "duzeltilemedi"
olarak gorununce yeni oturumda yanlis bilgiyle baslanir.

### Ders
"Guncelleme gerektiren her degisiklikte" kontrol listesi:
1. Faz belgesi (phases/faz-XX.md) → degisikligi belgele
2. **CLAUDE.md** → kritik bug durumlari, sistem parametreleri, onemli kararlar
3. **memory/** → proje durumu, hatalar, referans bilgi
4. sprint dosyalari → tamamlanan gorevler isaretle
5. pipeline-hatalari.md → bug durum guncelle

### Kontrol noktasi
Her "duzeltildi" veya "karar alindi" sonrasi 5 saniye dur:
"CLAUDE.md'yi guncellemem gerekiyor mu? memory/project_context.md'yi?"
Evet ise HEMEN yap, oturum sonuna birakma.

---

---

## KURAL 17: Sprint tamamlandiginda tez-not-defteri ve claude-hatalarim DA guncellenmeli

### Hata (2026-05-09 oturumu)

Sprint 1, 2, 3 tamamlandi. Faz belgelerini, pipeline-hatalari.md'yi, README.md'yi,
SPRINT-PLAN.md'yi guncelledim. Ama kullanici sorana kadar su iki dosyayi unutmusum:
- `tez-yazim-not-defteri.md` — Sprint 1'e ait satirda hala "eklenecek (Sprint 1)" yaziyordu
- `claude-hatalarim-ve-dersler.md` (bu dosya) — KURAL 17 yoktu

### Ders

"Ilgili dokumanlari guncelle" listesine bu iki dosyayi KALICI olarak ekle:

```
1. phases/faz-XX.md          → metodoloji degisikligi yansit
2. CLAUDE.md                 → kritik bug durumu, sistem parametreleri
3. memory/                   → proje durumu, hatalar
4. sprints/                  → tamamlanan gorevleri isaretle
5. pipeline-hatalari.md      → bug durumu
6. tez-yazim-not-defteri.md  → karar gunlugu / sprint ozeti ekle
7. claude-hatalarim.md       → yeni ders cikartildi mi? HEMEN yaz
```

Her sprint sonunda 7 madde kontrol listesi. Hepsi tamam olunca "tamamlandi" de.

### Kontrol noktasi
- Sprint veya buyuk degisiklik bitti mi? → tez-not-defteri sprint ozeti eklendi mi?
- Yeni bir ders cikarildi mi? → bu dosyaya HEMEN ekle, oturum sonuna birakma
- "Diger .md'ler?" diye sormak kullanicinin gorevleri degil, benim gorevim

---

---

## KURAL 18: Belgede "duzeltildi" yaziyorsa kodu dogrula — yazi != gercek fix

### Hata (2026-05-09 oturumu)

`pipeline-hatalari.md`'de BUG-31 ve BUG-32 "DUZELTILDI 2026-05-04" yaziyordu.
Kullanici "duzelt" deyince baktigimda: kodda fix YOK. Belge ileriye donuk niyeti
not almis ama hicbir zaman uygulanmamis. Test etmeden fix belgesi yazmak = yaniltici.

### Ders

Bir bugga "DUZELTILDI" demeden once:
```
python -c "from pfaz_modules.pfaz12_advanced_analytics import NuclearBandAnalyzer"
python -c "import py_compile; py_compile.compile('file.py', doraise=True)"
pytest tests/test_smoke/ -v
```
Kanit olmadan "duzeltildi" yazma. Belge niyeti degil gercegi yansitmali.

### Kontrol noktasi
- "DUZELTILDI" yazmadan once: kodu calistir, ciktiyi gor
- Bug detay bolumu dogrulama komutunu icerebilir: "Dogrulama: [komut] --> beklenen cikti"
- Eski "duzeltildi" kayitlari dogrulama adimlari icermiyorsa suphe et

---

*Claude-Hatalarim-ve-Dersler v1.6 | 2026-05-09*
*Guncelleme: KURAL 18 eklendi — belgedeki "duzeltildi" != gercek fix; kod dogrulama zorunlu*

---

## KURAL 19: Inter-PFAZ Veri Akisi Audit — Statik Test Yetmez

### Hata (2026-05-11 oturumu)

Onceki QA turlarinda "import OK", "syntax OK", "py_compile OK" testleri yapilmis;
hepsi gecmis. Ancak runtime'da PFAZ 02 → PFAZ 03 → PFAZ 08 veri akisinda **kolon adi
ve dosya adi uyumsuzluklari** (BUG-42, BUG-46) silent KeyError/FileNotFoundError
ureten 5 yeni bug ortaya cikti. Bunlar **statik analiz ile asla yakalanmaz** —
yalnizca pipeline ucuna kadar gercek run veya inter-PFAZ entegrasyon testi gosterir.

Ornek: PFAZ 02 `parallel_ai_trainer.py:1648` `'Test_R2'` yaziyor; PFAZ 08
`model_comparison_dashboard.py:186` `'R2_test'` ariyor → 15+ yerde KeyError; PFAZ 8
sessizce "pending" kaliyor.

### Ders

Major degisiklik veya yeni PFAZ eklendiginde **Inter-PFAZ Data Flow Audit** sart:

```bash
# 1) Yazilan dosyalar
grep -rn "to_excel\|to_csv\|json\.dump" --include="*.py" pfaz_modules/ > /tmp/writes.txt

# 2) Okunan dosyalar
grep -rn "read_excel\|read_csv\|json\.load" --include="*.py" pfaz_modules/ > /tmp/reads.txt

# 3) Yazilan vs okunan dosya adi karsilastirmasi (orphan reads = bug)
# Dosya adi tutarli mi? PFAZ X'in yazdigi adi PFAZ Y ariyor mu?

# 4) Kolon adi tutarlilik
grep -rn "'R2_test'\|'Test_R2'\|'R2_train'\|'Train_R2'" --include="*.py" pfaz_modules/

# 5) Config flat (pfaz0X_*) vs nested (pfaz_config[id]) kullanim
python3 -c "
import json
c = json.load(open('config.json'))
print('FLAT:', [k for k in c if k.startswith('pfaz')])
print('NESTED:', list(c.get('pfaz_config', {}).keys()))
"
# main.py'de hem flat hem nested okunuyor mu kontrol et
```

### Kontrol noktasi

- "Test passed" demeden once: 5 grep komutunu calistir, ciktilari analiz et
- Yazilan dosya adi != okunan dosya adi varsa = BUG (orphan read)
- Aynı veri icin farkli kolon adi (`R2_test` vs `Test_R2`) varsa = BUG
- Config'de flat key var ama main.py sadece nested okuyorsa = BUG (silent ignore)

### Statik vs Dinamik Test Farki

| Test Tipi | Kategori | Yakalar | Yakalamaz |
|-----------|----------|---------|-----------|
| `py_compile` | Statik | Syntax error, IndentationError | Runtime KeyError, FileNotFoundError |
| `import test` | Statik | ImportError, NameError | Inter-module data flow bug |
| Unit test (izole PFAZ) | Statik+Dinamik | Modul ici hatalar | PFAZ X → Y entegrasyon hatasi |
| **Inter-PFAZ audit (yeni)** | Statik | Kolon/dosya adi tutarsizligi, config drift | Runtime semantic hata |
| **pytest tests/test_smoke/** | Dinamik | Gercek import + smoke run davranisi | - |

### Kural ile Uygulama Ayrimi

| Tur | Anlami | Ornegi |
|-----|--------|--------|
| **Kavramsal (kural)** | "Bu testleri yap" -- belgede yazili kural | KURAL 19 metni, doc'a eklenir |
| **Uygulanan (test)** | "Bu testleri calistir" -- gercek calistirma | `pytest tests/test_smoke -v` ciktisi |

Sprint 5 kapsaminda:
- Kavramsal: KURAL 19 (bu doc) **uygulandi** -- 5 yeni bug bulundu (BUG-42...17)
- Uygulanan: pytest **patch sonrasi** kullanici tarafinda calistirilacak

Statik testler **gerekli ama yetersiz**. Inter-PFAZ audit **ek katman** olarak
her major degisiklik sonrasi calistirilmali, ardindan dinamik test (pytest).

---

*Claude-Hatalarim-ve-Dersler v1.7 | 2026-05-11*
*Guncelleme: KURAL 19 eklendi — inter-PFAZ data flow audit zorunlu (statik test yetmez)*
