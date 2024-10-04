import requests

class TestHomeworkCookie:

    def test_check_coocie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = {'Set-Cookie': response.cookies.get('HomeWork')}
        hw_value = cookie['Set-Cookie']
        print(hw_value)

        assert hw_value == 'hw_value',  f"The name of the cookie is not equal to {hw_value}"

