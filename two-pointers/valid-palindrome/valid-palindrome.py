class Solution:
    def isPalindromeReformat(self, s: str) -> bool:
        left = 0
        s_reformat = self.reformatStr(s)
        right = len(s_reformat) - 1

        while left < right:
            if s_reformat[left] != s_reformat[right]:
                return False
            left += 1
            right -= 1

        return True

    def reformatStr(self, s: str) -> str:
        res = []

        for char in s:
            if char.isalnum():
                res.append(char.lower())

        return "".join(res)

    def isPalindromeNoReformat(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            cl = s[left]
            cr = s[right]
            if not cl.isalnum():
                left += 1
                continue

            if not cr.isalnum():
                right -= 1
                continue

            if cl.lower() != cr.lower():
                return False

            left += 1
            right -= 1

        return True


def run_test(name, s, expected):
    for method in ("isPalindromeReformat", "isPalindromeNoReformat"):
        result = getattr(Solution(), method)(s)
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} ({method})")
        print(f"  input:    s={s!r}")
        print(f"  expected: {expected}")
        print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "A man, a plan, a canal: Panama",
        True,
    )

    run_test(
        "Example 2",
        "race a car",
        False,
    )

    run_test(
        "Example 3",
        " ",
        True,
    )
