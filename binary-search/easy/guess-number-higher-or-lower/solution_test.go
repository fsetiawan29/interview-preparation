package solution

import "testing"

func Test_guessNumberBruteForce(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		n    int
		pick int
		want int
	}{
		{
			name: "valid",
			n:    10,
			pick: 6,
			want: 6,
		},
		{
			name: "pick is lower bound",
			n:    10,
			pick: 1,
			want: 1,
		},
		{
			name: "pick is upper bound",
			n:    10,
			pick: 10,
			want: 10,
		},
		{
			name: "n is 1",
			n:    1,
			pick: 1,
			want: 1,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			guess = func(num int) int {
				switch {
				case num > tt.pick:
					return -1
				case num < tt.pick:
					return 1
				default:
					return 0
				}
			}

			got := guessNumberBruteForce(tt.n)
			if got != tt.want {
				t.Errorf("guessNumberBruteForce() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_guessNumber(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		n    int
		pick int
		want int
	}{
		{
			name: "valid",
			n:    10,
			pick: 6,
			want: 6,
		},
		{
			name: "pick is lower bound",
			n:    10,
			pick: 1,
			want: 1,
		},
		{
			name: "pick is upper bound",
			n:    10,
			pick: 10,
			want: 10,
		},
		{
			name: "n is 1",
			n:    1,
			pick: 1,
			want: 1,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			guess = func(num int) int {
				switch {
				case num > tt.pick:
					return -1
				case num < tt.pick:
					return 1
				default:
					return 0
				}
			}

			got := guessNumber(tt.n)
			if got != tt.want {
				t.Errorf("guessNumber() = %v, want %v", got, tt.want)
			}
		})
	}
}
