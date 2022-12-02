from django.db import models

# Create your models here.


class Protein(models.Model):
    uniprot_ID = models.CharField(max_length=50, primary_key=True)
    genename = models.TextField()  # string values
    geneID = models.CharField(max_length=50)  # string values
    entry_name = models.TextField()  # long string values
    protein_name = models.TextField()  # long string values
    custome_field = models.TextField()  # something for noting
