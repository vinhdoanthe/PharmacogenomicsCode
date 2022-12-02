# drug
from django.db import models

# Create your models here.


class Drug(models.Model):
    drug_bankID = models.CharField(max_length=20, primary_key=True)
    drugtype = models.IntegerField()  # being either 'biotech' or 'small molecule'
    name = models.CharField(max_length=225)  # string values
    groups = models.CharField(max_length=50, default="None")  # string values

    categories = models.CharField(
        max_length=50, default="None")  # string values
    description = models.TextField()  # long string values
    # SMILES = models.CharField(max_length=200)
    # InChIKey = models.CharField(max_length=200)
    aliases = models.TextField()  # similar to name
    kingdom = models.CharField(
        max_length=50, default="None"
    )  # being one of several values: 'Organic Compounds' 'Organic compounds' 'None' 'Inorganic compounds'
    superclass = models.CharField(
        max_length=50, default="None"
    )  # chars of numbers for encoded values
    classname = models.CharField(
        max_length=50, default="None"
    )  # chars of numbers for encoded values
    subclass = models.CharField(
        max_length=50, default="None"
    )  # chars of numbers for encoded values
    direct_parent = models.CharField(
        max_length=50, default="None"
    )  # chars of numbers for encoded values
    indication = models.TextField()  # long string values
    pharmacodynamics = models.TextField()  # long string values
    moa = models.TextField()  # long string values
    absorption = models.TextField()  # long string values

    toxicity = models.TextField()  # long string values
    halflife = models.TextField()  # long string values
    distribution_volume = models.TextField()  # long string values
    protein_binding = models.TextField()  # long string values

    dosages = models.TextField()  # long string values
    properties = models.TextField()  # long string values

    def __str__(self):
        return "Drugname: " + self.name + " with drugbank ID: " + self.drug_bankID

    # class Meta():
    #     db_table = 'drugs'
