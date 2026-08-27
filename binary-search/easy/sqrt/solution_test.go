package solution

import "testing"

func Test_mySqrt(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		x    int
		want int
	}{
		{
			name: "zero",
			x:    0,
			want: 0,
		},
		{
			name: "one",
			x:    1,
			want: 1,
		},
		{
			name: "perfect square",
			x:    4,
			want: 2,
		},
		{
			name: "rounds down",
			x:    8,
			want: 2,
		},
		{
			name: "perfect square, odd root",
			x:    9,
			want: 3,
		},
		{
			name: "one below a perfect square",
			x:    15,
			want: 3,
		},
		{
			name: "one above a perfect square",
			x:    17,
			want: 4,
		},
		{
			name: "large perfect square",
			x:    808201, // 899 * 899
			want: 899,
		},
		{
			name: "largest constraint value",
			x:    2147483647, // 2^31 - 1
			want: 46340,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := mySqrt(tt.x)
			if got != tt.want {
				t.Errorf("mySqrt() = %v, want %v", got, tt.want)
			}
		})
	}
}
