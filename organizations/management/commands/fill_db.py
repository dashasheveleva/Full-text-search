from django.core.management.base import BaseCommand
from django.db import transaction
from organizations.models import Organization
from faker import Faker
import random


def generate_organizations(num):
    fake = Faker('ru_RU')

    full_names = ['Общество с ограниченной ответственностью', 'Федеральное государственное унитарное предприятие',
                  'Публичное акционерное общество', 'Бюджетное учреждение здравоохранения',
                  'Государственная корпорация', 'Муниципальное унитарное предприятие',
                  'Акционерное общество', 'Министерство здравоохранения', 'Федеральное государственное казенное учреждение',
                  'Администрация губернатора']

    short_names = ['ООО', 'ФГУП', 'ПАО', 'БУЗ', 'ГК', 'МУП', 'АО', 'Минздрав', 'ФГКУ', 'Администрация губернатора']

    # Создание пустого списка для хранения сгенерированных организаций.
    organizations = []

    for i in range(num):
        # Генерация случайного числа для выбора префикса из списков.
        random_number = random.randint(0, 9)

        random_name = fake.word().capitalize()

        full_name = full_names[random_number] + ' ' + '«' + random_name + '»'
        short_name = short_names[random_number] + ' ' + '«' + random_name + '»'

        # Генерация случайного 12-значного ИНН для организации.
        inn = str(random.randint(100000000000, 999999999999))

        organization = Organization(full_name=full_name, short_name=short_name, inn=inn)
        organizations.append(organization)

    Organization.objects.bulk_create(organizations)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('num_organizations', type=int, help='Количество организаций для создания')

    def handle(self, *args, **kwargs):
        num_organizations = kwargs['num_organizations']
        with transaction.atomic():
            generate_organizations(num_organizations)
