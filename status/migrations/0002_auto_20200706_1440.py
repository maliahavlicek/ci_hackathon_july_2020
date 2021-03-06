# Generated by Django 3.0.8 on 2020-07-06 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusinput',
            name='family_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='status',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]
