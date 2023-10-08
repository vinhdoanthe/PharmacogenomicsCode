# Generated by Django 4.0.8 on 2023-03-14 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtcAnatomicalGroup',
            fields=[
                ('id', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('name', models.CharField(default='None', max_length=100)),
            ],
            options={
                'db_table': 'atc_anatomical_group',
            },
        ),
        migrations.CreateModel(
            name='AtcChemicalGroup',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(default='None', max_length=100)),
            ],
            options={
                'db_table': 'atc_chemical_group',
            },
        ),
        migrations.CreateModel(
            name='AtcChemicalSubstance',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(default='None', max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.atcchemicalgroup')),
            ],
            options={
                'db_table': 'atc_chemical_substance',
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('drug_bankID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('aliases', models.TextField()),
                ('indication', models.TextField()),
                ('pharmacodynamics', models.TextField()),
                ('moa', models.TextField()),
                ('absorption', models.TextField()),
                ('toxicity', models.TextField()),
                ('halflife', models.TextField()),
                ('distribution_volume', models.TextField()),
                ('protein_binding', models.TextField()),
                ('dosages', models.TextField()),
                ('properties', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DrugCategory',
            fields=[
                ('drugcategory', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('category_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugcategory',
            },
        ),
        migrations.CreateModel(
            name='DrugChembl',
            fields=[
                ('drugchembl', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('chembl_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugchembl',
            },
        ),
        migrations.CreateModel(
            name='DrugClass',
            fields=[
                ('drugclass', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('class_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugclass',
            },
        ),
        migrations.CreateModel(
            name='DrugGroup',
            fields=[
                ('druggroup', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('group_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'druggroup',
            },
        ),
        migrations.CreateModel(
            name='DrugParent',
            fields=[
                ('drugparent', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('parent_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugparent',
            },
        ),
        migrations.CreateModel(
            name='DrugPubChemCompound',
            fields=[
                ('compound', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('compound_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugpubchemcompound',
            },
        ),
        migrations.CreateModel(
            name='DrugPubChemSubstance',
            fields=[
                ('drugpubchemblsubstance', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('pubchemblsubstance_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugpubchemblsubstance',
            },
        ),
        migrations.CreateModel(
            name='DrugSubclass',
            fields=[
                ('drugsubclass', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('subclass_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugsubclass',
            },
        ),
        migrations.CreateModel(
            name='DrugSuperclass',
            fields=[
                ('drugsuperclass', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('superclass_detail', models.TextField(default='None')),
            ],
            options={
                'db_table': 'drugsuperclass',
            },
        ),
        migrations.CreateModel(
            name='DrugType',
            fields=[
                ('drugtype', models.IntegerField(primary_key=True, serialize=False)),
                ('type_detail', models.CharField(default='None', max_length=20)),
            ],
            options={
                'db_table': 'drugtype',
            },
        ),
        migrations.CreateModel(
            name='DrugAtcAssociation',
            fields=[
                ('association_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('atc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.atcchemicalsubstance')),
                ('drug_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drug')),
            ],
            options={
                'db_table': 'drug_atc_association',
            },
        ),
        migrations.AddField(
            model_name='drug',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugcategory'),
        ),
        migrations.AddField(
            model_name='drug',
            name='chEMBL',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugchembl'),
        ),
        migrations.AddField(
            model_name='drug',
            name='classname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugclass'),
        ),
        migrations.AddField(
            model_name='drug',
            name='direct_parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugparent'),
        ),
        migrations.AddField(
            model_name='drug',
            name='drugtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugtype'),
        ),
        migrations.AddField(
            model_name='drug',
            name='groups',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.druggroup'),
        ),
        migrations.AddField(
            model_name='drug',
            name='pubChemCompound',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugpubchemcompound'),
        ),
        migrations.AddField(
            model_name='drug',
            name='pubChemSubstance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugpubchemsubstance'),
        ),
        migrations.AddField(
            model_name='drug',
            name='subclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugsubclass'),
        ),
        migrations.AddField(
            model_name='drug',
            name='superclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.drugsuperclass'),
        ),
        migrations.CreateModel(
            name='AtcTherapeuticGroup',
            fields=[
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(default='None', max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.atcanatomicalgroup')),
            ],
            options={
                'db_table': 'atc_therapeutic_group',
            },
        ),
        migrations.CreateModel(
            name='AtcPharmacologicalGroup',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(default='None', max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.atctherapeuticgroup')),
            ],
            options={
                'db_table': 'atc_pharmacological_group',
            },
        ),
        migrations.AddField(
            model_name='atcchemicalgroup',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug.atcpharmacologicalgroup'),
        ),
    ]