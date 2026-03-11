"""
ui/bootstrap/callbacks_setup.py — Configura todos os callbacks dos controllers.

Centraliza o wiring entre controllers, managers e widgets.
Recebe o LaserflixMainWindow como contexto (ctx).
"""


class CallbacksSetup:
    """
    Configura callbacks de todos os controllers após build completo da UI.
    ctx é o LaserflixMainWindow.
    """

    def __init__(self, ctx):
        self._wire_selection_bar(ctx)
        self._wire_selection_ctrl(ctx)
        self._wire_collection_ctrl(ctx)
        self._wire_analysis_ctrl(ctx)
        self._wire_progress(ctx)

    def _wire_selection_bar(self, ctx):
        ctx.selection_bar.on_select_all = (
            lambda: ctx.selection_ctrl.select_all(list(ctx.database.keys()))
        )
        ctx.selection_bar.on_deselect_all = ctx.selection_ctrl.deselect_all
        ctx.selection_bar.on_remove_selected = (
            lambda: ctx.selection_ctrl.remove_selected(ctx.root)
        )
        ctx.selection_bar.on_cancel = ctx.selection_ctrl.toggle_mode

    def _wire_selection_ctrl(self, ctx):
        ctx.selection_ctrl.on_mode_changed = ctx._on_selection_mode_changed
        ctx.selection_ctrl.on_selection_changed = ctx._on_selection_count_changed
        ctx.selection_ctrl.on_card_toggled = ctx._update_card_selection_visual
        ctx.selection_ctrl.on_projects_removed = ctx._on_projects_removed
        ctx.selection_ctrl.on_refresh_needed = ctx._refresh_all

    def _wire_collection_ctrl(self, ctx):
        ctx.collection_ctrl.on_collection_changed = ctx._refresh_all

    def _wire_analysis_ctrl(self, ctx):
        ctx.analysis_ctrl.on_analysis_complete = (
            lambda msg: ctx.status_bar.config(text=msg)
        )
        ctx.analysis_ctrl.on_refresh_ui = ctx._refresh_all
        ctx.analysis_ctrl.setup_callbacks()

    def _wire_progress(self, ctx):
        ctx.analysis_ctrl.on_show_progress = ctx.progress_ui.show
        ctx.analysis_ctrl.on_hide_progress = ctx.progress_ui.hide
        ctx.analysis_ctrl.on_update_progress = ctx.progress_ui.update
