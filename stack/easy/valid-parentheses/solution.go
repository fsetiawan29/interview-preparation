package solution

func validParentheses(s string) bool {
	closingToOpening := map[byte]byte{
		')': '(',
		'}': '{',
		']': '[',
	}

	stack := []byte{}
	for i := 0; i < len(s); i++ {
		char := s[i]

		expectedOpening, isClosing := closingToOpening[char]
		if !isClosing {
			stack = append(stack, char)
			continue
		}

		if len(stack) == 0 {
			return false
		}

		if stack[len(stack)-1] != expectedOpening {
			return false
		}

		stack = stack[:len(stack)-1]
	}

	return len(stack) == 0
}
