package solution

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func preorderTraversal(root *TreeNode) []int {
	var res []int

	var dfs func(node *TreeNode)
	dfs = func(node *TreeNode) {
		if node == nil {
			return
		}

		res = append(res, node.Val)

		dfs(node.Left)

		dfs(node.Right)
	}

	dfs(root)

	return res
}
