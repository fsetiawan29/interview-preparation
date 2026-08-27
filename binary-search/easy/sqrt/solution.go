package solution

func mySqrt(x int) int {
	left := 1
	right := x
	res := 0

	for left <= right {
		mid := left + (right-left)/2

		quotient := x / mid

		if mid > quotient {
			right = mid - 1
		} else {
			res = mid
			left = mid + 1
		}
	}

	return res
}
