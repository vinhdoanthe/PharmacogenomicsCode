# Generated by Django 4.0.8 on 2022-12-06 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vep', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vep',
            name='alleles',
        ),
        migrations.RemoveField(
            model_name='vep',
            name='annotation',
        ),
        migrations.RemoveField(
            model_name='vep',
            name='coding',
        ),
        migrations.RemoveField(
            model_name='vep',
            name='locus',
        ),
        migrations.RemoveField(
            model_name='vep',
            name='n_cases_defined',
        ),
        migrations.RemoveField(
            model_name='vep',
            name='pheno_sex',
        ),
        migrations.RemoveField(
            model_name='vep',
            name='phenocode',
        ),
    ]
