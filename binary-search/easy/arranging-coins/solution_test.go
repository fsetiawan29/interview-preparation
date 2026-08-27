package solution

import "testing"

func Test_arrangeCoins(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		n    int
		want int
	}{
		{
			name: "single coin, single row",
			n:    1,
			want: 1,
		},
		{
			name: "one coin short of a second row",
			n:    2,
			want: 1,
		},
		{
			name: "exactly two complete rows",
			n:    3,
			want: 2,
		},
		{
			name: "third row incomplete",
			n:    5,
			want: 2,
		},
		{
			name: "exactly three complete rows",
			n:    8,
			want: 3,
		},
		{
			name: "fourth row exact",
			n:    10,
			want: 4,
		},
		{
			name: "largest constraint value",
			n:    2147483647, // 2^31 - 1
			want: 65535,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := arrangeCoins(tt.n)
			if got != tt.want {
				t.Errorf("arrangeCoins() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_arrangeCoinsBruteForce(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		n    int
		want int
	}{
		{
			name: "single coin, single row",
			n:    1,
			want: 1,
		},
		{
			name: "one coin short of a second row",
			n:    2,
			want: 1,
		},
		{
			name: "exactly two complete rows",
			n:    3,
			want: 2,
		},
		{
			name: "third row incomplete",
			n:    5,
			want: 2,
		},
		{
			name: "exactly three complete rows",
			n:    8,
			want: 3,
		},
		{
			name: "fourth row exact",
			n:    10,
			want: 4,
		},
		{
			name: "largest constraint value",
			n:    2147483647, // 2^31 - 1
			want: 65535,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := arrangeCoinsBruteForce(tt.n)
			if got != tt.want {
				t.Errorf("arrangeCoinsBruteForce() = %v, want %v", got, tt.want)
			}
		})
	}
}
