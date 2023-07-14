# Generated by Django 3.2.20 on 2023-07-07 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Intent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('response', models.TextField(max_length=500)),
                ('tags', models.CharField(blank=True, max_length=100, null=True)),
                ('contexts', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=255, null=True)),
                ('intents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.intent')),
            ],
        ),
    ]
