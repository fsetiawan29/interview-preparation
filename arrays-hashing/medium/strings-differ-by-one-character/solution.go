package solution

func differByOne(dict []string) bool {
	if len(dict) < 2 {
		return false
	}

	m := len(dict[0])

	for i := 0; i < m; i++ {
		seen := make(map[string]struct{})

		for _, s := range dict {
			masked := s[:i] + "*" + s[i+1:]
			if _, exists := seen[masked]; exists {
				return true
			}
			seen[masked] = struct{}{}
		}
	}

	return false
}
