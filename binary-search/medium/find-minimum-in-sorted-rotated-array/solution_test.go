package solution

import "testing"

func Test_findMin(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums []int
		want int
	}{
		{
			name: "rotated in the middle",
			nums: []int{3, 4, 5, 1, 2},
			want: 1,
		},
		{
			name: "rotated once",
			nums: []int{2, 1},
			want: 1,
		},
		{
			name: "no rotation, ascending",
			nums: []int{1, 2, 3, 4, 5},
			want: 1,
		},
		{
			name: "rotated near the end",
			nums: []int{4, 5, 6, 7, 0, 1, 2},
			want: 0,
		},
		{
			name: "single element",
			nums: []int{1},
			want: 1,
		},
		{
			name: "two elements, no rotation",
			nums: []int{1, 2},
			want: 1,
		},
		{
			name: "min is first element after full rotation",
			nums: []int{11, 13, 15, 17},
			want: 11,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := findMin(tt.nums)
			if got != tt.want {
				t.Errorf("findMin() = %v, want %v", got, tt.want)
			}
		})
	}
}
