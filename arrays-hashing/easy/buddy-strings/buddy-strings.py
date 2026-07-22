class Solution:
    def buddyStrings_hashset(self, s: str, goal: str) -> bool:
        if len(s) != len(goal):
            return False
        
        if s == goal:
            # check for duplicate letters
            seen = set()
            for char in s:
                if char in seen:
                    return True
                
                seen.add(char)
            
            return False

        count = 0
        first = -1
        second = -1
        for i in range(len(s)):
            if s[i] != goal[i]:
                count +=1

                if count == 1:
                    first = i
                else:
                    second = i

        if count != 2:
            return False

        return s[first] == goal[second] and s[second] == goal[first]

    def buddyStrings_diffcount(self, s: str, goal: str) -> bool:
        if len(s) != len(goal):
            return False
        
        if s == goal:
            # check for duplicate letters
            seen = set()
            for char in s:
                if char in seen:
                    return True
                
                seen.add(char)
            
            return False

        diff = []
        for i in range(len(s)):
            if s[i] != goal[i]:

                diff.append((s[i], goal[i]))

                if len(diff) > 2:
                    return False

        if len(diff) != 2:
            return False

        return diff[0][0] == diff[1][1] and diff[0][1] == diff[1][0]


def run_test(name, s, goal, expected):
    for method in ("buddyStrings_hashset", "buddyStrings_diffcount"):
        result = getattr(Solution(), method)(s, goal)
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} ({method})")
        print(f"  input:    s={s!r}, goal={goal!r}")
        print(f"  expected: {expected}")
        print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "ab",
        "ba",
        True,
    )

    run_test(
        "Example 2",
        "ab",
        "ab",
        False,
    )

    run_test(
        "Example 3",
        "aa",
        "aa",
        True,
    )
