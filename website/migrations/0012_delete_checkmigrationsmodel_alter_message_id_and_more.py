# Generated by Django 4.0 on 2024-02-07 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_checkmigrationsmodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CheckmigrationsModel',
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
