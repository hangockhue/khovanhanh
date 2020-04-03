# Generated by Django 3.0.2 on 2020-04-02 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vanhanh', '0012_auto_20200330_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Phân loại')),
            ],
            options={
                'verbose_name': 'Classification',
                'verbose_name_plural': 'Phân loại',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='describe',
            field=models.TextField(blank=True, null=True, verbose_name='Mô tả'),
        ),
        migrations.AddField(
            model_name='product',
            name='out_stock',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Hết hàng'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Thông tin sản phẩm'),
        ),
        migrations.AlterField(
            model_name='product',
            name='wholesale',
            field=models.CharField(blank=True, default='150k/cái', max_length=50, null=True, verbose_name='Giá bán sĩ'),
        ),
        migrations.AddField(
            model_name='grouptype',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vanhanh.Classification'),
        ),
    ]