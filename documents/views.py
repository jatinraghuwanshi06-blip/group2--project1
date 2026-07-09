from rest_framework import generics, status
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = serializer.save()

        raw_text = extract_text_from_pdf(document.pdf_file.path)
        clean_text = clean_extracted_text(raw_text)

        document.extracted_text = clean_text
        document.save()

        companies = extract_companies(clean_text)
        dates = extract_dates(clean_text)
        governing_law = detect_governing_law(clean_text)

        clauses = detect_clause_types(clean_text)
        risks = detect_risks(clean_text)

        for clause in clauses:
            ExtractedClause.objects.create(
                document=document,
                clause_type=clause,
                clause_text=clean_text
            )

        for risk in risks:
            RiskFlag.objects.create(
                document=document,
                risk_level=risk["risk_level"],
                description=risk["keyword"]
            )
        print("\n" + "=" * 60)
        print("📄 DOCUMENT ANALYSIS RESULTS")
        print("=" * 60)
        
        print("\n🏢 Companies:")
        for company in companies:        
            print(f"  • {company}")
        
        print("\n📅 Dates:")
        for date in dates:
            print(f"  • {date}")
        
        print("\n⚖️ Governing Law:")
        print(f"  {governing_law}")
        
        print("\n📑 Clauses:")
        for clause in clauses:
            print(f"  • {clause}")
        
        print("\n🚩 Risks Detected:")
        if risks:
          for i, risk in enumerate(risks, start=1):
             print(f"  {i}. [{risk['risk_level']}] {risk['keyword']}")
        else:
            print("  No risks detected.")

        
        response_serializer = DocumentSerializer(document)

        return Response(
            {
                "message": "Document processed successfully",
                "companies": companies,
                "dates": dates,
                "governing_law": governing_law,
                "document": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )