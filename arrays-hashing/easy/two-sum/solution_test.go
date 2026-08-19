package solution

import (
	"slices"
	"testing"
)

func Test_twoSumBruteForce(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums   []int
		target int
		want   []int
	}{
		{
			name:   "valid",
			nums:   []int{1, 2, 3, 6},
			target: 5,
			want:   []int{1, 2},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := twoSumBruteForce(tt.nums, tt.target)
			if !slices.Equal(got, tt.want) {
				t.Errorf("twoSumBruteForce() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_twoSum(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums   []int
		target int
		want   []int
	}{
		{
			name:   "valid",
			nums:   []int{1, 2, 3, 6},
			target: 5,
			want:   []int{1, 2},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := twoSum(tt.nums, tt.target)
			if !slices.Equal(got, tt.want) {
				t.Errorf("twoSum() = %v, want %v", got, tt.want)
			}
		})
	}
}
