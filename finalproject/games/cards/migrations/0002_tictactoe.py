# Generated by Django 3.0.3 on 2020-05-04 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicTacToe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdTimestamp', models.DateTimeField(auto_now_add=True)),
                ('updatedTimestamp', models.DateTimeField(auto_now=True)),
                ('cell1', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell1', to=settings.AUTH_USER_MODEL)),
                ('cell2', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell2', to=settings.AUTH_USER_MODEL)),
                ('cell3', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell3', to=settings.AUTH_USER_MODEL)),
                ('cell4', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell4', to=settings.AUTH_USER_MODEL)),
                ('cell5', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell5', to=settings.AUTH_USER_MODEL)),
                ('cell6', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell6', to=settings.AUTH_USER_MODEL)),
                ('cell7', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell7', to=settings.AUTH_USER_MODEL)),
                ('cell8', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell8', to=settings.AUTH_USER_MODEL)),
                ('cell9', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell9', to=settings.AUTH_USER_MODEL)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p1_games', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p2_games', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_games', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
