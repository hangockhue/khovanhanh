# Generated by Django 2.1.7 on 2019-12-27 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vanhanh', '0005_auto_20191227_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_off',
            field=models.IntegerField(blank=True, null=True, verbose_name='Giá giảm'),
        ),
    ]
