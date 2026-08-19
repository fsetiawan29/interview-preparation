package solution

import "strconv"

func sumScores(ops []string) int {
	stack := []int{}

	for i := 0; i < len(ops); i++ {
		operation := ops[i]
		switch {
		case operation == "C":
			stack = stack[:len(stack)-1]
		case operation == "D":
			lastScore := stack[len(stack)-1]
			stack = append(stack, lastScore*2)
		case operation == "+":
			score := stack[len(stack)-1] + stack[len(stack)-2]
			stack = append(stack, score)
		default:
			score, _ := strconv.Atoi(operation)
			stack = append(stack, score)
		}
	}

	sum := 0
	for _, s := range stack {
		sum += s
	}

	return sum
}
