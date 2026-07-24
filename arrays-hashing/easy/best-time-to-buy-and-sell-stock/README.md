# Problem: Best Time to Buy and Sell Stock

## 1. Problem Understanding

### Problem Summary

Given an array `prices` where `prices[i]` is the price of a stock on day `i`, find the maximum profit achievable by buying on one day and selling on a later day. If no profit is possible, return `0`.

### Input

- An integer array `prices`

### Output

- An integer: the maximum achievable profit, or `0` if no profitable transaction exists.

### Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

### Example

Input:

```text
prices = [7,1,5,3,6,4]
```

Output:

```text
5
```

Manual walkthrough:

```text
Buy on day 1 (price = 1)
Sell on day 4 (price = 6)

Profit = 6 - 1 = 5

Buying on day 0 (price = 7) and selling later never beats this,
since every later price is lower than 7 except the ones already considered.
```

---

## 2. Brute Force Approach

### Idea

For every possible buy day `i`, check every later sell day `j` and compute the profit `prices[j] - prices[i]`, keeping the best one seen.

### Pseudocode

```text
n = length(prices)
max_profit = 0

for i = 0 to n - 1
    for j = i + 1 to n - 1
        profit = prices[j] - prices[i]
        max_profit = max(max_profit, profit)

return max_profit
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- There are `O(n^2)` pairs `(i, j)` with `i < j`, and each is checked with `O(1)` work.

#### Space Complexity

```text
O(1)
```

Why?

- Only `max_profit` and the two loop indices are used.

### Why this isn't good enough

Every buy day `i` is compared against every later sell day individually, even though only the *cheapest* buy day seen so far ever matters for a given sell day. Tracking a running minimum instead of re-checking every earlier day is what removes that repeated work.

---

## 3. Key Insight

### What makes this problem difficult?

A brute-force approach checks every pair of buy/sell days, which is `O(n^2)`. It's tempting to think you need to compare every day against every other day, but selling only ever needs to be compared against the *cheapest* day seen so far — not every earlier day individually.

### Key Observation

While scanning left to right, only one number matters from the past: the **minimum price seen so far**. Any profit worth considering today is `price - min_price_so_far`.

Example:

```text
prices = [7,1,5,3,6,4]

At day 4 (price=6): the cheapest price seen so far is 1 (day 1)
Profit if selling today = 6 - 1 = 5
```

### Why does this observation help?

Instead of comparing today's price against every previous day, we only need to track a single running minimum. This turns an `O(n^2)` comparison problem into a single `O(n)` left-to-right pass.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture walking along the price line left to right, carrying a sticky note with "cheapest price seen so far." At every new day, you first update the sticky note if today is cheaper, then check: "if I sold today against my cheapest note, what would I make?" Keep the best answer seen.

```text
prices:  7   1   5   3   6   4
          ↑
       day 0, min=7, profit=0

prices:  7   1   5   3   6   4
              ↑
           day 1, min=1, profit=max(0, 1-1)=0

prices:  7   1   5   3   6   4
                  ↑
               day 2, min=1, profit=max(0, 5-1)=4

prices:  7   1   5   3   6   4
                          ↑
                    day 4, min=1, profit=max(4, 6-1)=5
```

The sticky note (`min_price`) never goes up, only down or stays the same — it always reflects the best possible buy day discovered so far.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize min_price = prices[0], max_profit = 0
   │
   ▼
For each price in prices:
   │
   ▼
Is price < min_price ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
min_price = price   min_price unchanged
   │                    │
   └────────┬───────────┘
            ▼
   Is (price - min_price) > max_profit ?
            │
          ┌─┴─────────────┐
          │                │
         Yes               No
          │                │
          ▼                ▼
   max_profit = price - min_price   max_profit unchanged
          │                │
          └────────┬────────┘
                   ▼
           Next price (or Done)
                   │
                   ▼
             Return max_profit
```

Explanation of each decision:

- `min_price` is updated on every day, regardless of whether it improves `max_profit` — it always represents the cheapest buy opportunity so far.
- `max_profit` is only updated when selling today (against the running minimum) beats the best profit found so far.
- Because `min_price` can never represent a day *after* the current one, every candidate profit computed is a valid buy-before-sell pair.

---

## 6. Plain English Algorithm

1. Initialize `min_price` to `prices[0]` and `max_profit` to `0`.
2. Scan the array left to right. For each `price`:
   - Update `min_price` to be the smaller of `min_price` and `price`.
   - Compute the profit from selling today: `price - min_price`.
   - Update `max_profit` if this profit is larger than what's been seen so far.
3. After the scan, return `max_profit`.

---

## 7. Pseudocode

```text
min_price = prices[0]
max_profit = 0

for price in prices
    min_price = min(min_price, price)
    max_profit = max(max_profit, price - min_price)

return max_profit
```

---

## 8. Python Solution

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        min_price = prices[0]
        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)
        return max_profit
```

---

## 9. Dry Run

Example:

```text
prices = [7,1,5,3,6,4]
```

| Step | price | min_price | price - min_price | max_profit | Why? |
|------|-------|-----------|--------------------|------------|------|
| 1 | 7 | 7 | 0 | 0 | First day, nothing to compare against |
| 2 | 1 | 1 | 0 | 0 | New minimum, but 1-1=0 doesn't beat 0 |
| 3 | 5 | 1 | 4 | 4 | Selling at 5 after buying at 1 gives profit 4 |
| 4 | 3 | 1 | 2 | 4 | 3-1=2 doesn't beat 4 |
| 5 | 6 | 1 | 5 | 5 | Selling at 6 after buying at 1 gives profit 5 |
| 6 | 4 | 1 | 3 | 5 | 4-1=3 doesn't beat 5 |

Result: `5`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- A single left-to-right pass over `prices`, doing constant work per element.

### Space Complexity

```text
O(1)
```

Why?

- Only two running variables, `min_price` and `max_profit`, are used regardless of input size.
