# Generated by Django 4.0.3 on 2022-05-12 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_goalcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalcomment',
            name='user',
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goal_comments', to='goals.goal', verbose_name='Цель'),
        ),
    ]