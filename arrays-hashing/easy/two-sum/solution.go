package solution

func twoSumBruteForce(nums []int, target int) []int {
	for i := 0; i < len(nums); i++ {
		for j := i + 1; j < len(nums); j++ {
			if nums[i]+nums[j] == target {
				return []int{i, j}
			}
		}
	}

	return []int{}
}

func twoSum(nums []int, target int) []int {
	pairs := make(map[int]int)

	for i := 0; i < len(nums); i++ {
		complement := target - nums[i]

		idx, exists := pairs[complement]
		if exists {
			return []int{idx, i}
		}

		pairs[nums[i]] = i
	}

	return []int{}
}
