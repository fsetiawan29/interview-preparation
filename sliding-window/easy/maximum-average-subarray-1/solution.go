package main

import "fmt"

func main() {
	fmt.Println(maxAvgSubArray([]int{1, 2, 3, 4, 5}, 3))
	fmt.Println(maxAvgSubArraySlidingWindow([]int{1, 2, 3, 4, 5}, 3))
}

func maxAvgSubArray(nums []int, k int) float64 {
	maxTotal := 0
	for i := 0; i < k; i++ {
		maxTotal += nums[i]
	}

	for i := 1; i <= len(nums)-k; i++ {
		subTotal := 0
		for start := i; start < i+k; start++ {
			subTotal += nums[start]
		}

		if subTotal > maxTotal {
			maxTotal = subTotal
		}
	}

	return float64(maxTotal) / float64(k)
}

func maxAvgSubArraySlidingWindow(nums []int, k int) float64 {
	windowSum := 0
	for i := 0; i < k; i++ {
		windowSum += nums[i]
	}

	maxWindow := windowSum
	left := 0
	for right := k; right < len(nums); right++ {
		windowSum -= nums[left]
		windowSum += nums[right]

		if windowSum > maxWindow {
			maxWindow = windowSum
		}

		left++
	}

	return float64(maxWindow) / float64(k)
}
