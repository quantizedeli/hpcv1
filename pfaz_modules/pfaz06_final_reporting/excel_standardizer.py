"""
Excel Standardizer (Backward-Compatible Stub)
=============================================
Sprint 16 BUG-110 fix (2026-05-20): Asil kod utils/excel_standardizer.py'ye tasindi.

Bu dosya geriye dönuk uyumluluk icin re-export yapar. Eski import'lar
(pfaz_modules.pfaz06_final_reporting.excel_standardizer) calismaya devam eder.

Tercih edilen kullanim (Sprint 16+):
    from utils.excel_standardizer import ExcelStandardizer

Bu dosya gelecekte (Sprint 18+) silinebilir; ama Sprint 16 SON sprint oldugu icin
ve tez teslim sonrasi degisiklik yapilmayacagi icin korundu.

Mimari etkisi:
- Onceki: PFAZ12 -> PFAZ6 ve PFAZ6 -> PFAZ12 (dairesel)
- Sonra:  PFAZ12 -> utils/ ve PFAZ6 -> utils/ (tek yonlu, dongu yok)
"""

from utils.excel_standardizer import (  # noqa: F401
    ExcelStandardizer,
    autosize_and_header,
    add_r2_color_scale,
    color_cell,
)

__all__ = [
    'ExcelStandardizer',
    'autosize_and_header',
    'add_r2_color_scale',
    'color_cell',
]
