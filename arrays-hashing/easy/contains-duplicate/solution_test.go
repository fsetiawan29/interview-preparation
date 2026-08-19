package solution

import "testing"

func Test_containsDuplicate(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums []int
		want bool
	}{
		{
			name: "contain",
			nums: []int{1, 2, 3, 1},
			want: true,
		},
		{
			name: "not contains",
			nums: []int{1, 2, 3},
			want: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := containsDuplicate(tt.nums)
			if got != tt.want {
				t.Errorf("containsDuplicate() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_containsDuplicateBruteForce(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		nums []int
		want bool
	}{
		{
			name: "contain",
			nums: []int{1, 2, 3, 1},
			want: true,
		},
		{
			name: "not contains",
			nums: []int{1, 2, 3},
			want: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := containsDuplicateBruteForce(tt.nums)
			if got != tt.want {
				t.Errorf("containsDuplicateBruteForce() = %v, want %v", got, tt.want)
			}
		})
	}
}
