import spacy

nlp = spacy.load("en_core_web_sm")

text = """
The contract was signed by Microsoft on June 10, 2026 in Hyderabad.
"""

doc = nlp(text)

print("Entities Found:")

for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_}")