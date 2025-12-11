"""
Card operations for priority reorder addon.
Handles card searching, sorting, and reordering logic.
"""

import re
from typing import List
from aqt import mw
from anki.collection import OpChangesWithCount

from .config import get_current_config
from .occurrences import rewrite_search_string
from .log import *

def get_field_value(card, sort_field: str) -> float:
    try:
        value = float(card.note()[sort_field] or 0)
        return value if value > 0 else float("inf")
    except (ValueError, KeyError, TypeError):
        return float("inf")

def should_move_to_priority_queue(value: float, normal_prioritization: int | None, sort_reverse: bool) -> bool:
    return (normal_prioritization is not None and 
            (value > normal_prioritization if sort_reverse else value < normal_prioritization))

def should_move_to_normal_queue(value: float, priority_cutoff: int | None, sort_reverse: bool) -> bool:
    return (priority_cutoff is not None and 
            (value < priority_cutoff if sort_reverse else value > priority_cutoff))

def get_cards_from_search(search_string: str) -> List[int]:
    if not search_string.strip():
        return []
    
    try:
        rewritten_search = rewrite_search_string(search_string)
        final_search = f"{rewritten_search} is:new"
            
        card_ids = list(mw.col.find_cards(final_search, order="c.due asc"))
        
        return card_ids
    except Exception:
        return []

def sort_card_tuples(card_tuples: List[tuple], sort_reverse: bool) -> List[tuple]:
    card_tuples.sort(key=lambda x: x[1], reverse=sort_reverse)
    return card_tuples

def get_card_tuples_with_field_values(card_ids: List[int], sort_field: str) -> List[tuple]:
    return [(card_id, get_field_value(mw.col.get_card(card_id), sort_field)) for card_id in card_ids]

def create_priority_card_buckets(priority_search: List[str], priority_search_mode: str, sort_field: str) -> List[List[tuple]]:
    priority_card_buckets = []
    
    if priority_search_mode == "sequential":
        for search_string in priority_search:
            if search_string.strip():
                card_ids = get_cards_from_search(search_string)
                if card_ids:
                    card_tuples = get_card_tuples_with_field_values(card_ids, sort_field)
                    priority_card_buckets.append(card_tuples)
    elif priority_search_mode == "mix":
        combined_priority_ids = []
        for search_string in priority_search:
            if search_string.strip():
                card_ids = get_cards_from_search(search_string)
                combined_priority_ids.extend(card_ids)
        
        if combined_priority_ids:
            card_tuples = get_card_tuples_with_field_values(combined_priority_ids, sort_field)
            priority_card_buckets.append(card_tuples)
    
    return priority_card_buckets

def apply_cutoff_and_prioritization_rules(priority_card_buckets: List[List[tuple]], normal_card_ids: List[int], sort_field: str, priority_cutoff: int | None, normal_prioritization: int | None, sort_reverse: bool) -> tuple[List[List[tuple]], List[tuple]]:
    final_priority_buckets = []
    final_normal_cards = []
    
    for priority_bucket in priority_card_buckets:
        bucket_priority_cards = []
        
        for card_id, value in priority_bucket:
            if should_move_to_normal_queue(value, priority_cutoff, sort_reverse):
                final_normal_cards.append((card_id, value))
            else:
                bucket_priority_cards.append((card_id, value))
        
        if bucket_priority_cards:
            final_priority_buckets.append(bucket_priority_cards)
    
    for card_id in normal_card_ids:
        value = get_field_value(mw.col.get_card(card_id), sort_field)
        if should_move_to_priority_queue(value, normal_prioritization, sort_reverse):
            if final_priority_buckets:
                final_priority_buckets[-1].append((card_id, value))
        else:
            final_normal_cards.append((card_id, value))
    
    return final_priority_buckets, final_normal_cards

def sort_priority_cards(final_priority_buckets: List[List[tuple]], mode: str, sort_reverse: bool) -> List[tuple]:
    if mode == "sequential":
        final_priority_cards = []
        for bucket in final_priority_buckets:
            sorted_bucket = sort_card_tuples(bucket, sort_reverse)
            final_priority_cards.extend(sorted_bucket)
        return final_priority_cards
    elif mode == "mix":
        all_priority_cards = []
        for bucket in final_priority_buckets:
            all_priority_cards.extend(bucket)
        return sort_card_tuples(all_priority_cards, sort_reverse)

def apply_priority_limit(final_priority_cards: List[tuple], final_normal_cards: List[tuple], priority_limit: int | None) -> tuple[List[tuple], List[tuple]]:
    if priority_limit and len(final_priority_cards) > priority_limit:
        final_normal_cards.extend(final_priority_cards[priority_limit:])
        final_priority_cards = final_priority_cards[:priority_limit]
    return final_priority_cards, final_normal_cards

def reorder_cards_with_priority_queue_manual(_) -> OpChangesWithCount:
    log(DEBUG, "Begining reordering manually")
    return _reorder_cards_with_priority_queue_internal()

def reorder_cards_with_priority_queue_sync_finish() -> OpChangesWithCount:
    log(DEBUG, "Begining reordering on sync finish.")
    return _reorder_cards_with_priority_queue_internal()

def _reorder_cards_with_priority_queue_internal() -> OpChangesWithCount:
    from .config import reload_config
    reload_config()
    config = get_current_config()
    if not config.sort_field.strip():
        return OpChangesWithCount(count=0)
    
    priority_card_buckets = create_priority_card_buckets(config.priority_search, config.priority_search_mode, config.sort_field)
    normal_card_ids = get_cards_from_search(config.normal_search)
    if not (priority_card_buckets or normal_card_ids):
        return OpChangesWithCount(count=0)
    
    final_priority_buckets, final_normal_cards = apply_cutoff_and_prioritization_rules(
        priority_card_buckets, normal_card_ids, config.sort_field, config.priority_cutoff, config.normal_prioritization, config.sort_reverse
    )
    final_priority_cards = sort_priority_cards(final_priority_buckets, config.priority_search_mode, config.sort_reverse)
    final_priority_cards, final_normal_cards = apply_priority_limit(final_priority_cards, final_normal_cards, config.priority_limit)
    
    final_normal_cards = sort_card_tuples(final_normal_cards, config.sort_reverse)
    
    # Combines the final card order and removes duplicates
    final_card_order = list(dict.fromkeys(
        [card_id for card_id, _ in final_priority_cards + final_normal_cards]
    ))
    
    original_card_order = []
    match = re.compile(r"deck:\s*([^\s]+)|deck:\s*\"([^\"]+)\"").search(config.normal_search)
    if match:
        deck_name = match.group(1) or match.group(2)
        original_card_order = get_cards_from_search(f"deck:{deck_name} is:new")

    if not final_card_order or original_card_order == final_card_order:
        log(DEBUG, "No changes in card order.")
        return OpChangesWithCount(count=0)

    log(DEBUG, "Reorder complete")

    return mw.col.sched.reposition_new_cards(
        card_ids=final_card_order,
        starting_from=0,
        step_size=1,
        randomize=False,
        shift_existing=config.shift_existing
    )
