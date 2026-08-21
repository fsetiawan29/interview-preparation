package solution

import "strings"

func customSortString(order string, s string) string {
	seen := make(map[byte]int)
	for i := 0; i < len(s); i++ {
		seen[s[i]]++
	}

	var sb strings.Builder
	sb.Grow(len(s))

	for i := 0; i < len(order); i++ {
		char := order[i]
		if count, exists := seen[char]; exists {
			for j := 0; j < count; j++ {
				sb.WriteByte(char)
			}
			delete(seen, char)
		}
	}

	for char, count := range seen {
		for j := 0; j < count; j++ {
			sb.WriteByte(char)
		}
		delete(seen, char)
	}

	return sb.String()
}
