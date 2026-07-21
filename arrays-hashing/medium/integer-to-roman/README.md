# Problem

Name: Integer to Roman

Difficulty: Medium

----------------------------------------

# Pattern
Array Tuple Mapping Value and Symbol + Greedy Algorithm



----------------------------------------

# Recognition

# Idea

- Define a hash map that maps each Roman numeral symbol to its corresponding value.
- Use a greedy approach by always selecting the largest possible value that does not exceed the remaining number.
- Append the corresponding symbol to the result and subtract its value from the remaining number.
- Repeat until the number becomes `0`, then return the result.

# Steps

- INIT: `values`, a list of `(value, symbol)` tuples in descending order, including subtractive forms (`1000/M`, `900/CM`, `500/D`, `400/CD`, `100/C`, `90/XC`, `50/L`, `40/XL`, `10/X`, `9/IX`, `5/V`, `4/IV`, `1/I`)
- SCAN: for each `value, symbol` in `values`
- APPEND: while `num >= value`, append `symbol` to `res` and subtract `value` from `num`
- RETURN: `"".join(res)`

# Mistakes

- My initial instinct was to repeatedly search for the largest value less than or equal to the remaining number:

  ```python
  while num > 0:
      find the largest value <= num
      append symbol
      num -= value
  ```

- The correct greedy approach is to iterate through the predefined values in descending order:

  ```python
  for value, symbol in values:
      while num >= value:
          res += symbol
          num -= value
  ```

- This avoids repeatedly searching for the next largest value and keeps the implementation simpler and more efficient.



----------------------------------------

# Complexity

- Time: `O(1)` — the `values` list has a fixed size of 13 entries, and each symbol repeats at most 3 times, so the total work is bounded regardless of `num`
- Space: `O(1)` — fixed-size `values` list and `res` bounded by a constant number of symbols (at most 15 for `num < 4000`)
