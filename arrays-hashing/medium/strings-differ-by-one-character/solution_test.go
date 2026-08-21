package solution

import "testing"

func Test_differByOne(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		dict []string
		want bool
	}{
		{
			name: "differs by one character",
			dict: []string{"abcd", "acbd", "aacd"},
			want: true,
		},
		{
			name: "no pair differs by exactly one character",
			dict: []string{"ab", "cd", "yz"},
			want: false,
		},
		{
			name: "match found among several pairs",
			dict: []string{"abcd", "cccc", "abyd", "abab"},
			want: true,
		},
		{
			name: "differs by more than one character",
			dict: []string{"abc", "xyc"},
			want: false,
		},
		{
			name: "differs by exactly one character, two words",
			dict: []string{"abc", "abd"},
			want: true,
		},
		{
			name: "fewer than two words",
			dict: []string{"abc"},
			want: false,
		},
		{
			name: "empty dict",
			dict: []string{},
			want: false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := differByOne(tt.dict)
			if got != tt.want {
				t.Errorf("differByOne() = %v, want %v", got, tt.want)
			}
		})
	}
}
