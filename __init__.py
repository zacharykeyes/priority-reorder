"""
Priority Reorder Addon - Main entry point.
"""

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import QAction, QKeySequence
from aqt import gui_hooks
from aqt.operations import CollectionOp

from . import config
from . import cards
from .log import *

def run_in_background():
    """Run the reordering operation in the background"""
    operation = CollectionOp(parent=mw, op=cards.reorder_cards_with_priority_queue_manual).failure(
        lambda err: showInfo(f"Error during reordering: {err}")
    )
    operation.run_in_background()

def setup_sync_hook():
    """Set up sync hook if enabled in config"""
    if config.get_current_config().reorder_before_sync:
        gui_hooks.sync_did_finish.append(lambda: cards.reorder_cards_with_priority_queue_sync_finish())

def setup_menu():
    """Set up menu entries and shortcuts"""
    action = QAction("Reorder Cards", mw)
    action.setShortcut(QKeySequence("Ctrl+Alt+`"))
    qconnect(action.triggered, run_in_background)
    mw.form.menuTools.addAction(action)

# Initialize the addon
log(CRITICAL, "***********************************************************************")
config.reload_config()
setup_sync_hook()
setup_menu()