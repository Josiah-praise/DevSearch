# Generated by Django 5.0.2 on 2024-03-02 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_socials'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socials',
            options={'verbose_name': 'Social', 'verbose_name_plural': 'Socials'},
        ),
    ]
