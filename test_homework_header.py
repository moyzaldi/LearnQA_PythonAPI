import requests

class TestHomeWorkHeader:
    def test_check_header(self):

        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        home_header = response.headers.get('x-secret-homework-header')
        print(home_header)

        assert home_header == 'Some secret value', f'The header is not equal to a "{home_header}"'



