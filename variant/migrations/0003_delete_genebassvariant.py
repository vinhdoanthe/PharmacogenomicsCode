# Generated by Django 4.0.8 on 2023-02-19 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variant', '0002_alter_vepvariant_amino_acids_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GenebassVariant',
        ),
    ]
