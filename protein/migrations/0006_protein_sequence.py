# Generated by Django 4.0.8 on 2023-05-01 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protein', '0005_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='protein',
            name='sequence',
            field=models.TextField(null=True),
        ),
    ]
