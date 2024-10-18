from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import pytest
import allure


@allure.epic("Registration cases")
@allure.issue("GET-123")
class TestUserRegister(BaseCase):
    missed_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("Positive", "Registration")
    @allure.description("This is a successful  test for a user creation")
    def test_create_user_successfully(self):
        data= self.prepare_registration_date()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response,200)
        Assertions.assert_json_has_key(response,"id")


    @allure.tag("Negative", "Registration")
    @allure.description("This is a negative  test to create an existing user")
    def test_create_user_with_existing_email(self):
        email='vinkotov@example.com'
        data= self.prepare_registration_date(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.tag("Negative", "Registration")
    @allure.description("This is a negative  test to create user without @")
    def test_create_user_without_symbol(self):
        email = 'test.test.com'
        data= self.prepare_registration_date(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode( "utf-8") == f"Invalid email format", f"Invalid email format {response.content}"

    @allure.tag("Negative", "Registration")
    @allure.description("This is a negative  test to create user without short name")
    def test_create_user_with_short_name(self):
        data= self.prepare_registration_date()
        data['username'] = str(random.randint(1, 9))

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {response.content}"


    @allure.tag("Negative", "Registration")
    @allure.description("This is a negative  test to create user without long name")
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_date()
        data['username'] = str(random.randint(1, 9))*251

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f"Unexpected response content {response.content}"


    @allure.tag("Negative", "Registration")
    @pytest.mark.parametrize('missed_param',missed_params)
    @allure.description("This is a negative  test to create user  without required parameters")
    def test_create_user_without_param(self,missed_param):
        data = self.prepare_registration_date()

        data.pop(missed_param)
        data_with_missed_param = data

        response = MyRequests.post("/user/", data=data_with_missed_param)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {missed_param}", f"Unexpected response content {response.content}"

