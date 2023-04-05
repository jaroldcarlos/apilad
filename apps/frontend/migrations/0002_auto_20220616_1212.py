# Generated by Django 3.2.13 on 2022-06-16 10:12

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='images', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='page',
            name='publish_on',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.site'),
        ),
    ]
