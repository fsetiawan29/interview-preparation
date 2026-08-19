package solution

import "testing"

func Test_validPalindrome(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		s    string
		want bool
	}{
		{
			name: "valid",
			s:    "katak",
			want: true,
		},
		{
			name: "invalid",
			s:    "test",
			want: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := validPalindrome(tt.s)
			if got != tt.want {
				t.Errorf("validPalindrome() = %v, want %v", got, tt.want)
			}
		})
	}
}
