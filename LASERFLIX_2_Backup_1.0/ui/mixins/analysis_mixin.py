"""
ui/mixins/analysis_mixin.py — Métodos de análise do LaserflixMainWindow.
"""


class AnalysisMixin:
    """Mixin com todos os métodos de análise e geração de descrições."""

    def analyze_single_project(self, path) -> None:
        self.analysis_ctrl.analyze_single(path, self.database)

    def analyze_only_new(self) -> None:
        self.analysis_ctrl.analyze_only_new(self.database)

    def reanalyze_all(self) -> None:
        self.analysis_ctrl.reanalyze_all(self.database)

    def generate_descriptions_for_new(self) -> None:
        self.analysis_ctrl.generate_descriptions_for_new(self.database)

    def generate_descriptions_for_all(self) -> None:
        self.analysis_ctrl.generate_descriptions_for_all(self.database)
