# Generated by Django 4.0.8 on 2023-02-24 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('protein', '0003_remove_protein_custome_field'),
        ('drug', '0002_alter_drug_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('interaction_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('actions', models.TextField()),
                ('known_action', models.TextField()),
                ('interaction_type', models.CharField(max_length=100)),
                ('pubmed_ids', models.TextField(default='None')),
                ('drug_bankID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drug')),
                ('uniprot_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protein.protein')),
            ],
        ),
    ]
