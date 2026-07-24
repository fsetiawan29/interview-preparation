# Problem: Longest Repeating Character Replacement

## 1. Problem Understanding

### Problem Summary

Given a string `s` and an integer `k`, you may change up to `k` characters of `s` to any other uppercase English letter. Return the length of the longest substring that can be made to contain a single repeating letter after performing at most `k` such changes.

### Input

- A string `s` (uppercase English letters only)
- An integer `k`

### Output

- An integer: the length of the longest substring achievable where every character is the same letter, after at most `k` replacements.

### Constraints

- `1 <= s.length <= 10^5`
- `s` consists of only uppercase English letters.
- `0 <= k <= s.length`

### Example

Input:

```text
s = "ABAB", k = 2
```

Output:

```text
4
```

Explanation: Replace the two 'A's with two 'B's or vice versa.

Input:

```text
s = "AABABBA", k = 1
```

Output:

```text
4
```

Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA". The substring "BBBB" has the longest repeating letters, which is 4.

---

## 2. Brute Force Approach

### Idea

For every possible start index `left`, extend `right` outward one character at a time, keeping a frequency count for the current `[left, right]` window. At each step, check whether `(window length) - (max letter frequency in window) <= k`, and track the best window length that satisfies it. Unlike the optimized version, the window here never shrinks — every `(left, right)` pair is tried.

### Pseudocode

```text
n = length(s)
best = 0

for left = 0 to n - 1
    freq = {}
    max_freq = 0
    for right = left to n - 1
        freq[s[right]] = freq.get(s[right], 0) + 1
        max_freq = max(max_freq, freq[s[right]])

        window_len = right - left + 1
        if window_len - max_freq <= k
            best = max(best, window_len)

return best
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- `n = len(s)`; there are `n` possible start indices for `left`.
- For each `left`, `right` scans forward up to `n - left` positions, doing `O(1)` frequency work (bounded by 26 letters) at each step.
- Total: `O(n^2)`, which hits `~10^10` operations at the given constraint (`n` up to `10^5`) — too slow.

#### Space Complexity

```text
O(1)
```

Why?

- `freq` holds at most 26 uppercase-letter keys, independent of `n`, and is reset for each `left`.

### Why this isn't good enough

Every new `left` throws away the frequency information built up for the previous `left` and starts over, even though most of the window's content didn't change. Sliding a single window with a bounded shrink — instead of restarting from every `left` — is what brings this down to `O(n)`.

---

## 3. Key Insight

### What makes this problem difficult?

Checking every substring and every way to spend up to `k` replacements on it is combinatorial — far too slow for `s.length` up to `10^5`. The problem also mixes two things that need to be tracked together: which letter a window is "aiming" to become, and how many of the other letters in that window would need to change to reach it.

### Key Observation

A window `[left, right]` can be turned into one repeated letter with at most `k` replacements exactly when:

```text
(window length) - (count of the most frequent letter in the window) <= k
```

The left side is "how many letters in this window are *not* the majority letter" — those are the ones that would need replacing. `max_freq` (the count of the most frequent letter seen so far in the current window) can be tracked incrementally as `right` advances, instead of rescanning the window every time.

Example:

```text
s = "AABABBA", k = 1
window "AABA" (indices 0..3): length 4, max_freq(A) = 3 -> 4 - 3 = 1 <= 1  -> valid, can become "AAAA"
```

### Why does this observation help?

It reduces "can this window become monochrome?" to a single `O(1)` arithmetic check (`window_length - max_freq > k`) driven by a running frequency map, so the whole scan stays `O(n)` instead of re-deriving the majority count for every window from scratch.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a window sliding across `s`, carrying a letter tally and a "best letter count seen so far" (`max_freq`). As long as everything else in the window (`window_length - max_freq`) fits within the `k` replacements budget, the window keeps growing. The moment it doesn't fit, the window shrinks from the left by exactly one — just enough to stay within budget — rather than resetting.

```text
s:  A  A  B  A  B  B  A
k = 1

right=3: window "AABA"   length=4  max_freq=3 (A)   4-3=1 <= 1  -> valid, answer=4
right=4: window "AABAB"  length=5  max_freq=3 (A)   5-3=2 > 1   -> shrink left once
          window "ABAB"  length=4  max_freq=3 (A, stale but still valid ceiling)  4-3=1 <= 1 -> valid, answer stays 4
```

Note: `max_freq` is only ever pushed up, never recomputed downward after a shrink. It becomes a "high-water mark" — even if it's stale (no longer the true max of the shrunk window), it can only make the shrink condition *stricter*, never wrongly accept an invalid window. Since the answer is only updated to `right - left + 1`, and the window size never exceeds a previously-achieved valid size without a genuinely higher `max_freq` backing it, the final answer is still correct.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
left = 0, freq = {}, max_freq = 0, answer = 0
   │
   ▼
For right in 0 .. len(s)-1:
   │
   ▼
Add s[right] to freq; max_freq = max(max_freq, freq[s[right]])
   │
   ▼
Is (right - left + 1) - max_freq > k ?
   │
 ┌─┴─────────────────────┐
 │                        │
Yes                       No
 │                        │
 ▼                        │
Shrink: freq[s[left]] -= 1        │
left += 1                          │
Re-check the same condition        │
(loop until it's no longer > k)    │
 │                        │
 └───────────┬────────────┘
             ▼
   answer = max(answer, right - left + 1)
             │
             ▼
   Next right (or return answer if done)
```

Explanation of each decision:

- `max_freq` is updated *before* the shrink check, since the just-added character might itself be the new majority letter.
- The shrink is a `while`, not an `if`, but in practice it fires at most once per step here — because `max_freq` never decreases, the window length can grow by at most one before needing to shrink by at most one.
- `answer` is updated *after* the window is valid again, so it only ever records lengths that satisfy the replacement budget.

---

## 6. Plain English Algorithm

1. Initialize `left = 0`, an empty frequency map `freq`, `max_freq = 0`, and `answer = 0`.
2. For each `right` from `0` to `len(s) - 1`:
   - Add `s[right]` to `freq` and increment its count.
   - Update `max_freq` to be the larger of its current value and `freq[s[right]]`.
   - While the window's non-majority letters exceed the budget (`(right - left + 1) - max_freq > k`), remove `s[left]` from `freq` and advance `left`.
   - Update `answer` to the larger of its current value and the current window size `right - left + 1`.
3. Return `answer`.

---

## 7. Pseudocode

```text
left = 0
freq = {}
max_freq = 0
answer = 0

for right in 0 .. length(s) - 1
    freq[s[right]] = freq.get(s[right], 0) + 1
    max_freq = max(max_freq, freq[s[right]])

    while (right - left + 1) - max_freq > k
        freq[s[left]] -= 1
        left += 1

    answer = max(answer, right - left + 1)

return answer
```

---

## 8. Python Solution

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        left = 0
        freq = {}
        answer = 0
        max_freq = 0

        for right in range(len(s)):
            freq[s[right]] = freq.get(s[right], 0) + 1

            max_freq = max(max_freq, freq[s[right]])

            # replacement
            while (right - left + 1) - max_freq > k:
                freq[s[left]] -= 1
                left += 1

            answer = max(answer, right - left + 1)

        return answer
```

---

## 9. Dry Run

Example:

```text
s = "AABABBA", k = 1
```

| right | char | freq (after add) | max_freq | window size (before shrink) | Shrink? | left (after) | window size (final) | answer |
|-------|------|-------------------|----------|-------------------------------|---------|---------------|------------------------|--------|
| 0 | A | {A:1} | 1 | 1 | No | 0 | 1 | 1 |
| 1 | A | {A:2} | 2 | 2 | No | 0 | 2 | 2 |
| 2 | B | {A:2,B:1} | 2 | 3 | No | 0 | 3 | 3 |
| 3 | A | {A:3,B:1} | 3 | 4 | No | 0 | 4 | 4 |
| 4 | B | {A:3,B:2} | 3 | 5 | Yes: freq[A]=2, left=1 | 1 | 4 | 4 |
| 5 | B | {A:2,B:3} | 3 | 5 | Yes: freq[A]=1, left=2 | 2 | 4 | 4 |
| 6 | A | {A:2,B:3} | 3 | 5 | Yes: freq[B]=2, left=3 | 3 | 4 | 4 |

Result: `4`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(s)`; `right` visits every index once, and `left` only ever moves forward, so it advances at most `n` times in total across the whole run.
- Each iteration does `O(1)` frequency-map work (bounded by 26 uppercase letters), not a rescan of the window.

### Space Complexity

```text
O(1)
```

Why?

- `freq` holds at most 26 uppercase-letter keys, independent of `len(s)`.
