# Generated by Django 4.2.4 on 2023-09-03 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0003_remove_reply_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='registration_code',
            field=models.CharField(default=123456, max_length=6),
            preserve_default=False,
        ),
    ]
