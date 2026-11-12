import timeit


def eafp(line):
    try:
        reg, date, status = line.split(",")
        if status not in ("P", "A"):
            raise ValueError
        return status
    except ValueError:
        return None


def lbyl(line):
    parts = line.split(",")
    if len(parts) == 3 and parts[2] in ("P", "A"):
        return parts[2]
    return None


for label, bad_every in (("rare bad lines (1 in 100)", 100), ("common bad lines (1 in 2)", 2)):
    lines = [("1,2026-10-08" if i % bad_every == 0 else "1,2026-10-08,P") for i in range(10000)]
    for fn in (eafp, lbyl):
        t = timeit.timeit(lambda: [fn(x) for x in lines], number=20) / 20
        print(f"{label:<27}{fn.__name__:<6}{t*1000:7.2f} ms per 10,000 lines")
