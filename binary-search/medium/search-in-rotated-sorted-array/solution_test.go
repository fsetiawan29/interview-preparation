package solution

import "testing"

func Test_search(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums   []int
		target int
		want   int
	}{
		{
			name:   "target in right (unsorted) half",
			nums:   []int{4, 5, 6, 7, 0, 1, 2},
			target: 0,
			want:   4,
		},
		{
			name:   "target in left (sorted) half",
			nums:   []int{4, 5, 6, 7, 0, 1, 2},
			target: 5,
			want:   1,
		},
		{
			name:   "target not present",
			nums:   []int{4, 5, 6, 7, 0, 1, 2},
			target: 3,
			want:   -1,
		},
		{
			name:   "target at the pivot",
			nums:   []int{6, 7, 0, 1, 2, 4, 5},
			target: 0,
			want:   2,
		},
		{
			name:   "not rotated",
			nums:   []int{1, 2, 3, 4, 5},
			target: 4,
			want:   3,
		},
		{
			name:   "single element found",
			nums:   []int{1},
			target: 1,
			want:   0,
		},
		{
			name:   "single element not found",
			nums:   []int{1},
			target: 0,
			want:   -1,
		},
		{
			name:   "two elements rotated",
			nums:   []int{3, 1},
			target: 1,
			want:   1,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := search(tt.nums, tt.target)
			if got != tt.want {
				t.Errorf("search() = %v, want %v", got, tt.want)
			}
		})
	}
}
