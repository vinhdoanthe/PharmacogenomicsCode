# Generated by Django 4.0.8 on 2022-12-07 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vep', '0002_remove_vep_alleles_remove_vep_annotation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vep',
            name='DEOGEN2_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='FATHMM_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='LIST_S2_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='MVP_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='MetaRNN_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='Polyphen2_HDIV_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='Polyphen2_HVAR_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='SIFT4G_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='SIFT_score_std',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='vep',
            name='VEST4_score_std',
            field=models.FloatField(default=None),
        ),
    ]
