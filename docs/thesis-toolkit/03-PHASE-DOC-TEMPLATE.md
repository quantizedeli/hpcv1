# 03 — Phase Documentation Template

> **Bu şablonu HER faz için kopyala** ve `phases/faz-NN-{kebab-case}.md` olarak kaydet.

> **Atla yapma — bilgi yoksa "Açık Sorular" bölümüne yaz.**

> Aşağıdaki başlıklar zorunlu sıraya göre düzenlenmelidir.

---

## Şablon (Aşağıdaki Bloku Kopyala)

```markdown
# Faz NN: [Faz Adı]

> **Faz Numarası:** NN  
> **Kısa Ad:** kebab-case-isim  
> **Repo Yolu:** src/path/to/module/  
> **Ana Dosyalar:** file1.py, file2.py, ...  
> **Analiz Tarihi:** YYYY-MM-DD  
> **Durum:** ⏳ Devam ediyor | ✅ Tamamlandı | ❌ Açık Sorular var

---

## 1. Genel Bakış (Overview)

[Bu fazın ne yaptığını 2-3 cümlede açıkla. Tezin "Yöntem" bölümüne doğrudan
girecek seviyede özet.]

**Kısa Tanım:** ...

**Sınıflandırma:** [Veri Toplama | Önişleme | Özellik Çıkarma | Model Eğitimi | 
Değerlendirme | Görselleştirme | Sonuç Üretimi | ...]

---

## 2. Motivasyon (Niçin Bu Faz Var?)

[Bu faz neden gerekli? Hangi problemi çözüyor? Onsuz ne olur?]

- **Çözdüğü problem:** ...
- **Bu faz olmasaydı:** ...
- **Önceki yaklaşımlardan farkı:** ... (varsa atıfla)

---

## 3. Bağlam (Pipeline'daki Yeri)

### Önceki Fazlar (Bağımlılıklar)

| Faz | Beklenen Çıktı (Bu Faza Girdi Olarak) |
|-----|---------------------------------------|
| Faz N-1 | ... |

### Sonraki Fazlar (Bu Faz Kimi Besliyor?)

| Faz | Aldığı Girdi |
|-----|--------------|
| Faz N+1 | ... |

### Akış Diyagramı

```mermaid
flowchart LR
    A[Faz N-1 çıktısı] --> B[Bu Faz: ...]
    B --> C[Faz N+1 girdisi]
```

---

## 4. Girdi/Çıktı Spec'i

### Girdi (Input)

| Parametre | Tip | Şekil/Boyut | Birim | Açıklama |
|-----------|-----|-------------|-------|----------|
| ... | numpy.ndarray | (N, 1024) | counts | Gama enerji spektrumları |
| ... | dict | - | - | Yapılandırma parametreleri |

**Veri Kaynağı:** [Faz N-1 çıktısı | Disk: data/raw/*.npz | API | ...]

**Format:** [HDF5 | NumPy npz | ROOT | parquet | ...]

### Çıktı (Output)

| Parametre | Tip | Şekil/Boyut | Birim | Açıklama |
|-----------|-----|-------------|-------|----------|
| ... | ... | ... | ... | ... |

**Çıktı Konumu:** [bellek | data/processed/*.npz | model checkpoint | ...]

---

## 5. Yöntem (Nasıl Çalışıyor?)

[Bu fazın iç işleyişini adım adım anlat. Kod yapısını yansıtsın.]

### Adım 5.1: ...

[Açıklama. Hangi fonksiyon/sınıf? Neden bu yaklaşım?]

**Kod referansı:** `src/path/to/file.py:42-67`

### Adım 5.2: ...

[...]

### Adım 5.N: ...

[...]

---

## 6. Algoritmalar (Pseudocode)

> Faz'da kullanılan algoritmalar burada. Her birine A-NNN ID ata ve
> `06-FIGURE-TABLE-CATALOG.md`'ye kaydet.

### A-NNN: [Algoritma Adı]

**Kaynak:** [Yazar et al. (Yıl), kitap, paper, repo / "Bu çalışma"]

**Pseudocode:**

```
Input: ...
Output: ...

1. ...
2. ...
3. ...
```

**Karmaşıklık:** O(...)

**Kod karşılığı:** `src/path/to/file.py:LINE`

---

## 7. Formüller

> Her formüle F-NNN ID ata ve `06-FIGURE-TABLE-CATALOG.md`'ye kaydet.
> LaTeX zorunlu.

### F-NNN: [Formül Adı]

$$
y = f(x; \theta)
$$

Burada:
- $y$: ... (birim)
- $x$: ... (birim)
- $\theta$: ... (parametre)
- $f$: ... (fonksiyon)

**Kaynak:** [atıf]

**Kod karşılığı:** `src/path/to/file.py:LINE`

**Bağlam:** [Bu formül nerede ne için kullanılıyor?]

---

## 8. Değişkenler & Parametreler

### 8.1 Hesaplama Değişkenleri (Variables)

| Sembol | Ad | Tip | Birim | Aralık | Açıklama |
|--------|-----|-----|-------|--------|----------|
| $x$ | ... | float[] | counts | [0, 65535] | ... |
| ... | ... | ... | ... | ... | ... |

### 8.2 Hiperparametreler (Hyperparameters)

| Parametre | Varsayılan | Aralık | Birim | Açıklama | Kod |
|-----------|------------|--------|-------|----------|-----|
| `learning_rate` | 0.001 | [1e-5, 1e-1] | - | Adam optimizer LR | `train.py:23` |
| ... | ... | ... | ... | ... | ... |

### 8.3 Konfigürasyon (Config)

| Anahtar | Değer | Kaynak | Açıklama |
|---------|-------|--------|----------|
| `batch_size` | 32 | config.yaml | DataLoader batch boyutu |
| ... | ... | ... | ... |

---

## 9. Kısaltmalar & Semboller (Bu Fazda Kullanılan)

> Tam liste için `07-GLOSSARY-SYMBOLS.md`. Burada sadece bu fazda geçenler.

| Kısaltma | Tam Ad (TR) | Tam Ad (EN) | İlk Geçtiği Yer |
|----------|-------------|-------------|-----------------|
| CNN | Konvolüsyonel Sinir Ağı | Convolutional Neural Network | §5.1 |
| ... | ... | ... | ... |

| Sembol | Ad | Birim | İlk Geçtiği Yer |
|--------|-----|-------|-----------------|
| $\sigma$ | Tesir kesiti | barn | §7 (F-001) |
| ... | ... | ... | ... |

---

## 10. Uygulama Detayları (Implementation)

### 10.1 Ana Dosyalar

| Dosya | Satır Sayısı | Sorumluluk |
|-------|-------------|------------|
| `src/path/file1.py` | 234 | ... |
| `src/path/file2.py` | 89 | ... |

### 10.2 Ana Sınıflar

#### `ClassName` (`file.py:LINE`)

```python
class ClassName:
    """Bir cümlelik özet."""

    def __init__(self, ...):
        ...

    def method_one(self, ...):
        """..."""
        ...
```

**Sorumluluk:** ...

**Önemli metotlar:**
- `method_one(...)` — ...
- `method_two(...)` — ...

#### Ek sınıflar...

### 10.3 Önemli Fonksiyonlar

#### `function_name(args)` (`file.py:LINE`)

**Imza:**
```python
def function_name(arg1: type, arg2: type) -> ReturnType:
    """..."""
```

**Davranış:**
1. ...
2. ...

**Kullanılan formül:** F-NNN

### 10.4 External Dependencies

| Kütüphane | Sürüm | Kullanım Yeri | Notlar |
|-----------|-------|---------------|--------|
| numpy | >=1.26 | Tüm modül | Vector ops |
| ... | ... | ... | ... |

### 10.5 I/O İşlemleri

- **Dosya okuma:** `data/raw/*.npz` (numpy npz formatı)
- **Dosya yazma:** `data/processed/{run_id}.h5` (HDF5)
- **Bellek kullanımı:** ~X GB (N örnek için)

---

## 11. Hesaplama Karmaşıklığı

| Adım | Zaman Karmaşıklığı | Bellek Karmaşıklığı | Notlar |
|------|--------------------|--------------------|--------|
| Veri yükleme | O(N) | O(N × D) | N: örnek, D: özellik |
| ... | ... | ... | ... |

**Toplam:**
- **Zaman:** O(...)
- **Bellek:** O(...)

**Donanım gereksinimi:**
- CPU: [yeterli | minimum N çekirdek]
- GPU: [gerekli değil | NVIDIA, X GB VRAM]
- RAM: [minimum X GB]

**Tipik çalışma süresi:** ~Y dakika (donanım: ...)

---

## 12. Doğrulama & Test

### 12.1 Test Dosyaları

| Test | Konum | Kapsam |
|------|-------|--------|
| Unit test | `tests/test_*.py` | ... |
| Integration test | `tests/integration/...` | ... |

### 12.2 Doğrulama Yaklaşımı

[Sentetik veri ile mi, ground-truth ile mi, cross-validation ile mi?]

### 12.3 Sanity Check'ler

- [ ] Çıktı boyutu beklenen mi?
- [ ] Dağılım anormal mi?
- [ ] NaN / Inf var mı?
- [ ] Birim doğru mu?

### 12.4 Test Sonuçları

[Test koşulması yapıldıysa metrikler. Yoksa "Test eksik" — açık sorulara]

---

## 13. Sınırlamalar (Limitations)

[Bu fazın bilinen kısıtları, varsayımları, edge case'leri.]

- **Varsayım 1:** ... (Bu varsayım ihlal edilirse → ...)
- **Varsayım 2:** ...
- **Çalışmadığı durumlar:** ...
- **Numerik kararsızlık:** ... (varsa)
- **Ölçeklenebilirlik sınırı:** ...

---

## 14. Sonuçlar (Results)

### 14.1 Çıktı Örnekleri

[Faz çalıştırıldığında üretilen tipik çıktı.]

```
[Örnek output]
```

### 14.2 Performans Metrikleri (varsa)

| Metrik | Değer | Kaynak (kod) |
|--------|-------|--------------|
| Doğruluk (Accuracy) | %X | `evaluate.py:LINE` |
| F1-skoru | Y | ... |
| ... | ... | ... |

### 14.3 Görseller (Figures)

> Her görsele S-NNN ID ata ve `06-FIGURE-TABLE-CATALOG.md`'ye kaydet.

#### S-NNN: [Şekil Adı]

**Kaynak:** `src/path/visualize.py:LINE`

**Açıklama:** ...

[İmaj path'i veya mermaid]

---

## 15. Tezdeki Yeri

| Tezin Bölümü | Bu Fazın Katkısı |
|--------------|------------------|
| 1. Giriş | ... (varsa motivasyon kısmı) |
| 2. Yöntem | §2.X: bu fazın detaylı anlatımı |
| 3. Bulgular | §3.X: metrik ve görseller |
| 4. Tartışma | §4.X: sınırlamalar, kıyaslama |

**Önerilen alt-bölüm başlığı:** [örn: "2.3 Veri Önişleme"]

**Bu fazdan tezde geçecek formüller:** F-NNN, F-NNN, ...

**Bu fazdan tezde geçecek görseller:** S-NNN, S-NNN, ...

---

## 16. Kaynaklar (References)

### 16.1 Kullanılan Kütüphaneler

- **numpy:** Harris, C. R., et al. (2020). *Array programming with NumPy.* Nature, 585(7825), 357–362.
- ...

### 16.2 Algoritma/Yöntem Atıfları

- **F-NNN için:** [Yazar, Yıl, başlık, dergi/konferans, DOI]
- ...

### 16.3 Domain Bilgisi

- **Nükleer fizik temel:** [Krane, K. S. (1988). *Introductory Nuclear Physics.*]
- ...

---

## 17. Açık Sorular & Notlar

[Sen veya ben sonradan dönmemiz gereken şeyler.]

### 17.1 Bilgi Eksiklikleri

- [ ] Soru: ...?
- [ ] Soru: ...?

### 17.2 İyileştirme Önerileri

- [ ] ...

### 17.3 Tutarsızlıklar (Code-Comment, Code-Doc)

- [ ] ...

### 17.4 Memory MCP Notları

- [Faz entity ID]: ...
- [Eklenen relation'lar]: ...

---

*Faz NN dokümanı | Son güncelleme: YYYY-MM-DD*
```

---

## Şablon Doldurma Kuralları

### Atlamayı Kabul Et — Ama Açık Yaz

Bilgi yoksa boş bırakma:

❌ **Yanlış:**
```
## 7. Formüller

(boş)
```

✅ **Doğru:**
```
## 7. Formüller

Bu fazda doğrudan matematiksel formül kullanılmamaktadır.
İşlemler kütüphane fonksiyonu çağrıları ile yapılmaktadır
(bkz. §10.4 External Dependencies).
```

veya:

```
## 7. Formüller

Bu fazda kullanıldığı düşünülen formüller var ancak kaynak/türetim 
dokümante edilmemiş. Bkz. §17.1 Açık Sorular.
```

### Cross-Reference Disiplini

Her **F-NNN, S-NNN, T-NNN, A-NNN** ID:
1. Bu dosyada tanımlı (sadece bu faz'a özelse)
2. `06-FIGURE-TABLE-CATALOG.md`'de master kayıt

Her **kısaltma/sembol**:
1. Bu dosyada §9'da
2. `07-GLOSSARY-SYMBOLS.md`'de master kayıt

### Kod Referansı Formatı

✅ `src/preprocess/normalize.py:42`
✅ `src/preprocess/normalize.py:42-67` (aralık)
✅ `src/models/cnn.py:CNN.__init__:23` (sınıf metodu)

❌ `src/preprocess/normalize.py` (satırsız)
❌ "normalize fonksiyonunda" (yer belirsiz)

---

## Kalite Kapısı (Faz Doc'u Tamamlandı Mı?)

- [ ] 17 bölümün tamamı dolu
- [ ] Mermaid akış diyagramı var (§3)
- [ ] Tüm formüller LaTeX
- [ ] Tüm formüller F-NNN ID + 06'da kayıt
- [ ] Tüm sembollar/kısaltmalar 07'de kayıt
- [ ] Kod referansları satır numaralı
- [ ] Tezdeki yer belirtilmiş (§15)
- [ ] Kaynaklar (§16) — atıf formatı tutarlı
- [ ] Açık sorular (§17)
- [ ] Memory MCP entity güncellendi
- [ ] reports/faz-NN-analiz-notu.md yazıldı

---

*Phase Doc Template v1.0 | 2026-05-02*
