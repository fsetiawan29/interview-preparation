# Problem

Name: Custom Sort String

Difficulty: Medium

----------------------------------------

# Pattern
Hash Map — Frequency Count

----------------------------------------

# Recognition

Idea
- Count how many times each character of `s` occurs.
- Walk `order` once: for each character that appears in `s`, dump all of
  its occurrences into the result in one shot, then drop it from the
  frequency map so it isn't emitted again.
- Any character left in the frequency map never appeared in `order`, so
  its relative position is unconstrained — append it (and its full
  count) at the end in any order.

Steps

- COUNT: build `freq`, a char → count map, one pass over `s`
- ORDERED: for each `ch` in `order`, if `ch in freq`, append `ch * freq[ch]`
  to `res` and delete `ch` from `freq` — emits every occurrence at once
  and marks it as handled
- LEFTOVER: for each remaining `ch, count` in `freq` (chars not in
  `order`), append `ch * count` to `res`
- RETURN: `"".join(res)`

Mistakes
- I forgot that characters in `s` can appear multiple times.
  - When constructing the result based on `order`, append each character according to its frequency.

- Instead of decrementing the frequency one by one after processing a character, simply remove the key from the frequency map once all of its occurrences have been appended.

- After processing all characters in `order`, don't forget to append the remaining characters in the frequency map.
  - Each remaining character should be appended according to its frequency, not just once.


----------------------------------------

# Complexity

- Time: `O(n + m)` — n = len(s), m = len(order); one pass to build `freq`,
  one pass over `order`, and the leftover pass over `freq` together touch
  each character of `s` and `order` a constant number of times
- Space: `O(n)` — `freq` holds at most the distinct characters of `s`
  (bounded by the alphabet), and `res` holds all `n` output characters
