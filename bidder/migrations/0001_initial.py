# Generated by Django 3.2 on 2022-10-02 15:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(unique=True)),
                ('max_bid', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=2)),
                ('inc_bid', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=2)),
                ('dec_bid', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=2)),
                ('pass_after', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=2)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='graphs')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(unique=True)),
                ('max_bid', models.IntegerField()),
                ('inc_bid', models.IntegerField()),
                ('dec_bid', models.IntegerField()),
                ('pass_after', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
