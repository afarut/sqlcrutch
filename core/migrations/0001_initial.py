# Generated by Django 4.2.1 on 2023-05-23 15:07

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
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('views', models.PositiveIntegerField(default=0)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='images')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
