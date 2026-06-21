from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from .pdf_extractor import extract_text_from_pdf
from .text_cleaner import clean_extracted_text
from rest_framework.parsers import MultiPartParser, FormParser


class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        document = serializer.save()

        raw_text = extract_text_from_pdf(
            document.pdf_file.path
        )

        clean_text = clean_extracted_text(
            raw_text
        )

        document.extracted_text = clean_text
        document.save()