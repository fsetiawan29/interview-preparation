package solution

import (
	"reflect"
	"sort"
	"testing"
)

// normalizeTriplets sorts each triplet and then sorts the outer slice so
// two results containing the same triplets in different orders compare equal.
func normalizeTriplets(triplets [][]int) [][]int {
	normalized := make([][]int, len(triplets))
	for i, t := range triplets {
		c := append([]int(nil), t...)
		sort.Ints(c)
		normalized[i] = c
	}
	sort.Slice(normalized, func(i, j int) bool {
		a, b := normalized[i], normalized[j]
		for k := 0; k < len(a) && k < len(b); k++ {
			if a[k] != b[k] {
				return a[k] < b[k]
			}
		}
		return len(a) < len(b)
	})
	return normalized
}

func Test_threeSum(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums []int
		want [][]int
	}{
		{
			name: "valid",
			nums: []int{-1, 0, 1, 2, -1, -4},
			want: [][]int{
				{-1, -1, 2},
				{-1, 0, 1},
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := threeSum(tt.nums)
			if !reflect.DeepEqual(normalizeTriplets(got), normalizeTriplets(tt.want)) {
				t.Errorf("threeSum() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_threeSumBruteForce(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums []int
		want [][]int
	}{
		{
			name: "valid",
			nums: []int{-1, 0, 1, 2, -1, -4},
			want: [][]int{
				{-1, -1, 2},
				{-1, 0, 1},
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := threeSumBruteForce(tt.nums)
			if !reflect.DeepEqual(normalizeTriplets(got), normalizeTriplets(tt.want)) {
				t.Errorf("threeSumBruteForce() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_threeSumHashMap(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums []int
		want [][]int
	}{
		{
			name: "valid",
			nums: []int{-1, 0, 1, 2, -1, -4},
			want: [][]int{
				{-1, -1, 2},
				{-1, 0, 1},
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := threeSumHashMap(tt.nums)
			if !reflect.DeepEqual(normalizeTriplets(got), normalizeTriplets(tt.want)) {
				t.Errorf("threeSumHashMap() = %v, want %v", got, tt.want)
			}
		})
	}
}
