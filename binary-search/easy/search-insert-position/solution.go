package solution

// Find the first index where nums[i] >= target
func searchInsert(nums []int, target int) int {
	left := 0
	right := len(nums) - 1

	for left <= right {
		mid := left + (right-left)/2

		if nums[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return left
}

func searchInsertBruteForce(nums []int, target int) int {
	for i, num := range nums {
		if num >= target {
			return i
		}
	}

	return len(nums)
}
