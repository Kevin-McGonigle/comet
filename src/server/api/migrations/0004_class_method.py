# Generated by Django 3.0.5 on 2020-04-21 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200225_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_hash', models.CharField(editable=False, max_length=64, primary_key=True, serialize=False)),
                ('parent', models.CharField(max_length=64, null=True)),
                ('name', models.CharField(max_length=64)),
                ('arguments', models.CharField(max_length=64)),
                ('methods', models.CharField(max_length=64)),
                ('returns', models.CharField(max_length=64, null=True)),
                ('child_hash', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('method_hash', models.CharField(editable=False, max_length=64, primary_key=True, serialize=False)),
                ('parent', models.CharField(max_length=64, null=True)),
                ('name', models.CharField(max_length=64)),
                ('arguments', models.CharField(max_length=64)),
                ('returns', models.CharField(max_length=64)),
                ('child_hash', models.CharField(max_length=64, null=True)),
            ],
        ),
    ]
