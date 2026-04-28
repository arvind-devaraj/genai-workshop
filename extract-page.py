import pdfplumber
import sys

if len(sys.argv) > 1:
    pagenum = int(sys.argv[1])
else:
    print("No arguments were provided.")

with pdfplumber.open("Inference Engineering.pdf") as pdf:
    # Page index starts at 0
    page = pdf.pages[pagenum-1] # 3rd page
    print(page.extract_text())