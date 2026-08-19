package solution

func containsDuplicate(nums []int) bool {
	seen := make(map[int]struct{})

	for _, num := range nums {
		_, exists := seen[num]
		if exists {
			return true
		}

		seen[num] = struct{}{}
	}

	return false
}

func containsDuplicateBruteForce(nums []int) bool {
	for i := 0; i < len(nums); i++ {
		for j := i + 1; j < len(nums); j++ {
			if nums[i] == nums[j] {
				return true
			}
		}
	}

	return false
}
