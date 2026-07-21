class Solution:
    def isHappy(self, n: int) -> bool:
        # TODO: implement
        seen = set()
        while n != 1:
            if n in seen:
                return False
            
            seen.add(n)
            n = self.next_number(n)
        
        return True
    
    def next_number(self, n:int) -> int:
        res = 0
        while n > 0:
            digit = n % 10
            res += (digit * digit)
            n //= 10
        return res


def run_test(name, n, expected):
    result = Solution().isHappy(n)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    n={n}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        19,
        True,
    )

    run_test(
        "Example 2",
        2,
        False,
    )
