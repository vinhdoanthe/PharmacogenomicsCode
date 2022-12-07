# Generated by Django 4.0.8 on 2022-12-06 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('variantmarker', '0002_variantmarker_geneid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phenocode', models.CharField(max_length=200)),
                ('locus', models.CharField(max_length=200)),
                ('alleles', models.CharField(max_length=200)),
                ('annotation', models.TextField()),
                ('pheno_sex', models.CharField(max_length=200)),
                ('coding', models.CharField(max_length=200)),
                ('n_cases_defined', models.FloatField()),
                ('impact', models.CharField(max_length=20)),
                ('strand', models.IntegerField()),
                ('consequence', models.CharField(max_length=200)),
                ('cDNA_position', models.IntegerField()),
                ('CDS_position', models.IntegerField()),
                ('protein_position', models.IntegerField()),
                ('amino_acids', models.CharField(max_length=10)),
                ('codons', models.CharField(max_length=50)),
                ('existing_variation', models.CharField(max_length=50)),
                ('BayesDel_addAF_score', models.FloatField()),
                ('BayesDel_noAF_score', models.FloatField()),
                ('ClinPred_score', models.FloatField()),
                ('DANN_score', models.FloatField()),
                ('DEOGEN2_score', models.FloatField()),
                ('Eigen_PC_phred_coding', models.FloatField()),
                ('Eigen_PC_raw_coding', models.FloatField()),
                ('Eigen_phred_coding', models.FloatField()),
                ('Eigen_raw_coding', models.FloatField()),
                ('FATHMM_score', models.FloatField()),
                ('GM12878_fitCons_score', models.FloatField()),
                ('GenoCanyon_score', models.FloatField()),
                ('H1_hESC_fitCons_score', models.FloatField()),
                ('LIST_S2_score', models.FloatField()),
                ('LRT_Omega', models.FloatField()),
                ('LRT_pred', models.FloatField()),
                ('LRT_score', models.FloatField()),
                ('M_CAP_score', models.FloatField()),
                ('MVP_score', models.FloatField()),
                ('MetaLR_score', models.FloatField()),
                ('MetaRNN_score', models.FloatField()),
                ('MutPred_score', models.FloatField()),
                ('MutationAssessor_rankscore', models.FloatField()),
                ('MutationTaster_AAE', models.FloatField()),
                ('MutationTaster_pred', models.FloatField()),
                ('MutationTaster_score', models.FloatField()),
                ('PROVEAN_converted_rankscore', models.FloatField()),
                ('Polyphen2_HDIV_score', models.FloatField()),
                ('Polyphen2_HVAR_score', models.FloatField()),
                ('REVEL_score', models.FloatField()),
                ('SIFT4G_score', models.FloatField()),
                ('SIFT_score', models.FloatField()),
                ('VEST4_score', models.FloatField()),
                ('integrated_fitCons_score', models.FloatField()),
                ('phastCons30way_mammalian', models.FloatField()),
                ('markerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='variantmarker.variantmarker')),
            ],
        ),
    ]
