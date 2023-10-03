# Generated by Django 4.2.3 on 2023-08-01 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mapme', '0002_object_delete_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='object',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pci', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('basestation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapme.basestation')),
            ],
        ),
        migrations.AddField(
            model_name='basestation',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapme.object'),
        ),
    ]