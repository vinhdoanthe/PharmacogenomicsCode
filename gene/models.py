from django.db import models

# Create your models here.


class Gene(models.Model):
    gene_id = models.CharField(max_length=50, primary_key=True)
    genename = models.CharField(max_length=50)  # string values
    saige_version = models.CharField(max_length=50)  # string values
    inv_normalized = models.CharField(
        max_length=50
    )  # true or false that can ebe encoded

    def __str__(self):
        return "GeneID: "+self.gene_id + ", gene name: "+self.genename
