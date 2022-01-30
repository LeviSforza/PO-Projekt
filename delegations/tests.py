import time

from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from delegations.models import Employee


class TestAddDelegation(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome('D:\LenovoD\Downloads\chromedriver_win32\chromedriver.exe')
        super(TestAddDelegation, self).setUp()
        user = Employee.objects.create_superuser(username='admin',
                                                 password='pw',
                                                 first_name='super',
                                                 last_name='user')
        user.role = 'ORGANIZER'
        user.save()
        self.client.force_login(user)  # TestCase client login method
        session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.selenium.get('http://127.0.0.1:8000/')  # load any page
        self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 'value': session_key, 'path': '/'})

    def test_add_delegation_button_redirect_PT001(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/deleg/login/')
        selenium.find_element(By.ID, 'username').send_keys('lenovo')
        selenium.find_element(By.ID, 'password').send_keys('lenovo')
        selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        selenium.get('http://127.0.0.1:8000/deleg/')

        # click button "Add delegation"
        add_button = selenium.find_element(By.ID, 'add_button')
        add_button.click()

        assert selenium.current_url == 'http://127.0.0.1:8000/deleg/add_delegation/'

    def test_add_delegation_correct_data_PT002(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/deleg/login/')
        selenium.find_element(By.ID, 'username').send_keys('lenovo')
        selenium.find_element(By.ID, 'password').send_keys('lenovo')
        selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        selenium.get('http://127.0.0.1:8000/deleg/add_delegation/')

        # get form elements
        departure_date = selenium.find_element(By.ID, 'id_departure_date')
        return_date = selenium.find_element(By.ID, 'id_return_date')
        duration = selenium.find_element(By.ID, 'id_duration')
        country = selenium.find_element(By.ID, 'id_country')
        base_currency = selenium.find_element(By.ID, 'id_base_currency')

        # populate the form with data
        departure_date.send_keys('06.02.2022')
        return_date.send_keys('10.02.2022')
        country.send_keys('Niemcy')
        base_currency.send_keys('euro')
        duration.send_keys('4')

        # submit form
        selenium.find_element(By.ID, 'add_delegation').click()

        table = selenium.find_element(By.XPATH, "//table[@class='table']/tbody")
        row = table.find_element(By.XPATH, "//tr")
        td_departure = row.find_element(By.XPATH, "//td[@class='td departure']").text
        td_return = row.find_element(By.XPATH, "//td[@class='td return']").text
        td_duration = row.find_element(By.XPATH, "//td[@class='td duration']").text
        td_country = row.find_element(By.XPATH, "//td[@class='td country']").text

        assert td_departure == '6 lutego 2022'
        assert td_return == '10 lutego 2022'
        assert td_duration == '4'
        assert td_country == 'Niemcy'

    def test_add_delegation_incorrect_data_PT003(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/deleg/login/')
        selenium.find_element(By.ID, 'username').send_keys('lenovo')
        selenium.find_element(By.ID, 'password').send_keys('lenovo')
        selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        selenium.get('http://127.0.0.1:8000/deleg/add_delegation/')

        # get form elements
        departure_date = selenium.find_element(By.ID, 'id_departure_date')
        return_date = selenium.find_element(By.ID, 'id_return_date')
        duration = selenium.find_element(By.ID, 'id_duration')
        country = selenium.find_element(By.ID, 'id_country')
        base_currency = selenium.find_element(By.ID, 'id_base_currency')

        # populate the form with data
        departure_date.send_keys('16.02.2022')
        return_date.send_keys('10.02.2022')
        country.send_keys('Niemcy')
        base_currency.send_keys('euro')
        duration.send_keys('-1')

        # submit form
        selenium.find_element(By.ID, 'add_delegation').click()

        error_ul = selenium.find_element(By.XPATH, "//ul[@class='errorlist nonfield']")
        error_li = error_ul.find_element(By.XPATH, "//li").text

        assert error_li == 'Wprowadzone dane są niepoprawne! Data powrotu nie może być wcześniejsza od daty wyjazdu!!!'

        selenium.find_element(By.ID, 'id_return_date').send_keys('20.02.2022')
        selenium.find_element(By.ID, 'add_delegation').click()

        error_ul = selenium.find_element(By.XPATH, "//ul[@class='errorlist nonfield']")
        error_li = error_ul.find_element(By.XPATH, "//li").text
        assert error_li == 'Wprowadzone dane są niepoprawne! Czas trwania wyjazdu nie może być mniejszy od 0!!!'

    def test_add_delegation_not_enough_data_PT004(self):
        selenium = self.selenium

        selenium.get('http://127.0.0.1:8000/deleg/login/')

        selenium.find_element(By.ID, 'username').send_keys('lenovo')
        selenium.find_element(By.ID, 'password').send_keys('lenovo')

        selenium.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        selenium.get('http://127.0.0.1:8000/deleg/add_delegation/')

        departure_date = selenium.find_element(By.ID, 'id_departure_date')
        return_date = selenium.find_element(By.ID, 'id_return_date')
        duration = selenium.find_element(By.ID, 'id_duration')
        country = selenium.find_element(By.ID, 'id_country')
        base_currency = selenium.find_element(By.ID, 'id_base_currency')
        submit = selenium.find_element(By.ID, 'add_delegation')

        # populate the form with data
        return_date.send_keys('16.12.2023')
        base_currency.send_keys('zloty')
        duration.send_keys('6')

        # submit form
        submit.click()
        validation_message_1 = departure_date.get_attribute("validationMessage")

        assert validation_message_1 == 'Wypełnij to pole.'

        departure_date.send_keys('10.12.2023')
        submit.click()
        validation_message_2 = country.get_attribute("validationMessage")

        assert validation_message_2 == 'Wypełnij to pole.'

        country.send_keys('Polska')
        submit.click()

        table = selenium.find_element(By.XPATH, "//table[@class='table']/tbody")
        row = table.find_element(By.XPATH, "//tr")
        td_departure = row.find_element(By.XPATH, "//td[@class='td departure']").text
        td_return = row.find_element(By.XPATH, "//td[@class='td return']").text
        td_duration = row.find_element(By.XPATH, "//td[@class='td duration']").text
        td_country = row.find_element(By.XPATH, "//td[@class='td country']").text

        assert td_departure == '10 grudnia 2023'
        assert td_return == '16 grudnia 2023'
        assert td_duration == '6'
        assert td_country == 'Polska'

    def tearDown(self):
        self.selenium.quit()
        super(TestAddDelegation, self).tearDown()
