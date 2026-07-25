class MyHashSet:
    def __init__(self):
        self.size = 1000
        self.bucket = [[] for _ in range(self.size)]

    def add(self, key: int) -> None:
        bucket_index = key % self.size
        bucket = self.bucket[bucket_index]
        for b in bucket:
            if key == b:
                return

        bucket.append(key)

    def contains(self, key: int) -> bool:
        bucket_index = key % self.size
        bucket = self.bucket[bucket_index]
        for b in bucket:
            if b == key:
                return True
        
        return False

    def remove(self, key: int) -> None:
        bucket_index = key % self.size
        bucket = self.bucket[bucket_index]
        for i in range(len(bucket)):
            if bucket[i] == key:
                bucket.pop(i)
                return


def run_test(name, operations, args, expected):
    obj = None
    results = []

    for op, arg in zip(operations, args):
        if op == "MyHashSet":
            obj = MyHashSet()
            results.append(None)
        elif op == "add":
            results.append(obj.add(*arg))
        elif op == "contains":
            results.append(obj.contains(*arg))
        elif op == "remove":
            results.append(obj.remove(*arg))

    passed = results == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  operations: {operations}")
    print(f"  args:       {args}")
    print(f"  expected:   {expected}")
    print(f"  got:        {results}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        ["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"],
        [[], [1], [2], [1], [3], [2], [2], [2], [2]],
        [None, None, None, True, False, None, True, None, False],
    )
