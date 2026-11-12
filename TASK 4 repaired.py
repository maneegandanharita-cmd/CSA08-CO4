import traceback
from datetime import datetime


def log_error(message):
    with open("errors.log", "a", encoding="utf-8") as err:
        err.write(f"{datetime.now():%Y-%m-%d %H:%M:%S}  {message}\n")


def save_returns(books, day_file):
    with open("returns.log", "a", encoding="utf-8") as log:     # append mode
        for b in books:
            if b.strip():                                       # skip empty last line
                log.write(f"{day_file}: {b}\n")                 # newline after each book


def process(day_file):
    try:
        with open(day_file, encoding="utf-8") as f:
            books = f.read().split("\n")
        save_returns(books, day_file)
    except FileNotFoundError:
        log_error(f"{day_file} is missing")
        print("missing:", day_file)
    except Exception as exc:                                    # anything unexpected is saved
        log_error(f"{day_file} failed: {exc!r}")
        raise


open("returns.log", "w").close()                                # start the test with a clean log
for day in ("day1.txt", "day2.txt", "day9.txt", "day3.txt"):
    process(day)
print("--- returns.log ---")
print(open("returns.log", encoding="utf-8").read(), end="")
print("--- errors.log ---")
print(open("errors.log", encoding="utf-8").read(), end="")
