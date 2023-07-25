# Generated by Django 4.2.3 on 2023-07-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Images',
            },
        ),
    ]
