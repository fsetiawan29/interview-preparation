package solution

import "testing"

func Test_validParentheses(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		s    string
		want bool
	}{
		{
			name: "valid",
			s:    "[]",
			want: true,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := validParentheses(tt.s)
			if got != tt.want {
				t.Errorf("validParentheses() = %v, want %v", got, tt.want)
			}
		})
	}
}
