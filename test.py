result = [("test1", [0, 1, 2], 3, 1), ("test2", [5, 3, 2], 4, 2), ("test3", [23, 6, 7], 8, 29)]
result.sort(key=lambda z: z[2], reverse=True)
for y, n in enumerate(result):
    print(y, n)
