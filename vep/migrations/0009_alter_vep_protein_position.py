# Generated by Django 4.0.8 on 2022-12-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vep', '0008_alter_vep_cdna_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vep',
            name='protein_position',
            field=models.CharField(max_length=50),
        ),
    ]
