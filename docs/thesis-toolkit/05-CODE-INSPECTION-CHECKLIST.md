# 05 — Code Inspection Checklist (.py Dosya İnceleme Rehberi)

> **Amaç:** Her .py dosyasını tezde dokümante edilebilir seviyede incelemek için sistematik kontrol listesi.

> **Kullanım:** `01-WORKFLOW-PLAN.md` "Adım 2: Kod İncelemesi"nde bu protokol uygulanır.

---

## İçindekiler

1. [İnceleme Yaklaşımı](#i̇nceleme-yaklaşımı)
2. [9 Ana İnceleme Alanı](#9-ana-i̇nceleme-alanı)
3. [Skill & Agent Çağrı Sırası](#skill--agent-çağrı-sırası)
4. [Çıktı Formatı (Per .py Dosyası)](#çıktı-formatı-per-py-dosyası)
5. [Sık Karşılaşılan Durumlar](#sık-karşılaşılan-durumlar)
6. [Manuel Doğrulama: Kod Çalıştırma](#manuel-doğrulama-kod-çalıştırma)

---

## İnceleme Yaklaşımı

### Top-Down → Bottom-Up

```
1. Önce dosyanın AMACINI anla (header docstring, üst-düzey comment)
2. Sonra İSKELETİ çıkar (sınıflar, fonksiyonlar — sadece imzalar)
3. Sonra KRİTİK FONKSİYONları detaylı oku
4. En son YARDIMCI fonksiyonlar
```

### Tekrar Eden Pass'ler

Her .py dosyası **3 pass** ile incelenir:

| Pass | Hedef | Süre |
|------|-------|------|
| 1. Hızlı tarama | Yapı, dil, sorumluluk | 2-5 dk |
| 2. Detay okuma | Fonksiyonlar, formüller, akış | 10-20 dk |
| 3. Kalite review | Quality, security, edge case | 5-10 dk |

---

## 9 Ana İnceleme Alanı

### 1) Dosya Yapısı (Structure)

```
[ ] Dosyanın amacı tek cümlede özetlenebilir mi?
[ ] Module-level docstring var mı? (üst kısım """...""")
[ ] Import organizasyonu (stdlib, third-party, local)
[ ] __all__ tanımı var mı (public API)?
[ ] if __name__ == "__main__" bloğu (executable mi)?
[ ] Toplam satır sayısı (300+ ise refactor şüphesi)
```

**Kayıt:** Dosya adı, satır sayısı, tek-cümle amacı, public API listesi.

---

### 2) Davranış (Behavior)

```
[ ] Sınıfların sorumluluğu net mi (Single Responsibility)?
[ ] Her fonksiyonun bir tek işi var mı?
[ ] Side effect'ler tespit edildi mi?
    [ ] Disk I/O (read/write file)
    [ ] Network (HTTP, socket)
    [ ] Global state mutation
    [ ] Print/logging
    [ ] Random seed (set ediliyor mu?)
[ ] Saf fonksiyonlar (pure) hangileri?
[ ] Yan etkili fonksiyonlar belgelendi mi?
```

**Kayıt:** Her sınıf/fonksiyonun davranışı (1 satır), side effect listesi.

---

### 3) Formül & Matematiksel İfadeler

> **Bu PhD tezi için en kritik bölüm.**

```
[ ] np / scipy / sklearn / torch fonksiyon çağrıları
[ ] Hardcoded sayısal sabitler:
    [ ] Fizik sabiti (Avogadro, ışık hızı, vs.) → kaynak ata
    [ ] Hiperparametre (lr=0.001) → doğrula
    [ ] Magic number → şüphe
[ ] Manuel hesaplama loop'ları → formül tespiti
[ ] List comprehension içinde matematik
[ ] Vectorized ops (matmul, einsum, ...) → matematiksel anlam?
```

**Sentetik örnek:**
```python
energy = 0.5 * mass * velocity**2
# → Kinetic energy formula
# F-NNN olarak kayıt: E_k = (1/2) m v²

sigma = np.sqrt(np.sum((x - mean)**2) / n)
# → Standard deviation (population)
# F-NNN olarak kayıt: σ = √(Σ(xᵢ - μ)²/n)
```

**Kayıt:** Her matematiksel ifadeye F-NNN ata, 06'ya işle, LaTeX formunu yaz, değişkenleri tanımla.

---

### 4) Hardcoded Değerler & Sabitler

```
[ ] Tüm hardcoded sayıları listele:
    [ ] Çağırılma yeri (satır)
    [ ] Değer
    [ ] Anlamı
    [ ] Kaynak (kitap, paper, deneysel)
    [ ] Birim
[ ] Magic number'lar (config'e taşınmalı mı?)
[ ] String sabitler (path, regex, ...)
[ ] Dosya yolları
[ ] URL/endpoint'ler
[ ] Cihaz tanımları (cuda, mps, cpu)
```

**Sentetik örnek:**
```python
DETECTOR_EFFICIENCY = 0.34  # NaI(Tl) for 661 keV (Cs-137)
# → 06-CATALOG: T-NNN | Hardcoded constants tablosu
# → Açık soru: Bu değerin kalibrasyon kaynağı?
```

---

### 5) I/O İşlemleri

```
[ ] Dosya okuma:
    [ ] Hangi format? (npz, h5, csv, parquet, root, ...)
    [ ] Ne büyüklükte? (MB/GB)
    [ ] Lazy loading mi, full load mi?
[ ] Dosya yazma:
    [ ] Çıktı formatı
    [ ] Overwrite politikası
[ ] Network:
    [ ] API çağrısı, authentication, rate limiting
[ ] Database:
    [ ] Hangi DB?
[ ] GPU memory transfer (.to(device), .cpu(), .cuda())
```

---

### 6) Hata Yönetimi (Error Handling)

```
[ ] try/except blokları:
    [ ] Yakalananlar specific mi yoksa "except Exception"?
    [ ] Re-raise mi, swallow mu?
    [ ] Logging var mı?
[ ] Validation (input checking):
    [ ] Type check, value range, shape check
[ ] Assert kullanımı (production'da çıkar mı?)
[ ] Sessiz hatalar (return None on error)
[ ] Custom exception sınıfları
```

**ECC Skill:** `silent-failure-hunter` agent → otomatize.

---

### 7) Performans

```
[ ] Loop içinde costly ops
[ ] Vectorization fırsatları (manuel for → np.einsum)
[ ] Memory leak ihtimali
[ ] GPU vs CPU placement
[ ] Batch processing var mı?
[ ] Profiling done? (cProfile, line_profiler)
[ ] Tipik runtime
```

**ECC Skill:** `performance-optimizer`.

---

### 8) Güvenlik & Veri Etiği

```
[ ] Hardcoded API key, password, token? (KESINLIKLE OLMAMALI)
[ ] Input sanitization (file path injection)
[ ] eval(), exec() kullanımı (varsa şüphe)
[ ] pickle.load() (untrusted source ise risk)
[ ] requests/urllib SSL doğrulama
[ ] Kullanıcı verisi anonimizasyonu
[ ] PHI/PII varlığı
```

**ECC Skill:** `security-review` + `security-reviewer` agent.

---

### 9) Akademik Fact-Check

> **Tez için kritik adım.**

```
[ ] Kullanılan algoritmaların kaynağı belli mi?
    Örn: "VAE kullanılmış" → Kingma & Welling (2013) atıfı?
[ ] Kullanılan formüllerin türetimi/kaynağı?
[ ] Hiperparametrelerin gerekçesi var mı?
[ ] Veri seti kaynağı?
[ ] Önişleme adımlarının literatürel temeli?
[ ] State-of-the-art ile karşılaştırma yapılabilir mi?
[ ] Reproducibility:
    [ ] Random seed sabit mi?
    [ ] Bağımlılık sürümleri kayıtlı mı?
    [ ] Donanım belirtilmiş mi?
```

**ECC Skill:** `documentation-lookup` (Context7) + `exa-search` (paper).

---

## Skill & Agent Çağrı Sırası

```
1. Read tool → tam dosya içeriği

2. Pass 1: Hızlı tarama
   - python-patterns skill (otomatik) → idiomatic kontrol
   - comment-analyzer agent → comment kalitesi
   - Module-level docstring oku

3. Pass 2: Detay
   - code-explorer agent → execution path
   - documentation-lookup (Context7) → kütüphane API
   - Sequential Thinking MCP → karmaşık akıl yürütme

4. Pass 3: Kalite
   - python-reviewer agent → tam review
   - silent-failure-hunter agent → sessiz hatalar
   - type-design-analyzer agent → type tasarımı
   - security-reviewer agent (varsa hassas işlem)
```

### Hangi Agent Ne Zaman?

| Senaryo | Agent | Sebep |
|---------|-------|-------|
| Standart .py | `python-reviewer` | Genel kalite |
| Karmaşık veri pipeline | `code-explorer` | Akış izleme |
| Hata yönetimi şüphesi | `silent-failure-hunter` | Sessiz hata |
| Type-heavy | `type-design-analyzer` | Type tasarım |
| Auth/network/secret | `security-reviewer` | Güvenlik |
| Performans kritik | `performance-optimizer` | Profilleme |
| PyTorch model | `pytorch-patterns` skill | Framework |
| Test dosyası | `pr-test-analyzer` | Test kalitesi |

---

## Çıktı Formatı (Per .py Dosyası)

```markdown
### Dosya: `src/path/to/file.py`

**Satır:** 234  
**Sorumluluk:** [tek cümle]

#### Public API

| Tip | İsim | Satır | Sorumluluk |
|-----|------|-------|------------|
| class | `ClassName` | 12-89 | ... |
| function | `process(...)` | 92-145 | ... |

#### Tespit Edilen Formüller

| ID | Açıklama | Satır | LaTeX | Kaynak |
|----|----------|-------|-------|--------|
| F-001 | Sigma normalize | 67 | $z = (x-\mu)/\sigma$ | std stat |
| F-002 | ... | ... | ... | ... |

#### Hardcoded Sabitler

| Değer | Satır | Anlamı | Birim | Kaynak |
|-------|-------|--------|-------|--------|
| 0.34 | 23 | NaI(Tl) verim | dimensionless | Açık soru |
| 1024 | 56 | Spektrum boyutu | channels | Veri toplama |

#### External Dependencies

- `numpy` (>=1.26)
- `scipy.signal` (peak_find)
- `torch.nn` (CNN)

#### I/O

- Read: `data/raw/*.npz`
- Write: `data/processed/{run_id}.h5`

#### Side Effects

- Random seed set: `np.random.seed(42)` (satır 8)
- Disk write: yes
- Network: no

#### Quality Notes (python-reviewer agent)

✅ Type hints kullanılmış
⚠️ Bare except (satır 145)
❌ Magic number 0.34

#### Açık Sorular

- [ ] DETECTOR_EFFICIENCY=0.34 sabit nereden?
- [ ] `process()` 145 satırlık — refactor şüphesi
```

---

## Sık Karşılaşılan Durumlar

### A: Docstring Yok

```python
def process(x, y, z):
    return x * y + z
```

**Yapılacak:**
1. comment-analyzer agent
2. Sen tahmin et → "Bu fonksiyon ... yapıyor gibi görünüyor"
3. Açık Sorular'a yaz
4. Gerçek davranışı GÖZLEMLE — docstring uydurma

### B: Comment Eski (Code Drift)

```python
# Returns the mean
def process(data):
    return np.median(data)  # Aslında median
```

**Yapılacak:**
1. comment-analyzer tespit eder
2. "Tutarsızlık" olarak kayıt et (faz doc §17.3)
3. Comment'e değil, kodun gerçek davranışına güven

### C: Çok Karmaşık Fonksiyon

200+ satır, nested loops.

**Yapılacak:**
1. Sequential Thinking MCP ile parça parça
2. Pseudocode olarak özetle
3. Faz doc §6'ya A-NNN olarak kaydet
4. Açık Sorular'a "X fonksiyonu refactor adayı"

### D: External Library Davranışı Belirsiz

`from obscure_lib import something`

**Yapılacak:**
1. Context7 MCP → kütüphane docs
2. Yoksa: exa-search ile paper / GitHub repo
3. Hâlâ bulunamazsa: Açık Sorular'a
4. Tezde "X kütüphanesi kullanılmıştır (atıf)"

### E: Hardcoded Magic Number

`if value > 0.7:`

**Yapılacak:**
1. Çevreden ipucu çıkar (variable adları, comment)
2. Git history (`git log -L`) — ne zaman eklenmiş?
3. Yine bulunamazsa: Açık Sorular'a, kullanıcıya sor

### F: Test Yok

**Yapılacak:**
1. Faz doc §12'de "Test mevcut değil"
2. Tezde tartışmaya: "Daha kapsamlı test gelecek çalışma"

### G: Gizli Bağımlılık (System Tool)

`subprocess.run(["talys", ...])`

**Yapılacak:**
1. TALYS, MCNP, Geant4 gibi external tool tespit
2. Faz doc §10.4 External Dependencies'e ekle
3. Tezde version + atıf gerekli

---

## Manuel Doğrulama: Kod Çalıştırma

### Güvenli Çalıştırma Protokolü

```bash
1. Sandbox / venv:
   cd repo
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Tek-dosya / küçük unit test:
   python -c "from src.module import func; print(func(test_input))"

3. Çıktı/davranış doğrulama:
   - Beklenen output ne?
   - Edge case'ler (boş input, NaN)
   - Exception fırlatma davranışı

4. Sonuçları faz doc §12.4'e yaz
```

> ⚠️ Eğer kod external API çağırıyorsa, önce mock/stub.

---

## Faz İncelemesi Bittiğinde

```
[ ] Tüm .py dosyaları için "Çıktı Formatı" doldurulmuş
[ ] Tespit edilen tüm formüller 06'ya numaralı eklenmiş
[ ] Tespit edilen tüm sabitler tablo halinde
[ ] Tüm dependency'ler listeli
[ ] Açık sorular kullanıcıya iletilmek üzere kayıtlı
[ ] Faz dokümanı §10.1-§10.5 bölümleri tam
```

---

*Code Inspection Checklist v1.0 | 2026-05-02*
