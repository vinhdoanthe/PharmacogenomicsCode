from django.db import models
from variantmarker.models import VariantMarker
# from gene.models import Gene
# Create your models here.


class GenebassVariant(models.Model):
    markerID = models.ForeignKey(
        "variantmarker.VariantMarker", on_delete=models.CASCADE
    )
    # geneID = models.ForeignKey(
    #     "Gene.gene_id", on_delete=models.CASCADE
    # )

    n_cases = models.FloatField()
    n_controls = models.FloatField()
    heritability = models.FloatField()
    # encoded as categorical data
    trait_type = models.CharField(max_length=200)
    phenocode = models.CharField(max_length=200)
    pheno_sex = models.CharField(max_length=200)  # encoded as categorical data
    coding = models.TextField(default="None")
    n_cases_defined = models.FloatField()
    n_cases_both_sexes = models.FloatField()
    n_cases_females = models.FloatField()
    n_cases_males = models.FloatField()

    category = models.TextField(default="None")  # encoded as categorical data
    AC = models.FloatField()
    AF = models.FloatField()
    BETA = models.FloatField()
    SE = models.FloatField()
    AF_Cases = models.FloatField()
    AF_Controls = models.FloatField()
    Pvalue = models.FloatField()
    AC_calstat = models.FloatField()
    AF_calstat = models.FloatField()

    # def __str__(self):
    #     return "GeneID: " + self.geneID.gene_id + " with markerID: " + self.markerID
