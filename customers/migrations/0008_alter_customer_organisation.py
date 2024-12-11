# Generated by Django 5.1.4 on 2024-12-11 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_alter_customer_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customers.userprofile'),
            preserve_default=False,
        ),
    ]