# Generated by Django 4.0.8 on 2022-12-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor_name', models.CharField(max_length=200)),
                ('num_users', models.IntegerField()),
            ],
        ),
    ]