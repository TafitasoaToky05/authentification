# Generated by Django 5.2.2 on 2025-06-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=50, unique=True)),
                ('category', models.CharField(max_length=50)),
                ('stat', models.BooleanField(default=True)),
                ('repere', models.BooleanField(default=False)),
            ],
        ),
    ]
