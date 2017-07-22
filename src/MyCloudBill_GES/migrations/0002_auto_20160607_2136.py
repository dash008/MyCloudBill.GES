# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyCloudBill_GES', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='periodo',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
