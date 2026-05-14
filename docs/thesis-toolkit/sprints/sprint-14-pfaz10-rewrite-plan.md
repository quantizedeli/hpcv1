# Sprint 14 — PFAZ10 Rewrite Planı

**Tarih:** 2026-05-14  
**Hedef:** PFAZ10 tez derleme sistemini magnetic moment / quadrupole moment odaklı, gerçek veri üreten, LaTeX-PDF çıktısı veren sisteme dönüştür.  
**Format:** Claude Code için tek prompt — "bu dosyayı oku ve yap"  
**humanizer:** KULLANMA  
**Çıktı:** LaTeX → PDF (Word yok)

---

## CLAUDE CODE'A GÖNDERİLECEK TAM PROMPT

Aşağıdaki metni doğrudan Claude Code'a yapıştır:

---

```
Bu dosyayı oku (/arf/home/ahmacar/hpcv1/docs/thesis-toolkit/sprints/sprint-14-pfaz10-rewrite-plan.md)
ve "## PFAZ10 REWRITE GÖREVİ" bölümündeki tüm adımları uygula.
```

---

## PFAZ10 REWRITE GÖREVİ

### Bağlam

Bu proje 267 nükleer izotop için manyetik moment (MM), kuadrupol moment (QM) tahmin eden
bir makine öğrenmesi sistemidir. Pipeline: RF + XGBoost + DNN + ANFIS modeller eğitilir,
sonuçlar karşılaştırılır, tez derlenir.

**Mevcut sorun:** `pfaz10_thesis_compilation_system.py` ve alt modüller "binding energy",
"nuclear radius" gibi yanlış konular üretiyor. Tez içeriği projeyle eşleşmiyor.

**Hedef:** PFAZ10 gerçek pipeline çıktılarını (PFAZ2-9 Excel/JSON) okuyup doğru içerik
üretmeli ve `main.tex` → PDF derlemeli.

### Dosya Yapısı

```
pfaz_modules/pfaz10_thesis_compilation/
├── pfaz10_master_integration.py    ← Ana orkestratör (bu düzeltilecek)
├── pfaz10_chapter_generator.py     ← Bölüm üreticisi (düzeltilecek)
├── pfaz10_content_generator.py     ← İçerik üreticisi (düzeltilecek)
├── pfaz10_latex_integration.py     ← LaTeX derleyici (büyük ölçüde OK)
├── pfaz10_discussion_conclusion.py ← Tartışma/sonuç (düzeltilecek)
├── pfaz10_visualization_qa.py      ← Görsel QA (OK)
└── pfaz10_thesis_orchestrator.py   ← Yüksek seviye çağrı (OK)
```

### Gerçek Veri Kaynakları (PFAZ çıktıları)

```python
VERI_KAYNAKLARI = {
    # PFAZ2 AI eğitim sonuçları
    'pfaz2_summary':    'outputs/trained_models/training_summary.xlsx',
    'pfaz2_metrics':    'outputs/trained_models/**/metrics_*.json',  # glob
    # PFAZ3 ANFIS eğitim sonuçları
    'pfaz3_summary':    'outputs/anfis_models/anfis_training_results.xlsx',
    'pfaz3_comparison': 'outputs/anfis_models/anfis_vs_ai_comparison.xlsx',
    # PFAZ5 karşılaştırma
    'pfaz5_master':     'outputs/cross_model_analysis/MASTER_CROSS_MODEL_REPORT.xlsx',
    # PFAZ6 final rapor
    'pfaz6_thesis':     'outputs/final_reports/THESIS_COMPLETE_RESULTS*.xlsx',
    # PFAZ7 ensemble
    'pfaz7_ensemble':   'outputs/ensemble_models/ensemble_report*.xlsx',
    # PFAZ9 Monte Carlo
    'pfaz9_mc':         'outputs/aaa2_results/AAA2_Complete_*.xlsx',
    # PFAZ12 istatistiksel analiz
    'pfaz12_stats':     'outputs/advanced_analytics/statistical_tests/pfaz12_statistical_tests.xlsx',
    'pfaz12_bootstrap': 'outputs/advanced_analytics/bootstrap_ci/bootstrap_ci_results.xlsx',
    # PFAZ13 AutoML
    'pfaz13_trials':    'outputs/automl_results/automl_trials_details.xlsx',
}
```

### Tez Yapısı (Türkçe, IEEE format)

```
Kapak
Özet (TR) / Abstract (EN)
Teşekkür
İçindekiler
Şekiller Listesi
Tablolar Listesi
Kısaltmalar

Bölüm 1: Giriş
  1.1 Motivasyon -- Nükleer momentlerin önemi
  1.2 Problem Tanımı -- 267 izotop, MM + QM hedefleri
  1.3 Tezin Katkıları -- ML + ANFIS hibrit yaklaşım
  1.4 Tez Organizasyonu

Bölüm 2: Literatür Taraması
  (thesis/bolum-02-literatur-incelemesi.md dosyasından — 177 satır, IEEE atıflı)
  2.1 Nükleer Fizik Temelleri
  2.2 Makine Öğrenmesi Yaklaşımları
  2.3 ANFIS Yöntemi
  2.4 Mevcut Çalışmalar

Bölüm 3: Metodoloji
  3.1 Veri Seti (aaa2.txt: 267 nükleer izotop, 44 özellik)
  3.2 Özellik Mühendisliği (44 → 200+ aday, seçim)
  3.3 AI Modelleri (RF, XGBoost, DNN -- PFAZ2)
  3.4 ANFIS Modeli (8 konfigürasyon -- PFAZ3)
  3.5 Adaptif Dataset Seçimi (Top/Mid/Low -- BUG-74 fix)
  3.6 Ensemble Yöntemi (PFAZ7)
  3.7 İstatistiksel Doğrulama (Bootstrap CI, ANOVA -- PFAZ12)

Bölüm 4: Sonuçlar
  4.1 AI Model Performansı (PFAZ2 gerçek R² değerleri)
  4.2 ANFIS Performansı (PFAZ3 gerçek R² değerleri)
  4.3 Model Karşılaştırması (PFAZ5 AI_vs_ANFIS_Comparison)
  4.4 Sağlamlık Analizi (PFAZ2 robustness_summary)
  4.5 İstatistiksel Analiz (PFAZ12 Bootstrap CI, p-value)
  4.6 AutoML Optimizasyonu (PFAZ13 convergence)
  4.7 Monte Carlo Belirsizlik Analizi (PFAZ9)

Bölüm 5: Tartışma
  5.1 Genel Bulgular
  5.2 ANFIS vs AI Karşılaştırması
  5.3 Sınırlılıklar
  5.4 Gelecek Çalışmalar (AdvancedSensitivity, daha fazla izotop)

Bölüm 6: Sonuç

Kaynaklar (IEEE format, thesis/bolum-02-literatur-incelemesi.md'den)
Ekler
```

### Yapılacaklar (Claude Code Adım Adım)

#### Adım 1: Gerçek Veri Okuma Modülü

`pfaz_modules/pfaz10_thesis_compilation/pfaz10_data_reader.py` dosyasını oluştur:

```python
class PFAZ10DataReader:
    """PFAZ2-13 çıktılarını okur, tez içeriği için hazır dict döner."""
    
    def __init__(self, pfaz_outputs: dict):
        self.outputs = pfaz_outputs
    
    def read_ai_performance(self) -> dict:
        """PFAZ2: RF/XGBoost/DNN R², RMSE, MAE per target"""
        # training_summary.xlsx oku
        # metrics_*.json glob ile oku
        # return {'MM': {'RF': {'R2': 0.97, ...}, ...}, 'QM': {...}}
    
    def read_anfis_performance(self) -> dict:
        """PFAZ3: ANFIS konfigürasyon bazlı performans"""
        # anfis_training_results.xlsx → All_Results sheet
        # return {'MM': {'best_r2': 0.95, 'n_configs': 8, ...}, ...}
    
    def read_comparison(self) -> dict:
        """PFAZ5: AI_vs_ANFIS_Comparison sheet"""
    
    def read_bootstrap_ci(self) -> dict:
        """PFAZ12: Bootstrap CI sonuçları"""
        # bootstrap_ci_results.xlsx → Model_Performance sheet
        # return {'RF_MM': {'R2': 0.97, 'CI_lower': 0.954, 'CI_upper': 0.982}, ...}
    
    def read_robustness(self) -> dict:
        """PFAZ2: robustness_summary.xlsx"""
    
    def read_all(self) -> dict:
        """Tüm kaynakları oku, unified dict döner"""
```

#### Adım 2: pfaz10_content_generator.py Düzelt

Mevcut dosyada "binding energy" / "nuclear radius" referansları var. Bunları kaldır.
Gerçek `PFAZ10DataReader` çağrıları ile değiştir.

Her bölüm fonksiyonu şu yapıda olmalı:
```python
def generate_bolum4_sonuclar(self, data: dict) -> str:
    """Bölüm 4 LaTeX içeriği üret — gerçek PFAZ2-13 verileriyle."""
    ai_perf = data['ai_performance']
    # ...
    return latex_str
```

#### Adım 3: pfaz10_chapter_generator.py Düzelt

`thesis/bolum-02-literatur-incelemesi.md` dosyasını oku, LaTeX'e dönüştür.
Bölüm 2 içeriği bu dosyadan alınmalı (yeniden yazma, sadece dönüştür).

#### Adım 4: pfaz10_discussion_conclusion.py Düzelt

"binding energy" referanslarını kaldır.
ANFIS vs AI karşılaştırması gerçek Bootstrap CI p-value'ları ile yazılmalı.
Gelecek çalışmalarda: AdvancedSensitivity (Sobol), daha fazla izotop.

#### Adım 5: pfaz10_master_integration.py Düzelt

```python
def execute_full_pipeline(self, compile_pdf=False):
    # 1. PFAZ10DataReader ile gerçek verileri oku
    reader = PFAZ10DataReader(self.pfaz_outputs)
    data = reader.read_all()
    
    # 2. Bölümleri üret
    chapters = self._generate_all_chapters(data)
    
    # 3. main.tex derle
    self._write_main_tex(chapters)
    
    # 4. PDF derle (compile_pdf=True ise)
    if compile_pdf:
        self._run_latexmk()
```

#### Adım 6: LaTeX Şablonu Doğrula

`pfaz10_latex_integration.py` içindeki şablon kontrol et:
- Başlık: "Makine Öğrenmesi ve ANFIS Yöntemleri ile Nükleer Momentlerin Tahmini"
- Hedefler: MM ve QM (Beta_2 veya binding energy değil)
- Dil: Türkçe ana metin, İngilizce abstract
- Format: IEEE, 12pt, A4

#### Adım 7: Test

```bash
python main.py --pfaz 10 --mode run
# Beklenen çıktı:
# outputs/thesis_compilation/main.tex  -- 80+ sayfa
# outputs/thesis_compilation/main.pdf  -- compile_pdf=True ise
# outputs/thesis_compilation/execution_report.json
```

### Kritik Notlar

1. **humanizer KULLANMA** — Kemal istemedi, düz akademik Türkçe yeterli
2. **Word çıktısı YOK** — sadece LaTeX → PDF (Overleaf veya latexmk)
3. **Veri yoksa graceful fallback** — TRUBA çıktıları henüz yok olabilir, `data.get(key, 'N/A')` kullan
4. **thesis/bolum-02-literatur-incelemesi.md sil değil, oku** — 177 satır IEEE atıflı kaynak
5. **Mevcut pfaz10_latex_integration.py büyük ölçüde OK** — sadece içerik kısmını düzelt

### Beklenen Çıktı Dosyaları

```
outputs/thesis_compilation/
├── main.tex                    # Ana LaTeX dosyası
├── chapters/
│   ├── chapter1_giris.tex
│   ├── chapter2_literatur.tex
│   ├── chapter3_metodoloji.tex
│   ├── chapter4_sonuclar.tex
│   ├── chapter5_tartisma.tex
│   └── chapter6_sonuc.tex
├── figures/                    # PFAZ8'den kopyalanan PNG'ler
├── tables/                     # Gerçek veriden üretilen tablolar
├── references.bib              # IEEE format kaynaklar
├── main.pdf                    # (compile_pdf=True ise)
└── execution_report.json       # Ne üretildi, hangi kaynaktan
```

### Süre Tahmini

PFAZ10 tek başına çalışır, diğer fazlara bağımlı değil (çıktıları okur ama beklemez).
Süre: 5-15 dakika (PDF derleme dahil).
