# Priority Reorder Addon Configuration

**Note**: Either of the search fields may be left empty and cards will still be sorted normally. The addon automatically adds `is:new` to all searches to ensure only new cards are affected.

## Basic Configuration

### `priority_search`
- **Type**: String or List of Strings
- **Default**: `[]`
- **Description**: Anki search string(s) for priority queue cards. Can be a single string (for backward compatibility) or a list of strings for multiple priority searches
- **Example**: `"deck:Japanese added:3"` or `["deck:Japanese added:3", "deck:Japanese added:5"]` or `["tag:important", "deck:Japanese added:3"]`

### `priority_search_mode`
- **Type**: String
- **Default**: `"sequential"`
- **Description**: How to handle multiple priority searches when `priority_search` is a list
- **Valid Options**: 
  - `"sequential"`: Process each priority search separately, maintaining their order (priority_search[0] → priority_search[1] → ... → normal_search)
  - `"mix"`: Combine all priority searches before sorting (combined_priority_search → normal_search)
- **Example**: `"sequential"` or `"mix"`

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
- **Description**: If a normal card's field value is below this threshold, it moves to the priority queue (if using multiple priority searches this gets put into the first one)
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

## Search Options Configuration

The `search_fields` object contains configuration for advanced search functionality, for now only occurrence-based searching from Yomitan dictionaries. If you don't intend on using this functionality this section can be ignored.

### `search_fields.expression_field`
- **Type**: String or null
- **Default**: `null` (optional)
- **Description**: The name of the field containing the expression/word to match against occurrence dictionaries
- **Example**: `"Expression"`, `"Word"`, `"Front"`
- **Note**: If not set, occurrence search patterns will be ignored

### `search_fields.expression_reading_field`
- **Type**: String or null
- **Default**: `null` (optional)
- **Description**: The name of the field containing the reading/pronunciation to match against occurrence dictionaries
- **Example**: `"Reading"`, `"ExpressionReading"`, `"Pronunciation"`
- **Note**: If not set, occurrence search patterns will be ignored

## Priority Search Modes

### Sequential Mode (`"sequential"`)
When using multiple priority searches, each search is processed separately and maintains its order:
- Cards from `priority_search[0]` are sorted and placed first
- Cards from `priority_search[1]` are sorted and placed second
- And so on...
- Finally, normal search cards are placed last

**Example**: If you have `["deck:Japanese added:3", "deck:Japanese added:7"]`:
- All cards from "added:3" (sorted by your `sort_field`) come first
- All cards from "added:7" (sorted by your `sort_field`) come second  
- All normal search cards come last

### Mix Mode (`"mix"`)
When using multiple priority searches, all searches are combined before sorting:
- All cards from all priority searches are collected together
- The combined set is sorted by your `sort_field`
- Normal search cards are placed after the combined priority cards

**Example**: If you have `["deck:Japanese added:3", "deck:Japanese added:7"]`:
- All cards from both "added:3" and "added:7" are mixed together
- The entire mixed set is sorted by your `sort_field` value
- All normal search cards come last

## Occurrence Search Usage
As long as you have set up your `user_files` directory with occurrence dictionaries you can use occurrence search patterns in your `priority_search` and `normal_search` strings:
- `occurrences:dict_name>=50` - Cards with occurrence count >= 50 in dictionary "dict_name"
- `occurrences:dict_name<50` - Cards with occurrence count < 50 in dictionary "dict_name"
- `occurrences:dict_name=0` - Cards with no occurrences in dictionary "dict_name"