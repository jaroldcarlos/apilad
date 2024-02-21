# Generated by Django 4.2 on 2024-02-21 20:56

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frontend", "0015_rename_promotions_promotion"),
    ]

    operations = [
        migrations.AddField(
            model_name="promotion",
            name="description",
            field=ckeditor.fields.RichTextField(blank=True, verbose_name="description"),
        ),
        migrations.AddField(
            model_name="promotion",
            name="description_short",
            field=models.TextField(blank=True, verbose_name="description short"),
        ),
        migrations.AlterField(
            model_name="promotion",
            name="alt",
            field=models.CharField(
                blank=True,
                help_text="Texto alternativo para la imagen",
                max_length=255,
                null=True,
                verbose_name="alt image",
            ),
        ),
    ]