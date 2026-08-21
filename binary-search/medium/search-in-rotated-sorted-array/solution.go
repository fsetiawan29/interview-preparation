package solution

func search(nums []int, target int) int {
	left := 0
	right := len(nums) - 1

	for left <= right {
		mid := left + (right-left)/2

		if nums[left] <= nums[mid] {
			// sorted here
			if nums[left] <= target && nums[mid] >= target {
				if nums[mid] == target {
					return mid
				}

				if nums[mid] < target {
					left = mid + 1
				} else {
					right = mid - 1
				}
			} else {
				left = mid + 1
			}
		} else {
			// sorted here
			if nums[mid] <= target && nums[right] >= target {
				if nums[mid] == target {
					return mid
				}

				if nums[mid] < target {
					left = mid + 1
				} else {
					right = mid - 1
				}
			} else {
				right = mid - 1
			}
		}
	}

	return -1
}
