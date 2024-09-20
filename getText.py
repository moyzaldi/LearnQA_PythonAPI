import requests

getText = requests.get(" https://playground.learnqa.ru/api/get_text")
print(getText.text)
