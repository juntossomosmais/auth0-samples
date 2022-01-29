# Generated by Django 4.0.1 on 2022-01-31 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditAction',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('user_id', models.CharField(max_length=128)),
                ('action', models.CharField(max_length=128)),
                ('success', models.BooleanField()),
                ('ip_address', models.GenericIPAddressField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
