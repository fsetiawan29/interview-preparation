package solution

func searchInsert(nums []int, target int) int {
	left := 0
	right := len(nums) - 1

	for left <= right {
		mid := left + (right-left)/2

		if target == nums[mid] {
			return mid
		} else if target < nums[mid] {
			right = mid - 1
		} else {
			left = mid + 1
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
