from django.db import models


# Create your models here.


class VariantPhenocode(models.Model):
    phenocode = models.CharField(primary_key=True, max_length=200)
    description = models.TextField(null=True)
    description_more = models.TextField(null=True)

    def __str__(self):
        return "Phenocode: " + self.phenocode + "\n --- Description: "+self.description
