import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import random
import pytest

class TestUserRegister(BaseCase):
    missed_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]
    def setup_method(self):
        base_part = "learnga"
        domain = "example.com"
        random_part =  datetime.now().strftime("%m%d%Y%H%M%S")
        self.symbol = str(random.randint(1, 9))
        self.email = f"{base_part}{random_part}@{domain}"


    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response,200)
        Assertions.assert_json_has_key(response,"id")

    def test_create_user_with_existing_email(self):
        email='vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_without_symbol(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'test.test.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode( "utf-8") == f"Invalid email format", f"Invalid email format {response.content}"

    def test_create_user_with_short_name(self):
        username = self.symbol
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_with_long_name(self):
        username = self.symbol*251
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('missed_param',missed_params)
    def test_create_user_without_param(self,missed_param):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        data.pop(missed_param)
        data_with_missed_param = data

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data_with_missed_param)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {missed_param}", f"Unexpected response content {response.content}"

