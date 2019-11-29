# Generated by Django 2.2.5 on 2019-11-28 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('chat', '0003_chat_is_group_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='is_group_chat',
        ),
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_user_in_dialog', to='user.User')),
                ('second_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_user_in_dialog', to='user.User')),
            ],
        ),
    ]
