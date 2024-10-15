from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
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

    def test_create_user_successfully(self):
        data= self.prepare_registration_date()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response,200)
        Assertions.assert_json_has_key(response,"id")


    def test_create_user_with_existing_email(self):
        email='vinkotov@example.com'
        data= self.prepare_registration_date(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"


    def test_create_user_without_symbol(self):
        email = 'test.test.com'
        data= self.prepare_registration_date(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode( "utf-8") == f"Invalid email format", f"Invalid email format {response.content}"


    def test_create_user_with_short_name(self):
        data= self.prepare_registration_date()
        data['username'] = str(random.randint(1, 9))

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {response.content}"


    def test_create_user_with_long_name(self):
        data = self.prepare_registration_date()
        data['username'] = str(random.randint(1, 9))*251

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f"Unexpected response content {response.content}"


    @pytest.mark.parametrize('missed_param',missed_params)
    def test_create_user_without_param(self,missed_param):
        data = self.prepare_registration_date()

        data.pop(missed_param)
        data_with_missed_param = data

        response = MyRequests.post("/user/", data=data_with_missed_param)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {missed_param}", f"Unexpected response content {response.content}"

