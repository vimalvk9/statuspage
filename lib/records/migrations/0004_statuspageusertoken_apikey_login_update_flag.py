# Generated by Django 2.0.5 on 2018-05-25 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_statuspageusertoken_statuspage_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuspageusertoken',
            name='apikey_login_update_flag',
            field=models.BooleanField(default=False, max_length=100),
        ),
    ]
