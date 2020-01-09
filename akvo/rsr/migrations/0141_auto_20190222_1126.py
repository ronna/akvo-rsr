# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-22 11:26


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsr', '0140_auto_20190222_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginlog',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='user email'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='contact email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
