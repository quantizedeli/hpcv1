# PFAZ 10: Thesis Compilation
# =============================

# Main pipeline (ACTIVE -- Sprint 14 REWRITE)
from .pfaz10_master_integration import MasterThesisIntegration

# Sprint 14 yeni bilesen: gercek PFAZ ciktilarini okuyan DataReader
try:
    from .pfaz10_data_reader import PFAZ10DataReader
    DATA_READER_AVAILABLE = True
except Exception:  # noqa: BLE001
    PFAZ10DataReader = None
    DATA_READER_AVAILABLE = False

#  ACTIVATED MODULES: Thesis Compilation Tools (9 modüller aktif edildi)
try:
    from .pfaz10_complete_package import CompletePFAZ10Package
    COMPLETE_PACKAGE_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    CompletePFAZ10Package = None
    COMPLETE_PACKAGE_AVAILABLE = False

try:
    from .pfaz10_chapter_generator import ChapterGenerator
    CHAPTER_GENERATOR_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    ChapterGenerator = None
    CHAPTER_GENERATOR_AVAILABLE = False

try:
    from .pfaz10_content_generator import ContentGenerator
    CONTENT_GENERATOR_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    ContentGenerator = None
    CONTENT_GENERATOR_AVAILABLE = False

try:
    from .pfaz10_discussion_conclusion import DiscussionConclusionGenerator
    DISCUSSION_CONCLUSION_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    DiscussionConclusionGenerator = None
    DISCUSSION_CONCLUSION_AVAILABLE = False

try:
    from .pfaz10_latex_integration import LatexIntegration
    LATEX_INTEGRATION_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    LatexIntegration = None
    LATEX_INTEGRATION_AVAILABLE = False

try:
    from .pfaz10_thesis_compilation_system import ThesisCompilationSystem
    THESIS_COMPILATION_SYSTEM_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    ThesisCompilationSystem = None
    THESIS_COMPILATION_SYSTEM_AVAILABLE = False

try:
    from .pfaz10_thesis_orchestrator import ThesisOrchestrator
    THESIS_ORCHESTRATOR_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    ThesisOrchestrator = None
    THESIS_ORCHESTRATOR_AVAILABLE = False

try:
    from .pfaz10_visualization_qa import VisualizationQA
    VISUALIZATION_QA_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    VisualizationQA = None
    VISUALIZATION_QA_AVAILABLE = False

try:
    from .PFAZ10_COMPLETION_SUMMARY import PFAZ10CompletionSummary
    COMPLETION_SUMMARY_AVAILABLE = True
except Exception:  # noqa: BLE001 -- Unicode + opsiyonel modul yakalama
    PFAZ10CompletionSummary = None
    COMPLETION_SUMMARY_AVAILABLE = False

__all__ = [
    'MasterThesisIntegration',
    'PFAZ10DataReader', 'DATA_READER_AVAILABLE',
    'CompletePFAZ10Package', 'COMPLETE_PACKAGE_AVAILABLE',
    'ChapterGenerator', 'CHAPTER_GENERATOR_AVAILABLE',
    'ContentGenerator', 'CONTENT_GENERATOR_AVAILABLE',
    'DiscussionConclusionGenerator', 'DISCUSSION_CONCLUSION_AVAILABLE',
    'LatexIntegration', 'LATEX_INTEGRATION_AVAILABLE',
    'ThesisCompilationSystem', 'THESIS_COMPILATION_SYSTEM_AVAILABLE',
    'ThesisOrchestrator', 'THESIS_ORCHESTRATOR_AVAILABLE',
    'VisualizationQA', 'VISUALIZATION_QA_AVAILABLE',
    'PFAZ10CompletionSummary', 'COMPLETION_SUMMARY_AVAILABLE',
]
