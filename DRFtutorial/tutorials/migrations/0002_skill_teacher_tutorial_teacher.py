# Generated by Django 4.1.9 on 2023-05-23 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('level', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=70)),
                ('last_name', models.CharField(default='', max_length=70)),
                ('skill', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='tutorial',
            name='teacher',
            field=models.CharField(default='', max_length=70),
        ),
    ]
