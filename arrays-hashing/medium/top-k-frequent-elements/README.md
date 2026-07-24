# Problem: Top K Frequent Elements

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. The answer is guaranteed to be unique (no ties at the cutoff), and can be returned in any order.

### Input

- An array of integers `nums`
- An integer `k`

### Output

- An array of the `k` most frequent elements in `nums`.

### Constraints

- `1 <= nums.length <= 10^5`
- `k` is in the range `[1, the number of distinct elements in nums]`
- It is guaranteed that the answer is unique.

### Example

Input:

```text
nums = [1,1,1,2,2,3], k = 2
```

Output:

```text
[1,2]
```

Manual walkthrough:

```text
nums = [1,1,1,2,2,3]

Frequencies: 1 -> 3 times, 2 -> 2 times, 3 -> 1 time

Sorted by frequency (descending): 1 (3), 2 (2), 3 (1)

Take the top k=2: [1, 2]
```

---

# 2. Key Insight

## What makes this problem difficult?

Sorting all distinct elements by frequency to grab the top `k` costs `O(m log m)` where `m` is the number of distinct elements — not bad, but not the fastest possible, and it's easy to reach for `sorted()` without noticing a linear-time alternative exists.

## Key Observation

A frequency can never be larger than `len(nums)` (an element can't occur more times than there are elements in the array at all). That means frequency is a **bounded integer** — which makes it usable directly as a **bucket index**: create `len(nums) + 1` buckets, and drop each number into the bucket matching its own frequency.

Example:

```text
nums = [1,1,1,2,2,3]  (len = 6)

freq: {1:3, 2:2, 3:1}

buckets (index 0..6):
  bucket[1] = [3]
  bucket[2] = [2]
  bucket[3] = [1]
  (all other buckets empty)
```

## Why does this observation help?

Instead of sorting, walking the buckets from the highest index down to `1` visits elements in descending order of frequency "for free" — no comparison-based sort is needed, giving an overall `O(n)` solution (bucket sort).

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a row of labeled bins numbered `0` through `len(nums)`, one bin per possible frequency count. Every distinct number in `nums` gets dropped into the bin matching how many times it occurred. Reading the bins from the highest-numbered bin down to the lowest gives numbers in order from most frequent to least frequent.

```text
bins:  0    1    2    3    4    5    6
              [3]  [2]  [1]

Read from bin 6 down to bin 1:
  bin 6: empty
  bin 5: empty
  bin 4: empty
  bin 3: [1]   -> take 1
  bin 2: [2]   -> take 2   (now have k=2 results: [1, 2] -> stop)
```

No sorting needed — the bins themselves are already arranged from lowest frequency to highest, so reading backwards gives frequency order directly.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Build freq map: count occurrences of each number in nums
   │
   ▼
Create buckets = list of (len(nums)+1) empty lists
   │
   ▼
For each (n, c) in freq:
   Append n to buckets[c]
   │
   ▼
Initialize res = []
   │
   ▼
For i from len(buckets)-1 down to 1:
   │
   ▼
For each n in buckets[i]:
   │
   ▼
Append n to res
   │
   ▼
Is len(res) == k ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return res       Continue to next n /
                 next bucket index
```

Explanation of each decision:

- The frequency map's counts are guaranteed to be at most `len(nums)`, which is exactly why `len(nums)+1` buckets are enough to index every possible frequency.
- Walking bucket indices from highest to lowest visits numbers from most frequent to least frequent.
- The moment `res` reaches length `k`, the answer is complete and returned immediately — no need to keep scanning lower-frequency buckets.

---

# 5. Plain English Algorithm

1. Build a frequency map counting how many times each number appears in `nums`.
2. Create `len(nums) + 1` empty buckets, indexed `0` through `len(nums)`.
3. For each number and its count in the frequency map, append the number to the bucket at index equal to its count.
4. Walk the buckets from the highest index down to `1`:
   - For each number found in the current bucket, append it to the result.
   - As soon as the result has `k` elements, return it.

---

# 6. Pseudocode

```text
freq = empty map
for n in nums
    freq[n] = freq.get(n, 0) + 1

buckets = array of (length(nums) + 1) empty lists

for n, c in freq
    append n to buckets[c]

res = []
for i from length(buckets) - 1 down to 1
    for n in buckets[i]
        append n to res
        if length(res) == k
            return res
```

---

# 7. Python Solution

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # count the frequency
        freq = {}
        for n in nums:
            freq[n] = freq.get(n,0) + 1

        # store in the bucket with index is the count
        buckets = [[] for _ in range(len(nums)+1)]
        for n, c in freq.items():
            buckets[c].append(n)

        # harvest from the buckets
        res = []
        for i in range(len(buckets) - 1, 0, -1):
            for n in buckets[i]:
                res.append(n)
                if len(res) == k:
                    return res
```

---

# 8. Dry Run

Example:

```text
nums = [1,1,1,2,2,3], k = 2

freq = {1: 3, 2: 2, 3: 1}
buckets has indices 0..6 (len(nums)+1 = 7)
buckets[3] = [1], buckets[2] = [2], buckets[1] = [3], all others empty
```

| Step | Bucket index i | buckets[i] | Action | res after | len(res) == k? |
|------|-----------------|------------|--------|------------|-----------------|
| 1 | 6 | [] | Nothing to do | [] | No |
| 2 | 5 | [] | Nothing to do | [] | No |
| 3 | 4 | [] | Nothing to do | [] | No |
| 4 | 3 | [1] | Append 1 | [1] | No (1 != 2) |
| 5 | 2 | [2] | Append 2 | [1, 2] | Yes → return |

Result: `[1, 2]`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Counting frequencies is one linear pass, `O(n)`.
- Bucketing visits at most `n` distinct keys, `O(n)`.
- Harvesting walks at most `n+1` bucket slots and at most `n` total elements across all buckets combined.

### Space Complexity

```text
O(n)
```

Why?

- The frequency map holds at most `n` distinct keys.
- The buckets array holds `n+1` lists, whose combined contents hold at most `n` elements total.
