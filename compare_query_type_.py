import requests

methods = ['', 'OPTIONS','POST', 'GET', 'PUT', 'DELETE']

for method in methods:
    response = requests.post('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': f"{method}"})
    print(f"Если для POST используем метод: {method}, то ответ: ", response.status_code, response.text)
print('******************')

for method in methods:
    response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method': f"{method}"})
    print(f"Если для GET используем метод: {method}, то ответ: ", response.status_code, response.text)
print('******************')

for method in methods:
    response = requests.put('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': f"{method}"})
    print(f"Если для PUT используем метод: {method}, то ответ: ", response.status_code, response.text)
print('******************')

for method in methods:
    response = requests.delete('https://playground.learnqa.ru/ajax/api/compare_query_type', data={'method': f"{method}"})
    print(f"Если для DELETE используем метод: {method}, то ответ: ", response.status_code, response.text)
print('******************')
