from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import random


class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # REGISTER
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

        #EDIT

        new_name =  "Changed Name"
        response3 = MyRequests.put( f"/user/{user_id}",
        headers = {"x-csrf-token": token},
        cookies={'auth_sid': auth_sid},
        data = {"firstName": new_name}
         )

        Assertions.assert_code_status(response3,200)

        #GET
        response4 = MyRequests.get(f"/user/{user_id}",
        headers={"x-csrf-token": token},
        cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name (response4, "firstName", new_name, "Wrong name of the user after edit")


    def test_edit_user_without_auth(self):
        user_id = 2

        response = MyRequests.put( f"/user/{user_id}",
        data = {"firstName": "Changed Name"}
         )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == '{"error":"Auth token not supplied"}', f"Unexpected content {response.content}"


    def test_edit_user_with_auth_by_another_user(self):
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

        # EDIT

        new_name = "Changed Name"

        response4 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={'auth_sid': auth_sid},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response4, 400)
        assert response4.content.decode(
            'utf-8') == '{"error":"This user can only edit their own data."}', f"Unexpected content {response4.content}"

    def test_edit_user_email_with_auth_without_symbol(self):
        # REGISTER
        register_data = self.prepare_registration_date()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={'auth_sid': auth_sid},
                                   data={"email": 'test.test.com'}
                                   )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            'utf-8') == '{"error":"Invalid email format"}', f"Unexpected content {response3.content}"


    def test_edit_user_firstName_to_short_value_with_auth(self):
        # REGISTER
        register_data = self.prepare_registration_date()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT

        firstName = str(random.randint(1, 9))
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={'auth_sid': auth_sid},
                                   data={"firstName":  firstName}
                                   )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            'utf-8') == '{"error":"The value for field `firstName` is too short"}', f"Unexpected content {response3.content}"


