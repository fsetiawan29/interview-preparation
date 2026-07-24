# Problem: Merge Sorted Array

## 1. Problem Understanding

### Problem Summary

Given two integer arrays `nums1` and `nums2`, both sorted in non-decreasing order, merge `nums2` into `nums1` so that `nums1` becomes one single sorted array.

`nums1` has extra trailing space to hold the merged result: its first `m` elements are the real values to merge, and its last `n` elements are placeholder `0`s reserved for `nums2`'s `n` values. `nums2` itself has exactly `n` elements.

The merge must be done **in-place**, inside `nums1` — no new array is returned.

### Input

- An integer array `nums1` of length `m + n`
- An integer `m` — the count of real values at the front of `nums1`
- An integer array `nums2` of length `n`
- An integer `n` — the count of values in `nums2`

### Output

- Nothing is returned; `nums1` is modified in-place to hold all `m + n` values in sorted order.

### Constraints

- `nums1.length == m + n`
- `nums2.length == n`
- `0 <= m, n <= 200`
- `1 <= m + n <= 200`
- `-10^9 <= nums1[i], nums2[j] <= 10^9`

### Example

Input:

```text
nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
```

Output:

```text
[1,2,2,3,5,6]
```

Manual walkthrough:

```text
Real values

nums1 (first m):  [1,2,3]
nums2:             [2,5,6]

Merge the two sorted lists into one sorted sequence

↓

[1,2,2,3,5,6]

Written back into nums1, which had room for exactly this many values
```

---

# 2. Key Insight

## What makes this problem difficult?

`nums1`'s real values sit at the *front*, but the free space to write merged results also sits inside `nums1`, at the *back*. Merging left-to-right (the usual way to merge two sorted lists) would overwrite real values in `nums1` before they've been read and compared.

## Key Observation

Since the merged result is exactly `m + n` values and `nums1` already has exactly that much space, filling `nums1` **from the back forward** guarantees every write lands on a slot that's either unused padding or a value that's already been read and copied elsewhere. The largest remaining value — whichever of `nums1[i]` or `nums2[j]` is bigger — always belongs in the current last unfilled slot.

Example:

```text
nums1 = [1,2,3,0,0,0], m=3        nums2 = [2,5,6], n=3
             ↑                                 ↑
             i (last real value)               j (last value)

nums1[i]=3 < nums2[j]=6 -> 6 is the biggest remaining value overall,
so it belongs in the very last slot of nums1
```

## Why does this observation help?

Comparing `nums1[i]` and `nums2[j]` from the back and writing the bigger one into the back of `nums1` never destroys a value that still needs to be read — everything ahead of the write pointer `w` (toward the front) is still untouched real data, and everything behind it is already finalized. This turns the merge into a single `O(m + n)` pass with no extra array.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture filling a shelf from the right end backward. Two people, one holding `nums1`'s remaining real values and one holding `nums2`'s values, each present their *largest remaining* item. Whichever is bigger gets placed on the shelf's current rightmost open slot, and that person steps back to their next-largest item.

```text
nums1: [1,2,3,0,0,0]        nums2: [2,5,6]
            ↑                          ↑
            i                          j
                                              ↑
                                              w (rightmost open slot)

nums1[i]=3 vs nums2[j]=6 -> 6 is bigger -> place 6 at w, j moves back, w moves back

[1,2,3,0,0,6]
            ↑                       ↑
            i                       j
                                  ↑
                                  w
```

Once one side runs out, whatever's left on the other side is already sorted and already sitting in the correct front positions of `nums1` — for `nums2` leftovers specifically, they still need to be copied in; for `nums1` leftovers, they're already exactly where they belong.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize
i = m - 1  (last real value in nums1)
j = n - 1  (last value in nums2)
w = m + n - 1  (last slot in nums1)
   │
   ▼
Is i >= 0 AND j >= 0 ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is nums1[i] >= nums2[j] ?   Is j >= 0 ? (nums2 has leftovers)
   │                            │
 ┌─┴────────┐                 ┌─┴────────┐
 │          │                 │          │
Yes         No                Yes        No
 │          │                 │          │
 ▼          ▼                 ▼          ▼
nums1[w] = nums1[i]   nums1[w] = nums2[j]   nums1[w] = nums2[j]   Done — return
i -= 1                j -= 1                j -= 1               (nums1's own
 │          │          │                    w -= 1                leftovers are
 └────┬─────┘          └──────┬─────────────┘                     already in place)
      ▼                       │
   w -= 1                     └──▶ (repeat until j < 0)
      │
      └──▶ (back to "Is i >= 0 AND j >= 0 ?")
```

Explanation of each decision:

- The main loop only runs while **both** sides still have unmerged values — comparing is only meaningful when there's something on each side to compare.
- `nums1[i] >= nums2[j]` sends `nums1`'s value to the current back slot; otherwise `nums2`'s value goes there. Either way, `w` then moves one slot left.
- Once `j < 0`, every value in `nums2` has been placed — `nums1`'s remaining prefix `nums1[0..i]` is already sorted and already sits at the front, so no more writes are needed.
- Once `i < 0` first, `nums2` still has leftovers, and those must be explicitly copied into the remaining front slots of `nums1` (their sorted order is otherwise lost since `nums1` has no way to "already contain" them).

---

# 5. Plain English Algorithm

1. Point `i` at the last real value in `nums1` (`m - 1`), `j` at the last value in `nums2` (`n - 1`), and `w` at the last slot of `nums1` (`m + n - 1`).
2. While both `i` and `j` are still `>= 0`:
   - Compare `nums1[i]` and `nums2[j]`.
   - Write the bigger of the two into `nums1[w]`, then move that side's pointer (`i` or `j`) back by one.
   - Move `w` back by one.
3. If `nums2` still has leftover values (`j >= 0`), copy them into the remaining front slots of `nums1`, from `w` down to `0`.
4. If `nums1` still has leftover values instead, nothing more needs to happen — they're already in their correct sorted positions at the front.

---

# 6. Pseudocode

```text
i = m - 1
j = n - 1
w = m + n - 1

while i >= 0 and j >= 0
    if nums1[i] >= nums2[j]
        nums1[w] = nums1[i]
        i--
    else
        nums1[w] = nums2[j]
        j--

    w--

while j >= 0
    nums1[w] = nums2[j]
    j--
    w--
```

---

# 7. Python Solution

```python
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        i = m - 1
        j = n - 1
        w = m + n - 1

        while i >= 0 and j >= 0:
            if nums1[i] >= nums2[j]:
                nums1[w] = nums1[i]
                i -= 1
            else:
                nums1[w] = nums2[j]
                j -= 1

            w -= 1

        while j >= 0:
            nums1[w] = nums2[j]
            j -= 1
            w -= 1
```

---

# 8. Dry Run

Example:

```text
nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
```

| Step | i,j,w | nums1[i], nums2[j] | Action | Array State | Why? |
|------|-------|----------------------|--------|-------------|------|
| 1 | i=2,j=2,w=5 | 3, 6 | 3 not >= 6, write nums2[j]=6, j=1 | [1,2,3,0,0,6] | nums2's value is bigger |
| 2 | i=2,j=1,w=4 | 3, 5 | 3 not >= 5, write nums2[j]=5, j=0 | [1,2,3,0,5,6] | nums2's value is bigger |
| 3 | i=2,j=0,w=3 | 3, 2 | 3 >= 2, write nums1[i]=3, i=1 | [1,2,3,3,5,6] | nums1's value is bigger |
| 4 | i=1,j=0,w=2 | 2, 2 | 2 >= 2, write nums1[i]=2, i=0 | [1,2,2,3,5,6] | Tie resolved by taking nums1 |
| 5 | i=0,j=0,w=1 | 1, 2 | 1 not >= 2, write nums2[j]=2, j=-1 | [1,2,2,3,5,6] | nums2's value is bigger |
| 6 | i=0,j=-1 | — | Stop main loop | [1,2,2,3,5,6] | `j >= 0` is false |
| 7 | j=-1 | — | Skip leftover-copy loop | [1,2,2,3,5,6] | `j >= 0` is false, nothing left in nums2 |

Result: `[1,2,2,3,5,6]` — matches the expected output.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(m + n)
```

Why?

- Each of `i`, `j`, and `w` moves at most once per element.
- Every value from both arrays is written into `nums1` exactly once.

### Space Complexity

```text
O(1)
```

Why?

- The merge happens directly inside `nums1`, using its existing trailing space.
- Only the three pointers `i`, `j`, and `w` are used as extra state.
