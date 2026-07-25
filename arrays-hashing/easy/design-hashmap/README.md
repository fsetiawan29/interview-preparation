# Problem: Design HashMap

## 1. Problem Understanding

### Problem Summary

Design a HashMap without using any built-in hash table libraries (no
`dict`/`Map`/etc. as the underlying store). Implement `MyHashMap` with:
`put(key, value)` (insert or update), `get(key)` (return the mapped value,
or `-1` if the key isn't present), and `remove(key)` (delete the mapping if
it exists).

### Input

- A sequence of operations: `MyHashMap()`, `put(key, value)`, `get(key)`,
  `remove(key)`.

### Output

- `null` for `MyHashMap()`, `put`, and `remove`.
- An integer for `get` — the mapped value, or `-1` if the key has no
  mapping.

### Constraints

- `0 <= key, value <= 10^6`
- At most `10^4` calls will be made to `put`, `get`, and `remove`.

### Example

Input:

```text
["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
```

Output:

```text
[null, null, null, 1, -1, null, 1, null, -1]
```

Manual walkthrough:

```text
myHashMap = MyHashMap()      // map is empty
myHashMap.put(1, 1)          // map: {1: 1}
myHashMap.put(2, 2)          // map: {1: 1, 2: 2}
myHashMap.get(1)     -> 1    // key 1 maps to 1
myHashMap.get(3)     -> -1   // key 3 has no mapping
myHashMap.put(2, 1)          // map: {1: 1, 2: 1} (update existing key)
myHashMap.get(2)     -> 1
myHashMap.remove(2)          // map: {1: 1}
myHashMap.get(2)     -> -1   // key 2 was removed
```

---

## 2. Brute Force Approach

### Idea

Store every `(key, value)` pair in a single flat list, with no hashing at all. `put` scans the whole list for an existing `key` to update, or appends a new pair if not found. `get` and `remove` both do the same full linear scan looking for a matching `key`.

### Pseudocode

```text
data = []   # list of [key, value] pairs

put(key, value):
    for pair in data
        if pair[0] == key
            pair[1] = value
            return
    data.append([key, value])

get(key):
    for pair in data
        if pair[0] == key
            return pair[1]
    return -1

remove(key):
    for pair in data
        if pair[0] == key
            remove pair from data
            return
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- `n` = number of pairs currently stored; every `put`, `get`, and `remove` scans the entire list in the worst case (key not present, or present at the very end).

#### Space Complexity

```text
O(n)
```

Why?

- One entry stored per distinct key ever inserted.

### Why this isn't good enough

Every operation degrades to `O(n)` because *all* keys share one list — a map with `10^4` entries means up to `10^4` comparisons per call. Spreading keys across many smaller buckets (via a hash function) means each operation only has to scan the handful of keys that happen to land in the same bucket, not the entire map.

---

## 3. Key Insight

### What makes this problem difficult?

Without a built-in hash table, there's no way to jump straight to a key's value — some other mechanism is needed to avoid scanning every stored pair on every call.

### Key Observation

A key's value can be turned into an array index with a simple hash function (`key % size`), splitting all possible keys into a fixed number of buckets. Collisions (different keys landing in the same bucket) are resolved by chaining: each bucket holds its own small list of `[key, value]` pairs, scanned linearly only within that bucket.

Example:

```text
size = 1000

put(1, 1)  -> bucket_index = 1 % 1000 = 1    -> data[1] = [[1, 1]]
put(2, 2)  -> bucket_index = 2 % 1000 = 2    -> data[2] = [[2, 2]]

get(1) only scans data[1] (length 1), not the whole map.
```

### Why does this observation help?

As long as keys spread out roughly evenly across the `size` buckets, each bucket's chain stays short (average length ~ `n / size`), so every operation only scans a small fraction of the total entries instead of all of them.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a wall of `1000` labeled mailboxes (buckets). Every key gets deposited into mailbox number `key % 1000`. Two keys can land in the same mailbox (a collision), so each mailbox actually holds a small stack of slips, one per key it has received — checked one at a time to find the matching key.

```text
key = 1   -> mailbox 1: [(1, 1)]
key = 2   -> mailbox 2: [(2, 2)]
key = 1002 -> mailbox 2: [(2, 2), (1002, value)]   (collision with key 2, appended to same mailbox)
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
bucket_index = key % size
bucket = data[bucket_index]
   │
   ▼
Scan bucket for an entry whose stored key == key
   │
 ┌─┴─────────────────────────┐
 │                            │
Found                      Not found
 │                            │
 ▼                            ▼
put:    overwrite value    put:    append [key, value] to bucket
get:    return stored value   get:    return -1
remove: overwrite value        remove: no-op
        with -1 sentinel
```

Explanation of each decision:

- `bucket_index = key % size` maps any key into one of the `size` fixed buckets — the only "hashing" needed.
- Each bucket is a small list; finding the matching key means scanning just that bucket's entries, not the whole map.
- `put` either updates an existing entry's value in place or appends a brand-new `[key, value]` pair.
- `remove` overwrites the matching entry's value with `-1` rather than deleting it from the bucket list — since `put` only ever stores values in `[0, 10^6]`, a stored value of `-1` unambiguously marks "removed", and a later `get` on that key correctly returns `-1`.

---

## 6. Plain English Algorithm

1. Initialize a fixed-size array `data` of `size` empty buckets (lists).
2. `put(key, value)`: compute `bucket_index = key % size`, scan that bucket for an entry with a matching key — if found, overwrite its value; otherwise append `[key, value]`.
3. `get(key)`: compute `bucket_index = key % size`, scan that bucket for a matching key — return its value if found, else `-1`.
4. `remove(key)`: compute `bucket_index = key % size`, scan that bucket for a matching key — if found, overwrite its value with `-1` (the sentinel meaning "no mapping"); otherwise do nothing.

---

## 7. Pseudocode

```text
size = 1000
data = array of `size` empty lists

put(key, value):
    bucket = data[key % size]
    for pair in bucket
        if pair[0] == key
            pair[1] = value
            return
    bucket.append([key, value])

get(key):
    bucket = data[key % size]
    for pair in bucket
        if pair[0] == key
            return pair[1]
    return -1

remove(key):
    bucket = data[key % size]
    for pair in bucket
        if pair[0] == key
            pair[1] = -1
```

---

## 8. Python Solution

```python
class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.data = [[] for _ in range(self.size)]

    def put(self, key: int, value: int) -> None:
        bucket_index = key % self.size
        bucket = self.data[bucket_index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i][1] = value
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        bucket_index = key % self.size
        bucket = self.data[bucket_index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1]
        return -1

    def remove(self, key: int) -> None:
        bucket_index = key % self.size
        bucket = self.data[bucket_index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i][1] = -1
```

---

## 9. Dry Run

Example:

```text
["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
[[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
```

| Step | Call | bucket_index | bucket before | Action | bucket after | Returned |
|------|------|---------------|----------------|--------|----------------|----------|
| 1 | `MyHashMap()` | — | — | init 1000 empty buckets | — | `None` |
| 2 | `put(1, 1)` | 1 | `[]` | no match, append `[1,1]` | `[[1,1]]` | `None` |
| 3 | `put(2, 2)` | 2 | `[]` | no match, append `[2,2]` | `[[2,2]]` | `None` |
| 4 | `get(1)` | 1 | `[[1,1]]` | match at i=0 | `[[1,1]]` | `1` |
| 5 | `get(3)` | 3 | `[]` | no match | `[]` | `-1` |
| 6 | `put(2, 1)` | 2 | `[[2,2]]` | match at i=0, overwrite value | `[[2,1]]` | `None` |
| 7 | `get(2)` | 2 | `[[2,1]]` | match at i=0 | `[[2,1]]` | `1` |
| 8 | `remove(2)` | 2 | `[[2,1]]` | match at i=0, overwrite value with `-1` | `[[2,-1]]` | `None` |
| 9 | `get(2)` | 2 | `[[2,-1]]` | match at i=0, returns sentinel | `[[2,-1]]` | `-1` |

Result: `[None, None, None, 1, -1, None, 1, None, -1]`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n / size) average, O(n) worst case
```

Why?

- `n` = number of pairs stored; keys are spread across `size = 1000` fixed buckets, so each `put`/`get`/`remove` only scans its own bucket's chain (average length `n / size`).
- Worst case (all keys collide into the same bucket, e.g. every key a multiple of `1000` apart) degrades to `O(n)`, same as the brute-force list scan.

### Space Complexity

```text
O(n + size)
```

Why?

- `data` always holds `size = 1000` buckets regardless of how many keys are stored.
- Each `put` (and, in this implementation, each `remove`) leaves one entry per distinct key in its bucket — `remove` overwrites the value with `-1` in place rather than deleting the entry, so the chain length never shrinks even after a key is "removed".
