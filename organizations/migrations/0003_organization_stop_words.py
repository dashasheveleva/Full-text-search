import os

from django.db import migrations, models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver


def update_search_vector(sender, instance, **kwargs):
    # Обновляем поле search_vector с использованием SearchVector и исключаем стоп-слова.
    instance.search_vector = SearchVector('full_name', 'short_name', config='russian') - SearchVector(*instance.stop_words, config='russian')
    instance.save()


def load_stop_words(apps, schema_editor):
    # Получаем модель Organization из приложения organizations.
    Organization = apps.get_model('organizations', 'Organization')

    # Получаем путь к файлу stop_words.txt.
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../stop_words.txt'))

    # Открываем файл со стоп-словами и считываем его содержимое.
    with open(file_path, 'r', encoding='utf-8') as file:
        stop_words = [word.strip() for word in file.readlines()]

    # Обновляем объекты Organization, устанавливая стоп-слова для каждой организации.
    for organization in Organization.objects.all():
        organization.stop_words = stop_words
        organization.save()


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organization_search_vector'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='stop_words',
            field=ArrayField(models.CharField(max_length=100), default=list, blank=True),
        ),
        migrations.RunPython(load_stop_words),
    ]


# Создаем обработчик сигнала для post_save
@receiver(post_save, sender='organizations.Organization')
def update_organization_search_vector(sender, instance, **kwargs):
    update_search_vector(sender, instance, **kwargs)
