# Generated by Django 4.2.1 on 2023-05-23 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_alter_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.FloatField()),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='core.book')),
            ],
        ),
    ]
