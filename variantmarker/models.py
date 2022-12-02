from django.db import models
from gene.models import Gene
# Create your models here.


class VariantMarker(models.Model):
    markerID = models.CharField(
        primary_key=True, max_length=200
    )
    geneID = models.ForeignKey(
        "gene.Gene", default=1, on_delete=models.CASCADE)
    locus = models.CharField(max_length=200)
    alleles = models.CharField(max_length=200)  # ex: ["A","G"]
    annotation = models.TextField()

    def __str__(self):
        return "GeneID: " + self.geneID.gene_id + " with markerID: " + self.markerID
