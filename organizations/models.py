from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Класс модели для представления организации.
class Organization(models.Model):
    """Класс модели организации"""

    # Полное название организации (максимальная длина - 255 символов).
    full_name = models.CharField(max_length=255)

    # Сокращенное название организации (максимальная длина - 100 символов).
    short_name = models.CharField(max_length=100)

    # ИНН (Идентификационный номер налогоплательщика) организации (максимальная длина - 12 символов).
    inn = models.CharField(max_length=12)

    # Поле для хранения списка стоп-слов.
    stop_words = ArrayField(models.CharField(max_length=100), default=list, blank=True)

    search_vector = models.TextField(null=True, blank=True)

    def __str__(self):
        # Метод для представления объекта модели в виде строки (в данном случае, используется полное название).
        return self.full_name

    class Meta:
        # Определение метаданных модели.
        # app_label указывает, к какому приложению относится модель (в данном случае, 'organizations').
        app_label = 'organizations'

        indexes = [
            GinIndex(fields=['full_name'], name='full_name_gin_idx'),
            GinIndex(fields=['short_name'], name='short_name_gin_idx'),
        ]


# Создаем обработчик сигнала для post_save
@receiver(post_save, sender=Organization)
def update_search_vector(sender, instance, **kwargs):
    # Обновляем поле search_vector с использованием SearchVector и исключаем стоп-слова.
    instance.search_vector = SearchVector('full_name', 'short_name', config='russian') - SearchVector(*instance.stop_words, config='russian')
    instance.save()
