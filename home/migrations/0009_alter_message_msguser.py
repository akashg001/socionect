# Generated by Django 4.0.6 on 2022-08-04 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_message_msguser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='msguser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msguser', to='home.userprofile'),
        ),
    ]