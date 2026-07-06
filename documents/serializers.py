from rest_framework import serializers
from .models import Document, ExtractedClause, RiskFlag


class ExtractedClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedClause
        fields = [
            "id",
            "clause_type",
            "clause_text",
        ]


class RiskFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFlag
        fields = [
            "id",
            "risk_level",
            "description",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    clauses = ExtractedClauseSerializer(
        source="extractedclause_set",
        many=True,
        read_only=True,
    )

    risks = RiskFlagSerializer(
        source="riskflag_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "pdf_file",
            "uploaded_at",
            "extracted_text",
            "clauses",
            "risks",
        ]
        read_only_fields = [
            "uploaded_at",
            "extracted_text",
            "clauses",
            "risks",
        ]