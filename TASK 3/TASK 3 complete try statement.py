class InvalidRecord(Exception):
    """A line of the attendance file is not in the expected format."""


def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    reg, date, status = parts
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status {status!r}")
    try:
        year, month, day = (int(x) for x in date.split("-"))
    except ValueError as exc:
        raise InvalidRecord(f"invalid date {date!r}") from exc   # keeps original cause
    return reg, date, status


def summarise(path):
    present = absent = 0
    errors = []
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        errors.append((0, "file not found"))
    except PermissionError:
        errors.append((0, "permission denied"))
    else:                                         # runs only when open() succeeded
        try:
            for line_no, line in enumerate(f, start=1):
                try:
                    reg, date, status = parse_line(line)
                except InvalidRecord as err:
                    errors.append((line_no, str(err)))
                    continue
                present += status == "P"
                absent += status == "A"
        except UnicodeDecodeError:
            errors.append((0, "wrong encoding"))
        finally:
            f.close()                             # always closes the file
            print("   [finally] file closed:", f.closed)
    return present, absent, errors


with open("day.csv", "w", encoding="utf-8") as f:
    f.write("1,2026-10-08,P\n2,2026-10-08,A\n3,2026-1x-08,P\n4,2026-10-08,L\n")
with open("latin.csv", "wb") as f:
    f.write(b"1,2026-10-08,P\n\xff\xfe\n")

print("day.csv     ->", summarise("day.csv"))
print("latin.csv   ->", summarise("latin.csv"))
print("missing.csv ->", summarise("missing.csv"))
try:
    parse_line("3,2026-1x-08,P")
except InvalidRecord as e:
    print("raise ... from:", e, "| caused by:", repr(e.__cause__))
