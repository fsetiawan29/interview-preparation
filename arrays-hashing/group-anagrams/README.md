# Problem

Name: Group Anagrams

Difficulty: Medium

----------------------------------------

# Pattern

Hashing + String Encoding

----------------------------------------

# Recognition

Idea

- Create Hashing
- Can with sorted and join
- Can with tuple alphabet ASCII number

Steps

- SHAPE: Group by canonical form
- KEY: sort each string's characters and `join` back — anagrams always sort to the same key, e.g. `"eat"` and `"tea"` both become `"aet"`
- BUCKET: if the key isn't in `group` yet, start a new list for it
- STORE: append the original (unsorted) string to `group[key]`
- COLLECT: return `group.values()` — one list per distinct key

----------------------------------------

# Complexity

- Time: `O(n * k log k)` — for `n` strings of max length `k`, sorting each string's characters dominates
- Space: `O(n * k)` — every string is stored once across the grouped lists, plus the sorted keys
