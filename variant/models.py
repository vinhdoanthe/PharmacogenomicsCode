from django.db import models
from gene.models import Gene

# Create your models here.


class GenebassVariant(models.Model):
    genebass_variant_id = models.AutoField(
        auto_created=True, default=1, primary_key=True
    )
    gene_id = models.ForeignKey("gene.Gene", on_delete=models.CASCADE)
    locus = models.CharField(max_length=200)  # ex: chr1:1632219
    alleles = models.CharField(max_length=200)  # ex: ["A","G"]
    markerID = models.CharField(max_length=200)  # ex: chr1:1632219_A/G
    annotation = models.CharField(
        max_length=200
    )  # ex: missense, encoded as categorical data

    n_cases = models.FloatField()
    n_controls = models.FloatField()
    heritability = models.FloatField()
    # encoded as categorical data
    trait_type = models.CharField(max_length=200)
    phenocode = models.CharField(max_length=200)
    pheno_sex = models.CharField(max_length=200)  # encoded as categorical data
    coding = models.CharField(max_length=200)
    n_cases_defined = models.FloatField()
    n_cases_both_sexes = models.FloatField()
    n_cases_females = models.FloatField()
    n_cases_males = models.FloatField()
    description = models.TextField()
    description_more = models.TextField()
    coding_description = models.CharField(max_length=200)
    category = models.CharField(max_length=200)  # encoded as categorical data
    AC = models.FloatField()
    AF = models.FloatField()
    BETA = models.FloatField()
    SE = models.FloatField()
    AF_Cases = models.FloatField()
    AF_Controls = models.FloatField()
    Pvalue = models.FloatField()
    AC_calstat = models.FloatField()
    AF_calstat = models.FloatField()
