package solution

import "testing"

func Test_sumScores(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		ops  []string
		want int
	}{
		{
			name: "valid",
			ops:  []string{"1", "2", "+", "1", "C", "2", "D"},
			want: 12,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := sumScores(tt.ops)
			if got != tt.want {
				t.Errorf("sumScores() = %v, want %v", got, tt.want)
			}
		})
	}
}
