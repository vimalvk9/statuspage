# Generated by Django 2.0.5 on 2018-05-14 13:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppRedirectState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='StatuspageUserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statuspage_access_token', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='YellowAntRedirectState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='YellowUserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellowant_token', models.CharField(max_length=100)),
                ('yellowant_id', models.IntegerField(default=0)),
                ('yellowant_integration_invoke_name', models.CharField(max_length=100)),
                ('yellowant_intergration_id', models.IntegerField(default=0)),
                ('webhook_id', models.CharField(default='', max_length=100)),
                ('webhook_last_updated', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='statuspageusertoken',
            name='user_integration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.YellowUserToken'),
        ),
        migrations.AddField(
            model_name='appredirectstate',
            name='user_integration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.YellowUserToken'),
        ),
    ]
