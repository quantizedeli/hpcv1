"""
PFAZ 10 -- Comprehensive Content Generator (Sprint 14 REWRITE)
================================================================

Tez bolumleri icin LaTeX icerigi ureten ana sinif. Onceki surumde
"binding energy" / "nuclear radius" referansli yanlis konular vardi;
Sprint 14'te tamamen yeniden yazildi: tum metinler manyetik moment (MM)
ve kuadrupol moment (QM) odakli.

Veri kaynagi: pfaz10_data_reader.PFAZ10DataReader (TRUBA ciktilari).
Veri eksikse `\\textit{Veri TRUBA'dan beklenmektedir}` placeholder'i kullanir.

Yazim: 2026-05-14 (Sprint 14)
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .pfaz10_data_reader import PFAZ10DataReader, PLACEHOLDER

logger = logging.getLogger(__name__)


PLACEHOLDER_LATEX = "\\textit{Veri TRUBA'dan beklenmektedir}"


def _fmt(value: Any, ndigits: int = 4) -> str:
    """Sayisal degeri LaTeX'e uygun bicimde formatlar; eksik veri icin placeholder."""
    if value is None or value == PLACEHOLDER:
        return PLACEHOLDER_LATEX
    try:
        return f"{float(value):.{ndigits}f}"
    except (TypeError, ValueError):
        return str(value)


class ComprehensiveContentGenerator:
    """Tez bolumleri icin LaTeX icerigi ureten ana sinif.

    Args:
        results_dir: PFAZ ciktilari ana dizini (genelde `outputs/`).
        output_dir: Yazilacak `.tex` chapter dosyalarinin hedef dizini.
        project_dir: Proje kok dizini (DataReader icin).
    """

    TARGETS = ("MM", "QM")

    def __init__(
        self,
        results_dir: str | Path = "outputs",
        output_dir: str | Path = "outputs/thesis_compilation/chapters",
        project_dir: str | Path | None = None,
    ) -> None:
        self.results_dir = Path(results_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.project_dir = Path(project_dir) if project_dir else self.results_dir.parent

        self.reader = PFAZ10DataReader(self.project_dir)
        self.data: dict[str, Any] = {}

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def generate_all_chapters(self) -> dict[str, Path]:
        """6 bolum + ozet/abstract LaTeX dosyalarini uretir.

        Returns:
            Bolum adi -> dosya yolu sozlugu.
        """
        self.data = self.reader.read_all()
        outputs: dict[str, Path] = {}

        outputs["abstract"] = self._write("00_abstract.tex", self._render_abstract())
        outputs["chapter1"] = self._write("chapter1_giris.tex", self._render_chapter1_introduction())
        outputs["chapter3"] = self._write("chapter3_metodoloji.tex", self._render_chapter3_methodology())
        outputs["chapter4"] = self._write("chapter4_sonuclar.tex", self._render_chapter4_results())

        logger.info(
            "[CONTENT-GEN] %d bolum yazildi; read=%d, fallback=%d",
            len(outputs),
            self.data["meta"]["read_count"],
            self.data["meta"]["fallback_count"],
        )
        return outputs

    def _write(self, filename: str, content: str) -> Path:
        path = self.output_dir / filename
        path.write_text(content, encoding="utf-8")
        return path

    # ---------------------------------------------------------------------
    # Bolum Uretimi (LaTeX)
    # ---------------------------------------------------------------------

    def _render_abstract(self) -> str:
        ai_perf = self.data.get("ai_performance", {})
        anfis_perf = self.data.get("anfis_performance", {})
        best_ai_mm = self._best_model(ai_perf.get("MM", {}))
        best_ai_qm = self._best_model(ai_perf.get("QM", {}))
        anfis_mm_r2 = anfis_perf.get("MM", {}).get("best_r2", PLACEHOLDER)
        anfis_qm_r2 = anfis_perf.get("QM", {}).get("best_r2", PLACEHOLDER)

        tr_summary = (
            "Bu tezde, 267 nukleer izotop icin manyetik dipol moment (MM) ve "
            "elektrik kuadrupol moment (QM) tahmininde makine ogrenmesi (RF, XGBoost, "
            "LightGBM, CatBoost, SVR, DNN) ile uyumlu noro-bulanik cikarim "
            "sistemi (ANFIS, 8 konfigurasyon) yontemleri karsilastirilmistir. "
            f"En iyi yapay zeka sonuclari MM icin {_fmt(best_ai_mm[1])} (R\\textsuperscript{{2}}), "
            f"QM icin {_fmt(best_ai_qm[1])} duzeyinde elde edilmis; en iyi ANFIS "
            f"konfigurasyonu MM icin {_fmt(anfis_mm_r2)}, QM icin {_fmt(anfis_qm_r2)} "
            "R\\textsuperscript{2} degerine ulasmistir. Ozellik muhendisliginde fizik "
            "tabanli yaklasim benimsenmis; SEMF, Schmidt momenti ve sihirli sayi "
            "(magic\\_character) ozellikleri girdi vektorune dahil edilerek kabuk "
            "kapanmasi bolgelerindeki suremsizlikler modellenmistir. Belirsizlik "
            "analizi K=1000 Monte Carlo ile %95 guven aralig olarak raporlanmis, "
            "model karsilastirmasi paired t-test ve Bootstrap CI yontemleriyle "
            "istatistiksel anlamlilik temelinde dogrulanmistir."
        )

        en_summary = (
            "This thesis compares machine learning algorithms (RF, XGBoost, LightGBM, "
            "CatBoost, SVR, DNN) and adaptive neuro-fuzzy inference systems (ANFIS, "
            "eight configurations) for predicting nuclear magnetic dipole (MM) and "
            "electric quadrupole (QM) moments across 267 isotopes. The best machine "
            f"learning result reaches R\\textsuperscript{{2}} = {_fmt(best_ai_mm[1])} for MM and "
            f"{_fmt(best_ai_qm[1])} for QM; the best ANFIS configuration achieves "
            f"{_fmt(anfis_mm_r2)} for MM and {_fmt(anfis_qm_r2)} for QM. A physics-informed "
            "feature engineering scheme is adopted, integrating SEMF terms, Schmidt "
            "moments, and magic-number features to capture shell-closure "
            "discontinuities. Predictive uncertainty is quantified through K=1000 "
            "Monte Carlo bootstrap (95\\% CI), and model comparisons are validated "
            "with paired t-tests and Bootstrap confidence intervals."
        )

        return (
            "% Ozet (TR) / Abstract (EN) -- Sprint 14 REWRITE\n\n"
            "\\begin{ozet}\n"
            "\\textbf{Anahtar Kelimeler:} nukleer manyetik moment, kuadrupol moment, makine "
            "ogrenmesi, ANFIS, Monte Carlo belirsizlik analizi, sihirli sayi, fizik "
            "tabanli ozellik muhendisligi\\\\[1ex]\n\n"
            f"{tr_summary}\n"
            "\\end{ozet}\n\n"
            "\\begin{abstract}\n"
            "\\textbf{Keywords:} nuclear magnetic moment, quadrupole moment, machine "
            "learning, ANFIS, Monte Carlo uncertainty, magic numbers, physics-informed "
            "feature engineering\\\\[1ex]\n\n"
            f"{en_summary}\n"
            "\\end{abstract}\n"
        )

    def _render_chapter1_introduction(self) -> str:
        return (
            "% Bolum 1: Giris -- Sprint 14 REWRITE\n"
            "\\chapter{Giris}\n"
            "\\label{ch:giris}\n\n"
            "\\section{Motivasyon}\n"
            "Nukleer manyetik dipol moment (MM) ve elektrik kuadrupol moment (QM), "
            "bir cekirdegin temel durumdaki spin dagilimi, deformasyon yapisi ve tek "
            "parcacik konfigurasyonu hakkinda dogrudan bilgi tasiyan iki nicelliktir. "
            "Bu degerler hem temel nukleer yapi calismalari hem de kabuk modeli, "
            "kollektif model ve karma yaklasimlarin dogrulanmasi acisindan kritik "
            "oneme sahiptir. Deneysel olcum kapasitesi kararlilik vadisi cevresindeki "
            "izotoplarla sinirli kaldigi icin, henuz olculmemis cekirdekler icin "
            "guvenilir tahmin uretebilen model tabanli yaklasimlar arastirma "
            "literaturunde gittikce daha fazla yer kaplamaktadir.\n\n"
            "\\section{Problem Tanimi}\n"
            "Bu calismanin temel sorusu sudur: \\textit{Deneysel manyetik ve kuadrupol "
            "moment verileri ile egitilen makine ogrenmesi ve ANFIS modelleri, henuz "
            "olculmemis cekirdekler icin guvenilir tahmin uretebilir mi? Hangi "
            "modeller bu amac icin en ustun performansi sergiler?}\n\n"
            "Mevcut deneysel veri tabani 267 izotop icin tutarli MM ve QM olcumleri "
            "icermektedir. Bu boyut, makine ogrenmesi acisindan kucuk orneklem "
            "siniflandirmasina girer; bu nedenle hem ozellik muhendisliginde fizik "
            "bilgisinin agir basmasi hem de model seciminde asiri uyumu erken "
            "tespit eden filtrelerin uygulanmasi zorunludur.\n\n"
            "\\section{Tezin Katkilari}\n"
            "Bu tez literatuere uc temel eksende katki sunmaktadir: (i) 267 "
            "cekirdekli kapsamli bir veri seti uzerinde MM ve QM hedeflerinin "
            "dogrudan birincil cikti olarak konumlandirildigi bir makine ogrenmesi "
            "ve ANFIS karsilastirma cercevesi, (ii) fizik tabanli ozellik "
            "muhendisligi yoluyla sihirli sayi cevresindeki suremsizliklerin modele "
            "dahil edilmesi, (iii) K=1000 Monte Carlo ornekleme ile top-50 model "
            "uzerinde belirsizlik niceleme ve Bootstrap CI ile istatistiksel "
            "dogrulama. Bu uc katki bir araya geldiginde tez, manyetik moment ve "
            "kuadrupol moment tahmininde model tabanli yaklasimlarin "
            "kullanilabilirligini sistematik bir cerceve icinde ortaya koymaktadir.\n\n"
            "\\section{Tezin Organizasyonu}\n"
            "Tezin geri kalani su sekilde duzenlenmistir. Bolum~\\ref{ch:literatur} "
            "nukleer moment olcumleri ve makine ogrenmesi tabanli nukleer fizik "
            "calismalarinin kapsamli bir incelemesini sunar. Bolum~\\ref{ch:yontem} "
            "veri seti, ozellik muhendisligi, model mimarileri ve istatistiksel "
            "dogrulama yontemlerini detaylandirir. Bolum~\\ref{ch:bulgular} egitim "
            "ve dogrulama sonuclarini, model karsilastirmasini ve belirsizlik "
            "analizini sunar. Bolum~\\ref{ch:tartisma} bulgularin yorumlanmasi ve "
            "sinirliliklarini ele alir; Bolum~\\ref{ch:sonuc} ise temel sonuclari "
            "ve ileride yapilacak calismalari ozetler.\n"
        )

    def _render_chapter3_methodology(self) -> str:
        return (
            "% Bolum 3: Yontem -- Sprint 14 REWRITE\n"
            "\\chapter{Yontem}\n"
            "\\label{ch:yontem}\n\n"
            "\\section{Veri Seti}\n"
            "Bu calismada Stone (2005) derlemesi ve guncelleyici tablolarindan "
            "(2016, 2019) elde edilen 267 izotoplik bir veri seti kullanilmaktadir. "
            "Her bir kayit; proton sayisi (Z), notron sayisi (N), kutle numarasi "
            "(A), spin (J), parite ve deneysel olarak olculen MM ile QM degerlerini "
            "icermektedir.\n\n"
            "\\section{Ozellik Muhendisligi}\n"
            "Ham 12 sutunlu veri, fizik tabanli ozellik mhendisligi katmaniyla "
            "44 ozellige genisletilmektedir. SEMF (Bethe-Weizsacker) terimleri "
            "(hacim, yuzey, Coulomb, asimetri, ciftlenme), nukleer yaricap "
            "$R = R_0 A^{1/3}$, notron ve proton ayrilma enerjileri $S_n, S_p$, "
            "kabuk model ozellikleri (magic\\_character, $d_{Z,\\mathrm{magic}}$, "
            "$d_{N,\\mathrm{magic}}$), deformasyon parametresi $\\beta_2$ ve "
            "Schmidt moment degerleri girdi vektorune dahil edilir. Bu ozellikler "
            "sihirli sayi (2, 8, 20, 28, 50, 82, 126) cevresindeki suremsizlikleri "
            "modele dogrudan tanitir; aksi takdirde standart makine ogrenmesi "
            "algoritmalari yerel sureklilik varsayimi nedeniyle bu bolgelerde "
            "sistematik hata yapacaktir.\n\n"
            "\\section{Yapay Zeka Modelleri}\n"
            "Alti makine ogrenmesi algoritmasi sistematik olarak karsilastirilmistir: "
            "Random Forest (RF), XGBoost, LightGBM, CatBoost, Support Vector "
            "Regression (SVR) ve Derin Sinir Aglari (DNN). Toplam 50 konfigurasyon "
            "(20 RF + 15 XGBoost + 15 DNN) ve uc varsayilan model (LightGBM, "
            "CatBoost, SVR) 848 farkli veri seti varyaninda egitilmistir. "
            "Model kabul kriteri olarak cift R\\textsuperscript{2} filtresi uygulanmistir: "
            "$\\mathrm{val}\\_R^2 \\geq 0.5$, $\\mathrm{cv}\\_R^2 \\geq 0.0$ ve "
            "$\\mathrm{train}\\_R^2 - \\mathrm{cv}\\_R^2 < 0.6$ esiklerini "
            "saglayan modeller kaydedilmistir. Bu filtre asiri uyumun erken "
            "tespitini saglar (Shang ve ark., 2022; Utama ve ark., 2016).\n\n"
            "\\section{ANFIS Modeli}\n"
            "Birinci dereceden Takagi-Sugeno ANFIS yapisi, dort uyelik fonksiyonu "
            "tipi (ucgen, Gauss-2, Gauss-3, Bell) ve iki baslangic stratejisi "
            "(grid partitioning, K-Means tabanli subtractive clustering) "
            "kombinasyonunda sekiz farkli konfigurasyon olarak uygulanmistir. "
            "Hibrit ogrenme algoritmasi olarak en kucuk kareler tahmini (EKKT) "
            "konsekant parametrelerin kapali form cozumunu, L-BFGS-B optimizasyonu "
            "ise premis parametrelerinin gradyan tabanli iyilestirmesini yapar.\n\n"
            "\\section{Adaptif Dataset Secimi}\n"
            "ANFIS egitiminde tier tabanli adaptif veri seti secimi kullanilmistir: "
            "PFAZ02 R\\textsuperscript{2} sonuclarina gore Top ($R^2 \\geq 0.90$), Mid ($0.80 \\leq R^2 < 0.90$) "
            "ve Low ($R^2 < 0.80$) katmanlari belirlenip her bir hedef icin "
            "Top=50, Mid=50, Low=100 olmak uzere 200 veri seti secilmistir. "
            "Kotalarin doldurulamadigi durumlarda eksik kapasite round-robin "
            "esasiyla diger katmanlara dagitilarak hedef secim sayisi garanti "
            "altina alinir.\n\n"
            "\\section{Ensemble Yontemler}\n"
            "Bireysel model performansini asmak amaciyla dort agirlikli oylama "
            "(Simple, WeightedR\\textsuperscript{2}, WeightedRMSE, WeightedInvError) ve dort "
            "yiglama varyanti (Ridge, Lasso, RF, GBM meta-modelleri) "
            "karsilastirilmistir. Yiglama yontemi out-of-fold (OOF) tahminler "
            "uretmek icin 5-katli capraz dogrulama kullanir; bu sayede meta-model "
            "egitim setine hic dokunmamis tahminlerle egitilir.\n\n"
            "\\section{Istatistiksel Dogrulama}\n"
            "Model karsilastirmasi paired t-test ve Wilcoxon signed-rank test ile "
            "yapilir. Etki buyuklugu Cohen's d ile olculur; $\\alpha = 0.05$ "
            "anlamlilik esigi uygulanir. Belirsizlik niceleme K=1000 Monte Carlo "
            "Bootstrap ile gerceklestirilir; tum modeller icin %95 guven aralig "
            "$[P_{2.5}, P_{97.5}]$ yuzdelik dilim yontemiyle raporlanir "
            "(Efron ve Tibshirani, 1993). MC Dropout DNN modelleri icin "
            "100 ornek ile uygulanir (Gal ve Ghahramani, 2016).\n"
        )

    def _render_chapter4_results(self) -> str:
        ai_perf = self.data.get("ai_performance", {})
        anfis_perf = self.data.get("anfis_performance", {})
        bootstrap = self.data.get("bootstrap_ci", {})
        ai_vs = self.data.get("ai_vs_anfis_tests", {})
        ensemble = self.data.get("ensemble", {})
        mc = self.data.get("monte_carlo", {})
        automl = self.data.get("automl", {})

        ai_rows = self._ai_table_rows(ai_perf)
        anfis_rows = self._anfis_table_rows(anfis_perf)

        return (
            "% Bolum 4: Bulgular -- Sprint 14 REWRITE (gercek veri PFAZ10DataReader)\n"
            "\\chapter{Bulgular}\n"
            "\\label{ch:bulgular}\n\n"
            "\\section{AI Model Performansi}\n"
            "Tablo~\\ref{tab:ai-performance} her makine ogrenmesi algoritmasinin "
            "ortalama R\\textsuperscript{2}, RMSE ve MAE degerlerini MM ve QM hedefleri "
            "icin sunar.\n\n"
            "\\begin{table}[h]\n"
            "\\centering\n"
            "\\caption{AI Model Performans Ozeti}\n"
            "\\label{tab:ai-performance}\n"
            "\\begin{tabular}{lcccc}\n"
            "\\toprule\n"
            "Model & Hedef & R\\textsuperscript{2} & RMSE & N Konfig \\\\\n"
            "\\midrule\n"
            f"{ai_rows}"
            "\\bottomrule\n"
            "\\end{tabular}\n"
            "\\end{table}\n\n"
            "\\section{ANFIS Model Performansi}\n"
            "Sekiz farkli ANFIS konfigurasyonu MM ve QM hedefleri icin "
            "karsilastirilmistir. En iyi sonuclar Tablo~\\ref{tab:anfis-performance} "
            "altinda sunulmustur.\n\n"
            "\\begin{table}[h]\n"
            "\\centering\n"
            "\\caption{ANFIS En Iyi Konfigurasyon Sonuclari}\n"
            "\\label{tab:anfis-performance}\n"
            "\\begin{tabular}{lccc}\n"
            "\\toprule\n"
            "Hedef & En Iyi Konfig & En Iyi R\\textsuperscript{2} & Ortalama R\\textsuperscript{2} \\\\\n"
            "\\midrule\n"
            f"{anfis_rows}"
            "\\bottomrule\n"
            "\\end{tabular}\n"
            "\\end{table}\n\n"
            "\\section{Model Karsilastirmasi -- AI vs ANFIS}\n"
            f"PFAZ12 paired test sonuclarina gore toplam {ai_vs.get('n_tests', PLACEHOLDER)} "
            "veri seti varyaninda AI ve ANFIS yaklasimlarinin performansi "
            "karsilastirilmistir. Bootstrap CI dahilinde her iki yontemin "
            "R\\textsuperscript{2} ortalamasi ve %95 guven aralig "
            "Tablo~\\ref{tab:bootstrap-ci} altinda raporlanmistir.\n\n"
            "\\begin{table}[h]\n"
            "\\centering\n"
            "\\caption{Bootstrap CI Sonuclari (K=1000)}\n"
            "\\label{tab:bootstrap-ci}\n"
            "\\begin{tabular}{lccc}\n"
            "\\toprule\n"
            "Model & R\\textsuperscript{2} & CI alt & CI ust \\\\\n"
            "\\midrule\n"
            f"{self._bootstrap_table_rows(bootstrap)}"
            "\\bottomrule\n"
            "\\end{tabular}\n"
            "\\end{table}\n\n"
            "\\section{Saglamlik Analizi}\n"
            "Egitilen modellerin gurultu, outlier ve permutation testlerine "
            "dayanikligi PFAZ02 RobustnessTester yardimiyla olculmustur. "
            f"Toplam test edilen model sayisi: {self._safe_metric('robustness', 'n_models')}. "
            "Sonuclar tezde Sekil~\\ref{fig:robustness} ile sunulan model "
            "bazli noise tolerans grafigi uzerinden detaylandirilmistir.\n\n"
            "\\section{Topluluk Sonuclari}\n"
            f"Dort agirlikli oylama ve dort yiglama varyanti "
            f"({ensemble.get('n_methods', PLACEHOLDER)} yontem) karsilastirildiginda "
            f"en iyi performans \\textbf{{{ensemble.get('best_method', {}).get('name', PLACEHOLDER)}}} "
            f"ile R\\textsuperscript{{2}} = {_fmt(ensemble.get('best_method', {}).get('R2'))} "
            "duzeyinde elde edilmistir.\n\n"
            "\\section{Monte Carlo Belirsizlik Analizi}\n"
            f"267 cekirdek icin K=1000 Bootstrap ornekleme ile tahmin belirsizligi "
            f"hesaplanmistir. MM ortalama %95 CI genisligi: "
            f"{_fmt(mc.get('MM', {}).get('mean_ci_width'))}; QM icin: "
            f"{_fmt(mc.get('QM', {}).get('mean_ci_width'))}. "
            "Bootstrap orneklem sayisi N=1000, K=1000 standart deger olarak "
            "(Efron ve Tibshirani, 1993; Shang ve ark., 2022) literatur destegine "
            "sahiptir.\n\n"
            "\\section{AutoML Optimizasyonu}\n"
            f"PFAZ02'de R\\textsuperscript{{2}} < 0.90 olan modeller icin Optuna TPE "
            f"algoritmasiyla otomatik hiperparametre optimizasyonu uygulanmistir. "
            f"Toplam {automl.get('n_retrained', PLACEHOLDER)} model yeniden "
            f"egitilmis, ortalama iyilesme: "
            f"{_fmt(automl.get('mean_improvement'))} R\\textsuperscript{{2}} "
            f"birimi. Convergence grafigi Sekil~\\ref{{fig:automl}} ile sunulmustur.\n"
        )

    # ---------------------------------------------------------------------
    # Yardimci tablo uretme metodlari
    # ---------------------------------------------------------------------

    def _ai_table_rows(self, ai_perf: dict[str, Any]) -> str:
        if not ai_perf or "MM" not in ai_perf:
            return f"\\multicolumn{{5}}{{c}}{{{PLACEHOLDER_LATEX}}} \\\\\n"

        rows: list[str] = []
        for target in self.TARGETS:
            target_data = ai_perf.get(target, {})
            if not isinstance(target_data, dict):
                continue
            for model_name, stats in sorted(target_data.items()):
                if not isinstance(stats, dict):
                    continue
                rows.append(
                    f"{model_name} & {target} & {_fmt(stats.get('R2'))} & "
                    f"{_fmt(stats.get('RMSE'))} & {stats.get('n_configs', PLACEHOLDER)} \\\\"
                )
        return "\n".join(rows) + "\n" if rows else f"\\multicolumn{{5}}{{c}}{{{PLACEHOLDER_LATEX}}} \\\\\n"

    def _anfis_table_rows(self, anfis_perf: dict[str, Any]) -> str:
        rows: list[str] = []
        for target in self.TARGETS:
            target_data = anfis_perf.get(target, {})
            if not isinstance(target_data, dict):
                continue
            rows.append(
                f"{target} & {target_data.get('best_config', PLACEHOLDER)} & "
                f"{_fmt(target_data.get('best_r2'))} & "
                f"{_fmt(target_data.get('mean_r2'))} \\\\"
            )
        return "\n".join(rows) + "\n" if rows else f"\\multicolumn{{4}}{{c}}{{{PLACEHOLDER_LATEX}}} \\\\\n"

    def _bootstrap_table_rows(self, bootstrap: dict[str, Any]) -> str:
        models = bootstrap.get("models", {})
        if not isinstance(models, dict) or not models:
            return f"\\multicolumn{{4}}{{c}}{{{PLACEHOLDER_LATEX}}} \\\\\n"
        rows: list[str] = []
        for name, stats in list(models.items())[:10]:
            rows.append(
                f"{name} & {_fmt(stats.get('R2'))} & "
                f"{_fmt(stats.get('CI_lower'))} & "
                f"{_fmt(stats.get('CI_upper'))} \\\\"
            )
        return "\n".join(rows) + "\n"

    def _best_model(self, target_data: dict[str, Any]) -> tuple[str, Any]:
        """Hedef icin en yuksek R2'ye sahip model adi ve degerini doner."""
        if not isinstance(target_data, dict) or not target_data:
            return (PLACEHOLDER, PLACEHOLDER)
        best_name = PLACEHOLDER
        best_r2 = -float("inf")
        for name, stats in target_data.items():
            if not isinstance(stats, dict):
                continue
            r2 = stats.get("R2")
            try:
                if r2 is not None and r2 != PLACEHOLDER and float(r2) > best_r2:
                    best_r2 = float(r2)
                    best_name = name
            except (TypeError, ValueError):
                continue
        return (best_name, best_r2 if best_name != PLACEHOLDER else PLACEHOLDER)

    def _safe_metric(self, key: str, sub_key: str) -> Any:
        value = self.data.get(key, {})
        if isinstance(value, dict):
            return value.get(sub_key, PLACEHOLDER)
        return PLACEHOLDER


# Backwards-compatible alias used by some legacy callers
ContentGenerator = ComprehensiveContentGenerator
