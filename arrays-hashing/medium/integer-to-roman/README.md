# Problem: Integer to Roman

## 1. Problem Understanding

### Problem Summary

Convert an integer to a Roman numeral, following the standard subtractive notation rules (e.g. `4` is `IV` not `IIII`, `9` is `IX`, `40` is `XL`, `900` is `CM`).

### Input

- An integer `num`

### Output

- A string representing `num` as a Roman numeral.

### Constraints

- `1 <= num <= 3999`

### Example

Input:

```text
num = 1994
```

Output:

```text
"MCMXCIV"
```

Manual walkthrough:

```text
1994

Take as many 1000's (M) as possible: 1994 -> 994, append "M"
Take as many 900's (CM) as possible: 994 -> 94, append "CM"
Take as many 90's (XC) as possible:   94 -> 4,  append "XC"
Take as many 4's (IV) as possible:     4 -> 0,  append "IV"

Result: "M" + "CM" + "XC" + "IV" = "MCMXCIV"
```

---

# 2. Key Insight

## What makes this problem difficult?

Roman numerals mix additive symbols (`M`, `C`, `X`, `I`, ...) with subtractive pairs (`CM`, `XC`, `IV`, ...). A naive digit-by-digit conversion has to special-case every subtractive form (4, 9, 40, 90, 400, 900), which is easy to get wrong or leave incomplete.

## Key Observation

If the subtractive forms (`900/CM`, `400/CD`, `90/XC`, `40/XL`, `9/IX`, `4/IV`) are simply added as their **own entries** in a value-to-symbol table — sorted alongside the regular values in strictly descending order — then a single greedy rule works uniformly for every case: *always take as much of the largest available value as still fits*.

Example:

```text
num = 58

Largest value <= 58 in the table is 50/L -> take it, num = 8
Largest value <= 8 is 5/V               -> take it, num = 3
Largest value <= 3 is 1/I (x3)          -> take it three times, num = 0

Result: "L" + "V" + "III" = "LVIII"
```

## Why does this observation help?

By baking the subtractive pairs directly into the descending value list, there's no special-casing left to do at all — the same `while num >= value: append symbol; num -= value` loop, run once per table entry, handles both additive and subtractive symbols identically.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a cashier making change with a fixed set of coin denominations — except the "coins" are `1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1` (with `M, CM, D, CD, C, XC, L, XL, X, IX, V, IV, I` as their labels). The cashier always hands out as many of the *largest* coin that still fits before moving to the next-smaller denomination.

```text
num = 1994

coin 1000 (M):  fits once  -> hand out "M",  remaining 994
coin 900 (CM):  fits once  -> hand out "CM", remaining 94
coin 500 (D):   doesn't fit
coin 400 (CD):  doesn't fit
coin 100 (C):   doesn't fit
coin 90  (XC):  fits once  -> hand out "XC", remaining 4
coin 50..10..9..5: don't fit
coin 4   (IV):  fits once  -> hand out "IV", remaining 0

Change fully made: "M" + "CM" + "XC" + "IV" = "MCMXCIV"
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize values = [(1000,M),(900,CM),(500,D),(400,CD),
                      (100,C),(90,XC),(50,L),(40,XL),
                      (10,X),(9,IX),(5,V),(4,IV),(1,I)]
   │
   ▼
For each (value, symbol) in values:
   │
   ▼
Is num >= value ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Append symbol      Move to next (value, symbol)
num -= value            │
 │                       │
 └──▶ (repeat "Is num >= value ?" for same entry)
                         │
                         ▼
        All 13 entries processed — num is now 0
                         │
                         ▼
                 Join res and return
```

Explanation of each decision:

- Each `(value, symbol)` pair is tried in strictly descending order, so larger denominations are always preferred first — this is what guarantees the minimal/canonical Roman numeral form.
- The inner `while num >= value` lets the same symbol be appended multiple times in a row (e.g. `III` for 3, `MMM` for 3000) before moving to the next entry.
- Because the subtractive pairs (`CM`, `XC`, `IV`, ...) are entries in the same list, no special-casing is needed — they're picked up by the exact same rule.
- The loop is guaranteed to reduce `num` to exactly `0` by the time the last entry (`1/I`) is processed, since `1` divides any remaining amount.

---

# 5. Plain English Algorithm

1. Define a list of `(value, symbol)` pairs in strictly descending order, including the six subtractive pairs (`900/CM`, `400/CD`, `90/XC`, `40/XL`, `9/IX`, `4/IV`) alongside the standard ones.
2. For each pair in that list:
   - While `num` is at least `value`, append `symbol` to the result and subtract `value` from `num`.
3. Once every pair has been processed, `num` is `0`. Join the result list into a string and return it.

---

# 6. Pseudocode

```text
values = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
]

res = []

for (value, symbol) in values
    while num >= value
        append symbol to res
        num -= value

return join(res)
```

---

# 7. Python Solution

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        values = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I")
        ]

        res = []
        for (value, symbol) in values:
            while num >= value:
                res.append(symbol)
                num -= value

        return "".join(res)
```

---

# 8. Dry Run

Example:

```text
num = 1994
```

| Step | (value, symbol) | num >= value? | Action | num after | res after |
|------|------------------|----------------|--------|-----------|-----------|
| 1 | (1000, "M") | 1994 >= 1000 → yes | Append "M", subtract | 994 | ["M"] |
| 2 | (1000, "M") | 994 >= 1000 → no | Move to next pair | 994 | ["M"] |
| 3 | (900, "CM") | 994 >= 900 → yes | Append "CM", subtract | 94 | ["M","CM"] |
| 4 | (900, "CM") | 94 >= 900 → no | Move to next pair | 94 | ["M","CM"] |
| 5 | (500..100) | all no (94 < 100) | Skip four pairs | 94 | ["M","CM"] |
| 6 | (90, "XC") | 94 >= 90 → yes | Append "XC", subtract | 4 | ["M","CM","XC"] |
| 7 | (90, "XC") | 4 >= 90 → no | Move to next pair | 4 | ["M","CM","XC"] |
| 8 | (50..5) | all no (4 < 5) | Skip four pairs | 4 | ["M","CM","XC"] |
| 9 | (4, "IV") | 4 >= 4 → yes | Append "IV", subtract | 0 | ["M","CM","XC","IV"] |
| 10 | (4, "IV") | 0 >= 4 → no | Move to next pair | 0 | ["M","CM","XC","IV"] |
| 11 | (1, "I") | 0 >= 1 → no | Loop ends | 0 | ["M","CM","XC","IV"] |

Result: `"".join(["M","CM","XC","IV"])` = `"MCMXCIV"`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(1)
```

Why?

- The `values` list has a fixed size of 13 entries, regardless of `num`.
- Since `num <= 3999`, each symbol is appended at most 3 times (e.g. `MMM`, `III`), so the total number of loop iterations is bounded by a constant.

### Space Complexity

```text
O(1)
```

Why?

- `values` is a fixed-size list of 13 tuples.
- `res` holds at most a constant number of symbols (at most 15 characters for `num < 4000`), independent of the input value.
