import os, random, time, tempfile
from pathlib import Path

random.seed(1)
folder = Path(tempfile.mkdtemp())
S, F = 40, 20                              # students, daily files
regs = [f"1925{i:05d}" for i in range(S)]
for d in range(F):
    with open(folder / f"day{d:02d}.txt", "w") as f:
        for r in regs:
            f.write(f"{r},2026-10-{d+1:02d},{random.choice('PPPA')}\n")


def one_pass():                            # read every file once  -> O(f*l)
    count = {}
    for p in folder.glob("*.txt"):
        with open(p) as f:
            for line in f:
                r, _, s = line.strip().split(",")
                if s == "P":
                    count[r] = count.get(r, 0) + 1
    return count


def per_student():                         # re-read for every student -> O(s*f*l)
    count = {}
    for r in regs:
        n = 0
        for p in folder.glob("*.txt"):
            with open(p) as f:
                for line in f:
                    reg, _, s = line.strip().split(",")
                    if reg == r and s == "P":
                        n += 1
        count[r] = n
    return count


for fn in (one_pass, per_student):
    t = time.perf_counter(); res = fn(); dt = time.perf_counter() - t
    print(f"{fn.__name__:<12} {dt*1000:8.1f} ms")
print("same answer:", one_pass() == per_student())
