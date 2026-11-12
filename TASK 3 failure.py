import os, tempfile


def show(label, func):
    try:
        func()
        print(f"{label:<22} -> no exception")
    except Exception as e:
        print(f"{label:<22} -> {type(e).__name__}: {e}")


tmp = tempfile.mkdtemp()
bad = os.path.join(tmp, "bad.txt")
open(bad, "wb").write(b"192511001,2026-10-01,P\n\xff\xfe\xfa\n")
empty = os.path.join(tmp, "empty.txt"); open(empty, "w").close()

show("missing folder", lambda: os.listdir("no_such_folder"))
show("missing file", lambda: open("no_such_file.txt"))
show("path is a folder", lambda: open("."))
show("wrong encoding", lambda: open(bad, encoding="utf-8").read())
show("damaged (bad number)", lambda: int("P1"))
show("damaged (few fields)", lambda: "192511001,2026-10-01".split(",")[2])
show("empty file (read)", lambda: open(empty).read().splitlines()[0])
