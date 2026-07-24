# Problem: Maximum Sum of Distinct Subarrays With Length K

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` and an integer `k`, find the maximum subarray sum among all contiguous subarrays of length `k` whose elements are all distinct. If no such subarray exists, return `0`.

### Input

- An integer array `nums`
- An integer `k`

### Output

- An integer: the maximum sum of a length-`k` subarray with all distinct elements, or `0` if none exists.

### Constraints

- `1 <= k <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

### Example

Input:

```text
nums = [1,5,4,2,9,9,9], k = 3
```

Output:

```text
15
```

Explanation: The subarrays of length 3 with distinct elements are [1,5,4] and [5,4,2]. The maximum subarray sum is 15.

Manual walkthrough:

```text
nums: 1 5 4 2 9 9 9

[1,5,4] all distinct, sum=10
[5,4,2] all distinct, sum=11
[4,2,9] all distinct, sum=15   <- best
[2,9,9] has a repeated 9 -> skip
[9,9,9] has repeated 9s -> skip

-> 15
```

---

# 2. Key Insight

## What makes this problem difficult?

Two things need tracking at once for every length-`k` window: its sum, and whether all its elements are distinct. A naive approach might rebuild a `set` from scratch for every window to check distinctness, which is `O(n * k)`.

## Key Observation

A frequency map (not a set) can track both the running sum incrementally *and* distinctness: a window of size `k` has all-distinct elements exactly when the frequency map has `k` distinct keys — i.e. `len(freq) == k`. As the window slides, only one key's count decreases and one key's count increases (or a new key appears).

Example:

```text
window [4,2,9] -> freq = {4:1, 2:1, 9:1}, len(freq) = 3 == k -> distinct, sum=15
slide -> window [2,9,9] -> freq = {2:1, 9:2}, len(freq) = 2 != k -> not distinct
```

## Why does this observation help?

`len(freq) == k` is an `O(1)` check (dictionary length), replacing an `O(k)` rebuild-and-check for every window. Combined with an incrementally maintained `window_sum`, each slide is `O(1)`, keeping the whole scan `O(n)`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a window of fixed width `k` sliding across the array, carrying both a running sum and a tally of how many times each value currently appears inside it. The window qualifies as "all distinct" the instant the tally has exactly `k` different keys — any duplicate collapses two keys into one, immediately shrinking that count below `k`.

```text
nums: 1  5  4  2  9  9  9
     [-----]
     freq = {1:1, 5:1, 4:1}  len=3==k  sum=10  -> valid

slide ->

nums: 1  5  4  2  9  9  9
         [-----]
     freq = {5:1, 4:1, 2:1}  len=3==k  sum=11  -> valid

... slide further ...

nums: 1  5  4  2  9  9  9
               [-----]
     freq = {2:1, 9:2}       len=2!=k  sum=20  -> NOT valid (9 repeats)
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize left = 0, freq = {}, window_sum = 0, best_sum = 0
   │
   ▼
For right = 0 .. len(nums)-1
   │
   ▼
Add nums[right]: freq[nums[right]]++, window_sum += nums[right]
   │
   ▼
Is right - left + 1 == k ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is len(freq) == k ?   (continue to next right)
 │
┌─┴───────┐
│         │
Yes       No
│         │
▼         ▼
best_sum = max(best_sum, window_sum)   (skip update)
│         │
└────┬────┘
     ▼
Remove nums[left]: window_sum -= nums[left]
freq[nums[left]]--, delete key if 0
left += 1
     │
     └──▶ next right
               │
               ▼
       Loop finished -> Return best_sum
```

Explanation of each decision:

- Every `nums[right]` is added to the window's frequency map and sum before the window's size is checked.
- The window only qualifies for a `best_sum` update once it reaches exactly size `k`.
- `len(freq) == k` is the distinctness test: if any value repeats, the number of distinct keys is strictly less than `k`.
- After checking, the window always slides — removing the leftmost element and advancing `left` — so it keeps size `k` for the next iteration.
- Deleting a key once its frequency reaches `0` keeps `len(freq)` an accurate count of distinct values currently in the window.

---

# 5. Plain English Algorithm

1. Initialize `left = 0`, an empty frequency map `freq`, `window_sum = 0`, and `best_sum = 0`.
2. For each `right` from `0` to `len(nums) - 1`:
   - Increment `freq[nums[right]]` and add `nums[right]` to `window_sum`.
   - Once the window reaches size `k` (`right - left + 1 == k`):
     - If `len(freq) == k`, every element in the window is distinct — update `best_sum` with the larger of `best_sum` and `window_sum`.
     - Remove `nums[left]` from `window_sum`, decrement `freq[nums[left]]` (deleting the key if it hits `0`), and advance `left`.
3. Return `best_sum`.

---

# 6. Pseudocode

```text
left = 0
freq = {}
window_sum = 0
best_sum = 0

for right = 0 to length(nums) - 1
    freq[nums[right]] = freq.get(nums[right], 0) + 1
    window_sum += nums[right]

    if right - left + 1 == k
        if length(freq) == k
            best_sum = max(best_sum, window_sum)

        window_sum -= nums[left]
        freq[nums[left]] -= 1
        if freq[nums[left]] == 0
            delete freq[nums[left]]

        left++

return best_sum
```

---

# 7. Python Solution

```python
class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        left = 0
        freq = {}
        window_sum = 0
        best_sum = 0

        for right in range(len(nums)):
            nums_right = nums[right]
            freq[nums_right] = freq.get(nums_right, 0) + 1
            window_sum += nums_right

            if right - left + 1 == k:
                if len(freq) == k:
                    best_sum = max(best_sum, window_sum)

                nums_left = nums[left]
                window_sum -= nums_left
                freq[nums_left] -= 1
                if freq[nums_left] == 0:
                    del freq[nums_left]

                left += 1

        return best_sum
```

---

# 8. Dry Run

Example:

```text
nums = [1, 5, 4, 2, 9, 9, 9], k = 3
```

| Step | right | freq (after add) | window_sum | size==k? | len(freq)==k? | best_sum | Slide (remove nums[left]) |
|------|-------|--------------------|------------|----------|----------------|----------|------------------------------|
| 1 | 0 | {1:1} | 1 | No | — | 0 | — |
| 2 | 1 | {1:1,5:1} | 6 | No | — | 0 | — |
| 3 | 2 | {1:1,5:1,4:1} | 10 | Yes | Yes (3==3) | 10 | remove 1 -> sum=9, freq={5:1,4:1}, left=1 |
| 4 | 3 | {5:1,4:1,2:1} | 11 | Yes | Yes (3==3) | 11 | remove 5 -> sum=6, freq={4:1,2:1}, left=2 |
| 5 | 4 | {4:1,2:1,9:1} | 15 | Yes | Yes (3==3) | 15 | remove 4 -> sum=11, freq={2:1,9:1}, left=3 |
| 6 | 5 | {2:1,9:2} | 20 | Yes | No (2!=3) | 15 | remove 2 -> sum=18, freq={9:2}, left=4 |
| 7 | 6 | {9:3} | 27 | Yes | No (1!=3) | 15 | remove 9 -> sum=18, freq={9:2}, left=5 |

Result: `best_sum = 15`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(nums)`; one pass sliding the window across the array.
- Each add/remove of a frequency entry and each `len(freq)` check is `O(1)`.

### Space Complexity

```text
O(k)
```

Why?

- `freq` holds at most `k` entries — one per element currently in the window.
