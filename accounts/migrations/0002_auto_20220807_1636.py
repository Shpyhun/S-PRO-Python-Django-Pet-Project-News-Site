# Generated by Django 3.2.14 on 2022-08-07 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['email'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
