# Generated by Django 4.0 on 2024-02-05 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20240130_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckmigrationsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]