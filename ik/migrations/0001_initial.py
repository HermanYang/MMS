# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageKnowledge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_id', models.IntegerField()),
                ('knowledge_id', models.IntegerField()),
            ],
            options={
                'db_table': 'image_knowledge',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Knowledge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'knowledge',
            },
            bases=(models.Model,),
        ),
    ]
