package solution

// guess is normally supplied by the LeetCode judge, pre-wired to a hidden
// picked number for each test case:
//   - returns -1 if num is higher than the picked number
//   - returns  1 if num is lower than the picked number
//   - returns  0 if num is equal to the picked number
//
// Locally, nothing provides it, so it's declared as a package-level variable
// here and stubbed out per test case in solution_test.go.
var guess func(num int) int

func guessNumber(n int) int {
	left := 1
	right := n

	for left <= right {
		mid := left + (right-left)/2
		result := guess(mid)
		switch result {
		case 0:
			return mid
		case 1:
			left = mid + 1
		default:
			right = mid - 1
		}
	}

	return -1
}

func guessNumberBruteForce(n int) int {
	for i := 1; i <= n; i++ {
		result := guess(i)
		if result == 0 {
			return i
		}
	}
	return -1
}
