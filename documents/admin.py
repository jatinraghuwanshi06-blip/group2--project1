from django.contrib import admin
from .models import Document, ExtractedClause, RiskFlag


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "uploaded_at",
    )
    search_fields = (
        "title",
        "extracted_text",
    )
    list_filter = (
        "uploaded_at",
    )
    ordering = (
        "-uploaded_at",
    )
    list_per_page = 10


@admin.register(ExtractedClause)
class ExtractedClauseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "clause_type",
    )
    search_fields = (
        "clause_type",
        "clause_text",
        "document__title",
    )
    list_filter = (
        "clause_type",
    )
    ordering = (
        "clause_type",
    )
    list_per_page = 10


@admin.register(RiskFlag)
class RiskFlagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "risk_level",
    )
    search_fields = (
        "risk_level",
        "description",
        "document__title",
    )
    list_filter = (
        "risk_level",
    )
    ordering = (
        "risk_level",
    )
    list_per_page = 10