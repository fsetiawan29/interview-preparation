package solution

import "testing"

func Test_isPerfectSquareBruteForce(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		num  int
		want bool
	}{
		{
			name: "smallest perfect square",
			num:  1,
			want: true,
		},
		{
			name: "perfect square",
			num:  16,
			want: true,
		},
		{
			name: "not a perfect square",
			num:  14,
			want: false,
		},
		{
			name: "perfect square, prime root",
			num:  9,
			want: true,
		},
		{
			name: "one below a perfect square",
			num:  15,
			want: false,
		},
		{
			name: "one above a perfect square",
			num:  17,
			want: false,
		},
		{
			name: "large perfect square",
			num:  808201, // 899 * 899
			want: true,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := isPerfectSquareBruteForce(tt.num)
			if got != tt.want {
				t.Errorf("isPerfectSquareBruteForce() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_isPerfectSquare(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		num  int
		want bool
	}{
		{
			name: "smallest perfect square",
			num:  1,
			want: true,
		},
		{
			name: "perfect square",
			num:  16,
			want: true,
		},
		{
			name: "not a perfect square",
			num:  14,
			want: false,
		},
		{
			name: "perfect square, prime root",
			num:  9,
			want: true,
		},
		{
			name: "one below a perfect square",
			num:  15,
			want: false,
		},
		{
			name: "one above a perfect square",
			num:  17,
			want: false,
		},
		{
			name: "large perfect square",
			num:  808201, // 899 * 899
			want: true,
		},
		{
			name: "large non-square near int32 max",
			num:  2147483647,
			want: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := isPerfectSquare(tt.num)
			if got != tt.want {
				t.Errorf("isPerfectSquare() = %v, want %v", got, tt.want)
			}
		})
	}
}
