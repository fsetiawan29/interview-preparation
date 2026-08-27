package solution

import (
	"reflect"
	"testing"
)

func buildList(vals []int) *ListNode {
	dummy := &ListNode{}
	tail := dummy
	for _, v := range vals {
		tail.Next = &ListNode{Val: v}
		tail = tail.Next
	}
	return dummy.Next
}

func toSlice(head *ListNode) []int {
	vals := []int{}
	for node := head; node != nil; node = node.Next {
		vals = append(vals, node.Val)
	}
	return vals
}

func Test_reverseList(t *testing.T) {
	tests := []struct {
		name string // description of this test case
		// Named input parameters for target function.
		head []int
		want []int
	}{
		{
			name: "odd length list",
			head: []int{1, 2, 3, 4, 5},
			want: []int{5, 4, 3, 2, 1},
		},
		{
			name: "even length list",
			head: []int{1, 2},
			want: []int{2, 1},
		},
		{
			name: "empty list",
			head: []int{},
			want: []int{},
		},
		{
			name: "single node",
			head: []int{1},
			want: []int{1},
		},
		{
			name: "negative and repeated values",
			head: []int{-5, 0, -5, 3},
			want: []int{3, -5, 0, -5},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := toSlice(reverseList(buildList(tt.head)))
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("reverseList() = %v, want %v", got, tt.want)
			}
		})
	}
}
