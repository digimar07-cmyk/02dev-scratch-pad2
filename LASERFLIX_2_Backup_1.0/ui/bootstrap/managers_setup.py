"""
ui/bootstrap/managers_setup.py — Instancia e configura todos os managers.

Recebe o LaserflixMainWindow como contexto (ctx) para acessar
widgets e callbacks já existentes sem criar acoplamento circular.
"""
from ui.recursive_import_integration import RecursiveImportManager
from ui.managers.toggle_manager import ToggleManager
from ui.managers.collection_dialog_manager import CollectionDialogManager
from ui.managers.progress_ui_manager import ProgressUIManager
from ui.managers.orphan_manager import OrphanManager
from ui.managers.modal_generator import ModalGenerator


class ManagersSetup:
    """
    Instancia os managers e injeta callbacks a partir do contexto (ctx).
    ctx é o LaserflixMainWindow.
    """

    def __init__(self, ctx):
        self.import_manager = RecursiveImportManager(
            parent=ctx.root,
            database=ctx.database,
            project_scanner=ctx.scanner,
            text_generator=ctx.text_generator,
            analysis_manager=ctx.analysis_manager,
            on_complete=ctx._on_import_complete,
        )

        self.toggle_mgr = ToggleManager(ctx.database, ctx.db_manager)
        self.toggle_mgr.on_invalidate_cache = ctx._invalidate_cache

        self.collection_dialog_mgr = CollectionDialogManager(
            ctx.root, ctx.collections_manager, ctx.database, ctx.collection_ctrl
        )
        self.collection_dialog_mgr.on_status_update = (
            lambda msg: ctx.status_bar.config(text=msg)
        )
        self.collection_dialog_mgr.on_refresh = lambda: (
            ctx.sidebar.refresh(ctx.database, ctx.collections_manager),
            ctx._invalidate_cache(),
        )

        self.progress_ui = ProgressUIManager(
            ctx.progress_bar, ctx.stop_btn, ctx.status_bar, ctx.root
        )

        self.orphan_mgr = OrphanManager(
            database=ctx.database,
            db_manager=ctx.db_manager,
            collections_manager=ctx.collections_manager,
            on_refresh=ctx._refresh_all,
            on_status_update=lambda msg: ctx.status_bar.config(text=msg),
        )

        self.modal_gen = ModalGenerator(
            text_generator=ctx.text_generator,
            database=ctx.database,
            db_manager=ctx.db_manager,
        )
