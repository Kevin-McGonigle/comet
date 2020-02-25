# Generated by Django 2.2.7 on 2019-12-02 14:48

import api.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('hash', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('hash', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('when_uploaded', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=api.models.uploaded_file_path)),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('hash', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('return_type', models.CharField(default='void', max_length=255)),
                ('class_hash', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.Class')),
                ('file_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.File')),
            ],
        ),
        migrations.CreateModel(
            name='MethodParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(default='', max_length=255)),
                ('method_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Method')),
            ],
        ),
        migrations.CreateModel(
            name='ClassRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(default='association', max_length=255)),
                ('child_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.Class')),
                ('parent_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.Class')),
            ],
        ),
        migrations.CreateModel(
            name='ClassParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(default='', max_length=255)),
                ('class_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Class')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='file_hash',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.File'),
        ),
    ]