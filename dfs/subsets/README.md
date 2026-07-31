# Problem: Subsets

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

### Input

- An integer array `nums` of unique elements

### Output

- A list of lists, where each inner list is one subset of `nums`, and together they form the full power set.

### Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are unique.

### Example

Input:

```text
nums = [1,2,3]
```

Output:

```text
[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

---

## 2. Brute Force Approach

### Idea

Enumerate every possible subset using a bitmask. For `n` elements there are exactly `2^n` possible subsets, and each one corresponds to a unique integer from `0` to `2^n - 1`: bit `i` of that integer tells whether `nums[i]` is included.

### Pseudocode

```text
n = length(nums)
result = []

for mask in 0 .. (2^n - 1):
    subset = []
    for i in 0 .. n-1:
        if bit i of mask is set:
            subset.append(nums[i])
    result.append(subset)

return result
```

### Complexity Analysis

#### Time Complexity

```text
O(n * 2^n)
```

Why?

- There are `2^n` masks to try, and building each subset requires checking all `n` bits.

#### Space Complexity

```text
O(n)
```

Why?

- Excluding the output, only one `subset` list (up to size `n`) is being built at a time.

### Why this isn't good enough

It matches the optimal time complexity, but it hides the underlying decision structure behind bit tricks. Expressing the same generation as a "take or skip" recursion instead makes the decision explicit at each index, which is the pattern that generalizes to every other problem in this group (duplicates, target sums, fixed-size combinations, etc.).

---

## 3. Key Insight

### What makes this problem difficult?

The output isn't one answer but every combination of decisions — for each of the `n` elements there's an independent binary choice (include it or not), and those choices compound across all `n` elements into `2^n` outcomes.

### Key Observation

Every subset can be built by walking through `nums` index by index and making exactly one binary decision per index: take `nums[index]` or skip it. Once all `n` decisions have been made (`index == len(nums)`), whatever has been accumulated is a complete, valid subset — unlike Word Search, there's no "invalid" state to detect and prune.

### Why does this observation help?

This turns "generate the power set" into a simple recursion with exactly 2 branches per call — take, then skip — and a base case that only needs to *record* the current path, not validate it. Every root-to-leaf path through this decision tree is automatically a distinct, valid subset.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a binary decision tree with one level per element in `nums`. At each level the tree forks into two branches: "take this element" and "skip this element." Walking any root-to-leaf path spells out one sequence of take/skip decisions, and whatever was taken along the way forms one subset. With `n` levels there are `2^n` leaves — exactly matching `2^n` subsets.

```text
                         []
              take /            \ skip
            [1]                    []
        take/ \skip           take/  \skip
     [1,2]     [1]           [2]      []
    take/\skip take/\skip  take/\skip take/\skip
 [1,2,3][1,2] [1,3][1]    [2,3] [2]  [3]   []
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
dfs(index, subset)
   │
   ▼
Is index == len(nums) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Record a copy    TAKE: subset.append(nums[index])
of subset into          │
result                  ▼
                  dfs(index + 1, subset)
                        │
                        ▼
                  BACKTRACK: subset.pop()
                        │
                        ▼
                  SKIP: dfs(index + 1, subset)
```

Explanation of each decision:

- Checking `index == len(nums)` first means every element has already been decided (taken or skipped) by the time this frame is reached — the accumulated `subset` is already a complete, valid answer.
- Recording `subset.copy()` (not `subset` itself) is required because `subset` keeps mutating as the recursion continues — storing the reference directly would let every recorded "subset" reflect only the final state.
- The `pop()` between the take and skip branches undoes the take, restoring `subset` to exactly the state it had on entry to this frame, so the skip branch starts clean.

---

## 6. Plain English Algorithm

1. Start `dfs` at `index = 0` with an empty `subset`.
2. If `index` has reached `len(nums)`, every element has been decided — append a copy of `subset` to `result` and return.
3. Otherwise, take `nums[index]`: append it to `subset`, then recurse to `index + 1`.
4. After that branch returns, backtrack by popping `nums[index]` back off `subset`, so it doesn't leak into the next branch.
5. Skip `nums[index]`: recurse to `index + 1` again, this time without it in `subset`.
6. Once the initial `dfs(0, [])` call returns, `result` holds every subset — return it.

---

## 7. Pseudocode

```text
function dfs(index, subset):
    if index == length(nums):
        result.append(copy of subset)
        return

    subset.append(nums[index])   # take
    dfs(index + 1, subset)

    subset.pop()                 # backtrack

    dfs(index + 1, subset)       # skip

result = []
dfs(0, [])
return result
```

---

## 8. Python Solution

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        def dfs(index, subset):
            if index == len(nums):
                result.append(subset.copy())
                return

            # Take
            subset.append(nums[index])
            dfs(index+1, subset)

            # Backtrack
            subset.pop()

            # Skip
            dfs(index+1, subset)

        dfs(0, [])
        return result
```

---

## 9. Dry Run

Example:

```text
nums = [1,2,3]
```

| Step | Call | `subset` before | Action | `subset` after | Why? |
|------|------|------------------|--------|-----------------|------|
| 1 | `dfs(0, [])` | `[]` | take `1` | `[1]` | begin take branch for index 0 |
| 2 | `dfs(1, [1])` | `[1]` | take `2` | `[1,2]` | take branch for index 1 |
| 3 | `dfs(2, [1,2])` | `[1,2]` | take `3` | `[1,2,3]` | take branch for index 2 |
| 4 | `dfs(3, [1,2,3])` | `[1,2,3]` | `index==len(nums)` → record `[1,2,3]` | `[1,2,3]` | full take path |
| 5 | return to `dfs(2,...)` | `[1,2,3]` | `pop()` | `[1,2]` | backtrack index 2's take |
| 6 | `dfs(3, [1,2])` | `[1,2]` | `index==len(nums)` → record `[1,2]` | `[1,2]` | index 2 skipped |
| 7 | return to `dfs(1,...)` | `[1,2]` | `pop()` | `[1]` | backtrack index 1's take |
| 8 | `dfs(2, [1])` | `[1]` | take `3` | `[1,3]` | index 1 skipped, take index 2 |
| 9 | `dfs(3, [1,3])` | `[1,3]` | record `[1,3]` | `[1,3]` | full path |
| 10 | return to `dfs(2,...)` | `[1,3]` | `pop()` | `[1]` | backtrack index 2's take |
| 11 | `dfs(3, [1])` | `[1]` | record `[1]` | `[1]` | indices 1 and 2 both skipped |
| 12 | return to `dfs(0,...)` | `[1]` | `pop()` | `[]` | backtrack index 0's take |
| 13 | `dfs(1, [])` | `[]` | mirrors steps 2–11 without `1` | — | produces `[2,3]`, `[2]`, `[3]`, `[]` |

Result: `[[1,2,3],[1,2],[1,3],[1],[2,3],[2],[3],[]]` (order follows take-before-skip recursion; matches the expected power set)

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n * 2^n)
```

Why?

- There are `2^n` leaves in the decision tree, one per subset, and recording each one via `subset.copy()` costs `O(n)`. Every internal node does `O(1)` work, so the total is dominated by `O(n * 2^n)`.

### Space Complexity

```text
O(n)
```

Why?

- Excluding the output, the recursion stack holds at most `n` frames (one per index, down to the base case), and `subset` itself holds at most `n` elements at a time. The `O(n * 2^n)` needed to store the output is required by the problem, not extra auxiliary space.
