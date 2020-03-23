# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-23 03:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acertado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acertado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('architecture', models.IntegerField()),
                ('city', models.IntegerField()),
                ('friends', models.IntegerField()),
                ('batman', models.IntegerField()),
                ('minecraft', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('nPiezas', models.IntegerField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=60)),
                ('link1', models.URLField()),
                ('link2', models.URLField(null=True)),
                ('categoria', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
                ('nPiezas', models.IntegerField()),
                ('observaciones', models.TextField()),
                ('estado', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='calificacion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recomendador.Producto'),
        ),
        migrations.AddField(
            model_name='calificacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acertado',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recomendador.Producto'),
        ),
        migrations.AddField(
            model_name='acertado',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
