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
    pubmed_ids = models.TextField(default="None")

    def __str__(self):
        return self.uniprot_ID.uniprot_ID + " acts as a " + self.interaction_type + " for drug " + self.drug_bankID.drug_bankID
