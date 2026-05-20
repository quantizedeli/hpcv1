"""
PFAZ 10 -- Master Thesis Integration (Sprint 14 REWRITE)
==========================================================

Tez derleme orkestratoru. v5.0.0 surumde "binding energy" / "nuclear radius"
icerikli yanlis konular ureten kod tabanli mantik vardi; Sprint 14'te
manyetik moment (MM) ve kuadrupol moment (QM) odakli yeni surume gecildi.

Yeni mimari:
- 6 chapter (Giris, Literatur, Yontem, Bulgular, Tartisma, Sonuc) + 3-4 appendix
- PFAZ10DataReader ile gercek PFAZ2-13 ciktilarini okur
- Graceful fallback: TRUBA cikislari yoksa PLACEHOLDER kullanir
- ComprehensiveContentGenerator + ChapterGenerator + DiscussionConclusionGenerator
  ayri sorumluluk modullerini orkestre eder

Backwards-compatible API:
- MasterThesisIntegration(project_dir, output_dir, pfaz_outputs, metadata)
- execute_full_pipeline(compile_pdf=False)

Yazim: 2026-05-14 (Sprint 14)
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from .pfaz10_chapter_generator import ChapterGenerator
from .pfaz10_content_generator import ComprehensiveContentGenerator
from .pfaz10_data_reader import PFAZ10DataReader
from .pfaz10_discussion_conclusion import DiscussionConclusionGenerator

logger = logging.getLogger(__name__)


DEFAULT_METADATA = {
    "title": "Makine Ogrenmesi ve ANFIS Yontemleri ile Nukleer Momentlerin Tahmini",
    "title_en": "Machine Learning and ANFIS-Based Prediction of Nuclear Moments",
    "subtitle": "267 Izotop Uzerinde Manyetik Dipol ve Elektrik Kuadrupol Moment Tahmini",
    "author": "Research Student",
    "supervisor": "Prof. Supervisor Name",
    "university": "University Name",
    "department": "Department of Physics",
    "thesis_type": "Doctor of Philosophy",
    "language": "Turkish",
}


class MasterThesisIntegration:
    """PFAZ 10 ana orkestratoru -- Sprint 14 REWRITE.

    Args:
        project_dir: Proje kok dizini (str veya Path). DataReader bu dizini kullanir.
        output_dir: PFAZ10 cikis dizini (genelde `outputs/thesis_compilation/`).
        pfaz_outputs: PFAZ adi -> dizin yolu haritasi (opsiyonel).
        metadata: Tez metadata sozlugu (title, author, vs.).
    """

    def __init__(
        self,
        project_dir: str | Path,
        output_dir: str | Path,
        pfaz_outputs: dict[str, str | Path] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.project_dir = Path(project_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pfaz_outputs = pfaz_outputs or {}
        self.metadata: dict[str, Any] = {**DEFAULT_METADATA, **(metadata or {})}

        # Alt dizinler
        self.chapters_dir = self.output_dir / "chapters"
        self.figures_dir = self.output_dir / "figures"
        self.tables_dir = self.output_dir / "tables"
        self.bib_dir = self.output_dir / "bibliography"
        for sub in (self.chapters_dir, self.figures_dir, self.tables_dir, self.bib_dir):
            sub.mkdir(parents=True, exist_ok=True)

        # Bilesenler
        self.reader = PFAZ10DataReader(self.project_dir, pfaz_outputs)
        # BUG-C FIX (Sprint 17): results_dir=project_dir/"outputs" yanlistı.
        # project_dir zaten output_dir (scratch) oldugu icin fazladan /outputs ekliyordu.
        # Dogru: results_dir=project_dir (yani /arf/scratch/ahmacar/hpcv1_outputs)
        self.content_gen = ComprehensiveContentGenerator(
            results_dir=self.project_dir,
            output_dir=self.chapters_dir,
            project_dir=self.project_dir,
        )
        self.chapter_gen = ChapterGenerator(
            thesis_md_dir=self.project_dir / "thesis",
            output_dir=self.chapters_dir,
        )

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def execute_full_pipeline(self, compile_pdf: bool = False) -> dict[str, Any]:
        """Tum tez derleme akisini calistirir.

        Args:
            compile_pdf: True ise `latexmk`/`pdflatex` ile PDF derler.

        Returns:
            Calistirma raporu (dict).
        """
        logger.info("[PFAZ10] === Sprint 14 REWRITE: thesis compilation basliyor ===")
        report: dict[str, Any] = {
            "version": "6.0.0",
            "started_at": datetime.now().isoformat(),
            "metadata": self.metadata,
            "steps": {},
        }

        # 1) Veri okuma
        data = self.reader.read_all()
        report["steps"]["data_read"] = {
            "read_count": data["meta"]["read_count"],
            "fallback_count": data["meta"]["fallback_count"],
        }

        # 2) Sekilleri kopyala (PFAZ8 -> figures/)
        copied_figures = self._copy_figures()
        report["steps"]["figures_copied"] = len(copied_figures)

        # 3) Bolumleri uret
        chapters_written = self._generate_chapters(data)
        report["steps"]["chapters_written"] = {
            name: str(path.relative_to(self.output_dir))
            for name, path in chapters_written.items()
        }

        # 4) Bibliyografya yaz
        bib_path = self._write_bibliography()
        report["steps"]["bibliography"] = str(bib_path.relative_to(self.output_dir))

        # 5) main.tex ana dokuman
        main_tex_path = self._write_main_tex(chapters_written)
        report["steps"]["main_tex"] = str(main_tex_path.relative_to(self.output_dir))

        # 6) Compile script (Windows .bat + Unix .sh)
        compile_scripts = self._write_compile_scripts()
        report["steps"]["compile_scripts"] = [str(p.relative_to(self.output_dir)) for p in compile_scripts]

        # 7) Kalite kontrolu
        qc = self._quality_check(chapters_written, main_tex_path)
        report["steps"]["quality_check"] = qc

        # 8) Opsiyonel PDF derleme
        if compile_pdf:
            compile_result = self._compile_pdf(main_tex_path)
            report["steps"]["pdf_compile"] = compile_result

        report["finished_at"] = datetime.now().isoformat()
        report["status"] = "ok"

        # Rapor JSON olarak kaydet
        report_path = self.output_dir / "execution_report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("[PFAZ10] === Tamamlandi: %s ===", report_path)
        return report

    # ---------------------------------------------------------------------
    # Adim 1-7 (private)
    # ---------------------------------------------------------------------

    def _copy_figures(self) -> list[Path]:
        """PFAZ8 ciktilarindan figures/ dizinine PNG kopyalar."""
        copied: list[Path] = []
        visualizations_dir = self._resolve_pfaz_dir("visualizations", "visualizations")
        if not visualizations_dir or not visualizations_dir.exists():
            logger.warning("[PFAZ10] PFAZ8 visualizations dizini yok: %s", visualizations_dir)
            return copied

        try:
            for png in visualizations_dir.rglob("*.png"):
                dest = self.figures_dir / png.name
                if dest.exists():
                    continue
                shutil.copy2(png, dest)
                copied.append(dest)
        except Exception as exc:  # noqa: BLE001
            logger.warning("[PFAZ10] Figure kopyalama hatasi: %s", exc)
        return copied

    def _generate_chapters(self, data: dict[str, Any]) -> dict[str, Path]:
        """6 chapter + abstract LaTeX dosyalarini uretir."""
        outputs: dict[str, Path] = {}

        # ComprehensiveContentGenerator (abstract + chapter 1, 3, 4)
        content_outputs = self.content_gen.generate_all_chapters()
        outputs.update(content_outputs)

        # ChapterGenerator (chapter 2 -- literatur)
        outputs["chapter2"] = self.chapter_gen.generate_literature_chapter()

        # DiscussionConclusionGenerator (chapter 5 + 6)
        disc_gen = DiscussionConclusionGenerator(
            chapters_dir=self.chapters_dir,
            results_summary=data,
        )
        outputs["chapter5"] = disc_gen.generate_chapter5_discussion()
        outputs["chapter6"] = disc_gen.generate_chapter6_conclusion()

        return outputs

    def _write_bibliography(self) -> Path:
        """references.bib yazar (literatur md'deki atiflara dayanir)."""
        bib_path = self.bib_dir / "references.bib"
        # Sprint 14: zarif fallback -- ileride literatur md'den otomatik uret
        if bib_path.exists():
            return bib_path
        bib_content = (
            "% references.bib -- Sprint 14 STUB\n"
            "% Tam BibTeX kayitlari literatur md (Atif Listesi) icinden uretilecektir.\n"
            "% Su an placeholder -- el ile veya bib-generation script ile doldurulmali.\n\n"
            "@article{ref1,\n"
            "  author  = {Stone, N. J.},\n"
            "  title   = {Table of nuclear magnetic dipole and electric quadrupole moments},\n"
            "  journal = {At. Data Nucl. Data Tables},\n"
            "  volume  = {90},\n"
            "  pages   = {75--176},\n"
            "  year    = {2005},\n"
            "  doi     = {10.1016/j.adt.2005.04.001}\n"
            "}\n\n"
            "@article{ref6,\n"
            "  author  = {Utama, R. and Piekarewicz, J. and Prosperous, H. B.},\n"
            "  title   = {Nuclear mass predictions: A Bayesian neural network approach},\n"
            "  journal = {Phys. Rev. C},\n"
            "  volume  = {93},\n"
            "  pages   = {014311},\n"
            "  year    = {2016},\n"
            "  doi     = {10.1103/PhysRevC.93.014311}\n"
            "}\n\n"
            "@article{ref15,\n"
            "  author  = {Jang, J.-S. R.},\n"
            "  title   = {{ANFIS}: Adaptive-network-based fuzzy inference system},\n"
            "  journal = {IEEE Trans. Syst., Man, Cybern.},\n"
            "  volume  = {23},\n"
            "  pages   = {665--685},\n"
            "  year    = {1993},\n"
            "  doi     = {10.1109/21.256541}\n"
            "}\n\n"
            "@article{ref40,\n"
            "  author  = {Efron, B. and Tibshirani, R. J.},\n"
            "  title   = {An Introduction to the Bootstrap},\n"
            "  publisher = {Chapman \\& Hall},\n"
            "  year    = {1993}\n"
            "}\n"
        )
        bib_path.write_text(bib_content, encoding="utf-8")
        return bib_path

    def _write_main_tex(self, chapters: dict[str, Path]) -> Path:
        """Ana main.tex dokumanini yazar (6 chapter + appendix yapisi).

        `chapters` haritasi gercek dosya yollarini icerir; varsayilan
        adlandirma kullanilamadiginda buradaki yollardan input uretilir.
        """
        main_tex = self.output_dir / "main.tex"
        title = self.metadata.get("title", DEFAULT_METADATA["title"])
        author = self.metadata.get("author", DEFAULT_METADATA["author"])
        supervisor = self.metadata.get("supervisor", DEFAULT_METADATA["supervisor"])
        university = self.metadata.get("university", DEFAULT_METADATA["university"])
        department = self.metadata.get("department", DEFAULT_METADATA["department"])
        thesis_type = self.metadata.get("thesis_type", DEFAULT_METADATA["thesis_type"])

        order_keys = ("chapter1", "chapter2", "chapter3", "chapter4", "chapter5", "chapter6")
        default_filenames = {
            "chapter1": "chapter1_giris.tex",
            "chapter2": "chapter2_literatur.tex",
            "chapter3": "chapter3_metodoloji.tex",
            "chapter4": "chapter4_sonuclar.tex",
            "chapter5": "chapter5_tartisma.tex",
            "chapter6": "chapter6_sonuc.tex",
        }
        chapter_inputs: list[str] = []
        for key in order_keys:
            path = chapters.get(key)
            if path is not None and path.exists():
                rel = path.relative_to(self.output_dir).as_posix()
            else:
                rel = f"chapters/{default_filenames[key]}"
            chapter_inputs.append(f"\\input{{{rel}}}")

        chapters_block = "\n".join(chapter_inputs)

        content = (
            "% main.tex -- Sprint 14 REWRITE\n"
            "% Otomatik uretilmistir; MasterThesisIntegration v6.0.0\n"
            f"% Olusturma: {datetime.now().isoformat()}\n\n"
            "\\documentclass[12pt,a4paper,oneside]{report}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\usepackage[T1]{fontenc}\n"
            "\\usepackage[turkish,english]{babel}\n"
            "\\usepackage{amsmath, amssymb}\n"
            "\\usepackage{graphicx}\n"
            "\\usepackage{booktabs}\n"
            "\\usepackage{longtable}\n"
            "\\usepackage{hyperref}\n"
            "\\usepackage{geometry}\n"
            "\\geometry{a4paper, margin=2.5cm}\n"
            "\\usepackage{caption}\n\n"
            "% IEEE-style biblio\n"
            "\\usepackage[backend=biber, style=ieee]{biblatex}\n"
            "\\addbibresource{bibliography/references.bib}\n\n"
            "% Ozet ve abstract ortamlari\n"
            "\\newenvironment{ozet}{\\chapter*{Ozet}}{}\n"
            "\\renewenvironment{abstract}{\\chapter*{Abstract}}{}\n\n"
            f"\\title{{{title}}}\n"
            f"\\author{{{author}}}\n"
            f"\\date{{\\today}}\n\n"
            "\\begin{document}\n"
            "\\selectlanguage{turkish}\n\n"
            "\\begin{titlepage}\n"
            "\\centering\n"
            "\\vspace*{2cm}\n"
            f"{{\\Large \\textbf{{{university}}}\\\\[0.5cm]}}\n"
            f"{{\\large {department}\\\\[2cm]}}\n"
            f"{{\\LARGE \\textbf{{{title}}}\\\\[1.5cm]}}\n"
            f"{{\\large {thesis_type} Tezi\\\\[0.5cm]}}\n"
            f"{{\\large {author}\\\\[0.5cm]}}\n"
            f"{{\\large Danisman: {supervisor}\\\\[2cm]}}\n"
            "{\\large \\today}\n"
            "\\end{titlepage}\n\n"
            "\\input{chapters/00_abstract.tex}\n\n"
            "\\tableofcontents\n"
            "\\listoffigures\n"
            "\\listoftables\n\n"
            f"{chapters_block}\n\n"
            "\\printbibliography\n\n"
            "\\end{document}\n"
        )
        main_tex.write_text(content, encoding="utf-8")
        return main_tex

    def _write_compile_scripts(self) -> list[Path]:
        """compile.bat (Windows) ve compile.sh (Unix) scriptleri."""
        bat_path = self.output_dir / "compile.bat"
        sh_path = self.output_dir / "compile.sh"

        bat_path.write_text(
            "@echo off\n"
            "REM main.tex PDF derleme scripti (Windows)\n"
            "cd /d %~dp0\n"
            "pdflatex main.tex\n"
            "biber main\n"
            "pdflatex main.tex\n"
            "pdflatex main.tex\n"
            "echo Tamam: main.pdf\n",
            encoding="utf-8",
        )
        sh_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -e\n"
            "cd \"$(dirname \"$0\")\"\n"
            "pdflatex main.tex\n"
            "biber main\n"
            "pdflatex main.tex\n"
            "pdflatex main.tex\n"
            "echo \"Tamam: main.pdf\"\n",
            encoding="utf-8",
        )
        try:
            sh_path.chmod(0o755)
        except OSError:
            pass
        return [bat_path, sh_path]

    def _quality_check(self, chapters: dict[str, Path], main_tex: Path) -> dict[str, Any]:
        """Beklenen dosyalarin var oldugunu dogrula."""
        missing: list[str] = []
        for name in ("abstract", "chapter1", "chapter2", "chapter3", "chapter4", "chapter5", "chapter6"):
            if name not in chapters or not chapters[name].exists():
                missing.append(name)
        return {
            "main_tex_exists": main_tex.exists(),
            "missing_chapters": missing,
            "n_chapters": len([p for p in chapters.values() if p.exists()]),
        }

    def _compile_pdf(self, main_tex: Path) -> dict[str, Any]:
        """latexmk veya pdflatex ile PDF derleme."""
        result: dict[str, Any] = {"attempted": True, "success": False}
        cmd_candidates = [
            ["latexmk", "-pdf", "-interaction=nonstopmode", str(main_tex)],
            ["pdflatex", "-interaction=nonstopmode", str(main_tex)],
        ]
        for cmd in cmd_candidates:
            try:
                proc = subprocess.run(
                    cmd,
                    cwd=self.output_dir,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                result["cmd"] = cmd[0]
                result["returncode"] = proc.returncode
                if proc.returncode == 0:
                    result["success"] = True
                    break
                logger.warning("[PFAZ10] %s basarisiz (rc=%d)", cmd[0], proc.returncode)
            except FileNotFoundError:
                logger.warning("[PFAZ10] %s bulunamadi (kurulu degil)", cmd[0])
                continue
            except Exception as exc:  # noqa: BLE001
                logger.warning("[PFAZ10] %s hata: %s", cmd[0], exc)
                continue
        return result

    # ---------------------------------------------------------------------
    # Yardimcilar
    # ---------------------------------------------------------------------

    def _resolve_pfaz_dir(self, key: str, fallback_subpath: str) -> Path:
        """pfaz_outputs inject haritasinda anahtarini ara, yoksa default doner.

        BUG-F FIX (Sprint 17): Integer key lookup duzeltildi ve fallback'teki
        'outputs/' prefix kaldirildi. project_dir zaten output_dir (scratch) oldugu icin
        'outputs/visualizations' -> '/scratch/.../outputs/visualizations' yanlistir.
        Dogru fallback: project_dir / 'visualizations' (prefix'siz).
        """
        if key in self.pfaz_outputs:
            return Path(self.pfaz_outputs[key])
        # int anahtar destegi (main.py'da {8: Path('.../visualizations')} seklinde gelir)
        # key='visualizations' ise pfaz_outputs[8]'in son parcasina bak
        for k, v in self.pfaz_outputs.items():
            try:
                if Path(v).name == key or str(k) == key:
                    return Path(v)
            except Exception:
                pass
        # BUG-F FIX: fallback_subpath'ten 'outputs/' prefix'ini cikar
        clean = fallback_subpath
        if clean.startswith("outputs/"):
            clean = clean[len("outputs/"):]
        return self.project_dir / clean


# Backwards-compatible aliases
MasterThesisIntegrationV6 = MasterThesisIntegration
