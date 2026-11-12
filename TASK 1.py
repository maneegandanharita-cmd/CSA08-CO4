from decimal import Decimal, InvalidOperation


def total_mess_bills(filename):
    """Return (total, report_lines, rejected) for a mess-bill file."""

    total = Decimal("0")
    report_lines = []
    rejected = []  # (line number, text, reason)

    try:
        with open(filename, encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()

                if line == "":
                    continue

                parts = [p.strip() for p in line.split(",")]

                if len(parts) != 3:
                    rejected.append(
                        (line_no, line, f"expected 3 fields, found {len(parts)}")
                    )
                    continue

                reg_no, name, amount_text = parts

                try:
                    amount = Decimal(amount_text)  # keeps paise exact
                except InvalidOperation:
                    rejected.append(
                        (line_no, line, f"invalid amount {amount_text!r}")
                    )
                    continue

                total += amount
                report_lines.append(f"{name:<10}{amount:>10}")

    except FileNotFoundError:
        rejected.append((0, filename, "file not found"))

    except PermissionError:
        rejected.append((0, filename, "permission denied"))

    return total, report_lines, rejected


total, report_lines, rejected = total_mess_bills("mess_oct.txt")

print("\n".join(report_lines))
print("Total", total)
print("Rejected lines:", len(rejected))

for item in rejected:
    print("  ", item)


print(total_mess_bills("no_such_file.txt"))
