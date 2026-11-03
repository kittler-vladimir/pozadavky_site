from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Requirement, Requirement_type


class RequirementAdminChangelistTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('admin', 'admin@example.com', 'pw')
        group = Group.objects.create(name='Oddělení A')
        req_type = Requirement_type.objects.create(requirement_type_text='Typ')
        for name, cj in (('S číslem', 'ABC-123/2025'), ('Bez čísla', None)):
            Requirement.objects.create(
                requirement=name,
                cislo_jednaci=cj,
                author=cls.admin,
                category=0,
                requirement_type=req_type,
                group_owner=group,
            )

    def setUp(self):
        self.client.force_login(self.admin)

    def test_changelist_shows_cislo_jednaci_column(self):
        response = self.client.get(reverse('admin:pozadavky_requirement_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Č. j.')
        self.assertContains(response, 'ABC-123/2025')
        self.assertContains(response, '<td class="field-cislo_jednaci">-</td>', html=True)

    def test_changelist_search_by_cislo_jednaci(self):
        response = self.client.get(
            reverse('admin:pozadavky_requirement_changelist'), {'q': 'ABC-123'}
        )
        self.assertContains(response, 'S číslem')
        self.assertNotContains(response, 'Bez čísla')
