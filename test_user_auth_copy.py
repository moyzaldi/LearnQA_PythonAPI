import requests
import pytest

class TestUserAuth:
    def test_auth_user(self):
        data = {
        'email': 'vinkotov@example.com',
        'password': '1234'
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)
        assert "auth_sid" in response1.cookies, "В ответе нет куки"
        assert  "x-csrf-token" in response1.headers,  "В Ответе нет CSRF"
        assert "user_id" in response1.json(),"В ответе  нет  юзерID"

        auth_sid = response1.cookies.get("auth_sid")
        token  = response1.headers.get ("x-csrf-token")
        user_id_from_auth_method = response1.json ()["user_id"]

        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        assert  "user_id" in response2.json(), "Нет юзер ид во втором ответе"
        user_id_from_check_method = response2.json ()["user_id"]

        assert user_id_from_auth_method == user_id_from_check_method, " Не совпадают юзер ид из методов"

    exlude_params = [
        ("no_cookee"),
        ("no_token")
    ]

    @pytest.mark.parametrize('conditions',exlude_params)
    def test_negative_auth_check(self, conditions):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)
            assert "auth_sid" in response1.cookies, "В ответе нет куки"
            assert "x-csrf-token" in response1.headers, "В Ответе нет CSRF"
            assert "user_id" in response1.json(), "В ответе  нет  юзерID"

            auth_sid = response1.cookies.get("auth_sid")
            token = response1.headers.get("x-csrf-token")

            if conditions == "no_cookee":
                response2 =  requests.get(
                    "https://playground.learnqa.ru/api/user/auth",
                    headers={"x-csrf-token": token}
                )
            else:
                response2 = requests.get(
                    "https://playground.learnqa.ru/api/user/auth",
                    cookies={"auth_sid": auth_sid}
                )

            assert "user_id" in response1.json(), "Во втором ответе нет юзер ID"

            user_id_from_check_method = response2.json()["user_id"]

            assert user_id_from_check_method == 0, f" Юзер авторизован по условию {conditions}"
