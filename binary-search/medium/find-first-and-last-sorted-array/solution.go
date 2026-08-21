package solution

func searchRange(nums []int, target int) []int {
	left := findLeft(nums, target)
	right := findRight(nums, target)

	return []int{left, right}
}

func findLeft(nums []int, target int) int {
	left := 0
	right := len(nums) - 1
	res := -1

	for left <= right {
		mid := left + (right-left)/2

		if nums[mid] < target {
			left = mid + 1
		} else if nums[mid] > target {
			right = mid - 1
		} else {
			res = mid
			right = mid - 1
		}
	}

	return res
}

func findRight(nums []int, target int) int {
	left := 0
	right := len(nums) - 1
	res := -1

	for left <= right {
		mid := left + (right-left)/2

		if nums[mid] < target {
			left = mid + 1
		} else if nums[mid] > target {
			right = mid - 1
		} else {
			res = mid
			left = mid + 1
		}
	}

	return res
}
