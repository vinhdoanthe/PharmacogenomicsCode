# interaction
from django.db import models
from drug.models import Drug
from protein.models import Protein

# Create your models here.


class Interaction(models.Model):
    interaction_id = models.AutoField(auto_created=True, primary_key=True)
    drug_bankID = models.ForeignKey(
        "drug.Drug", on_delete=models.CASCADE)
    uniprot_ID = models.ForeignKey(
        "protein.Protein", on_delete=models.CASCADE)
    actions = models.TextField()  # String list, Can be set of categorical data
    known_action = models.TextField()  # String list, Can be set of categorical data
    interaction_type = models.CharField(
        max_length=100
    )  # being one of several values: transporter, enzyme, target, carrier
    atc_codes = models.TextField()
    pubmed_ids = models.TextField()
    ChEMBL = models.TextField()

    def __str__(self):
        return str(self.interaction_id) + " _ " + self.interaction_type
