from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import QAction, QKeySequence
from aqt import gui_hooks
from aqt.operations import CollectionOp
from anki.collection import OpChangesWithCount
from typing import List

def reload_config():
    """Reload configuration from addon settings"""
    global config, PRIORITY_SEARCH, NORMAL_SEARCH, SORT_FIELD, SORT_REVERSE
    global PRIORITY_CUTOFF, NORMAL_PRIORITIZATION, PRIORITY_LIMIT, SHIFT_EXISTING, REORDER_BEFORE_SYNC
    
    config = mw.addonManager.getConfig(__name__)
    PRIORITY_SEARCH = config.get("priority_search", "")
    NORMAL_SEARCH = config.get("normal_search", "")
    SORT_FIELD = config.get("sort_field", "")
    SORT_REVERSE = config.get("sort_reverse", False)
    PRIORITY_CUTOFF = config.get("priority_cutoff", None)
    NORMAL_PRIORITIZATION = config.get("normal_prioritization", None)
    PRIORITY_LIMIT = config.get("priority_limit", None)
    SHIFT_EXISTING = config.get("shift_existing", True)
    REORDER_BEFORE_SYNC = config.get("reorder_before_sync", True)

def get_field_value(card) -> float:
    """Extract numeric value from the sort field, return infinity if invalid"""
    try:
        value = float(card.note()[SORT_FIELD] or 0)
        return value if value > 0 else float("inf")
    except (ValueError, KeyError, TypeError):
        return float("inf")

def should_move_to_priority_queue(value: float) -> bool:
    """Check if a card should be moved to priority queue based on normal prioritization"""
    return (NORMAL_PRIORITIZATION is not None and 
            (value > NORMAL_PRIORITIZATION if SORT_REVERSE else value < NORMAL_PRIORITIZATION))

def should_move_to_normal_queue(value: float) -> bool:
    """Check if a card should be moved to normal queue based on priority cutoff"""
    return (PRIORITY_CUTOFF is not None and 
            (value < PRIORITY_CUTOFF if SORT_REVERSE else value > PRIORITY_CUTOFF))

def get_cards_from_search(search_string: str) -> List[int]:
    """Get card IDs from a search string, return empty list if search is empty"""
    if not search_string.strip():
        return []
    
    try:
        return list(mw.col.find_cards(f"{search_string} is:new", order="c.due asc"))
    except Exception:
        return []

def sort_cards_by_field(card_ids: List[int]) -> List[tuple]:
    """Sort cards by the specified field, return (card_id, field_value) tuples"""
    if not card_ids:
        return []
    
    card_values = [(card_id, get_field_value(mw.col.get_card(card_id))) for card_id in card_ids]
    return sort_card_tuples(card_values)

def sort_card_tuples(card_tuples: List[tuple]) -> List[tuple]:
    """Sort a list of (card_id, field_value) tuples by field value"""
    card_tuples.sort(key=lambda x: x[1], reverse=SORT_REVERSE)
    return card_tuples

def reorder_cards_with_priority_queue(col) -> OpChangesWithCount:
    """Main function to reorder cards using priority queue system"""
    reload_config()
    
    if not SORT_FIELD.strip():
        return OpChangesWithCount(count=0)
    
    priority_card_ids = get_cards_from_search(PRIORITY_SEARCH)
    normal_card_ids = get_cards_from_search(NORMAL_SEARCH)
    
    if not (priority_card_ids or normal_card_ids):
        return OpChangesWithCount(count=0)
    
    sorted_priority_cards = sort_cards_by_field(priority_card_ids)
    sorted_normal_cards = sort_cards_by_field(normal_card_ids)
    
    # Apply cutoff and prioritization rules
    final_priority_cards = []
    final_normal_cards = []
    
    for card_id, value in sorted_priority_cards:
        if should_move_to_normal_queue(value):
            final_normal_cards.append((card_id, value))
        else:
            final_priority_cards.append((card_id, value))
    
    for card_id, value in sorted_normal_cards:
        if should_move_to_priority_queue(value):
            final_priority_cards.append((card_id, value))
        else:
            final_normal_cards.append((card_id, value))
    
    # Apply priority limit if configured
    if PRIORITY_LIMIT and len(final_priority_cards) > PRIORITY_LIMIT:
        final_normal_cards.extend(final_priority_cards[PRIORITY_LIMIT:])
        final_priority_cards = final_priority_cards[:PRIORITY_LIMIT]
    
    # Final sort of both queues
    final_priority_cards = sort_card_tuples(final_priority_cards)
    final_normal_cards = sort_card_tuples(final_normal_cards)
    
    # Prevent duplicates by converting to dict and back
    final_card_order = list(dict.fromkeys(
        [card_id for card_id, _ in final_priority_cards + final_normal_cards]
    ))
    if not final_card_order:
        return OpChangesWithCount(count=0)
    
    try:
        current_order = list(mw.col.find_cards(f"cid:{' or cid:'.join(map(str, final_card_order))}", order="c.due asc"))
        if current_order == final_card_order:
            return OpChangesWithCount(count=0)
    except Exception:
        pass
    
    return mw.col.sched.reposition_new_cards(
        card_ids=final_card_order,
        starting_from=0,
        step_size=1,
        randomize=False,
        shift_existing=SHIFT_EXISTING
    )

def run_in_background():
    operation = CollectionOp(parent=mw, op=reorder_cards_with_priority_queue).failure(
        lambda err: showInfo(f"Error during reordering: {err}")
    )
    operation.run_in_background()

def setup_sync_hook():
    """Set up sync hook if enabled in config"""
    if REORDER_BEFORE_SYNC:
        gui_hooks.sync_will_start.append(lambda: reorder_cards_with_priority_queue(mw.col))

reload_config()
setup_sync_hook()

# Menu entries
action = QAction("Reorder Cards", mw)
action.setShortcut(QKeySequence("Ctrl+Alt+`"))
qconnect(action.triggered, run_in_background)
mw.form.menuTools.addAction(action)
