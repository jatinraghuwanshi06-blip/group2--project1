from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Document, ExtractedClause, RiskFlag
from .serializers import DocumentSerializer
from .pdf_extractor import extract_text_from_pdf
from .text_cleaner import clean_extracted_text
from .nlp_engine import (
    extract_companies,
    extract_dates,
    detect_governing_law,
    detect_clause_types,
    detect_risks,
)


class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Save uploaded document
        document = serializer.save()

        # Extract text from PDF
        raw_text = extract_text_from_pdf(document.pdf_file.path)

        # Clean extracted text
        clean_text = clean_extracted_text(raw_text)
        companies = extract_companies(clean_text)
        dates = extract_dates(clean_text)
        governing_law = detect_governing_law(clean_text)
        clauses = detect_clause_types(clean_text)
        risks = detect_risks(clean_text)

        # Save extracted text
        document.extracted_text = clean_text
        document.save()

        # Detect clause types
        clauses = detect_clause_types(clean_text)

        for clause in clauses:
            ExtractedClause.objects.create(
                document=document,
                clause_type=clause,
                clause_text=clean_text
            )

        # Detect risks
        risks = detect_risks(clean_text)

        for risk in risks:
            RiskFlag.objects.create(
                document=document,
                risk_level=risk["risk_level"],
                description=risk["keyword"]
            )

        print("Companies:", companies)
        print("Dates:", dates)
        print("Governing Law:", governing_law)
        print("Clauses:", clauses)
        print("Risks:", risks)