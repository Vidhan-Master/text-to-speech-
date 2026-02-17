import sys
import importlib
import pyttsx3

# Replace fragile direct imports with a dynamic lookup for known PDF packages
PdfReader = None
for pkg in ("pypdf", "PyPDF2", "pypdf2"):
    try:
        mod = importlib.import_module(pkg)
        # common class name used by these packages
        PdfReader = getattr(mod, "PdfReader", None)
        if PdfReader:
            break
    except ModuleNotFoundError:
        continue

if PdfReader is None:
    print("Missing PDF library: please install one of: pypdf or PyPDF2")
    print(f"Install with: {sys.executable} -m pip install pypdf PyPDF2")
    sys.exit(1)

from tkinter.filedialog import askopenfilename
import os

book = askopenfilename(filetypes=[("PDF files", "*.pdf")])
if not book:
    sys.exit()

if not os.path.exists(book):
    print("File not found")
    sys.exit()

try:
    pdfreader = PdfReader(book)
    if hasattr(pdfreader, "pages"):
        pages = len(pdfreader.pages)
    else:
        pages = getattr(pdfreader, "numPages", 0)

    speaker = pyttsx3.init()

    for num in range(pages):
        if hasattr(pdfreader, "pages"):
            page = pdfreader.pages[num]
        else:
            page = pdfreader.getPage(num)

        if hasattr(page, "extract_text"):
            text = page.extract_text() or ""
        elif hasattr(page, "extractText"):
            text = page.extractText() or ""
        else:
            text = ""

        if not text.strip():
            print(f"Page {num+1} has no text")
            continue

        print(f"Reading page {num+1}/{pages}...")
        speaker.say(text)
        speaker.runAndWait()

except Exception as e:
    print("Error:", e)
    sys.exit(1)