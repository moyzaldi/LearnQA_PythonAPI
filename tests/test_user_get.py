from http.client import responses
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("User details cases")
@allure.issue("GET-123")
class TestUserGet(BaseCase):

    @allure.tag("Negative", "Getting")
    @allure.description("This is a negative  test of getting user information without authorization")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.tag("Positive", "Getting")
    @allure.description("This is a successful  test of getting user information with authorization")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 =  MyRequests.post("/user/login",data=data)

        auth_sid =  self.get_cookie(response1,"auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1,"user_id")

        response2 =  MyRequests.get(
    f"/user/{user_id_from_auth_method}",
        headers = {"x-csrf-token":token},
        cookies = {"auth_sid": auth_sid}
        )

        expected_fields = ["username","email","firstName","lastName"]
        Assertions.assert_json_has_keys(response2,  expected_fields)

    @allure.tag("Negative", "Getting")
    @allure.description("This is a negative  test of getting information about another user")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_as_another_user = (self.get_json_value(response1, "user_id"))+1


        response2 = MyRequests.get(
            f"/user/{user_id_from_as_another_user}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")

