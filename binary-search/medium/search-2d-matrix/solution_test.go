package solution

import "testing"

func Test_searchMatrixBruteForce(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		matrix [][]int
		target int
		want   bool
	}{
		{
			name: "target present in middle row",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 3,
			want:   true,
		},
		{
			name: "target not present (falls in a gap)",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 13,
			want:   false,
		},
		{
			name: "target at top-left corner",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 1,
			want:   true,
		},
		{
			name: "target at bottom-right corner",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 60,
			want:   true,
		},
		{
			name: "target at end of a row (row boundary)",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 20,
			want:   true,
		},
		{
			name: "target at start of a row (row boundary)",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 23,
			want:   true,
		},
		{
			name: "target smaller than every value",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: -5,
			want:   false,
		},
		{
			name: "target larger than every value",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 100,
			want:   false,
		},
		{
			name:   "single row, target present",
			matrix: [][]int{{1, 3, 5, 7, 9}},
			target: 7,
			want:   true,
		},
		{
			name:   "single row, target absent",
			matrix: [][]int{{1, 3, 5, 7, 9}},
			target: 4,
			want:   false,
		},
		{
			name: "single column, target present",
			matrix: [][]int{
				{1},
				{3},
				{5},
				{7},
			},
			target: 5,
			want:   true,
		},
		{
			name: "single column, target absent",
			matrix: [][]int{
				{1},
				{3},
				{5},
				{7},
			},
			target: 6,
			want:   false,
		},
		{
			name:   "single element, found",
			matrix: [][]int{{5}},
			target: 5,
			want:   true,
		},
		{
			name:   "single element, not found",
			matrix: [][]int{{5}},
			target: 1,
			want:   false,
		},
		{
			name:   "negative numbers",
			matrix: [][]int{{-10, -8, -6}, {-4, -2, 0}, {2, 4, 6}},
			target: -4,
			want:   true,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := searchMatrixBruteForce(tt.matrix, tt.target)
			if got != tt.want {
				t.Errorf("searchMatrixBruteForce() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_searchMatrix(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		matrix [][]int
		target int
		want   bool
	}{
		{
			name: "target present in middle row",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 3,
			want:   true,
		},
		{
			name: "target not present (falls in a gap)",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 13,
			want:   false,
		},
		{
			name: "target at top-left corner",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 1,
			want:   true,
		},
		{
			name: "target at bottom-right corner",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 60,
			want:   true,
		},
		{
			name: "target at end of a row (row boundary)",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 20,
			want:   true,
		},
		{
			name: "target at start of a row (row boundary)",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 23,
			want:   true,
		},
		{
			name: "target smaller than every value",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: -5,
			want:   false,
		},
		{
			name: "target larger than every value",
			matrix: [][]int{
				{1, 3, 5, 7},
				{10, 11, 16, 20},
				{23, 30, 34, 60},
			},
			target: 100,
			want:   false,
		},
		{
			name:   "single row, target present",
			matrix: [][]int{{1, 3, 5, 7, 9}},
			target: 7,
			want:   true,
		},
		{
			name:   "single row, target absent",
			matrix: [][]int{{1, 3, 5, 7, 9}},
			target: 4,
			want:   false,
		},
		{
			name: "single column, target present",
			matrix: [][]int{
				{1},
				{3},
				{5},
				{7},
			},
			target: 5,
			want:   true,
		},
		{
			name: "single column, target absent",
			matrix: [][]int{
				{1},
				{3},
				{5},
				{7},
			},
			target: 6,
			want:   false,
		},
		{
			name:   "single element, found",
			matrix: [][]int{{5}},
			target: 5,
			want:   true,
		},
		{
			name:   "single element, not found",
			matrix: [][]int{{5}},
			target: 1,
			want:   false,
		},
		{
			name:   "negative numbers",
			matrix: [][]int{{-10, -8, -6}, {-4, -2, 0}, {2, 4, 6}},
			target: -4,
			want:   true,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := searchMatrix(tt.matrix, tt.target)
			if got != tt.want {
				t.Errorf("searchMatrix() = %v, want %v", got, tt.want)
			}
		})
	}
}
