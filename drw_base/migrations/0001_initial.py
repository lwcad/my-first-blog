# Generated by Django 4.0.3 on 2022-03-23 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_arch', models.CharField(max_length=30)),
                ('nr_rys', models.CharField(max_length=30)),
                ('nazwa', models.CharField(max_length=256)),
                ('opis', models.TextField()),
                ('zweryfik', models.BooleanField(default=False)),
                ('data_wprow', models.DateTimeField(default=django.utils.timezone.now)),
                ('wprowadzil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
