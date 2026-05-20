"""
PFAZ 10 -- Veri Okuyucu (Sprint 14 REWRITE)
============================================

PFAZ 2..13 cikti dosyalarini okur ve tez bolumleri icin hazir Python
sozluk yapilarinda doner. TRUBA ciktisi mevcut degilse her metoda
graceful fallback uygular (sozluk degeri 'N/A' veya bos yapilar olur).

Yazim: 2026-05-14 (Sprint 14)
Kaynak referans: docs/thesis-toolkit/sprints/sprint-14-pfaz10-rewrite-plan.md
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


PLACEHOLDER = "N/A"
PLACEHOLDER_NOTE = "Veri TRUBA'dan beklenmektedir"


class PFAZ10DataReader:
    """PFAZ2-13 ciktilarini okuyup unified dict doner.

    Eksik dosyalarda fallback: PLACEHOLDER ('N/A') ve PLACEHOLDER_NOTE ile
    doldurulur. Boylece LaTeX uretimi tamamlanir; veri eksik bolumler
    `\\textit{Veri TRUBA'dan beklenmektedir}` notu ile isaretlenir.

    Args:
        project_dir: Cikti ana dizini (Path). Dosyalar bu dizin altinda aranir.
            TRUBA'da /arf/scratch/ahmacar/hpcv1_outputs olmali.
        pfaz_outputs: PFAZ no (int veya str) -> dizin yolu inject sozlugu (opsiyonel).
            main.py'den {1: Path(...), 2: Path(...)} seklinde gelir.
            Bu sozluk verildiginde DEFAULT_PATHS fallback yerine bu dizinler kullanilir.

    BUG-A FIX (Sprint 17): pfaz_outputs integer key'leri (1,2,3...) string key'lerle
        ('pfaz2_summary' gibi) eslestiriliyor. Onceden override hic calismiyordu.
    BUG-B FIX (Sprint 17): DEFAULT_PATHS'teki 'outputs/' prefix kaldirildi.
        project_dir zaten output_dir oldugunda 'outputs/trained_models' ->
        '/scratch/.../outputs/trained_models' yanlis yola gidiyordu.
    """

    # BUG-B FIX: 'outputs/' prefix kaldirildi -- project_dir zaten output_dir'dir
    DEFAULT_PATHS = {
        "pfaz2_summary":        "trained_models/training_summary.xlsx",
        "pfaz2_results_summary":"trained_models/training_results_summary.xlsx",
        "pfaz2_robustness":     "trained_models/robustness_summary.xlsx",
        "pfaz3_summary":        "anfis_models/anfis_training_results.xlsx",
        "pfaz3_comparison":     "anfis_models/anfis_vs_ai_comparison.xlsx",
        "pfaz5_master":         "cross_model_analysis/MASTER_CROSS_MODEL_REPORT.xlsx",
        "pfaz6_thesis":         "reports/THESIS_COMPLETE_RESULTS.xlsx",
        "pfaz7_ensemble_report":"ensemble_results/evaluation/comprehensive_report.json",
        "pfaz9_aaa2_mm":        "aaa2_results/AAA2_Complete_MM.xlsx",
        "pfaz9_aaa2_qm":        "aaa2_results/AAA2_Complete_QM.xlsx",
        "pfaz12_stats":         "advanced_analytics/statistical_tests/pfaz12_statistical_tests.xlsx",
        "pfaz12_bootstrap":     "advanced_analytics/bootstrap_ci/bootstrap_ci_results.xlsx",
        "pfaz12_ai_vs_anfis":   "advanced_analytics/ai_vs_anfis/paired_test_results.xlsx",
        "pfaz13_summary":       "automl_results/automl_improvement_report.xlsx",
        "pfaz13_trials":        "automl_results/automl_trials_details.xlsx",
    }

    # BUG-A FIX: integer pfaz_outputs key -> DEFAULT_PATHS string key eslestirmesi
    _PFAZ_INT_TO_SUBDIR: dict[int, str] = {
        2:  "trained_models",
        3:  "anfis_models",
        5:  "cross_model_analysis",
        6:  "reports",
        7:  "ensemble_results",
        9:  "aaa2_results",
        12: "advanced_analytics",
        13: "automl_results",
    }

    def __init__(
        self,
        project_dir: str | Path,
        pfaz_outputs: dict[str, str | Path] | None = None,
    ) -> None:
        self.project_dir = Path(project_dir)
        raw_overrides = pfaz_outputs or {}

        # BUG-A FIX: integer key'leri (1,2,3...) subdir override'a donustur
        # main.py {2: Path('/scratch/.../trained_models')} -> subdir_overrides['trained_models'] = Path(...)
        subdir_overrides: dict[str, Path] = {}
        for k, v in raw_overrides.items():
            if isinstance(k, int) and k in self._PFAZ_INT_TO_SUBDIR:
                subdir_overrides[self._PFAZ_INT_TO_SUBDIR[k]] = Path(v)

        # DEFAULT_PATHS uzerinden gercek path'leri hesapla:
        # Once DEFAULT_PATHS subdir'ini subdir_overrides'da ara, yoksa project_dir altinda bul
        self.paths: dict[str, Path] = {}
        for key, rel in self.DEFAULT_PATHS.items():
            rel_path = Path(rel)
            subdir = rel_path.parts[0]  # orn. 'trained_models'
            if subdir in subdir_overrides:
                # inject edilmis dizin kullan
                self.paths[key] = subdir_overrides[subdir] / Path(*rel_path.parts[1:])
            else:
                self.paths[key] = self.project_dir / rel_path

        self._fallback_count = 0
        self._read_count = 0

    def _placeholder(self, reason: str) -> dict[str, str]:
        """Eksik veri icin standart sozluk doner."""
        self._fallback_count += 1
        return {"status": PLACEHOLDER, "note": PLACEHOLDER_NOTE, "reason": reason}

    def _read_excel_sheet(self, path: Path, sheet_name: str | int = 0) -> pd.DataFrame | None:
        """Excel dosyasindan bir sayfayi okur, hata varsa None doner."""
        if not path.exists():
            logger.warning("[PFAZ10DataReader] Dosya yok: %s", path)
            return None
        try:
            df = pd.read_excel(path, sheet_name=sheet_name)
            self._read_count += 1
            return df
        except Exception as exc:  # noqa: BLE001
            logger.warning("[PFAZ10DataReader] Excel okuma hatasi (%s): %s", path, exc)
            return None

    def _read_json(self, path: Path) -> Any:
        """JSON dosyasini okur, hata varsa None doner."""
        if not path.exists():
            logger.warning("[PFAZ10DataReader] Dosya yok: %s", path)
            return None
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            self._read_count += 1
            return data
        except Exception as exc:  # noqa: BLE001
            logger.warning("[PFAZ10DataReader] JSON okuma hatasi (%s): %s", path, exc)
            return None

    # ---------------------------------------------------------------------
    # PFAZ 2 -- AI Performance
    # ---------------------------------------------------------------------

    def read_ai_performance(self) -> dict[str, Any]:
        """PFAZ2 sonuclari: model tipi x hedef R2/RMSE/MAE ortalamalari.

        Returns:
            {
              'MM': {'RF': {'R2': 0.97, 'RMSE': 0.55, ...}, 'XGBoost': {...}, ...},
              'QM': {...},
              'configs_total': int,
              'models_saved': int,
            }
        """
        path_pri = self.paths["pfaz2_results_summary"]
        path_sec = self.paths["pfaz2_summary"]
        df = self._read_excel_sheet(path_pri, sheet_name="All_Results")
        if df is None:
            df = self._read_excel_sheet(path_sec, sheet_name="All_Results")
        if df is None:
            return self._placeholder("PFAZ2 training_summary.xlsx bulunamadi")

        out: dict[str, Any] = {"MM": {}, "QM": {}, "configs_total": int(len(df)), "models_saved": 0}

        if "Target" not in df.columns or "Model_Type" not in df.columns:
            return self._placeholder("PFAZ2 Excel beklenen kolonlari icermiyor")

        saved_mask = df.get("PKL_Saved", pd.Series([True] * len(df))).astype(bool)
        out["models_saved"] = int(saved_mask.sum())

        for target in ("MM", "QM"):
            target_df = df[df["Target"] == target]
            for model_type in target_df["Model_Type"].dropna().unique():
                sub = target_df[target_df["Model_Type"] == model_type]
                model_stats = {
                    "R2": _safe_mean(sub.get("Test_R2")),
                    "RMSE": _safe_mean(sub.get("Test_RMSE")),
                    "MAE": _safe_mean(sub.get("Test_MAE")),
                    "Val_R2": _safe_mean(sub.get("Val_R2")),
                    "CV_R2": _safe_mean(sub.get("CV_R2")),
                    "n_configs": int(len(sub)),
                }
                out[target][str(model_type)] = model_stats

        return out

    # ---------------------------------------------------------------------
    # PFAZ 2 -- Robustness (Sprint 13 BUG-96)
    # ---------------------------------------------------------------------

    def read_robustness(self) -> dict[str, Any]:
        """PFAZ2 robustness_summary.xlsx -- noise/outlier/perturbation testleri."""
        path = self.paths["pfaz2_robustness"]
        df = self._read_excel_sheet(path)
        if df is None:
            return self._placeholder("robustness_summary.xlsx bulunamadi (Sprint 13 BUG-96)")
        return {
            "n_models": int(len(df)),
            "columns": list(df.columns),
            "summary": df.describe(include="all").to_dict() if not df.empty else {},
        }

    # ---------------------------------------------------------------------
    # PFAZ 3 -- ANFIS Performance
    # ---------------------------------------------------------------------

    def read_anfis_performance(self) -> dict[str, Any]:
        """PFAZ3 anfis_training_results.xlsx: konfigurasyon bazli ozet."""
        path = self.paths["pfaz3_summary"]
        df = self._read_excel_sheet(path, sheet_name="All_Results")
        if df is None:
            df = self._read_excel_sheet(path)
        if df is None:
            return self._placeholder("PFAZ3 anfis_training_results.xlsx bulunamadi")

        out: dict[str, Any] = {"MM": {}, "QM": {}, "n_configs": 8}
        if "Target" not in df.columns:
            return self._placeholder("PFAZ3 Excel beklenen kolonlari icermiyor")

        for target in ("MM", "QM"):
            target_df = df[df["Target"] == target]
            if target_df.empty:
                out[target] = {"best_r2": PLACEHOLDER, "n_configs": 0}
                continue
            out[target] = {
                "best_r2": _safe_max(target_df.get("Test_R2")),
                "mean_r2": _safe_mean(target_df.get("Test_R2")),
                "best_config": _safe_argmax_value(
                    target_df,
                    value_col="Test_R2",
                    label_col="Config_ID",
                ),
                "n_configs": int(len(target_df)),
            }
        return out

    # ---------------------------------------------------------------------
    # PFAZ 5 -- Cross-Model + AI vs ANFIS (Sprint 13 BUG-96)
    # ---------------------------------------------------------------------

    def read_comparison(self) -> dict[str, Any]:
        """PFAZ5 MASTER_CROSS_MODEL_REPORT.xlsx -- AI_vs_ANFIS_Comparison sheet."""
        path = self.paths["pfaz5_master"]
        df = self._read_excel_sheet(path, sheet_name="AI_vs_ANFIS_Comparison")
        if df is None:
            df = self._read_excel_sheet(path, sheet_name="Model_Statistics")
        if df is None:
            return self._placeholder("PFAZ5 MASTER_CROSS_MODEL_REPORT.xlsx bulunamadi")
        return {
            "n_datasets": int(len(df)),
            "columns": list(df.columns),
            "head_rows": df.head(20).to_dict(orient="records") if not df.empty else [],
        }

    # ---------------------------------------------------------------------
    # PFAZ 7 -- Ensemble Results
    # ---------------------------------------------------------------------

    def read_ensemble(self) -> dict[str, Any]:
        """PFAZ7 comprehensive_report.json -- voting + stacking sonuclari."""
        path = self.paths["pfaz7_ensemble_report"]
        data = self._read_json(path)
        if data is None:
            return self._placeholder("PFAZ7 comprehensive_report.json bulunamadi")

        results = data.get("results", {}) if isinstance(data, dict) else {}
        return {
            "timestamp": data.get("timestamp", PLACEHOLDER) if isinstance(data, dict) else PLACEHOLDER,
            "n_methods": len(results),
            "methods": {
                name: {
                    "R2": _safe_get(method, "R2"),
                    "RMSE": _safe_get(method, "RMSE"),
                    "MAE": _safe_get(method, "MAE"),
                }
                for name, method in results.items()
                if isinstance(method, dict)
            },
            "best_method": _best_ensemble_method(results),
        }

    # ---------------------------------------------------------------------
    # PFAZ 9 -- Monte Carlo
    # ---------------------------------------------------------------------

    def read_monte_carlo(self) -> dict[str, Any]:
        """PFAZ9 AAA2_Complete_{MM,QM}.xlsx -- belirsizlik analizi."""
        out: dict[str, Any] = {}
        for target in ("MM", "QM"):
            path = self.paths[f"pfaz9_aaa2_{target.lower()}"]
            df = self._read_excel_sheet(path, sheet_name="Uncertainty")
            if df is None:
                out[target] = self._placeholder(f"PFAZ9 AAA2_Complete_{target}.xlsx bulunamadi")
                continue
            out[target] = {
                "n_nuclei": int(len(df)),
                "mean_ci_width": _safe_mean(df.get("CI_Width")),
                "mean_std": _safe_mean(df.get("Std_Prediction")),
                "n_bootstrap": 1000,  # Sprint 4 BUG-38 + Sprint 8 BUG-64 sonrasi
            }
        return out

    # ---------------------------------------------------------------------
    # PFAZ 12 -- Bootstrap CI
    # ---------------------------------------------------------------------

    def read_bootstrap_ci(self) -> dict[str, Any]:
        """PFAZ12 bootstrap_ci_results.xlsx -- Model_Performance sheet."""
        path = self.paths["pfaz12_bootstrap"]
        df = self._read_excel_sheet(path, sheet_name="Model_Performance")
        if df is None:
            df = self._read_excel_sheet(path)
        if df is None:
            return self._placeholder("PFAZ12 bootstrap_ci_results.xlsx bulunamadi")

        models: dict[str, dict[str, float | str]] = {}
        if "Model_Name" not in df.columns:
            return self._placeholder("Bootstrap_CI: Model_Name kolonu yok")

        for _, row in df.iterrows():
            name = str(row.get("Model_Name", "?"))
            models[name] = {
                "R2": _row_get(row, "R2_Mean"),
                "CI_lower": _row_get(row, "R2_CI_Lower"),
                "CI_upper": _row_get(row, "R2_CI_Upper"),
                "n_bootstrap": int(row.get("Bootstrap_N", 1000)) if "Bootstrap_N" in row else 1000,
            }
        return {"n_models": len(models), "models": models}

    # ---------------------------------------------------------------------
    # PFAZ 12 -- AI vs ANFIS Paired Tests (Sprint 13 BUG-97)
    # ---------------------------------------------------------------------

    def read_ai_vs_anfis_tests(self) -> dict[str, Any]:
        """PFAZ12 paired_test_results.xlsx -- AI ve ANFIS karsilastirmasi."""
        path = self.paths["pfaz12_ai_vs_anfis"]
        df = self._read_excel_sheet(path)
        if df is None:
            return self._placeholder("PFAZ12 paired_test_results.xlsx bulunamadi (Sprint 13 BUG-97)")

        tests: list[dict[str, Any]] = []
        for _, row in df.iterrows():
            tests.append(
                {
                    "dataset": str(row.get("Dataset", "?")),
                    "target": str(row.get("Target", "?")),
                    "p_value": _row_get(row, "p_value"),
                    "cohens_d": _row_get(row, "cohens_d"),
                    "significant": bool(row.get("significant", False)),
                }
            )
        return {"n_tests": len(tests), "tests": tests}

    # ---------------------------------------------------------------------
    # PFAZ 13 -- AutoML
    # ---------------------------------------------------------------------

    def read_automl(self) -> dict[str, Any]:
        """PFAZ13 automl_improvement_report.xlsx + automl_trials_details.xlsx."""
        path_main = self.paths["pfaz13_summary"]
        df_main = self._read_excel_sheet(path_main, sheet_name="Summary")
        if df_main is None:
            df_main = self._read_excel_sheet(path_main)

        path_trials = self.paths["pfaz13_trials"]
        df_trials = self._read_excel_sheet(path_trials, sheet_name="Convergence")

        if df_main is None and df_trials is None:
            return self._placeholder("PFAZ13 automl ciktilari bulunamadi")

        out: dict[str, Any] = {}
        if df_main is not None and not df_main.empty:
            out["n_retrained"] = int(len(df_main))
            out["mean_improvement"] = _safe_mean(df_main.get("R2_Improvement"))
            out["columns"] = list(df_main.columns)
        if df_trials is not None and not df_trials.empty:
            out["n_trials"] = int(len(df_trials))
            out["convergence_best"] = _safe_max(df_trials.get("Best_R2_So_Far"))
        return out or self._placeholder("PFAZ13: bos cikti tablosu")

    # ---------------------------------------------------------------------
    # Toplu okuma
    # ---------------------------------------------------------------------

    def read_all(self) -> dict[str, Any]:
        """Tum kaynaklari okur, unified dict doner.

        Returns:
            Asagidaki anahtarlardan olusan sozluk:
              - ai_performance: PFAZ2 sonuclari
              - robustness: PFAZ2 RobustnessTester (Sprint 13)
              - anfis_performance: PFAZ3 sonuclari
              - comparison: PFAZ5 AI vs ANFIS sheet
              - ensemble: PFAZ7 ensemble sonuclari
              - monte_carlo: PFAZ9 belirsizlik analizi
              - bootstrap_ci: PFAZ12 Bootstrap CI
              - ai_vs_anfis_tests: PFAZ12 paired test
              - automl: PFAZ13 AutoML sonuclari
              - meta: okuma istatistikleri
        """
        data = {
            "ai_performance": self.read_ai_performance(),
            "robustness": self.read_robustness(),
            "anfis_performance": self.read_anfis_performance(),
            "comparison": self.read_comparison(),
            "ensemble": self.read_ensemble(),
            "monte_carlo": self.read_monte_carlo(),
            "bootstrap_ci": self.read_bootstrap_ci(),
            "ai_vs_anfis_tests": self.read_ai_vs_anfis_tests(),
            "automl": self.read_automl(),
        }
        data["meta"] = {
            "read_count": self._read_count,
            "fallback_count": self._fallback_count,
            "project_dir": str(self.project_dir),
        }
        return data


# ---------------------------------------------------------------------------
# Yardimci fonksiyonlar
# ---------------------------------------------------------------------------


def _safe_mean(series: pd.Series | None) -> float | str:
    if series is None or series.empty:
        return PLACEHOLDER
    try:
        value = pd.to_numeric(series, errors="coerce").mean()
        return PLACEHOLDER if pd.isna(value) else float(value)
    except Exception:  # noqa: BLE001
        return PLACEHOLDER


def _safe_max(series: pd.Series | None) -> float | str:
    if series is None or series.empty:
        return PLACEHOLDER
    try:
        value = pd.to_numeric(series, errors="coerce").max()
        return PLACEHOLDER if pd.isna(value) else float(value)
    except Exception:  # noqa: BLE001
        return PLACEHOLDER


def _safe_argmax_value(df: pd.DataFrame, value_col: str, label_col: str) -> str:
    if value_col not in df.columns or label_col not in df.columns or df.empty:
        return PLACEHOLDER
    try:
        idx = pd.to_numeric(df[value_col], errors="coerce").idxmax()
        return PLACEHOLDER if pd.isna(idx) else str(df.loc[idx, label_col])
    except Exception:  # noqa: BLE001
        return PLACEHOLDER


def _safe_get(d: Any, key: str) -> Any:
    if isinstance(d, dict):
        return d.get(key, PLACEHOLDER)
    return PLACEHOLDER


def _row_get(row: pd.Series, key: str) -> Any:
    if key in row:
        value = row[key]
        try:
            if pd.isna(value):
                return PLACEHOLDER
        except (TypeError, ValueError):
            pass
        return value
    return PLACEHOLDER


def _best_ensemble_method(results: dict[str, Any]) -> dict[str, Any]:
    best_name = PLACEHOLDER
    best_r2 = -float("inf")
    for name, method in results.items():
        if not isinstance(method, dict):
            continue
        r2 = method.get("R2")
        try:
            if r2 is not None and float(r2) > best_r2:
                best_r2 = float(r2)
                best_name = name
        except (TypeError, ValueError):
            continue
    if best_name == PLACEHOLDER:
        return {"name": PLACEHOLDER, "R2": PLACEHOLDER}
    return {"name": best_name, "R2": best_r2}
