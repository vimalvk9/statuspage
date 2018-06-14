# Generated by Django 2.0.5 on 2018-05-29 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_statuspageusertoken_apikey_login_update_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.CharField(default='', max_length=25)),
            ],
        ),
        migrations.RemoveField(
            model_name='statuspageusertoken',
            name='statuspage_page',
        ),
        migrations.AddField(
            model_name='pagedetail',
            name='user_integration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.StatuspageUserToken'),
        ),
    ]