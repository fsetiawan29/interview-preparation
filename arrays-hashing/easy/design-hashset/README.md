# Problem: Design HashSet

## 1. Problem Understanding

### Problem Summary

Design a HashSet without using any built-in hash table libraries (no
`set`/`dict`/etc. as the underlying store). Implement `MyHashSet` with:
`add(key)` (insert the value if not already present), `contains(key)`
(return whether the value exists), and `remove(key)` (delete the value if
present, otherwise do nothing).

### Input

- A sequence of operations: `MyHashSet()`, `add(key)`, `contains(key)`,
  `remove(key)`.

### Output

- `null` for `MyHashSet()`, `add`, and `remove`.
- A boolean for `contains` — whether the key is currently in the set.

### Constraints

- `0 <= key <= 10^6`
- At most `10^4` calls will be made to `add`, `remove`, and `contains`.

### Example

Input:

```text
["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"]
[[], [1], [2], [1], [3], [2], [2], [2], [2]]
```

Output:

```text
[null, null, null, true, false, null, true, null, false]
```

Manual walkthrough:

```text
myHashSet = MyHashSet()      // set is empty
myHashSet.add(1)             // set: {1}
myHashSet.add(2)             // set: {1, 2}
myHashSet.contains(1) -> true    // 1 is in the set
myHashSet.contains(3) -> false   // 3 is not in the set
myHashSet.add(2)             // set: {1, 2} (already present, no change)
myHashSet.contains(2) -> true
myHashSet.remove(2)          // set: {1}
myHashSet.contains(2) -> false  // 2 was removed
```

---

## 2. Brute Force Approach

### Idea

Store every key in a single flat list, with no hashing at all. `add` scans the whole list to check for an existing `key` before appending. `contains` and `remove` both do the same full linear scan looking for a matching `key`.

### Pseudocode

```text
data = []   # list of keys

add(key):
    if key in data
        return
    data.append(key)

contains(key):
    for k in data
        if k == key
            return true
    return false

remove(key):
    for k in data
        if k == key
            remove k from data
            return
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- `n` = number of keys currently stored; every `add`, `contains`, and `remove` scans the entire list in the worst case (key not present, or present at the very end).

#### Space Complexity

```text
O(n)
```

Why?

- One entry stored per distinct key ever inserted.

### Why this isn't good enough

Every operation degrades to `O(n)` because *all* keys share one list — a set with `10^4` entries means up to `10^4` comparisons per call. Spreading keys across many smaller buckets (via a hash function) means each operation only has to scan the handful of keys that happen to land in the same bucket, not the entire set.

---

## 3. Key Insight

### What makes this problem difficult?

Without a built-in hash table, there's no way to check membership in `O(1)` directly — some other mechanism is needed to avoid scanning every stored key on every call.

### Key Observation

A key can be turned into an array index with a simple hash function (`key % size`), splitting all possible keys into a fixed number of buckets. Collisions (different keys landing in the same bucket) are resolved by chaining: each bucket holds its own small list of keys, scanned linearly only within that bucket.

Example:

```text
size = 1000

add(1) -> bucket_index = 1 % 1000 = 1   -> bucket[1] = [1]
add(2) -> bucket_index = 2 % 1000 = 2   -> bucket[2] = [2]

contains(1) only scans bucket[1] (length 1), not the whole set.
```

### Why does this observation help?

As long as keys spread out roughly evenly across the `size` buckets, each bucket's chain stays short (average length ~ `n / size`), so every operation only scans a small fraction of the total entries instead of all of them.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a wall of `1000` labeled mailboxes (buckets). Every key gets deposited into mailbox number `key % 1000`. Two keys can land in the same mailbox (a collision), so each mailbox actually holds a small stack of slips, one per key it has received — checked one at a time to find (or rule out) the matching key.

```text
key = 1    -> mailbox 1: [1]
key = 2    -> mailbox 2: [2]
key = 1002 -> mailbox 2: [2, 1002]   (collision with key 2, appended to same mailbox)
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
bucket_index = key % size
bucket = self.bucket[bucket_index]
   │
   ▼
Scan bucket for an entry equal to key
   │
 ┌─┴─────────────────────────┐
 │                            │
Found                      Not found
 │                            │
 ▼                            ▼
add:      return (no-op,   add:      append key to bucket
          already present)
contains: return True      contains: return False
remove:   pop the entry    remove:   return (no-op)
          from bucket
```

Explanation of each decision:

- `bucket_index = key % size` maps any key into one of the `size` fixed buckets — the only "hashing" needed.
- Each bucket is a small list; finding the matching key means scanning just that bucket's entries, not the whole set.
- `add` only appends if no equal key is already present in the bucket (no duplicates).
- `remove` (in this implementation) actually pops the matching entry out of the bucket list — unlike a sentinel-value approach, the bucket's length shrinks immediately.

---

## 6. Plain English Algorithm

1. Initialize a fixed-size array `bucket` of `size` empty buckets (lists).
2. `add(key)`: compute `bucket_index = key % size`, scan that bucket — if `key` is already present, do nothing; otherwise append it.
3. `contains(key)`: compute `bucket_index = key % size`, scan that bucket — return `True` if a matching entry is found, `False` otherwise.
4. `remove(key)`: compute `bucket_index = key % size`, scan that bucket — if a matching entry is found, remove it from the bucket; otherwise do nothing.

---

## 7. Pseudocode

```text
size = 1000
bucket = array of `size` empty lists

add(key):
    b = bucket[key % size]
    for k in b
        if k == key
            return
    b.append(key)

contains(key):
    b = bucket[key % size]
    for k in b
        if k == key
            return true
    return false

remove(key):
    b = bucket[key % size]
    for i in range(len(b))
        if b[i] == key
            pop b[i]
            return
```

---

## 8. Python Solution

```python
class MyHashSet:
    def __init__(self):
        self.size = 1000
        self.bucket = [[] for _ in range(self.size)]

    def add(self, key: int) -> None:
        bucket_index = key % self.size
        bucket = self.bucket[bucket_index]
        for b in bucket:
            if key == b:
                return

        bucket.append(key)

    def contains(self, key: int) -> bool:
        bucket_index = key % self.size
        bucket = self.bucket[bucket_index]
        for b in bucket:
            if b == key:
                return True

        return False

    def remove(self, key: int) -> None:
        bucket_index = key % self.size
        bucket = self.bucket[bucket_index]
        for i in range(len(bucket)):
            if bucket[i] == key:
                bucket.pop(i)
                return
```

---

## 9. Dry Run

Example:

```text
["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"]
[[], [1], [2], [1], [3], [2], [2], [2], [2]]
```

| Step | Call | bucket_index | bucket before | Action | bucket after | Returned |
|------|------|---------------|----------------|--------|----------------|----------|
| 1 | `MyHashSet()` | — | — | init 1000 empty buckets | — | `None` |
| 2 | `add(1)` | 1 | `[]` | no match, append `1` | `[1]` | `None` |
| 3 | `add(2)` | 2 | `[]` | no match, append `2` | `[2]` | `None` |
| 4 | `contains(1)` | 1 | `[1]` | match found | `[1]` | `True` |
| 5 | `contains(3)` | 3 | `[]` | loop never runs, falls through to `return False` | `[]` | `False` |
| 6 | `add(2)` | 2 | `[2]` | match found, no-op | `[2]` | `None` |
| 7 | `contains(2)` | 2 | `[2]` | match found | `[2]` | `True` |
| 8 | `remove(2)` | 2 | `[2]` | match at i=0, `pop(0)` | `[]` | `None` |
| 9 | `contains(2)` | 2 | `[]` | loop never runs, falls through to `return False` | `[]` | `False` |

Result: `[None, None, None, True, False, None, True, None, False]`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n / size) average, O(n) worst case
```

Why?

- `n` = number of keys stored; keys are spread across `size = 1000` fixed buckets, so each `add`/`contains`/`remove` only scans its own bucket's chain (average length `n / size`).
- Worst case (all keys collide into the same bucket, e.g. every key a multiple of `1000` apart) degrades to `O(n)`, same as the brute-force list scan.

### Space Complexity

```text
O(n + size)
```

Why?

- `bucket` always holds `size = 1000` buckets regardless of how many keys are stored.
- Unlike a sentinel-based removal, `remove` here calls `pop`, actually deleting the entry from its bucket — so space usage shrinks immediately after a key is removed, rather than accumulating stale entries.
