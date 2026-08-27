package solution

func arrangeCoins(n int) int {
	left := 1
	right := n
	res := 0

	for left <= right {
		mid := left + (right-left)/2

		var valid bool
		if mid%2 == 0 {
			valid = mid/2 <= n/(mid+1)
		} else {
			valid = (mid+1)/2 <= n/mid
		}

		if valid {
			res = mid
			left = mid + 1

		} else {
			right = mid - 1
		}
	}

	return res
}

func arrangeCoinsBruteForce(n int) int {
	remaining := n
	res := 0

	for row := 1; remaining >= row; row++ {
		remaining -= row
		res = row
	}

	return res
}
