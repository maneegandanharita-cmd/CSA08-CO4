class InvalidRecord(Exception):
    pass


def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3 or parts[2] not in ("P", "A"):
        raise InvalidRecord("bad line")
    return tuple(parts)


def summarise(lines):
    present, absent = 0, 0
    for line in lines:
        try:
            reg, date, status = parse_line(line)
            if status == "P":
                presnt += 1                # typing error: should be 'present'
            else:
                absent += 1
        except Exception:
            pass                           # hides EVERYTHING
    return present, absent


lines = ["1,2026-10-08,P", "2,2026-10-08,A", "3,2026-10-08,P", "4,2026-10-08,A"]
print(summarise(lines))                    # expected (2, 2)
