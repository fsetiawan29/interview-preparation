# Problem

Name: Maximum Number of Vowels in a Substring of Given Length

Difficulty: Medium

----------------------------------------

# Pattern
Fixed-Size Sliding Window


----------------------------------------

# Recognition

Idea

- Keep a `VOWELS` set for `O(1)` membership checks.
- Initialize the sliding window with:
  - `left = 0`
  - `right = k - 1` because `right` represents the last index of a window with size `k`.
- Compute the initial window's vowel count with `countVowel(s, k)`, counting vowels in `s[:k]`.
- Initialize `best = window_vowels`, tracking the best **count** seen so far.
- Slide the window until `right` reaches the end of the string:
  - Update `best` if the current `window_vowels` is larger.
  - If `right` is already at the last index, stop.
  - Otherwise:
    - If `s[left]` (the character leaving the window) is a vowel, decrement `window_vowels`.
    - If `s[right + 1]` (the character entering the window) is a vowel, increment `window_vowels`.
    - Advance both `left` and `right`.
- Return `best`.

Steps

1. Count the vowels in the first window.
2. Initialize the best vowel count.
3. Slide the window one position at a time.
4. Update the window's vowel count and the best count seen so far.
5. Return the best count.

Mistakes
- Break the next slide window with `right == len(nums)`, should be `right == len(nums) - 1`
- Forget to calculate the `best`


----------------------------------------

# Complexity

- Time: `O(n)` — n = len(s), one pass sliding the window across the string
- Space: `O(1)` — a fixed-size `VOWELS` set, a running `window_vowels` count, and two pointers
