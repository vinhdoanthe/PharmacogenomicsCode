# Generated by Django 4.0.8 on 2023-03-10 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protein', '0003_remove_protein_custome_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latin_name', models.CharField(max_length=100, unique=True)),
                ('common_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'species',
            },
        ),
    ]
