# Problem: Group Anagrams

## 1. Problem Understanding

### Problem Summary

Given an array of strings `strs`, group the strings that are anagrams of each other (same characters, same counts, any order) into sublists. The result can be returned in any order.

### Input

- An array of strings `strs`

### Output

- A list of lists, where each inner list contains one group of anagrams from `strs`.

### Constraints

- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.

### Example

Input:

```text
strs = ["eat","tea","tan","ate","nat","bat"]
```

Output:

```text
[["bat"],["nat","tan"],["ate","eat","tea"]]
```

Manual walkthrough:

```text
"eat" sorted -> "aet"
"tea" sorted -> "aet"   -> same key as "eat"
"tan" sorted -> "ant"
"ate" sorted -> "aet"   -> same key as "eat"/"tea"
"nat" sorted -> "ant"   -> same key as "tan"
"bat" sorted -> "abt"

Group by key:
  "aet" -> ["eat","tea","ate"]
  "ant" -> ["tan","nat"]
  "abt" -> ["bat"]

Result (order of groups/order within groups may vary):
[["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

---

## 2. Brute Force Approach

### Idea

Compare every pair of strings directly: two strings belong in the same group exactly when they're anagrams of each other (same sorted characters).

### Pseudocode

```text
n = length(strs)
used = array of n false values
groups = []

for i = 0 to n - 1
    if used[i]
        continue

    group = [strs[i]]
    used[i] = true

    for j = i + 1 to n - 1
        if not used[j] and isAnagram(strs[i], strs[j])
            group.append(strs[j])
            used[j] = true

    groups.append(group)

return groups

function isAnagram(a, b)
    freq_a = frequency map of a
    freq_b = frequency map of b
    return freq_a == freq_b
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2 * k)
```

Why?

- `n = len(strs)`, `k` = max string length.
- There are `O(n^2)` pairs to compare, and each `isAnagram` check costs `O(k)` to build and compare frequency maps.

#### Space Complexity

```text
O(n * k)
```

Why?

- Every original string ends up stored exactly once across all the groups.

### Why this isn't good enough

Every string is compared against every other ungrouped string individually to test if they're anagrams. Reducing each string to a canonical "sorted characters" key turns matching into a single hash map lookup — strings with the same key are anagrams automatically — replacing all the pairwise `O(k)` comparisons with one `O(k log k)` key computation per string.

---

## 3. Key Insight

### What makes this problem difficult?

Comparing every pair of strings to check if they're anagrams of each other would be `O(n^2)` comparisons, each of which could itself cost `O(k)` — far too slow for `n` up to `10^4`. We need a way to recognize "these strings are anagrams" without pairwise comparison.

### Key Observation

Two strings are anagrams **if and only if** sorting their characters produces the exact same string. That sorted string is a **canonical form** — a single "fingerprint" shared by every member of an anagram group.

Example:

```text
"eat" -> sorted characters -> "aet"
"tea" -> sorted characters -> "aet"   (same fingerprint)
"tan" -> sorted characters -> "ant"   (different fingerprint)
```

### Why does this observation help?

Once every string has a canonical key, grouping becomes a single pass with a hash map: compute each string's key, and append the string to the bucket for that key. No pairwise comparisons are needed — the hash map does the matching in `O(1)` average time per lookup.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a wall of labeled bins, one per distinct "sorted-letters" fingerprint. Each incoming string gets its letters sorted to find which bin it belongs to, then the *original* (unsorted) string is dropped into that bin.

```text
"eat" -> sort -> "aet" -> bin["aet"] += "eat"
"tea" -> sort -> "aet" -> bin["aet"] += "tea"
"tan" -> sort -> "ant" -> bin["ant"] += "tan"
"ate" -> sort -> "aet" -> bin["aet"] += "ate"
"nat" -> sort -> "ant" -> bin["ant"] += "nat"
"bat" -> sort -> "abt" -> bin["abt"] += "bat"

bins:
  "aet": [eat, tea, ate]
  "ant": [tan, nat]
  "abt": [bat]
```

Once every string has been dropped into its bin, the bins themselves (their contents) are the answer.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize empty map: group
   │
   ▼
For each str in strs:
   │
   ▼
key = sorted characters of str, joined
   │
   ▼
Is key already in group ?
   │
 ┌─┴─────────────────┐
 │                    │
No                   Yes
 │                    │
 ▼                    ▼
Create group[key] = []   (bucket already exists)
 │                    │
 └────────┬───────────┘
          ▼
   Append str to group[key]
          │
          └──▶ (loop to next str)
                     │
                     ▼
        All strings processed — collect
        group.values() as the result
                     │
                     ▼
                    Done
```

Explanation of each decision:

- The key is computed the same way for every string — sorting its characters and joining them back into a string.
- A key not yet seen means this is the first string with that particular letter multiset — start a new bucket.
- A key already present means a prior string had the same fingerprint — the current string joins that same anagram group.
- After processing every string, each bucket in `group` is exactly one group of anagrams.

---

## 6. Plain English Algorithm

1. Create an empty map `group` from canonical key to list of strings.
2. For each string in `strs`:
   - Compute its key by sorting its characters and joining them back into a string.
   - If the key isn't in `group` yet, start a new empty list for it.
   - Append the original (unsorted) string to `group[key]`.
3. Return the values of `group` as a list of lists — one list per distinct key.

---

## 7. Pseudocode

```text
group = empty map

for str in strs
    key = join(sorted(characters of str))

    if key not in group
        group[key] = empty list

    append str to group[key]

return values of group
```

---

## 8. Python Solution

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        group = {}
        for str in strs:
            key = "".join(sorted(str))
            if key not in group:
                group[key] = []
            group[key].append(str)

        result = []
        for v in group.values():
            result.append(v)

        return result
```

---

## 9. Dry Run

Example:

```text
strs = ["eat","tea","tan","ate","nat","bat"]
```

| Step | str | key = sorted(str) | In group? | Action | group state after |
|------|-----|--------------------|-----------|--------|--------------------|
| 1 | "eat" | "aet" | No | Create bucket, append | {"aet": ["eat"]} |
| 2 | "tea" | "aet" | Yes | Append | {"aet": ["eat","tea"]} |
| 3 | "tan" | "ant" | No | Create bucket, append | {"aet": [...], "ant": ["tan"]} |
| 4 | "ate" | "aet" | Yes | Append | {"aet": ["eat","tea","ate"], "ant": ["tan"]} |
| 5 | "nat" | "ant" | Yes | Append | {"aet": [...], "ant": ["tan","nat"]} |
| 6 | "bat" | "abt" | No | Create bucket, append | {"aet": [...], "ant": [...], "abt": ["bat"]} |

Final `group.values()`: `[["eat","tea","ate"], ["tan","nat"], ["bat"]]` — the same groups as the expected output `[["bat"],["nat","tan"],["ate","eat","tea"]]`, just in a different (insertion) order, which the problem explicitly allows.

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n * k log k)
```

Why?

- `n` = number of strings, `k` = max string length.
- Sorting each string's characters costs `O(k log k)`, done once per string.
- Hash map insertions/lookups are `O(1)` average, done `n` times.

### Space Complexity

```text
O(n * k)
```

Why?

- Every original string is stored exactly once across all the grouped lists (total `n * k` characters).
- The sorted keys themselves also cost `O(k)` each, `O(n * k)` total.
