# Generated by Django 4.0.8 on 2023-02-10 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0003_delete_editors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gene',
            name='inv_normalized',
        ),
        migrations.RemoveField(
            model_name='gene',
            name='saige_version',
        ),
    ]