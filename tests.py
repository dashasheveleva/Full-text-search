import unittest
from django.test import TestCase
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_service.settings")
django.setup()


from organizations.models import Organization


class OrganizationModelTestCase(TestCase):
    def setUp(self):
        self.organization_data = {
            'full_name': 'Общество с ограниченной ответственностью "Звезда"',
            'short_name': 'ООО "Звезда"',
            'inn': '123456789012'
        }

    def test_organization_creation(self):
        organization = Organization.objects.create(**self.organization_data)
        self.assertEqual(organization.full_name, self.organization_data['full_name'])
        self.assertEqual(organization.short_name, self.organization_data['short_name'])
        self.assertEqual(organization.inn, self.organization_data['inn'])

    def test_organization_full_name_max_length(self):
        max_length = Organization._meta.get_field('full_name').max_length
        organization = Organization.objects.create(**self.organization_data)
        self.assertLessEqual(len(organization.full_name), max_length)

    def test_organization_short_name_max_length(self):
        max_length = Organization._meta.get_field('short_name').max_length
        organization = Organization.objects.create(**self.organization_data)
        self.assertLessEqual(len(organization.short_name), max_length)

    def test_organization_inn_max_length(self):
        max_length = Organization._meta.get_field('inn').max_length
        organization = Organization.objects.create(**self.organization_data)
        self.assertLessEqual(len(organization.inn), max_length)


if __name__ == '__main__':
    unittest.main()
