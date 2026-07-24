# Problem: Maximum Average Subarray I

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` and an integer `k`, find the contiguous subarray of length `k` that has the maximum average value, and return that average.

### Input

- An integer array `nums`
- An integer `k`

### Output

- A float: the maximum average of any contiguous subarray of length `k`.

### Constraints

- `n == nums.length`
- `1 <= k <= n <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

### Example

Input:

```text
nums = [1,12,-5,-6,50,3], k = 4
```

Output:

```text
12.75000
```

Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75

Manual walkthrough:

```text
nums: 1 12 -5 -6 50 3

Windows of size 4:
[1,12,-5,-6]  sum=2    avg=0.5
[12,-5,-6,50] sum=51   avg=12.75  <- best
[-5,-6,50,3]  sum=42   avg=10.5

-> 12.75000
```

---

## 2. Brute Force Approach

### Idea

For every possible start index, sum the `k` elements of that window from scratch, then keep the best sum seen. Divide by `k` only at the very end.

### Pseudocode

```text
n = length(nums)
best = -infinity

for i = 0 to n - k
    window_sum = 0
    for j = i to i + k - 1
        window_sum += nums[j]
    best = max(best, window_sum)

return best / k
```

### Complexity Analysis

#### Time Complexity

```text
O(n * k)
```

Why?

- There are roughly `n = len(nums)` starting positions to try.
- For each one, summing the window from scratch costs `O(k)`.
- Total: `O(n * k)`, which hits `~10^10` operations at the given constraint (`n` up to `10^5`) — too slow.

#### Space Complexity

```text
O(1)
```

Why?

- Only `window_sum` and `best` are used; no additional array or data structure is created.

### Why this isn't good enough

Every window re-adds `k` elements even though consecutive windows share `k - 1` of them. Sliding the sum incrementally — dropping one element, adding one element — is what removes that repeated work.

---

## 3. Key Insight

### What makes this problem difficult?

Recomputing the sum of every length-`k` window from scratch is `O(n * k)` — wasteful, since consecutive windows overlap in all but two elements.

### Key Observation

Sliding the window by one position only changes two elements: the value leaving on the left and the value entering on the right. The sum can be updated incrementally instead of recomputed.

Example:

```text
window [1,12,-5,-6] sum = 2
slide right by one -> drop 1, add 50
new sum = 2 - 1 + 50 = 51
```

### Why does this observation help?

Updating the sum in `O(1)` per slide turns the whole scan into `O(n)` total. Dividing by `k` is also deferred until the very end (applied only to the best sum found), avoiding a division on every single window.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a window of fixed width `k` sliding one step at a time across the array, carrying a running total. Each slide simply swaps the outgoing left value for the incoming right value in that total.

```text
nums:  1  12  -5  -6  50   3
      [--------------]
      window_sum = 2

slide ->

nums:  1  12  -5  -6  50   3
          [--------------]
      window_sum = 2 - 1 + 50 = 51
```

The best sum seen across all slides, divided by `k` once at the end, is the answer.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize left = 0, right = k - 1
window_sum = sum(nums[0..k-1])
best = window_sum
   │
   ▼
Is right < len(nums) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
best = max(best, window_sum)   Return best / k
 │
 ▼
Is right == len(nums) - 1 ?
 │
┌─┴───────┐
│         │
Yes       No
│         │
▼         ▼
break     Slide: window_sum -= nums[left]
          window_sum += nums[right + 1]
          left += 1, right += 1
          │
          └──▶ (back to "Is right < len(nums) ?")
```

Explanation of each decision:

- The window starts already covering indices `0..k-1`, so its sum is computed once up front.
- `best` is updated with the *current* window before checking whether to slide further.
- Stopping when `right` reaches the last index avoids sliding past the end of the array.
- Dividing by `k` only happens once, on the final `best` sum.

---

## 6. Plain English Algorithm

1. Set `left = 0` and `right = k - 1` — the first window covers indices `0` through `k - 1`.
2. Compute `window_sum` as the sum of that first window; initialize `best` to it.
3. While `right` is within the array:
   - Update `best` with the larger of `best` and `window_sum`.
   - If `right` is already the last index, stop sliding.
   - Otherwise, remove `nums[left]` and add `nums[right + 1]` to `window_sum`, then advance both `left` and `right`.
4. Return `best / k`.

---

## 7. Pseudocode

```text
left = 0
right = k - 1
window_sum = sum(nums[0..k-1])
best = window_sum

while right < length(nums)
    best = max(best, window_sum)

    if right == length(nums) - 1
        break

    window_sum -= nums[left]
    window_sum += nums[right + 1]

    left++
    right++

return best / k
```

---

## 8. Python Solution

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        left = 0
        right = k - 1
        window_sum = sum(nums[:k])
        best = window_sum

        while right < len(nums):
            best = max(best, window_sum)

            if right == len(nums) - 1:
                break

            window_sum -= nums[left]
            window_sum += nums[right + 1]

            left += 1
            right += 1

        return best / k
```

---

## 9. Dry Run

Example:

```text
nums = [1, 12, -5, -6, 50, 3], k = 4
```

| Step | left, right | window_sum | best | Action | Why? |
|------|-------------|------------|------|--------|------|
| 1 | 0, 3 | 2 | 2 | best=max(2,2)=2; slide: sum -= nums[0]=1, += nums[4]=50 -> 51 | right(3) != last index (5) |
| 2 | 1, 4 | 51 | 51 | best=max(2,51)=51; slide: sum -= nums[1]=12, += nums[5]=3 -> 42 | right(4) != last index (5) |
| 3 | 2, 5 | 42 | 51 | best=max(51,42)=51; right==last index -> break | right(5) == last index (5) |

Result: `best / k = 51 / 4 = 12.75000`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(nums)`; the initial window sum is computed once in `O(k)`.
- Each subsequent slide does `O(1)` work, and there are `O(n)` slides total.

### Space Complexity

```text
O(1)
```

Why?

- Only `window_sum`, `best`, and the two pointers are used.
- No additional array or data structure is created.
