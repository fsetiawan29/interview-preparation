# Arrays & Hashing

## What is this pattern?

A broad bucket of problems solved by trading space for time: instead of
re-scanning the array (`O(n)` per lookup → `O(n^2)` overall), stash what
you've seen in a **hash set** or **hash map** so every lookup becomes `O(1)`
average. Almost all of them boil down to one pass over the array plus a
dictionary/set that answers "have I seen this before, and what did I know
about it?"

Use this pattern when the problem is about:
- Detecting **duplicates** or checking membership
- Finding **pairs/complements** that satisfy a condition (`a + b == target`)
- **Counting frequency** of elements (mode, top-K, anagrams)
- **Grouping** elements by some derived key (anagrams, same remainder, etc.)
- Needing `O(1)` lookup instead of nested loops / repeated `in` checks on a list

## The general shape

Almost every problem here is a variation of this skeleton:

```python
def solve(nums):
    seen = {}  # or set() if you only need membership, not a value

    for i, num in enumerate(nums):
        # 1. CHECK — before touching `seen`, ask "does my partner/duplicate
        #    already exist?" Do this BEFORE the store step.
        if condition_on(num, seen):
            return answer

        # 2. STORE — record what's needed for future iterations
        #    (the value itself, its index, or a running count)
        seen[num] = i  # or seen.add(num), or seen[num] = seen.get(num, 0) + 1

    return default_answer
```

Two steps, always in this order:

1. **CHECK first** — look up the current element's *partner* (complement,
   duplicate, anagram key) in `seen` before you store anything from this
   iteration. Checking after storing lets an element pair with itself
   (e.g. `nums[i]` satisfying `target - nums[i] == nums[i]` using its own
   index).
2. **STORE second** — only after the check passes (or fails), record the
   current element so later iterations can find it.

## Common sub-patterns

**Hash Set — membership / duplicates**
```python
seen = set()
for n in nums:
    if n in seen:
        return True
    seen.add(n)
return False
```

**Hash Map — complement lookup** (two-sum style)
```python
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
```

**Hash Map — frequency counter**
```python
from collections import Counter
counts = Counter(nums)  # or build manually with counts[n] = counts.get(n, 0) + 1
```

**Hash Map — grouping by derived key** (group anagrams style)
```python
groups = {}
for s in strs:
    key = "".join(sorted(s))  # or tuple(char counts), any canonical form
    groups.setdefault(key, []).append(s)
```

## Complexity

- **Time:** `O(n)` for a single pass with `O(1)` average hash lookups/inserts
  (sorting-based keys, e.g. group-anagrams, add an `O(n log n)` factor per
  element for the sort).
- **Space:** `O(n)` worst case — every element gets stored in the hash
  set/map before a match is found (or no match exists).

## Common pitfalls

- **Checking after storing** — lets an element incorrectly pair with itself.
  Always check before you store (see two-sum's complement check).
- **Using a list instead of a set/dict for membership tests** — `x in list`
  is `O(n)`, silently turning your `O(n)` algorithm back into `O(n^2)`.
- **Picking an unhashable/unstable grouping key** — e.g. an unsorted string
  or a plain `list` (not hashable) as a dict key.
- **Off-by-one on "at least twice" vs "more than twice"** — be precise about
  whether the count threshold is `>= 2` or `> 2`.

## Problems in this folder

### Easy

- [contains-duplicate](./easy/contains-duplicate) — hash set membership
  check, the simplest form of "have I seen this before?"
- [valid-anagram](./easy/valid-anagram) — frequency counter over one string,
  decremented by the other; any nonzero count means it's not an anagram.
- [two-sum](./easy/two-sum) — hash map complement lookup, the canonical
  check-then-store problem.
- [best-time-to-buy-and-sell-stock](./easy/best-time-to-buy-and-sell-stock) —
  not hashing, but the same single-pass "running state" shape: track the
  minimum price seen so far and the best profit against it.
- [intersection-of-two-arrays](./easy/intersection-of-two-arrays) — hash set
  membership check between two arrays; distinct values only.
- [intersection-of-two-arrays-2](./easy/intersection-of-two-arrays-2) —
  frequency counter instead of a set, so each shared value appears as many
  times as it's shared.
- [happy-number](./easy/happy-number) — hash set to detect a cycle in the
  digit-square-sum sequence instead of a fixed iteration cap.
- [isomorphic-strings](./easy/isomorphic-strings) — two hash maps (one per
  direction) to enforce a strict one-to-one character mapping.
- [word-pattern](./easy/word-pattern) — same one-to-one mapping idea as
  isomorphic-strings, but mapping pattern characters to whole words.
- [find-the-difference](./easy/find-the-difference) — frequency counter over
  the shorter string, decremented by the longer; the leftover char is the
  extra letter.
- [majority-element](./easy/majority-element) — frequency counter (`O(n)`
  space) vs. Boyer-Moore voting (`O(1)` space): a majority element cancels
  out every other value pairwise, so the surviving candidate must be it.

### Medium

- [group-anagrams](./medium/group-anagrams) — grouping by a derived key
  (sorted string) instead of a single check/store.
- [top-k-frequent-elements](./medium/top-k-frequent-elements) — frequency
  counter feeding a bucket sort (index = count) to avoid an `O(n log n)`
  sort.
- [product-of-array-except-self](./medium/product-of-array-except-self) —
  prefix/suffix running products instead of hashing; two passes, `O(1)`
  extra space (excluding the output array).
- [valid-sudoku](./medium/valid-sudoku) — one hash set per row, column, and
  3x3 box; check-then-store against all three before moving to the next
  cell.
- [longest-consecutive-sequence](./medium/longest-consecutive-sequence) —
  hash set membership to detect sequence starts (`n-1` not present) in
  `O(n)`, then walk each streak forward.
