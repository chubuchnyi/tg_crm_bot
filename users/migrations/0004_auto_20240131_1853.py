# Generated by Django 3.2.9 on 2024-01-31 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rm_unused_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='topic_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
