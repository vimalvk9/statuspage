# Generated by Django 2.0.5 on 2018-06-13 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0007_pagedetail_page_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagedetail',
            name='page_name',
        ),
    ]