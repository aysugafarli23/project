# Generated by Django 5.0.6 on 2024-06-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0005_remove_content_module_remove_content_section_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='recordings/'),
        ),
    ]
