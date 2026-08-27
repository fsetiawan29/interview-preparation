package solution

func isPerfectSquare(num int) bool {
	left := 1
	right := num

	for left <= right {
		mid := left + (right-left)/2

		quotient := num / mid

		if num%mid == 0 && mid == quotient {
			return true
		}

		if mid < quotient {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return false
}

func isPerfectSquareBruteForce(num int) bool {
	for i := 1; i*i <= num; i++ {
		if i*i == num {
			return true
		}
	}

	return false
}
