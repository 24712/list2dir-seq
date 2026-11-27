# list2dir-seq

**AR:** أداة لنسخ الملفات من قائمة مسارات نصية (`paths.txt`) إلى مجلد وجهة مع إضافة ترقيم تسلسلي في بداية كل اسم (`001_filename.ext`، `002_filename.ext`) مع الحفاظ على الامتداد الأصلي.  
**EN:** A lightweight utility to copy files listed in a text file (`paths.txt`) into a destination folder with zero-padded sequential prefixes (`001_filename.ext`, `002_filename.ext`) while preserving original extensions.

---

## How It Works | الفكرة
1. **Read & Clean | القراءة والتنظيف:** Reads paths with **UTF-8** encoding, ignores blank lines, and trims whitespace and surrounding quotes (`"` or `'`).
2. **Validate | التحقق:** Checks that each entry exists and points to a file before copying.
3. **Number & Copy | الترقيم والنسخ:** Copies valid files to the destination folder prefixed with a 3-digit index (`001`, `002`, ...) so alphabetical sorting matches the list order.

---

## Usage | الاستخدام

### Python
Place one path per line in `paths.txt` and run:

```python
from pathlib import Path
import shutil

paths_file = Path("paths.txt")
dest_dir = Path(r"D:\Destination_Folder")
dest_dir.mkdir(parents=True, exist_ok=True)

raw_lines = paths_file.read_text(encoding="utf-8-sig").splitlines()
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
    shutil.copy2(src, dst)
    copied_count += 1

print(f"Copied {copied_count} file(s).")
if missing:
    print("Missing files:")
    for item in missing:
        print(" -", item)
```

### PowerShell
```powershell
$PathsFile = ".\paths.txt"
$DestDir   = "D:\Destination_Folder"

if (-not (Test-Path -Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
}

$lines = Get-Content -Path $PathsFile -Encoding UTF8 |
    ForEach-Object { $_.Trim().Trim('"').Trim("'") } |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) }

$i = 1
foreach ($rawPath in $lines) {
    if (Test-Path -LiteralPath $rawPath -PathType Leaf) {
        $fileName = Split-Path -LiteralPath $rawPath -Leaf
        $numberedName = "{0:D3}_{1}" -f $i, $fileName
        $destPath = Join-Path -Path $DestDir -ChildPath $numberedName
        Copy-Item -LiteralPath $rawPath -Destination $destPath -Force
        $i++
    } else {
        Write-Warning "File not found: $rawPath"
    }
}
```

---

## Key Notes on Quotes, Spaces, UTF-8 & Naming | ملاحظات مهمة

* **Quotes inside `.txt` vs. CLI | علامات التنصيص داخل ملف التكست مقابل سطر الأوامر:**  
  Inside `paths.txt`, quotes are optional because the script reads each line as a single string and strips leading/trailing `"` or `'` automatically. However, when passing paths directly in **CMD** or **PowerShell**, spaces split arguments unless wrapped in quotes (`"..."`).
* **Arabic & UTF-8 | العربية وترميز UTF-8:**  
  Save `paths.txt` as **UTF-8**. Using `utf-8-sig` in Python safely handles UTF-8 files even if they include a BOM header, and `-Encoding UTF8` in PowerShell reads UTF-8 text cleanly.
* **Script File Naming | تسمية ملفات السكريبت:**  
  Avoid special shell operators like `&` or `+` in script filenames (prefer hyphens `-` or underscores `_`) to prevent unintended shell parsing in terminals or automation scripts.

---

## Commands & Functions Reference | جدول الأوامر والخصائص

### Python Reference Table

| Command / Function | Role & Behavior | الدور والوظيفة |
| :--- | :--- | :--- |
| `from pathlib import Path` | Imports `Path` for cross-platform path handling. | استيراد كلاس `Path` للتعامل الآمن مع المسارات. |
| `import shutil` | Imports high-level file copying utilities. | استيراد مكتبة `shutil` لعمليات نسخ الملفات. |
| `Path(...)` | Converts a string into a `Path` object. | تحويل المسار النصي إلى كائن مسار. |
| `.mkdir(parents=True, exist_ok=True)` | Creates destination directory, parent folders if needed, without error if it exists. | إنشاء مجلد الوجهة والمسارات الأب إن لزم دون خطأ إذا كان موجوداً. |
| `.read_text(encoding="utf-8-sig")` | Reads the entire list file using UTF-8 (stripping BOM if present). | قراءة ملف المسارات بالكامل بترميز UTF-8 مع معالجة BOM. |
| `.splitlines()` | Splits text into lines across `\n` and `\r\n`. | تقسيم النص إلى قائمة سطور. |
| `.strip()` | Removes leading/trailing whitespace on each line. | إزالة الفراغات والأسطر الفارغة من أطراف السطر. |
| `.strip('"').strip("'")` | Removes surrounding double or single quotes from paths. | إزالة علامات التنصيص المزدوجة والمفردة من أطراف المسار. |
| `enumerate(paths, start=1)` | Generates a 1-based counter alongside each path. | توليد رقم تسلسلي يبدأ من `1` لكل عنصر. |
| `.exists()` & `.is_file()` | Verifies the path exists and points to a regular file (not a folder). | التحقق من وجود المسار وأنه ملف وليس مجلداً. |
| `f"{index:03d}_{src.name}"` | Formats a 3-digit zero-padded prefix with original filename and extension. | صياغة رقم بثلاث خانات (`001`) متبوعاً بالاسم الأصلي والامتداد. |
| `shutil.copy2(src, dst)` | Copies file contents while preserving metadata (such as timestamps) where supported. | نسخ الملف مع محاولة الحفاظ على البيانات الوصفية مثل التواريخ. |

### PowerShell Reference Table

| Command / Expression | Role & Behavior | الدور والوظيفة |
| :--- | :--- | :--- |
| `Test-Path -Path $DestDir` | Checks whether the destination directory exists. | التحقق من وجود مجلد الوجهة. |
| `New-Item -ItemType Directory -Path $DestDir -Force` | Creates the destination folder and required parent directories. | إنشاء مجلد الوجهة الجديد. |
| `Out-Null` | Suppresses console output from `New-Item`. | منع طباعة تفاصيل المجلد المنشأ في الشاشة. |
| `Get-Content -Path $PathsFile -Encoding UTF8` | Reads list lines using UTF-8 encoding. | قراءة ملف القائمة سطراً بسطر بترميز UTF-8. |
| `ForEach-Object { ... }` | Processes each item in the pipeline. | تمرير كل سطر عبر خطوة معالجة داخل الـ Pipeline. |
| `$_.Trim().Trim('"').Trim("'")` | Trims spaces and surrounding `"` or `'` characters. | إزالة المسافات وعلامات التنصيص من بداية ونهاية السطر. |
| `Where-Object { -not [string]::IsNullOrWhiteSpace($_) }` | Filters out empty or whitespace-only lines. | استبعاد السطور الفارغة أو التي تحتوي على فراغات فقط. |
| `Test-Path -LiteralPath $rawPath -PathType Leaf` | Checks literal path existence (safe for brackets like `[1]`) and confirms it is a file. | التحقق من وجود المسار حرفياً وأنه ملف (`Leaf`) وليس مجلداً. |
| `Split-Path -LiteralPath $rawPath -Leaf` | Extracts the filename with extension from the full path. | استخراج اسم الملف مع امتداده من المسار الكامل. |
| `"{0:D3}_{1}" -f $i, $fileName` | Formats a 3-digit zero-padded number (`001`) followed by the filename. | تنسيق الرقم التسلسلي بثلاث خانات (`001`) ودمجه مع الاسم. |
| `Join-Path -Path $DestDir -ChildPath $numberedName` | Safely combines destination folder and numbered filename. | دمج مسار الوجهة مع الاسم الجديد بشكل صحيح. |
| `Copy-Item -LiteralPath $rawPath -Destination $destPath -Force` | Copies the file to the destination, overwriting if an identical target name exists. | نسخ الملف إلى الوجهة والكتابة فوق الملف الموجود بنفس الاسم إن وُجد. |
| `Write-Warning "..."` | Outputs a warning message when a source file is not found. | طباعة رسالة تحذير عند عدم العثور على الملف المصدر. |
