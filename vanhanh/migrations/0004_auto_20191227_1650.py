# Generated by Django 2.1.7 on 2019-12-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vanhanh', '0003_auto_20191227_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(null=True, verbose_name='Mô tả'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Image'),
        ),
    ]
