# Generated by Django 4.0.6 on 2022-08-04 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='msguser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msguser', to='home.userprofile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='reciepient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='home.userprofile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='home.userprofile'),
        ),
    ]