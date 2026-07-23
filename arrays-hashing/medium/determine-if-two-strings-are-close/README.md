# Problem

Name: Determine if Two Strings Are Close

Difficulty: Medium

----------------------------------------

# Pattern
Hash Map — Frequency Count

----------------------------------------

# Recognition

Idea
- Operation 1 (swap any two characters) means *positions* never matter —
  only which characters appear and how often.
- Operation 2 (swap all occurrences of one character with another) means
  the *character labels* never matter either — only the multiset of
  frequencies. Two strings are close exactly when they use the same set
  of characters, and that set's frequencies match up after sorting (each
  frequency value can be "relabeled" onto a matching frequency in the
  other string via repeated Operation 2).
- So two conditions, both on frequency: same character set, same sorted
  list of frequency counts.

Steps

- GUARD: if `len(word1) != len(word2)`, return `False` — different
  lengths can never have matching frequency multisets
- COUNT: build `freq1`, a char → count map, one pass over `word1`
- COUNT: build `freq2`, a char → count map, one pass over `word2`
- CHECK SET: `freq1.keys() == freq2.keys()` — same characters used, just
  maybe at different frequencies
- CHECK MULTISET: `sorted(freq1.values()) == sorted(freq2.values())` —
  the frequency counts themselves match once relabeled via Operation 2
- RETURN: `True` only if both checks pass

Mistakes
- Forget to check the length must be same — a length mismatch can't be
  fixed by either operation, so skipping this guard lets same-length-only
  logic (like the sorted-values comparison) give a false positive.
- Comparing `freq1 == freq2` directly instead of `.keys()` and
  `sorted(.values())` separately — that would wrongly require the exact
  same character-to-count mapping instead of allowing Operation 2 to
  relabel counts between different characters.

----------------------------------------

# Complexity

- Time: `O(n)` — n = len(word1) == len(word2); two passes to build the
  frequency maps, plus sorting the value lists which is bounded by the
  26-letter alphabet (`O(1)`)
- Space: `O(1)` — both frequency maps are bounded by the lowercase
  English alphabet (at most 26 entries), independent of string length
