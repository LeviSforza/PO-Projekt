
from django.test import TestCase
from delegations.models import Delegation, Employee


class DelegationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Delegation.objects.create(departure_date='2022-01-21', return_date='2022-01-29', country='Polska',
                                  duration=8, FK_organizer=Employee.objects.get(id=1))

    def test_country_max_length(self):
        author = Delegation.objects.get(pk=7)
        print(author)
        max_length = author._meta.get_field('country').max_length
        self.assertEqual(max_length, 45)

    # def test_str(self):
    #     author = Author.objects.get(id=1)
    #     expected_object_name = f'{author.last_name}, {author.first_name}'
    #     self.assertEqual(str(author), expected_object_name)
