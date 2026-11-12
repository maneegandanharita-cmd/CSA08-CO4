import builtins

opened = []
real_open = builtins.open
def tracking_open(*a, **k):
    f = real_open(*a, **k); opened.append(f); return f
builtins.open = tracking_open


def v1_manual_no_finally(path):          # close() skipped when write fails
    f = open(path, "w")
    f.write(None)
    f.close()


def v2_try_finally(path):                # manual close inside finally
    f = open(path, "w")
    try:
        f.write(None)
    finally:
        f.close()


def v3_with(path):                       # with statement
    with open(path, "w") as f:
        f.write(None)


for fn in (v1_manual_no_finally, v2_try_finally, v3_with):
    opened.clear()
    for i in range(5):                   # five days, every day fails
        try:
            fn("tmp_out.txt")
        except TypeError:
            pass
    print(f"{fn.__name__:<22} files still open after 5 errors: {sum(not f.closed for f in opened)}")
