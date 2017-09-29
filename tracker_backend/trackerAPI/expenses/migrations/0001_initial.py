# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 14:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clothing', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Entertainment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('electronics', models.DecimalField(decimal_places=2, max_digits=8)),
                ('games', models.DecimalField(decimal_places=2, max_digits=8)),
                ('movies', models.DecimalField(decimal_places=2, max_digits=8)),
                ('bar', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.date.today)),
                ('clothes', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Clothes')),
                ('entertainment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Entertainment')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.DecimalField(decimal_places=2, max_digits=8)),
                ('groceries', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('housing', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rent', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health', models.DecimalField(decimal_places=2, max_digits=8)),
                ('household', models.DecimalField(decimal_places=2, max_digits=8)),
                ('car', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Miscellaneous',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Savings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel', models.DecimalField(decimal_places=2, max_digits=8)),
                ('parking', models.DecimalField(decimal_places=2, max_digits=8)),
                ('public', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Utilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hydro', models.DecimalField(decimal_places=2, max_digits=8)),
                ('electricity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('gas', models.DecimalField(decimal_places=2, max_digits=8)),
                ('internet', models.DecimalField(decimal_places=2, max_digits=8)),
                ('mobile', models.DecimalField(decimal_places=2, max_digits=8)),
                ('television', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='food',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Food'),
        ),
        migrations.AddField(
            model_name='expense',
            name='housing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Housing'),
        ),
        migrations.AddField(
            model_name='expense',
            name='insurance',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Insurance'),
        ),
        migrations.AddField(
            model_name='expense',
            name='miscellaneous',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Miscellaneous'),
        ),
        migrations.AddField(
            model_name='expense',
            name='savings',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Savings'),
        ),
        migrations.AddField(
            model_name='expense',
            name='transportation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Transportation'),
        ),
        migrations.AddField(
            model_name='expense',
            name='utilities',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expenses.Utilities'),
        ),
    ]
