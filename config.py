"""
Handles loading and managing addon configuration settings.
"""

from dataclasses import dataclass
from typing import List
from aqt import mw

@dataclass(frozen=True)
class SearchConfig:
    expression_field: str | None
    expression_reading_field: str | None

@dataclass(frozen=True)
class AddonConfig:
    # Basic search configuration
    priority_search: List[str]
    priority_search_mode: str
    normal_search: str
    sort_field: str
    sort_reverse: bool
    
    # Advanced configuration
    priority_cutoff: int | None
    normal_prioritization: int | None
    priority_limit: int | None
    shift_existing: bool
    reorder_before_sync: bool
    
    # Search configuration
    search_config: SearchConfig | None

def get_config() -> AddonConfig:
    config = mw.addonManager.getConfig(__name__)

    search_fields = config.get("search_fields", {})
    search_config = None
    if search_fields:
        search_config = SearchConfig(
            expression_field=search_fields.get("expression_field", None),
            expression_reading_field=search_fields.get("expression_reading_field", None),
        )
    
    priority_search_raw = config.get("priority_search", [])
    if isinstance(priority_search_raw, str):
        priority_search = [priority_search_raw] if priority_search_raw.strip() else []
    elif isinstance(priority_search_raw, list):
        priority_search = [str(item).strip() for item in priority_search_raw if str(item).strip()]
    else:
        priority_search = []
    
    priority_search_mode = config.get("priority_search_mode", "sequential")
    if priority_search_mode not in ["sequential", "mix"]:
        priority_search_mode = "sequential"
    
    return AddonConfig(
        priority_search=priority_search,
        priority_search_mode=priority_search_mode,
        normal_search=config.get("normal_search", ""),
        sort_field=config.get("sort_field", ""),
        sort_reverse=config.get("sort_reverse", False),
        priority_cutoff=config.get("priority_cutoff", None),
        normal_prioritization=config.get("normal_prioritization", None),
        priority_limit=config.get("priority_limit", None),
        shift_existing=config.get("shift_existing", True),
        reorder_before_sync=config.get("reorder_before_sync", True),
        search_config=search_config,
    )

# Global config instance
_config: AddonConfig | None = None

def reload_config():
    global _config
    _config = get_config()

def get_current_config() -> AddonConfig:
    global _config
    if _config is None:
        _config = get_config()
    return _config
