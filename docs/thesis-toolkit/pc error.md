PS C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12> python C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\main.py
2026-05-04 17:03:38,925 - root - INFO - [LOG] WarningTracker aktif: outputs/pipeline_warnings.json
2026-05-04 17:03:38,925 - root - INFO - [LOG] Rotating log: logs\main_20260504_170338.log (max 200 MB x 5 yedek = toplam ~1 GB)
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1777903419.743209   20888 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1777903420.757721   20888 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.

    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║   NUCLEAR PHYSICS AI PROJECT - MAIN ORCHESTRATOR                        ║
    ║                                                                          ║
    ║   13 PFAZ Pipeline Management System                                    ║
    ║   Version 6.0.0 - Production Ready                                      ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    

================================================================================
[CHECK] Kütüphane kontrolü yapılıyor...
================================================================================
[OK] numpy
[OK] pandas
[OK] scikit-learn
[OK] scipy
[OK] matplotlib
[OK] seaborn
[OK] xgboost
[OK] tensorflow
[OK] torch
[OK] openpyxl
[OK] plotly
[OK] joblib
[OK] tqdm

[SUCCESS] Tüm kütüphaneler mevcut! (13/13)
2026-05-04 17:03:42,304 - __main__ - INFO - ================================================================================
2026-05-04 17:03:42,304 - __main__ - INFO - [START] NUCLEAR PHYSICS AI ORCHESTRATOR v6.0
2026-05-04 17:03:42,305 - __main__ - INFO - ================================================================================
2026-05-04 17:03:42,305 - __main__ - INFO - Config: config.json
2026-05-04 17:03:42,306 - __main__ - INFO - Output: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs

[TIP] Kullanım için --help kullanın
[TIP] Interaktif mod için: python main.py --interactive

================================================================================
[INTERACTIVE] INTERAKTIF MOD
================================================================================

================================================================================
[STATUS] PFAZ DURUM OZETI
================================================================================
[DONE] PFAZ_01: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.061662
[DONE] PFAZ_02: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.182723
[DONE] PFAZ_03: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.336257
[DONE] PFAZ_04: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.355259
[DONE] PFAZ_05: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.395769
[WAIT] PFAZ_06: pending    (  0%) - Son güncelleme: Hiç
[DONE] PFAZ_07: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.439769
[WAIT] PFAZ_08: pending    (  0%) - Son güncelleme: Hiç
[DONE] PFAZ_09: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.613836
[WAIT] PFAZ_10: pending    (  0%) - Son güncelleme: Hiç
[WAIT] PFAZ_11: pending    (  0%) - Son güncelleme: Hiç
[DONE] PFAZ_12: completed  (100%) - Son güncelleme: 2026-05-04T17:02:39.647353
[FAIL] PFAZ_13: failed     (  0%) - Son güncelleme: 2026-05-04T17:02:39.694867
================================================================================

--------------------------------------------------------------------------------
Seçenekler:
  1-13: PFAZ fazını çalıştır
  all: Tüm fazları çalıştır
  predict: Tek çekirdek tahmini (SingleNucleusPredictor)
  status: Durum özeti göster
  reset: Durumu sıfırla
  exit: Çıkış
--------------------------------------------------------------------------------

Seçiminiz: all

Mod seçin:
  1. Run (Yeni başlat)
  2. Resume (Devam et)
  3. Update (Güncelle)
Seçim (1-3): 1
2026-05-04 17:03:49,125 - __main__ - INFO - [INFO] PFAZ11 (Production Deployment) kullanıcı talebi ile ertelenmiştir.
2026-05-04 17:03:49,125 - __main__ - INFO - [ORDER] Bagimsizlik sirasi: [1, 2, 3, 4, 5, 7, 9, 12, 13, 6, 8, 10, 11]
2026-05-04 17:03:49,125 - __main__ - INFO - [ORDER] Not: PFAZ6 PFAZ9/13'ten, PFAZ10 PFAZ12/13'ten sonra calisir
2026-05-04 17:03:49,125 - __main__ - INFO - 
================================================================================
2026-05-04 17:03:49,125 - __main__ - INFO - [START] TUM PFAZ FAZLARI BASLATILIYOR
2026-05-04 17:03:49,125 - __main__ - INFO - ================================================================================
2026-05-04 17:03:49,125 - __main__ - INFO - Aralik  : PFAZ 1 -> PFAZ 13  (13 faz)
2026-05-04 17:03:49,125 - __main__ - INFO - Yurütme sirasi: [1, 2, 3, 4, 5, 7, 9, 12, 13, 6, 8, 10, 11]
2026-05-04 17:03:49,125 - __main__ - INFO - Baslangic: 2026-05-04 17:03:49
2026-05-04 17:03:49,126 - __main__ - INFO - [NOTE] PFAZ 11 otomatik olarak atlanacaktir (deferred)
2026-05-04 17:03:49,126 - __main__ - INFO - [NOTE] PFAZ 6/10 bagimli fazlardan sonra calisacaktir (veri bütünlügü)

[==============================================================================]
  PFAZ  1/13  [░░░░░░░░░░░░░░░░░░░░]   0%  Geçen: 00:00  Tahmini kalan: ?  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,126 - __main__ - INFO - 
================================================================================
2026-05-04 17:03:49,126 - __main__ - INFO - [PFAZ 1] DATASET GENERATION
2026-05-04 17:03:49,126 - __main__ - INFO - ================================================================================
2026-05-04 17:03:49,196 - __main__ - INFO - [PFAZ 1] Scaling varyantları: ['NoScaling', 'Standard', 'Robust', 'MinMax']
2026-05-04 17:03:49,196 - __main__ - INFO - [PFAZ 1] Sampling varyantları: ['Random', 'Stratified']
2026-05-04 17:03:49,196 - __main__ - INFO - [PFAZ 1] Toplam kombinasyon: 8
2026-05-04 17:03:49,196 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 1/8: NoScaling_Random
2026-05-04 17:03:49,197 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,197 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,197 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,199 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,199 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,200 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: NoScaling
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Random
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,201 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,201 - __main__ - ERROR - [ERROR] NoScaling_Random başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,202 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 2/8: NoScaling_Stratified
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,203 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,203 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,204 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: NoScaling
2026-05-04 17:03:49,205 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Stratified
2026-05-04 17:03:49,205 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,205 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,205 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,205 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,205 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,205 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,205 - __main__ - ERROR - [ERROR] NoScaling_Stratified başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,206 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 3/8: Standard_Random
2026-05-04 17:03:49,206 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,206 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,207 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: Standard
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Random
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,208 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,208 - __main__ - ERROR - [ERROR] Standard_Random başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,209 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 4/8: Standard_Stratified
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,210 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,210 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: Standard
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Stratified
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,211 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,212 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,212 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,212 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,212 - __main__ - ERROR - [ERROR] Standard_Stratified başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,213 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 5/8: Robust_Random
2026-05-04 17:03:49,213 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,213 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,213 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,213 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,213 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,214 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: Robust
2026-05-04 17:03:49,215 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Random
2026-05-04 17:03:49,215 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,215 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,215 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,215 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,215 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,215 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,215 - __main__ - ERROR - [ERROR] Robust_Random başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,216 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 6/8: Robust_Stratified
2026-05-04 17:03:49,216 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,216 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,217 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: Robust
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Stratified
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,218 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,219 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,219 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,219 - __main__ - ERROR - [ERROR] Robust_Stratified başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,220 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 7/8: MinMax_Random
2026-05-04 17:03:49,220 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,220 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,220 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,220 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,220 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,220 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,221 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: MinMax
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Random
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,222 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,222 - __main__ - ERROR - [ERROR] MinMax_Random başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,224 - __main__ - INFO - 
[PFAZ 1] Kombinasyon 8/8: MinMax_Stratified
2026-05-04 17:03:49,225 - pfaz_modules.pfaz01_dataset_generation.excluded_nuclei_tracker - INFO - ExcludedNucleiTracker başlatıldı
2026-05-04 17:03:49,225 - physics_modules.theoretical_calculations_manager - INFO - Teorik Hesaplama Yöneticisi başlatıldı
2026-05-04 17:03:49,225 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Outlier Handler başlatıldı
2026-05-04 17:03:49,226 - pfaz_modules.pfaz01_dataset_generation.data_quality_modules - INFO - Data Validator başlatıldı
2026-05-04 17:03:49,226 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - Feature Combination Manager initialized
2026-05-04 17:03:49,226 - pfaz_modules.pfaz01_dataset_generation.feature_combination_manager - INFO - SHAP-based sets: 35, Legacy sets: 5
2026-05-04 17:03:49,226 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Input-Output Configuration Manager initialized
2026-05-04 17:03:49,226 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available I/O configs: ['2In1Out', '3In1Out', '3In2Out', '4In1Out', '5InAdv', '10InAdv', '20InAdv']
2026-05-04 17:03:49,226 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Scenario Manager initialized
2026-05-04 17:03:49,226 - pfaz_modules.pfaz01_dataset_generation.io_config_manager - INFO - Available scenarios: ['S70', 'S80']
2026-05-04 17:03:49,227 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,227 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - DATASET GENERATION PIPELINE INITIALIZED (FAZ 3)
2026-05-04 17:03:49,227 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,227 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Source data: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,227 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,227 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Nucleus counts: [75, 100, 150, 200, 'ALL']
2026-05-04 17:03:49,227 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Targets: ['MM', 'QM']
2026-05-04 17:03:49,228 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Feature sets: TARGET_SPECIFIC
2026-05-04 17:03:49,228 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenarios: ['S70', 'S80']
2026-05-04 17:03:49,228 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scenario: S70
2026-05-04 17:03:49,228 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Scaling: MinMax
2026-05-04 17:03:49,228 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Sampling: Stratified
2026-05-04 17:03:49,229 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,229 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - STARTING COMPLETE DATASET GENERATION PIPELINE
2026-05-04 17:03:49,229 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - ================================================================================
2026-05-04 17:03:49,229 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - 
[STEP 1] LOADING RAW DATA
2026-05-04 17:03:49,229 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - --------------------------------------------------------------------------------
2026-05-04 17:03:49,229 - pfaz_modules.pfaz01_dataset_generation.dataset_generation_pipeline_v2 - INFO - Loading data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,229 - __main__ - ERROR - [ERROR] MinMax_Stratified başarısız: Source data not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\aaa2.txt
2026-05-04 17:03:49,231 - __main__ - INFO - [SUCCESS] PFAZ 1 tamamlandı!
2026-05-04 17:03:49,231 - __main__ - INFO - [PFAZ 1] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ  2/13  [█░░░░░░░░░░░░░░░░░░░]   7%  Geçen: 00:00  Tahmini kalan: 00:01  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,232 - __main__ - INFO - 
================================================================================
2026-05-04 17:03:49,232 - __main__ - INFO - [PFAZ 2] AI MODEL TRAINING
2026-05-04 17:03:49,232 - __main__ - INFO - ================================================================================
2026-05-04 17:03:49,236 - root - WARNING - LightGBM not available — install: pip install lightgbm
2026-05-04 17:03:49,238 - root - WARNING - CatBoost not available — install: pip install catboost
2026-05-04 17:03:49,241 - root - WARNING - Optuna not available! pip install optuna
2026-05-04 17:03:49,252 - tensorflow - WARNING - TensorFlow GPU support is not available on native Windows for TensorFlow >= 2.11. Even if CUDA/cuDNN are installed, GPU will not be used. Please use WSL2 or the TensorFlow-DirectML plugin.
2026-05-04 17:03:49,253 - utils.gpu_manager - INFO - [GPU] GPU bulunamadi -- CPU modu
2026-05-04 17:03:49,253 - utils.gpu_manager - INFO - [SYSTEM] CPU: 32 mantiksal cekirdek
2026-05-04 17:03:49,253 - utils.gpu_manager - INFO - [SYSTEM] GPU: yok | VRAM: 0 MB | torch_device: cpu
2026-05-04 17:03:49,253 - utils.gpu_manager - INFO - [SYSTEM] Optimal workers -- AI:10 ANFIS:20 MC:16
2026-05-04 17:03:49,253 - __main__ - INFO - [GPU] PFAZ2 gpu=False, workers=10
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.seed_tracker - INFO - SeedTracker initialized: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models\seed_reports
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - [ACTIVATED] Seed Tracker initialized
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - PARALLEL AI TRAINER INITIALIZED
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Datasets directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Training config: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\pfaz_modules\pfaz02_ai_training\training_configs_50.json
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Workers: 10
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - GPU enabled: False
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Hyperparameter tuning: False
2026-05-04 17:03:49,254 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Model validation: True
2026-05-04 17:03:49,255 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Advanced models: False
2026-05-04 17:03:49,255 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================
2026-05-04 17:03:49,256 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - 
================================================================================
2026-05-04 17:03:49,256 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - TRAIN ALL MODELS - PARALLEL EXECUTION
2026-05-04 17:03:49,256 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================
2026-05-04 17:03:49,256 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - 
Training mode: PARALLEL
2026-05-04 17:03:49,256 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================
2026-05-04 17:03:49,256 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - WARNING - Training config not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\pfaz_modules\pfaz02_ai_training\training_configs_50.json
2026-05-04 17:03:49,258 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Creating default training configurations...
2026-05-04 17:03:49,258 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Using 50 training configurations
2026-05-04 17:03:49,258 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - WARNING - No datasets found in C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,259 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Found 0 datasets
2026-05-04 17:03:49,259 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - DNN available (TF installed) but disabled (use_advanced_models=False)
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Model types: ['RF', 'XGBoost', 'SVR']
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Created 0 training jobs
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO -   Datasets requested: 0
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO -   Datasets valid: 0
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO -   Model types: 3
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO -   Configs per model: 50
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - 
[START] Starting PARALLEL training with 10 workers...
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - 
================================================================================
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - STARTING PARALLEL TRAINING
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Total jobs: 0
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Workers: 10
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================

2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - 
================================================================================
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - PARALLEL TRAINING COMPLETED
2026-05-04 17:03:49,260 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================
2026-05-04 17:03:49,261 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Total jobs: 0
2026-05-04 17:03:49,261 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Successful: 0
2026-05-04 17:03:49,261 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Failed: 0
2026-05-04 17:03:49,261 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Total time: 0.00 minutes
2026-05-04 17:03:49,261 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Avg time per job: N/A (no jobs executed)
2026-05-04 17:03:49,261 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - ================================================================================

2026-05-04 17:03:49,261 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - INFO - Summary report saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models\training_summary.json
2026-05-04 17:03:49,262 - pfaz_modules.pfaz02_ai_training.seed_tracker - INFO - 
================================================================================
2026-05-04 17:03:49,262 - pfaz_modules.pfaz02_ai_training.seed_tracker - INFO - SEED TRACKER SUMMARY
2026-05-04 17:03:49,262 - pfaz_modules.pfaz02_ai_training.seed_tracker - INFO - ================================================================================
2026-05-04 17:03:49,262 - pfaz_modules.pfaz02_ai_training.seed_tracker - INFO - Total seeds recorded: 0
2026-05-04 17:03:49,262 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - WARNING - [WARNING] Could not save seed tracking report: 'unique_seeds'
2026-05-04 17:03:49,264 - root - WARNING - statsmodels not available - some tests disabled
2026-05-04 17:03:49,267 - root - WARNING - SALib not available - install: pip install SALib
2026-05-04 17:03:49,283 - pfaz_modules.pfaz02_ai_training.parallel_ai_trainer - WARNING - [WARNING] NuclearPatternAnalyzer basarisiz (devam): unexpected indent (pfaz6_final_reporting.py, line 1267)
2026-05-04 17:03:49,284 - __main__ - INFO - [SUCCESS] PFAZ 2 tamamlandı!
2026-05-04 17:03:49,284 - __main__ - INFO - [PFAZ 2] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ  3/13  [███░░░░░░░░░░░░░░░░░]  15%  Geçen: 00:00  Tahmini kalan: 00:00  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,284 - __main__ - INFO - 
================================================================================
2026-05-04 17:03:49,284 - __main__ - INFO - [PFAZ 3] ANFIS TRAINING
2026-05-04 17:03:49,284 - __main__ - INFO - ================================================================================
2026-05-04 17:03:49,321 - root - WARNING - MATLAB ANFIS trainer not available: No module named 'progress_tracker'
2026-05-04 17:03:49,323 - __main__ - INFO - [GPU] PFAZ3 gpu=False, workers=20
2026-05-04 17:03:49,323 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ================================================================================
2026-05-04 17:03:49,323 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ANFIS PARALLEL TRAINER V2 INITIALIZED
2026-05-04 17:03:49,323 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ================================================================================
2026-05-04 17:03:49,323 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Datasets directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,323 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models
2026-05-04 17:03:49,323 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Workers: 20
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Config Manager: True
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Adaptive Strategy: False
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Performance Analyzer: True
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Save Datasets: True
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ================================================================================
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ANFIS PARALLEL TRAINING (3-PHASE SOFT STRATEGY)
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ================================================================================
2026-05-04 17:03:49,324 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Using 8 ANFIS configurations
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO -   Total: 0 ANFIS-feasible datasets | skipped non-dataset: 1 | skipped too-many-inputs: 0
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Found 0 datasets
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Wave 1 PILOT: 0 jobs (0 skipped)
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Wave 2 ADVANCED: 0 jobs
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - 
================================================================================
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ANFIS PARALLEL TRAINING COMPLETED
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ================================================================================
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Total jobs: 0
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Successful: 0
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Failed: 0
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Total time: 0.00 minutes
2026-05-04 17:03:49,325 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - ================================================================================
2026-05-04 17:03:49,326 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Summary JSON saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models\anfis_training_summary.json
2026-05-04 17:03:49,332 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Summary Excel saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models\anfis_training_results.xlsx
2026-05-04 17:03:49,345 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Generating AI vs ANFIS comparison Excel...
2026-05-04 17:03:49,372 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - Comparison Excel saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models\anfis_vs_ai_comparison.xlsx
2026-05-04 17:03:49,373 - pfaz_modules.pfaz03_anfis_training.anfis_performance_analyzer - INFO - ================================================================================
2026-05-04 17:03:49,373 - pfaz_modules.pfaz03_anfis_training.anfis_performance_analyzer - INFO - ANFIS PERFORMANCE ANALYZER INITIALIZED
2026-05-04 17:03:49,373 - pfaz_modules.pfaz03_anfis_training.anfis_performance_analyzer - INFO - ================================================================================
2026-05-04 17:03:49,373 - pfaz_modules.pfaz03_anfis_training.anfis_performance_analyzer - INFO - Found 0 ANFIS result files
2026-05-04 17:03:49,373 - pfaz_modules.pfaz03_anfis_training.anfis_performance_analyzer - INFO - Loaded results for 0 configs
2026-05-04 17:03:49,373 - pfaz_modules.pfaz03_anfis_training.anfis_performance_analyzer - INFO - Generating Excel report: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models\performance_analysis\ANFIS_Performance_Analysis.xlsx
2026-05-04 17:03:49,377 - pfaz_modules.pfaz03_anfis_training.anfis_performance_analyzer - INFO - [SUCCESS] Excel report saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models\performance_analysis\ANFIS_Performance_Analysis.xlsx
2026-05-04 17:03:49,377 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - [OK] ANFISPerformanceAnalyzer: Excel raporu olusturuldu -> performance_analysis/
2026-05-04 17:03:49,377 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO -   [INFO] ANFISRobustnessTester: basarili sonuc yok -- atlanıyor
2026-05-04 17:03:49,378 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - [OK] ANFISAdaptiveStrategy/PatternTracker: örüntü analizi -> adaptive_pattern_analysis/
2026-05-04 17:03:49,378 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - [INFO] ANFISDatasetSelector: deactivated (3-phase pilot strategy active)
2026-05-04 17:03:49,392 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - WARNING - [WARNING] NuclearPatternAnalyzer basarisiz (devam): unexpected indent (pfaz6_final_reporting.py, line 1267)
2026-05-04 17:03:49,393 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO - [KERNEL REPORT] Generated: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models\kernel_usage_report.json
2026-05-04 17:03:49,393 - pfaz_modules.pfaz03_anfis_training.anfis_parallel_trainer_v2 - INFO -   Total trainings tracked: 0
2026-05-04 17:03:49,394 - __main__ - INFO - [SUCCESS] PFAZ 3 tamamlandı!
2026-05-04 17:03:49,394 - __main__ - INFO - [PFAZ 3] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ  4/13  [████░░░░░░░░░░░░░░░░]  23%  Geçen: 00:00  Tahmini kalan: 00:00  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,394 - __main__ - INFO - 
[PFAZ 4] UNKNOWN NUCLEI PREDICTIONS
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - ================================================================================
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - PFAZ 4: UNKNOWN NUCLEI PREDICTOR v2.0 INITIALIZED
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - ================================================================================
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - AI models dir   : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - ANFIS models dir: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - Datasets dir    : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - Output dir      : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\unknown_predictions
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - ================================================================================
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - 
================================================================================
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - PREDICTING ON UNKNOWN (TEST) NUCLEI
2026-05-04 17:03:49,396 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - ================================================================================
2026-05-04 17:03:49,397 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - Found 0 datasets with test.csv
2026-05-04 17:03:49,397 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - 
================================================================================
2026-05-04 17:03:49,397 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - COMPLETED: 0 total model-dataset combinations
2026-05-04 17:03:49,397 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - ================================================================================

2026-05-04 17:03:49,397 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - Generating Excel report: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\unknown_predictions\Unknown_Nuclei_Results.xlsx
2026-05-04 17:03:49,397 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - WARNING - No results to report.
2026-05-04 17:03:49,398 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - INFO - Generating Excel report: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\unknown_predictions\Unknown_Nuclei_Results.xlsx
2026-05-04 17:03:49,398 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - WARNING - No results to report.
2026-05-04 17:03:49,400 - pfaz_modules.pfaz04_unknown_predictions.unknown_nuclei_predictor - WARNING - [AAA2 Comparison] No per-nucleus results available. Run predict_unknown_nuclei() first.
2026-05-04 17:03:49,401 - __main__ - INFO - [OK] AAA2 karşılaştırma Excel raporu oluşturuldu
2026-05-04 17:03:49,401 - __main__ - INFO - [SUCCESS] PFAZ 4 tamamlandı!
2026-05-04 17:03:49,401 - __main__ - INFO - [PFAZ 4] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ  5/13  [██████░░░░░░░░░░░░░░]  30%  Geçen: 00:00  Tahmini kalan: 00:00  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,401 - __main__ - INFO - 
[PFAZ 5] CROSS-MODEL ANALYSIS
2026-05-04 17:03:49,405 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - ================================================================================
2026-05-04 17:03:49,405 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - PFAZ 5: CROSS-MODEL ANALYSIS PIPELINE v2.0
2026-05-04 17:03:49,405 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - ================================================================================
2026-05-04 17:03:49,405 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - AI models dir   : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models
2026-05-04 17:03:49,405 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - ANFIS models dir: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models
2026-05-04 17:03:49,405 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - Datasets dir    : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,406 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - Output dir      : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\cross_model_analysis
2026-05-04 17:03:49,406 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - ================================================================================
2026-05-04 17:03:49,406 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - 
================================================================================
2026-05-04 17:03:49,406 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - FAZ 5: CROSS-MODEL ANALYSIS STARTING
2026-05-04 17:03:49,406 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - ================================================================================
2026-05-04 17:03:49,406 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - 
[1/4] Collecting model predictions...
2026-05-04 17:03:49,406 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - 
--- Collecting predictions from all models ---
2026-05-04 17:03:49,407 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - Found 0 datasets with test.csv
2026-05-04 17:03:49,407 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   MM: 0 model predictions collected
2026-05-04 17:03:49,407 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   QM: 0 model predictions collected
2026-05-04 17:03:49,407 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   Beta_2: 0 model predictions collected
2026-05-04 17:03:49,407 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - 
[2/4] Running cross-model evaluation per target...
2026-05-04 17:03:49,407 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - WARNING -   MM: <2 models, skipping cross-model analysis
2026-05-04 17:03:49,408 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - WARNING -   QM: <2 models, skipping cross-model analysis
2026-05-04 17:03:49,409 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - 
[3/4] Building master Excel report...
2026-05-04 17:03:49,409 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   Writing: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\cross_model_analysis\MASTER_CROSS_MODEL_REPORT.xlsx
2026-05-04 17:03:49,413 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   [OK] Master report saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\cross_model_analysis\MASTER_CROSS_MODEL_REPORT.xlsx
2026-05-04 17:03:49,413 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - 
[4/4] Saving summary JSON...
2026-05-04 17:03:49,414 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   [OK] Summary JSON saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\cross_model_analysis\cross_model_analysis_summary.json
2026-05-04 17:03:49,414 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - 
================================================================================
2026-05-04 17:03:49,414 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - FAZ 5: CROSS-MODEL ANALYSIS COMPLETED
2026-05-04 17:03:49,414 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   Duration       : 0.0s (0.0 min)
2026-05-04 17:03:49,414 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   Targets done   : []
2026-05-04 17:03:49,414 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO -   Output dir     : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\cross_model_analysis
2026-05-04 17:03:49,414 - pfaz_modules.pfaz05_cross_model.faz5_cross_model_analysis - INFO - ================================================================================
2026-05-04 17:03:49,415 - __main__ - INFO - [SUCCESS] PFAZ 5 tamamlandı!
2026-05-04 17:03:49,415 - __main__ - INFO - [PFAZ 5] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ  7/13  [███████░░░░░░░░░░░░░]  38%  Geçen: 00:00  Tahmini kalan: 00:00  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,415 - __main__ - INFO - 
[PFAZ 7] ENSEMBLE & META-MODELS
2026-05-04 17:03:49,416 - root - WARNING - CatBoost not available
2026-05-04 17:03:49,419 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - ================================================================================
2026-05-04 17:03:49,419 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - PFAZ 7: COMPLETE ENSEMBLE & META-MODEL PIPELINE
2026-05-04 17:03:49,420 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - ================================================================================
2026-05-04 17:03:49,420 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO -   trained_models : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models
2026-05-04 17:03:49,420 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO -   anfis_models   : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\anfis_models
2026-05-04 17:03:49,420 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO -   datasets       : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\generated_datasets
2026-05-04 17:03:49,420 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO -   output         : C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\ensemble_results
2026-05-04 17:03:49,420 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - 
============================================================
2026-05-04 17:03:49,421 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - TARGET: MM
2026-05-04 17:03:49,421 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - ============================================================
2026-05-04 17:03:49,421 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO -   Top-20 MM: AI=0, ANFIS=0 (pool: 0 AI + 0 ANFIS)
2026-05-04 17:03:49,421 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - WARNING -   [WARNING] No models found for MM, skipping
2026-05-04 17:03:49,422 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - 
============================================================
2026-05-04 17:03:49,422 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - TARGET: QM
2026-05-04 17:03:49,422 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - ============================================================
2026-05-04 17:03:49,423 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO -   Top-20 QM: AI=0, ANFIS=0 (pool: 0 AI + 0 ANFIS)
2026-05-04 17:03:49,423 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - WARNING -   [WARNING] No models found for QM, skipping
2026-05-04 17:03:49,427 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - ERROR - [ERROR] Excel write failed: At least one sheet must be visible
2026-05-04 17:03:49,428 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - [OK] Summary JSON: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\ensemble_results\ensemble_summary.json
2026-05-04 17:03:49,429 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - 
================================================================================
2026-05-04 17:03:49,429 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - PFAZ 7: FINAL SUMMARY
2026-05-04 17:03:49,429 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - ================================================================================
2026-05-04 17:03:49,429 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - [COMPLETE] PFAZ 7 COMPLETED SUCCESSFULLY!
2026-05-04 17:03:49,429 - pfaz_modules.pfaz07_ensemble.pfaz7_complete_ensemble_pipeline - INFO - ================================================================================
2026-05-04 17:03:49,429 - __main__ - INFO - [SUCCESS] PFAZ 7 tamamlandı!
2026-05-04 17:03:49,429 - __main__ - INFO - [PFAZ 7] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ  9/13  [█████████░░░░░░░░░░░]  46%  Geçen: 00:00  Tahmini kalan: 00:00  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,430 - __main__ - INFO - 
[PFAZ 9] AAA2 CONTROL GROUP ANALYSIS
2026-05-04 17:03:49,430 - __main__ - INFO - [GPU] PFAZ9 gpu=False (DNN inference)
2026-05-04 17:03:49,476 - root - WARNING - SHAP not available - install: pip install shap
2026-05-04 17:03:49,478 - root - WARNING - Excel libraries not available
2026-05-04 17:03:49,480 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - ================================================================================
2026-05-04 17:03:49,480 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - AAA2 CONTROL GROUP ANALYZER - COMPLETE %100
2026-05-04 17:03:49,480 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - ================================================================================
2026-05-04 17:03:49,480 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - Output: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\aaa2_results
2026-05-04 17:03:49,480 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
================================================================================
2026-05-04 17:03:49,480 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - PFAZ 9: AAA2 CONTROL GROUP - COMPLETE PIPELINE
2026-05-04 17:03:49,480 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - ================================================================================
2026-05-04 17:03:49,481 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - Start: 2026-05-04 17:03:49
2026-05-04 17:03:49,481 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
================================================================================
2026-05-04 17:03:49,481 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - PHASE 1: LOAD & ENRICH AAA2 DATA
2026-05-04 17:03:49,481 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - ================================================================================
2026-05-04 17:03:49,481 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - -> Loading raw AAA2: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\data\aaa2.txt
2026-05-04 17:03:49,481 - utils.file_io_utils - INFO - Reading nuclear data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\data\aaa2.txt
2026-05-04 17:03:49,483 - utils.file_io_utils - INFO -   Successfully read with delimiter: '\t'
2026-05-04 17:03:49,483 - utils.file_io_utils - INFO -   [SUCCESS] Loaded: 267 rows, 12 columns
2026-05-04 17:03:49,483 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - [OK] Loaded 267 nuclei
2026-05-04 17:03:49,483 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
-> Calculating theoretical features...
2026-05-04 17:03:49,483 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   -> Calculating Woods-Saxon features...
2026-05-04 17:03:49,484 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   [OK] Added 4 Woods-Saxon features
2026-05-04 17:03:49,484 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   -> Calculating Nilsson model features...
2026-05-04 17:03:49,486 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   [OK] Added 5 Nilsson model features
2026-05-04 17:03:49,486 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   -> Calculating shell model features...
2026-05-04 17:03:49,487 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   [OK] Added 5 shell model features
2026-05-04 17:03:49,487 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
[OK] Total features: 26
2026-05-04 17:03:49,490 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - [OK] Enriched data saved: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\aaa2_results\aaa2_enriched_with_theory.csv
2026-05-04 17:03:49,490 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
================================================================================
2026-05-04 17:03:49,490 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - TARGET: MM
2026-05-04 17:03:49,490 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - ================================================================================
2026-05-04 17:03:49,492 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
-> Selecting top 50 models (AI + ANFIS) for MM...
2026-05-04 17:03:49,492 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - [OK] Scanned 0 models (AI: 0, ANFIS: 0)
2026-05-04 17:03:49,492 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   Top-50 breakdown: AI=0, ANFIS=0
2026-05-04 17:03:49,492 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
-> Generating predictions for MM...
2026-05-04 17:03:49,492 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - WARNING - No models selected
2026-05-04 17:03:49,493 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
================================================================================
2026-05-04 17:03:49,493 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - TARGET: QM
2026-05-04 17:03:49,494 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - ================================================================================
2026-05-04 17:03:49,494 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
-> Selecting top 50 models (AI + ANFIS) for QM...
2026-05-04 17:03:49,494 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - [OK] Scanned 0 models (AI: 0, ANFIS: 0)
2026-05-04 17:03:49,494 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO -   Top-50 breakdown: AI=0, ANFIS=0
2026-05-04 17:03:49,494 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
-> Generating predictions for QM...
2026-05-04 17:03:49,494 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - WARNING - No models selected
2026-05-04 17:03:49,495 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - ================================================================================
2026-05-04 17:03:49,496 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - AAA2.TXT DETAYLI VERİ KALİTE KONTROLÜ
2026-05-04 17:03:49,496 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - ================================================================================
2026-05-04 17:03:49,496 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
1. Dosya yükleniyor...
2026-05-04 17:03:49,496 - utils.file_io_utils - INFO - Reading nuclear data from: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\data\aaa2.txt
2026-05-04 17:03:49,497 - utils.file_io_utils - INFO -   Successfully read with delimiter: '\t'
2026-05-04 17:03:49,497 - utils.file_io_utils - INFO -   [SUCCESS] Loaded: 267 rows, 12 columns
2026-05-04 17:03:49,497 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    [OK] Toplam satır: 267
2026-05-04 17:03:49,497 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    [OK] Sütunlar: ['NUCLEUS', 'A', 'Z', 'N', 'SPIN', 'PARITY', 'P-factor', 'Beta_2', 'MAGNETIC MOMENT [µ]', 'QUADRUPOLE MOMENT [Q]', 'Nn', 'Np']
2026-05-04 17:03:49,497 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
2. Eksik değer kontrolü...
2026-05-04 17:03:49,500 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    -> Eksik değer sayısı: 70
2026-05-04 17:03:49,500 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
3. Sıfır değer kontrolü...
2026-05-04 17:03:49,501 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    -> MM=0 sayısı: 0
2026-05-04 17:03:49,501 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
4. Metin ve tarih kontrolleri...
2026-05-04 17:03:49,503 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    -> Metin içeren sayısal veri: 2
2026-05-04 17:03:49,503 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
5. PARITY kontrolü...
2026-05-04 17:03:49,503 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    -> Geçersiz PARITY: 0
2026-05-04 17:03:49,503 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
6. A = Z + N kontrolü...
2026-05-04 17:03:49,504 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    -> A!=Z+N uyuşmazlığı: 0
2026-05-04 17:03:49,504 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
7. MM=0 tek-A kontrolü...
2026-05-04 17:03:49,505 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    -> MM=0 tek-A: 0
2026-05-04 17:03:49,505 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
8. QM (Q) eksiklik kontrolü...
2026-05-04 17:03:49,506 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    -> QM eksik: 65
2026-05-04 17:03:49,506 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
9. İstatistiksel özetler...
2026-05-04 17:03:49,507 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    [OK] Toplam çekirdek: 267
2026-05-04 17:03:49,507 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    [OK] A aralığı: (np.int64(2), np.int64(254))
2026-05-04 17:03:49,507 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    [OK] MM mevcut: 0 (0.0%)
2026-05-04 17:03:49,507 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    [OK] QM mevcut: 0 (0.0%)
2026-05-04 17:03:49,507 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
10. Excel raporu oluşturuluyor...
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO -    [OK] Excel raporu kaydedildi: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\aaa2_results\data_quality\aaa2_quality_report_20260504_170349.xlsx
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - 
================================================================================
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - VERİ KALİTE KONTROLÜ TAMAMLANDI
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_quality_checker - INFO - ================================================================================
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - [OK] AAA2QualityChecker: veri kalitesi raporu -> data_quality/
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - ================================================================================
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - MONTE CARLO SIMULATION SYSTEM INITIALIZED
2026-05-04 17:03:49,566 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - ================================================================================
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - Output directory: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\aaa2_results\monte_carlo_analysis
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - Config: 7 components
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - 
================================================================================
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - MONTE CARLO ANALYSIS - MM
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - ================================================================================
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - Start time: 2026-05-04 17:03:49
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - 
-> Loading top 10 models for MM...
2026-05-04 17:03:49,567 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - ERROR -   Performance summary not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models\performance_summary_MM.csv
2026-05-04 17:03:49,568 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - ERROR -   No models loaded. Aborting.
2026-05-04 17:03:49,570 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - 
================================================================================
2026-05-04 17:03:49,570 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - MONTE CARLO ANALYSIS - QM
2026-05-04 17:03:49,570 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - ================================================================================
2026-05-04 17:03:49,570 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - Start time: 2026-05-04 17:03:49
2026-05-04 17:03:49,570 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - INFO - 
-> Loading top 10 models for QM...
2026-05-04 17:03:49,570 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - ERROR -   Performance summary not found: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\trained_models\performance_summary_QM.csv
2026-05-04 17:03:49,571 - pfaz_modules.pfaz09_aaa2_monte_carlo.monte_carlo_simulation_system - ERROR -   No models loaded. Aborting.
2026-05-04 17:03:49,572 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - [OK] MonteCarloSimulationSystem: 2 hedef MC analizi -> monte_carlo_analysis/
2026-05-04 17:03:49,572 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - 
================================================================================
2026-05-04 17:03:49,572 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - [SUCCESS] PFAZ 9 COMPLETE!
2026-05-04 17:03:49,572 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - ================================================================================
2026-05-04 17:03:49,572 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - Duration: 0.0s (0.0min)
2026-05-04 17:03:49,573 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - Targets processed: 0
2026-05-04 17:03:49,573 - pfaz_modules.pfaz09_aaa2_monte_carlo.aaa2_control_group_complete_v4 - INFO - Output: C:\Users\elifk\OneDrive\Masaüstü\thesis-nuclear-ai-v12\thesis-nuclear-ai-v12\repo\outputs\aaa2_results
2026-05-04 17:03:49,573 - __main__ - INFO - [SUCCESS] PFAZ 9 tamamlandı!
2026-05-04 17:03:49,573 - __main__ - INFO - [PFAZ 9] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ 12/13  [██████████░░░░░░░░░░]  53%  Geçen: 00:00  Tahmini kalan: 00:00  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,573 - __main__ - INFO - 
[PFAZ 12] ADVANCED ANALYTICS
2026-05-04 17:03:49,574 - __main__ - WARNING - [PFAZ12] Yeterli model verisi bulunamadı (0 model tipi). PFAZ2'nin tamamlanması gerekiyor.
2026-05-04 17:03:49,575 - __main__ - INFO - 
[PFAZ12] NuclearMomentBandAnalyzer basliyor...
2026-05-04 17:03:49,590 - __main__ - WARNING - [PFAZ12] Bant analizi atlandı: unexpected indent (pfaz6_final_reporting.py, line 1267)
2026-05-04 17:03:49,604 - __main__ - WARNING - [PFAZ12] Pattern analizi atlandı: unexpected indent (pfaz6_final_reporting.py, line 1267)
2026-05-04 17:03:49,606 - __main__ - INFO - [SUCCESS] PFAZ 12 tamamlandı!
2026-05-04 17:03:49,606 - __main__ - INFO - [PFAZ 12] Tamamlandı -- süre: 00:00

[==============================================================================]
  PFAZ 13/13  [████████████░░░░░░░░]  61%  Geçen: 00:00  Tahmini kalan: 00:00  Şu an: 17:03:49
  Mod: RUN
[==============================================================================]
2026-05-04 17:03:49,606 - __main__ - INFO - 
[PFAZ 13] AUTOML INTEGRATION
2026-05-04 17:03:49,607 - __main__ - INFO - [GPU] PFAZ13 gpu=False
2026-05-04 17:03:49,613 - root - WARNING - SHAP not available - SHAP-based selection disabled
2026-05-04 17:03:49,615 - root - WARNING - MATLAB engine not available - using sklearn approximation
2026-05-04 17:03:49,622 - __main__ - ERROR - [ERROR] PFAZ 13 başarısız: unexpected indent (automl_retraining_loop.py, line 539)
2026-05-04 17:03:49,623 - __main__ - ERROR - [ERROR] PFAZ 13 başarısız (00:00): unexpected indent (automl_retraining_loop.py, line 539)