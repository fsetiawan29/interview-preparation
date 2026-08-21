package solution

import "testing"

func Test_customSortString(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		order string
		s     string
		want  string
	}{
		{
			name:  "valid",
			order: "cba",
			s:     "abcd",
			want:  "cbad",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := customSortString(tt.order, tt.s)
			if got != tt.want {
				t.Errorf("customSortString() = %v, want %v", got, tt.want)
			}
		})
	}
}
