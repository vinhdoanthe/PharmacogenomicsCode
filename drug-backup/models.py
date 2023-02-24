# drug
from django.db import models

# Create your models here.


class DrugType(models.Model):
    drugtype = models.IntegerField(primary_key=True)  
    type_detail = models.CharField(max_length=20, default="None") # being either 'biotech' or 'small molecule' 

    class Meta():
        db_table = 'drugtype'

class DrugGroup(models.Model):
    druggroup = models.CharField(max_length=50, primary_key=True)  
    group_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'druggroup'

class DrugName(models.Model):
    drugname = models.CharField(max_length=50, primary_key=True)  
    name_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'drugname'

class DrugClass(models.Model):
    drugclass = models.CharField(max_length=50, primary_key=True)  
    class_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'drugclass'

class DrugSubclass(models.Model):
    drugsubclass = models.CharField(max_length=50, primary_key=True)  
    subclass_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'drugsubclass'

class DrugSuperclass(models.Model):
    drugsuperclass = models.CharField(max_length=50, primary_key=True)  
    superclass_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'drugsuperclass'

class DrugParent(models.Model):
    drugparent = models.CharField(max_length=50, primary_key=True)  
    parent_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'drugparent'

class DrugCategory(models.Model):
    drugcategory = models.CharField(max_length=50, primary_key=True)  
    category_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'drugcategory'

class DrugPubChemCompound(models.Model):
    compound = models.CharField(max_length=50, primary_key=True)  
    compound_detail = models.TextField(default="None") 

    class Meta():
        db_table = 'drugpubchemcompound'

class Drug(models.Model):
    drug_bankID = models.CharField(max_length=20, primary_key=True)
    drugtype = models.ForeignKey(
        "drug.drugtype", on_delete=models.CASCADE)
    name = models.ForeignKey(
        "drug.drugname", on_delete=models.CASCADE)
    groups = models.ForeignKey(
        "drug.druggroup", on_delete=models.CASCADE)

    categories = models.ForeignKey(
        "drug.drugcategory", on_delete=models.CASCADE)
    description = models.TextField()  # long string values
    # SMILES = models.CharField(max_length=200)
    # InChIKey = models.CharField(max_length=200)
    aliases = models.TextField()  # similar to name
    # kingdom = models.CharField(
    #     max_length=50, default="None"
    # )  # being one of several values: 'Organic Compounds' 'Organic compounds' 'None' 'Inorganic compounds'
    superclass = models.ForeignKey(
        "drug.drugsuperclass", on_delete=models.CASCADE)
    classname = models.ForeignKey(
        "drug.drugclass", on_delete=models.CASCADE)
    subclass = models.ForeignKey(
        "drug.drugsubclass", on_delete=models.CASCADE)
    direct_parent = models.ForeignKey(
        "drug.drugparent", on_delete=models.CASCADE)
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

    atc_codes = models.TextField(default="None")
    atc_code_detail = models.TextField(default="None")

    chEMBL = models.CharField(
        max_length=250, default="None"
    ) 
    pubChemCompound = models.ForeignKey(
        "drug.drugpubchemcompound", on_delete=models.CASCADE)
    pubChemSubstance = models.TextField(default="None")
    


    def __str__(self):
        return "Drugname: " + self.name + " with drugbank ID: " + self.drug_bankID

    class Meta():
        db_table = 'drug'

