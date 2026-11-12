import time, tracemalloc


def make_file(name, n):
    with open(name, "w") as f:
        for i in range(n):
            f.write(f"1925{i:05d},Student{i},{1000 + i % 500}.50\n")


def by_iteration(name):
    total = 0.0
    with open(name) as f:
        for line in f:
            total += float(line.split(",")[2])
    return total


def by_readlines(name):
    total = 0.0
    with open(name) as f:
        lines = f.readlines()          # whole file in memory
    for line in lines:
        total += float(line.split(",")[2])
    return total


make_file("big_mess.txt", 50000)
for fn in (by_iteration, by_readlines):
    tracemalloc.start()
    t = time.perf_counter()
    result = fn("big_mess.txt")
    elapsed = time.perf_counter() - t
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    print(f"{fn.__name__:<13} total={result:.2f}  time={elapsed*1000:6.1f} ms  peak memory={peak/1024:8.1f} KB")
