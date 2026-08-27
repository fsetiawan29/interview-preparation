package solution

func searchMatrixBruteForce(matrix [][]int, target int) bool {
	for row := 0; row < len(matrix); row++ {
		for col := 0; col < len(matrix[row]); col++ {
			if matrix[row][col] == target {
				return true
			}
		}

	}

	return false
}

func searchMatrix(matrix [][]int, target int) bool {
	m := len(matrix)
	n := len(matrix[0])

	left := 0
	right := m*n - 1

	for left <= right {
		mid := left + (right-left)/2

		row := mid / n
		col := mid % n

		if matrix[row][col] == target {
			return true
		}

		if matrix[row][col] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return false
}
