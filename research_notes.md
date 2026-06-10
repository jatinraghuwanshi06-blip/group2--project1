# NLP Research Notes

## spaCy Installation
Successfully installed spaCy using:

pip install spacy

## English Model
Installed English model:

python -m spacy download en_core_web_sm

## Entity Extraction Test

Sample text:
"The contract was signed by Microsoft on June 10, 2026 in Hyderabad."

Results:
- Microsoft -> ORG
- June 10, 2026 -> DATE
- Hyderabad -> GPE

## Risk Keywords
Created a legal risk keyword list for future NLP analysis and risk detection