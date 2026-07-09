import spacy

nlp = spacy.load("en_core_web_sm")


def extract_companies(text):
    """
    Extract company/organization names from text.
    """
    doc = nlp(text)

    companies = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            companies.append(ent.text)

    return list(set(companies))

def extract_dates(text):
    """
    Extract dates from text.
    """
    doc = nlp(text)

    dates = []

    for ent in doc.ents:
        if ent.label_ == "DATE":
            dates.append(ent.text)

    return list(set(dates))

def detect_governing_law(text):
    """
    Detect Governing Law and Jurisdiction clauses.
    """
    keywords = [
        "governing law",
        "jurisdiction",
        "laws of",
        "court",
        "courts"
    ]

    text_lower = text.lower()

    for keyword in keywords:
        if keyword in text_lower:
            return {
                "found": True,
                "keyword": keyword
            }

    return {
        "found": False,
        "keyword": None
    }

def detect_clause_types(text):
    """
    Detect common legal clause types.
    """
    clause_keywords = {
        "Confidentiality": ["confidential", "non-disclosure", "nda"],
        "Termination": ["termination", "terminate", "ended"],
        "Payment": ["payment", "invoice", "fee", "amount"],
        "Liability": ["liability", "liable", "damages"],
        "Governing Law": ["governing law", "jurisdiction", "laws of"]
    }

    detected_clauses = []

    text_lower = text.lower()

    for clause, keywords in clause_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_clauses.append(clause)
                break

    return detected_clauses

def detect_risks(text):
    """
    Detect high-risk legal keywords.
    """
    risk_keywords = {
        "High": [
            "indemnify",
            "indemnification",
            "unlimited liability",
            "exclusive",
            "penalty",
            "breach",
            "terminate immediately",
            "without notice"
        ],
        "Medium": [
            "confidential",
            "damages",
            "liable",
            "termination",
            "non-disclosure"
        ],
        "Low": [
            "payment",
            "invoice",
            "fee",
            "agreement"
        ]
    }

    detected_risks = []
    text_lower = text.lower()

    for level, keywords in risk_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_risks.append({
                    "risk_level": level,
                    "keyword": keyword
                })

    return detected_risks