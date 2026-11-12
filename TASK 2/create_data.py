from pathlib import Path

folder = Path(__file__).parent / "attendance_oct"
folder.mkdir(exist_ok=True)

days = {
    "2026-10-01.txt": "192511001,2026-10-01,P\n192511002,2026-10-01,A\n192511003,2026-10-01,A\n192511004,2026-10-01,P\n",
    "2026-10-02.txt": "192511001,2026-10-02,P\n192511002,2026-10-02,A\n192511003,2026-10-02,A\n192511004,2026-10-02\n",
    "2026-10-03.txt": "192511001,2026-10-03,P\n192511002,2026-10-03,P\n192511003,2026-10-03,A\n192511004,2026-10-03,X\n",
    "2026-10-04.txt": "192511001,2026-10-04,A\n192511002,2026-10-04,P\n192511003,2026-10-04,A\n192511004,2026-10-04,P\n",
}
for name, text in days.items():
    (folder / name).write_text(text, encoding="utf-8")
print("Created", len(days), "files in", folder)
