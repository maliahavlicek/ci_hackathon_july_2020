# Generated by Django 3.0.8 on 2020-07-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_post_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]
