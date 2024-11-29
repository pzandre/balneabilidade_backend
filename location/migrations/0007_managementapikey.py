# Generated by Django 5.1.3 on 2024-11-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_cityurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementAPIKey',
            fields=[
                ('id', models.CharField(editable=False, max_length=150, primary_key=True, serialize=False, unique=True)),
                ('prefix', models.CharField(editable=False, max_length=8, unique=True)),
                ('hashed_key', models.CharField(editable=False, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(default=None, help_text='A free-form name for the API key. Need not be unique. 50 characters max.', max_length=50)),
                ('revoked', models.BooleanField(blank=True, default=False, help_text='If the API key is revoked, clients cannot use it anymore. (This cannot be undone.)')),
                ('expiry_date', models.DateTimeField(blank=True, help_text='Once API key expires, clients cannot use it anymore.', null=True, verbose_name='Expires')),
            ],
            options={
                'verbose_name': 'Management API Key',
                'verbose_name_plural': 'Management API Keys',
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]