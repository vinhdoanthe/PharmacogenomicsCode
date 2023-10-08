from django_tables2 import tables
from drug.models import Drug


class DrugTable(tables.Table):

    class Meta:
        model = Drug
        fields = ('drug_bankID', 'name', 'description')
