from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

class ExtractedClause(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    clause_type = models.CharField(max_length=100)
    clause_text = models.TextField()

    def __str__(self):
        return self.clause_type


class RiskFlag(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    risk_level = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.risk_level