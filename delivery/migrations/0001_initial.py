# Generated by Django 5.1.1 on 2024-09-07 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TCUSERNAME', models.CharField(help_text='Хэрэглэгчийн нэр', max_length=100)),
                ('TCPASSWORD', models.CharField(help_text='Нууц үг', max_length=100)),
                ('TCGENDER', models.BooleanField(default=False, help_text='Хүйс')),
                ('TCEMAIL', models.CharField(help_text='Имэйл хаяг', max_length=100, unique=True)),
            ],
        ),
    ]
