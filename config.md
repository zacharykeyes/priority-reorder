# Priority Reorder Addon Configuration

**Note**: Either of the search strings may be left empty and cards will still be sorted normally. The addon automatically adds `is:new` to all searches to ensure only new cards are affected.

## Basic Configuration

### `priority_search`
- **Type**: String
- **Default**: `""`
- **Description**: Anki search string for priority queue cards
- **Example**: `"deck:Japanese added:4"` or `"tag:important"`

### `normal_search`
- **Type**: String
- **Default**: `""`
- **Description**: Anki search string for normal queue cards
- **Example**: `"deck:Japanese -added:4"` or `"deck:Japanese -tag:important"`

### `sort_field`
- **Type**: String
- **Default**: `""` (required)
- **Description**: The field name to sort cards by
- **Example**: `"FreqSort"`, `"Frequency"`, `"Difficulty"`

### `sort_reverse`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Whether to sort in descending order
- **Note**: `false` = ascending (lowest values first), `true` = descending (highest values first)

## Advanced Configuration

### `priority_cutoff`
- **Type**: Number or null
- **Default**: `null`
- **Description**: If a priority card's field value exceeds this threshold, it moves to the normal queue
- **Behavior with `sort_reverse`**: When `sort_reverse` is true, cards with values BELOW the cutoff move to normal queue
- **Example**: With `sort_reverse: false` and `priority_cutoff: 1000`, priority cards with frequency > 1000 move to normal queue

### `normal_prioritization`
- **Type**: Number or null
- **Default**: `null`
- **Description**: If a normal card's field value is below this threshold, it moves to the priority queue
- **Behavior with `sort_reverse`**: When `sort_reverse` is true, cards with values ABOVE the threshold move to priority queue
- **Example**: With `sort_reverse: false` and `normal_prioritization: 500`, normal cards with frequency < 500 move to priority queue

### `priority_limit`
- **Type**: Number or null
- **Default**: `null`
- **Description**: Maximum number of cards allowed in the priority queue. If exceeded, excess cards are moved to the normal queue
- **Behavior**: After all other rules are applied, if the priority queue has more cards than this limit, only the top N cards (sorted by the sort field) remain in priority
- **Example**: With `priority_limit: 50`, only the 50 highest-priority cards will be in the priority queue

### `shift_existing`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Whether to shift existing cards when repositioning new cards

### `reorder_before_sync`
- **Type**: Boolean
- **Default**: `true`
- **Description**: Whether to automatically reorder cards before sync operations
- **Note**: When disabled, you can still manually trigger reordering
