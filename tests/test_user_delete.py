import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Deletion cases")
@allure.issue("DEL-123")
class TestUserDelete(BaseCase):

    @allure.description("This is a negative test  to delete a system user with the number 1-5")
    @allure.tag("Negative", "Deletion")
    def test_delete_system_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 =  MyRequests.post("/user/login",data=data)

        auth_sid =  self.get_cookie(response1,"auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1,"user_id")

        response2 =  MyRequests.delete(
    f"/user/{user_id_from_auth_method}",
        headers = {"x-csrf-token":token},
        cookies = {"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            'utf-8') == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}', f"Unexpected content {response2.content}"

    @allure.tag("Positive",  "Deletion")
    @allure.description("This test is successfully  deletion of the user himself")
    def test_delete_just_created_user(self):
        # REGISTER1
        register_data =  self.prepare_registration_date()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1,  200)
        Assertions.assert_json_has_key(response1, "id")

        email =  register_data['email']
        password = register_data['password']
        user_id= self.get_json_value(response1,"id")

        #LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        #DELETE

        new_name =  "Changed Name"
        response3 = MyRequests.delete( f"/user/{user_id}",
        headers = {"x-csrf-token": token},
        cookies={'auth_sid': auth_sid},
        data = {"firstName": new_name}
         )

        Assertions.assert_code_status(response3,200)

        #GET
        response4 = MyRequests.get(f"/user/{user_id}")

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode(
            'utf-8') == 'User not found', f"Unexpected content {response4.content}"

    @allure.tag("Negative", "Deletion")
    @allure.description("This negative test is for trying to delete another user")
    def test_delete_user_with_auth_by_another_user(self):
        # REGISTER_1
        register_data = self.prepare_registration_date()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        # REGISTER_2
        register_data_2 = self.prepare_registration_date()
        response2 = MyRequests.post("/user/", data=register_data_2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user_id = self.get_json_value(response2, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, 'auth_sid')
        token = self.get_header(response3, 'x-csrf-token')

        # DELETE


        response4 = MyRequests.delete(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response4, 400)
        assert response4.content.decode(
            'utf-8') == '{"error":"This user can only delete their own account."}', f"Unexpected content {response4.content}"