Reorders your cards, allowing you to prioritize certain cards with a handful of options.

## Configuration

**Note**: Either of the search strings may be left empty and cards will still be sorted normally.

### Basic Settings

- **`priority_search`**: Anki search string for priority queue cards (e.g., "deck:Japanese added:4")
- **`normal_search`**: Anki search string for normal queue cards (e.g., "deck:Japanese -added:4")
- **`sort_field`**: Field name to sort by (e.g., "Frequency")
- **`sort_reverse`**: Whether to sort in descending order (default: false = ascending)

### Advanced Settings

- **`priority_cutoff`**: If a priority card's field value exceeds this (or is less than for reverse), it moves to normal queue
- **`normal_prioritization`**: If a normal card's field value is below this (or above for reverse), it moves to priority queue
- **`priority_limit`**: Maximum number of cards in the priority queue (excess cards move to normal queue)
- **`shift_existing`**: Whether to shift existing cards when repositioning (default: true)
- **`reorder_before_sync`**: Whether to automatically reorder before sync operations (default: true)

## Use Case Examples

The default configuration shows an example prioritizing recently added cards:
- **Priority Queue**: `deck:日本語::Mining added:4` (cards added in the last 4 days)
- **Normal Queue**: `deck:日本語::Mining -added:4` (older cards)

You can also prioritize by tags to prioritize certain types of content, for example:
- **Priority Queue**: `deck:日本語::Mining tag:ノベルゲーム::銀色、遥か` (specific content)
- **Normal Queue**: `deck:日本語::Mining -tag:ノベルゲーム::銀色、遥か` (other content)

## Examples

### Basic Usage
```json
{
    "priority_search": "deck:日本語::Mining added:4",
    "normal_search": "deck:日本語::Mining -added:4",
    "sort_field": "FreqSort",
    "sort_reverse": false
}
```

### With Cutoff And Prioritization Rules
```json
{
    "priority_search": "deck:日本語::Mining added:4",
    "normal_search": "deck:日本語::Mining -added:4",
    "sort_field": "FreqSort",
    "sort_reverse": false,
    "priority_cutoff": 10000,
    "normal_prioritization": 1000
}
```

This configuration means:
- Recently added cards (added:4) with frequency > 10000 move to normal queue
- Older cards (-added:4) with frequency < 1000 move to priority queue

### Reverse Sorting
```json
{
    "priority_search": "deck:日本語::Mining added:4",
    "normal_search": "deck:日本語::Mining -added:4",
    "sort_field": "FreqSort",
    "sort_reverse": true,
    "priority_cutoff": 1000,
    "normal_prioritization": 10000
}
```

With reverse sorting:
- Recently added cards with frequency < 1000 move to normal queue
- Older cards with frequency > 10000 move to priority queue

### With Priority Limit
```json
{
    "priority_search": "deck:日本語::Mining added:4",
    "normal_search": "deck:日本語::Mining -added:4",
    "sort_field": "FreqSort",
    "sort_reverse": false,
    "priority_limit": 50
}
```

This configuration ensures that only the top 50 highest-priority cards (based on FreqSort) will be in the priority queue, regardless of how many cards match the priority search criteria.

## Usage
The addon will run automatically before sync if enabled. You can also manually trigger the reodering with Ctrl+Alt+` or Tools → Reorder Cards.
