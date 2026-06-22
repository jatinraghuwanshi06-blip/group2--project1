import re

def clean_extracted_text(text):
    # Remove duplicate spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove broken line breaks inside paragraphs
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Remove extra empty lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove leading/trailing spaces
    return text.strip()