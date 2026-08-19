package solution

import "sort"

func threeSum(nums []int) [][]int {
	var res [][]int

	sort.Ints(nums)

	for i := 0; i < len(nums); i++ {
		left := i + 1
		right := len(nums) - 1

		if i > 0 && nums[i] == nums[i-1] {
			continue
		}

		for left < right {
			sum := nums[i] + nums[left] + nums[right]
			if sum == 0 {
				res = append(res, []int{nums[i], nums[left], nums[right]})

				left++
				right--

				for left < right && nums[left] == nums[left-1] {
					left++
				}

				for left < right && nums[right] == nums[right+1] {
					right--
				}
			} else if sum < 0 {
				left++
			} else {
				right--
			}
		}
	}

	return res
}

type Triplet struct {
	a int
	b int
	c int
}

func threeSumBruteForce(nums []int) [][]int {
	var res [][]int
	seen := make(map[Triplet]bool)
	for i := 0; i < len(nums); i++ {
		for j := i + 1; j < len(nums); j++ {
			for k := j + 1; k < len(nums); k++ {
				if nums[i]+nums[j]+nums[k] == 0 {
					triplet := []int{nums[i], nums[j], nums[k]}
					sort.Ints(triplet)
					key := Triplet{
						a: triplet[0],
						b: triplet[1],
						c: triplet[2],
					}

					if _, exist := seen[key]; !exist {
						seen[key] = true
						res = append(res, triplet)
					}
				}
			}
		}
	}

	return res
}

func threeSumHashMap(nums []int) [][]int {
	var res [][]int
	seenRes := make(map[Triplet]struct{})
	for i := 0; i < len(nums); i++ {
		seen := make(map[int]struct{})
		for j := i + 1; j < len(nums); j++ {
			complement := -nums[i] - nums[j]

			if _, exists := seen[complement]; exists {
				triplet := []int{nums[i], nums[j], complement}
				sort.Ints(triplet)

				key := Triplet{
					a: triplet[0],
					b: triplet[1],
					c: triplet[2],
				}

				if _, exist := seenRes[key]; !exist {
					seenRes[key] = struct{}{}
					res = append(res, triplet)
				}
			}

			seen[nums[j]] = struct{}{}
		}
	}

	return res
}
