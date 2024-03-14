# Generated by Django 5.0.3 on 2024-03-14 14:04

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ips',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='Endereço IP')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='loan',
            name='ip_address',
        ),
        migrations.AlterField(
            model_name='loan',
            name='description',
            field=models.CharField(max_length=30, verbose_name='Descrição do Empréstimo'),
        ),
        migrations.AddField(
            model_name='loan',
            name='ip',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ips', to='loan.ips'),
            preserve_default=False,
        ),
    ]
