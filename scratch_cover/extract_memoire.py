import pypdf
import os

pdf_path = "Mémoire - ALMODOVAR Thomas.pdf"
reader = pypdf.PdfReader(pdf_path)
total = len(reader.pages)
print(f"Total pages: {total}")

os.makedirs("scratch_cover", exist_ok=True)
with open("scratch_cover/all_text_raw.txt", "w", encoding="utf-8") as f:
    for i, page in enumerate(reader.pages):
        txt = page.extract_text() or ""
        f.write(f"\n<<< PAGE {i+1} >>>\n")
        f.write(txt)
        f.write("\n")

print("Done writing full text!")
