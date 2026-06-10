import fitz

pdf = fitz.open("sample_contracts/Basic-Non-Disclosure-Agreement.pdf")

text = ""

for page in pdf:
    text += page.get_text()

print(text[:1000])