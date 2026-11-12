import builtins

# ---------- setup: create the three day files (they were missing) ----------
day_data = {
    "day1.txt": "Data Structures\nOperating Systems",
    "day2.txt": "Computer Networks\nSoftware Engineering",
    "day3.txt": "Database Systems\nAI Fundamentals\nCompilers",
}
for name, text in day_data.items():
    with open(name, "w") as f:
        f.write(text)

# ---------- original (faulty) program from the question ----------
def save_returns(books):
    log = open("returns.log", "w")
    for b in books:
        log.write(b)
    log.close()


def process(day_file):
    try:
        books = open(day_file).read().split("\n")
        save_returns(books)
    except FileNotFoundError:
        print("missing")


# ---------- Task 4.2: test for three days ----------
for day in ("day1.txt", "day2.txt", "day3.txt"):
    process(day)
print("returns.log after 3 days:")
print(repr(open("returns.log").read()))

# defect 3: write() fails -> file stays open, no message saved
opened = []
real_open = builtins.open
def tracking_open(*a, **k):
    f = real_open(*a, **k); opened.append(f); return f
builtins.open = tracking_open
try:
    save_returns(["Book A", None, "Book C"])        # None makes write() fail
except TypeError as e:
    print("\nwrite() failed:", e)
builtins.open = real_open
print("log file closed after the error?", opened[-1].closed)
process("day9.txt")                                  # missing file day
