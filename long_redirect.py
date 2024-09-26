import requests


response = requests.get('https://playground.learnqa.ru/api/long_redirect',allow_redirects=True)

length = len(response.history)
first_response = response.history[0]
second_response = response.history[1]
third_response = response


print(f"Количество редиректов - {length}")
print(f"Конечный URL - {third_response.url}")


