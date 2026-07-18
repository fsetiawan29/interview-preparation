from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        group = {}
        for str in strs:
            key = "".join(sorted(str))
            if key not in group:
                group[key] = []
            group[key].append(str)

        result = []
        for v in group.values():
            result.append(v)
        
        return result


def run_test(name, strs, expected):
    result = Solution().groupAnagrams(strs)
    passed = (
        sorted(sorted(group) for group in result) == sorted(sorted(group) for group in expected)
        if result
        else False
    )
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    strs={strs}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        ["eat", "tea", "tan", "ate", "nat", "bat"],
        [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
    )

    run_test(
        "Example 2",
        [""],
        [[""]],
    )

    run_test(
        "Example 3",
        ["a"],
        [["a"]],
    )
