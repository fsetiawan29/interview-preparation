# Problem

Name: Best Time to Buy and Sell Stock

Difficulty: Easy

----------------------------------------

# Pattern

Array + Dynamic Programming

----------------------------------------

# Recognition

Idea

- The cheapest stock price i've ever seen and find the max by calculating with the price today
- Track the minimum price seen so far as we scan left to right; selling today only ever makes sense against that running minimum

Steps

- INIT: `min_price` starts at `prices[0]`, `max_profit` starts at 0
- SCAN: for each `price` in `prices`, update `min_price = min(min_price, price)`
- PROFIT: update `max_profit = max(max_profit, price - min_price)` (profit from selling today at the cheapest buy seen so far)
- RETURN: `max_profit`

----------------------------------------

# Complexity

- Time: `O(n)` — single pass over `prices`
- Space: `O(1)` — only two running variables are kept

