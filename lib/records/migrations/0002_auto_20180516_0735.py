# Generated by Django 2.0.5 on 2018-05-16 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yellowusertoken',
            old_name='yellowant_intergration_id',
            new_name='yellowant_integration_id',
        ),
    ]