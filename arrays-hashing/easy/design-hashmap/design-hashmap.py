class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.data = [[] for _ in range(self.size)]

    def put(self, key: int, value: int) -> None:
        bucket_index = key % self.size
        bucket = self.data[bucket_index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i][1] = value
                return
        bucket.append([key,value])

    def get(self, key: int) -> int:
        bucket_index = key % self.size
        bucket = self.data[bucket_index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1]
        return -1

    def remove(self, key: int) -> None:
        bucket_index = key % self.size
        bucket = self.data[bucket_index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i][1] = -1


def run_test(name, operations, args, expected):
    obj = None
    results = []

    for op, arg in zip(operations, args):
        if op == "MyHashMap":
            obj = MyHashMap()
            results.append(None)
        elif op == "put":
            results.append(obj.put(*arg))
        elif op == "get":
            results.append(obj.get(*arg))
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
        ["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"],
        [[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]],
        [None, None, None, 1, -1, None, 1, None, -1],
    )
