# Generated by Django 2.0.5 on 2018-06-13 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_auto_20180611_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagedetail',
            name='page_name',
            field=models.CharField(default='', max_length=70),
        ),
    ]
