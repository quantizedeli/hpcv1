"""
PFAZ 10 -- Chapter Generator (Sprint 14 REWRITE)
==================================================

Ozellikle Bolum 2 (Literatur Incelemesi) ve diger ekstra bolumlerin uretiminden
sorumludur. Bolum 2, projedeki `thesis/bolum-02-literatur-incelemesi.md`
dosyasindaki 177 satirlik IEEE atifli icerigi LaTeX'e donusturur.

Yazim: 2026-05-14 (Sprint 14)
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


PLACEHOLDER_LATEX = "\\textit{Veri TRUBA'dan beklenmektedir}"


class ChapterGenerator:
    """Literatur ve diger zenginlestirilmis bolumlerin LaTeX urecisi.

    Args:
        thesis_md_dir: `thesis/` dizinin yolu (literatur markdown dosyasinin bulundugu).
        output_dir: Yazilacak chapter `.tex` dosyalarinin hedef dizini.
    """

    LITERATURE_FILENAME = "bolum-02-literatur-incelemesi.md"

    def __init__(
        self,
        thesis_md_dir: str | Path = "thesis",
        output_dir: str | Path = "outputs/thesis_compilation/chapters",
        chapters_dir: str | Path | None = None,
        results_summary: dict[str, Any] | None = None,
    ) -> None:
        # Backwards-compatible parametre desteği
        self.thesis_md_dir = Path(thesis_md_dir)
        self.output_dir = Path(chapters_dir or output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = results_summary or {}

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def generate_literature_chapter(self) -> Path:
        """Bolum 2 (Literatur Incelemesi) LaTeX dosyasini uretir."""
        md_path = self.thesis_md_dir / self.LITERATURE_FILENAME
        if not md_path.exists():
            logger.warning("[CHAPTER-GEN] Literatur md yok: %s", md_path)
            content = self._stub_literature_chapter()
        else:
            md_text = md_path.read_text(encoding="utf-8")
            content = self._md_to_latex_literature(md_text)

        out_path = self.output_dir / "chapter2_literatur.tex"
        out_path.write_text(content, encoding="utf-8")
        logger.info("[CHAPTER-GEN] Bolum 2 yazildi: %s", out_path)
        return out_path

    def generate_chapter5_discussion_stub(self) -> Path:
        out_path = self.output_dir / "chapter5_tartisma.tex"
        if out_path.exists():
            return out_path
        out_path.write_text(
            "% Bolum 5: Tartisma stub'i -- DiscussionConclusionGenerator dolduracak\n"
            "\\chapter{Tartisma}\n"
            "\\label{ch:tartisma}\n\n"
            f"{PLACEHOLDER_LATEX}\n",
            encoding="utf-8",
        )
        return out_path

    def generate_chapter6_conclusion_stub(self) -> Path:
        out_path = self.output_dir / "chapter6_sonuc.tex"
        if out_path.exists():
            return out_path
        out_path.write_text(
            "% Bolum 6: Sonuc stub'i -- DiscussionConclusionGenerator dolduracak\n"
            "\\chapter{Sonuc}\n"
            "\\label{ch:sonuc}\n\n"
            f"{PLACEHOLDER_LATEX}\n",
            encoding="utf-8",
        )
        return out_path

    # Geriye uyumluluk: eski API
    def generate_chapter3_methodology(self) -> Path:
        """Eski API: stub doner; gercek metodoloji ContentGenerator tarafindan uretilir."""
        out_path = self.output_dir / "chapter3_metodoloji.tex"
        if out_path.exists():
            return out_path
        out_path.write_text(
            "% Bolum 3 stub -- ComprehensiveContentGenerator dolduracak\n"
            "\\chapter{Yontem}\n"
            "\\label{ch:yontem}\n\n"
            f"{PLACEHOLDER_LATEX}\n",
            encoding="utf-8",
        )
        return out_path

    # ---------------------------------------------------------------------
    # Markdown -> LaTeX donusum
    # ---------------------------------------------------------------------

    def _md_to_latex_literature(self, md_text: str) -> str:
        """Bolum 2 markdown icerigini LaTeX'e donusturur."""
        lines = md_text.splitlines()
        out: list[str] = []
        out.append("% Bolum 2: Literatur Incelemesi -- Sprint 14 REWRITE")
        out.append("% Kaynak: thesis/bolum-02-literatur-incelemesi.md (IEEE atifli)\n")
        out.append("\\chapter{Literatur Incelemesi}")
        out.append("\\label{ch:literatur}\n")

        in_metadata = False
        in_atif_listesi = False

        for raw_line in lines:
            line = raw_line.rstrip()

            if not line:
                out.append("")
                continue

            if line.startswith(">"):
                in_metadata = True
                continue
            if in_metadata and not line.startswith(">"):
                in_metadata = False

            # H1 / H2 atla -- chapter zaten yazildi
            if line.startswith("# ") or line.startswith("## "):
                continue

            if line.strip() == "---":
                continue

            if "Atıf Listesi" in line or "atıf listesi" in line.lower():
                in_atif_listesi = True
                out.append("\n% Atif listesi -- references.bib dosyasina bib formatinda")
                out.append("% aktarilmistir; tezde \\printbibliography ile sunulur.\n")
                continue

            if in_atif_listesi:
                if re.match(r"^\[\d+\]", line):
                    out.append(f"% BIB: {line}")
                else:
                    out.append(f"% {line}")
                continue

            section_match = re.match(r"^\*\*([^*]+)\*\*$", line)
            if section_match:
                title = section_match.group(1).strip()
                if re.match(r"^\d+(\.\d+)?\s", title):
                    parts = title.split(None, 1)
                    if len(parts) == 2:
                        out.append(f"\\section{{{self._escape_latex(parts[1])}}}")
                    else:
                        out.append(f"\\section{{{self._escape_latex(title)}}}")
                else:
                    out.append(f"\\textbf{{{self._escape_latex(title)}}}\n")
                continue

            if line.startswith("*") and line.endswith("*") and "|" in line:
                continue  # surum/tarih notu

            converted = self._convert_inline(line)
            out.append(converted)

        out.append("")
        return "\n".join(out)

    def _convert_inline(self, text: str) -> str:
        """Inline markdown to LaTeX cevirisi."""

        def cite_replace(match: re.Match[str]) -> str:
            inner = match.group(1)
            nums = re.findall(r"\d+", inner)
            if not nums:
                return match.group(0)
            keys = ", ".join(f"ref{n}" for n in nums)
            return f"\\cite{{{keys}}}"

        text = re.sub(r"\[([\d\s,–\-]+)\]", cite_replace, text)
        text = re.sub(
            r"\*\*([^*]+)\*\*",
            lambda m: f"\\textbf{{{self._escape_latex(m.group(1))}}}",
            text,
        )
        text = re.sub(
            r"(?<!\*)\*([^*\n]+)\*(?!\*)",
            lambda m: f"\\textit{{{self._escape_latex(m.group(1))}}}",
            text,
        )
        text = re.sub(
            r"`([^`]+)`",
            lambda m: f"\\texttt{{{self._escape_latex(m.group(1))}}}",
            text,
        )
        return self._escape_latex_paragraph(text)

    @staticmethod
    def _escape_latex(text: str) -> str:
        replacements = {
            "&": "\\&",
            "%": "\\%",
            "#": "\\#",
            "_": "\\_",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    @staticmethod
    def _escape_latex_paragraph(text: str) -> str:
        placeholders: dict[str, str] = {}

        def stash(match: re.Match[str]) -> str:
            token = f"\x00PH{len(placeholders)}\x00"
            placeholders[token] = match.group(0)
            return token

        # Nested {} bir seviye destekler (ornegin {R^2_{test}} gibi sub-script)
        protected = re.sub(
            r"\\(?:cite|textbf|textit|texttt)\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}",
            stash,
            text,
        )

        replacements = {
            "&": "\\&",
            "%": "\\%",
            "#": "\\#",
        }
        for old, new in replacements.items():
            protected = protected.replace(old, new)

        for token, value in placeholders.items():
            protected = protected.replace(token, value)
        return protected

    # ---------------------------------------------------------------------
    # Fallback stub
    # ---------------------------------------------------------------------

    def _stub_literature_chapter(self) -> str:
        return (
            "% Bolum 2: Literatur Incelemesi -- STUB (kaynak md bulunamadi)\n"
            "\\chapter{Literatur Incelemesi}\n"
            "\\label{ch:literatur}\n\n"
            f"{PLACEHOLDER_LATEX}\n\n"
            "\\textit{Bu bolumun icerigi `thesis/bolum-02-literatur-incelemesi.md` "
            "dosyasindan otomatik olarak uretilir. Dosya henuz mevcut degil "
            "veya okunamadi.}\n"
        )


# Backwards-compatible alias
DetailedChapterGenerator = ChapterGenerator
