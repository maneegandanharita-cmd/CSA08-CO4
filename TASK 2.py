from pathlib import Path


def process_month(folder, verbose=False):
    present, absent = {}, {}           # register number -> count
    damaged = []                       # (file name, line number, reason)
    for path in sorted(Path(folder).glob("*.txt")):
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                parts = line.strip().split(",")
                if len(parts) != 3:
                    damaged.append((path.name, line_no, f"expected 3 fields, found {len(parts)}"))
                    if verbose: print(f"  line {line_no}: {line.strip()!r:<28} -> DAMAGED")
                    continue
                reg, date, status = parts
                if status not in ("P", "A"):
                    damaged.append((path.name, line_no, f"invalid status {status!r}"))
                    if verbose: print(f"  line {line_no}: {line.strip()!r:<28} -> DAMAGED")
                    continue
                table = present if status == "P" else absent
                table[reg] = table.get(reg, 0) + 1
                if verbose: print(f"  line {line_no}: {line.strip()!r:<28} -> present={present} absent={absent}")
    return present, absent, damaged


def write_reports(present, absent, damaged, out_dir="."):
    below = []
    with open(Path(out_dir) / "attendance_report.csv", "w", encoding="utf-8") as f:
        f.write("register_no,present,total,percentage\n")
        for reg in sorted(set(present) | set(absent)):
            p, a = present.get(reg, 0), absent.get(reg, 0)
            pct = 100 * p / (p + a)
            f.write(f"{reg},{p},{p + a},{pct:.2f}\n")
            if pct < 75:
                below.append((reg, pct))
    with open(Path(out_dir) / "below_75.txt", "w", encoding="utf-8") as f:
        for reg, pct in below:
            f.write(f"{reg} {pct:.2f}%\n")
    with open(Path(out_dir) / "damaged_lines.log", "w", encoding="utf-8") as f:
        for name, line_no, reason in damaged:
            f.write(f"{name} line {line_no}: {reason}\n")


# ---- Task 2.4: trace of ONE small file with a damaged line ----
print("TRACE for 2026-10-02.txt")
import shutil, tempfile
tmp = Path(tempfile.mkdtemp()); shutil.copy("attendance_oct/2026-10-02.txt", tmp)
process_month(tmp, verbose=True)

# ---- whole month ----
present, absent, damaged = process_month("attendance_oct")
write_reports(present, absent, damaged)
for name in ("attendance_report.csv", "below_75.txt", "damaged_lines.log"):
    print(f"\n--- {name} ---")
    print(open(name, encoding="utf-8").read(), end="")
