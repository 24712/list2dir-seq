from pathlib import Path
import shutil

paths_file = Path("paths.txt")
dest_dir = Path(r"D:\Destination_Folder")
dest_dir.mkdir(parents=True, exist_ok=True)

# قراءة المسارات وتنظيف الفراغات والسطور الفارغة
raw_lines = paths_file.read_text(encoding="utf-8").splitlines()
paths = [line.strip().strip('"').strip("'") for line in raw_lines if line.strip()]

copied_count = 0
missing = []

for index, raw_path in enumerate(paths, start=1):
    src = Path(raw_path)
    if not src.exists() or not src.is_file():
        missing.append(raw_path)
        continue

    new_name = f"{index:03d}_{src.name}"
    dst = dest_dir / new_name
    shutil.copy2(src, dst)  # copy2 يحافظ على بيانات التوقيت قدر الإمكان
    copied_count += 1

print(f"تم نسخ {copied_count} ملف بنجاح.")
if missing:
    print("ملفات لم يُعثر عليها:")
    for item in missing:
        print(" -", item)
