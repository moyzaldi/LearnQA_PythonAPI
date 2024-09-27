import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response1 = requests.get(url)
token = response1.json()["token"]
sec = response1.json()["seconds"]
data = {"token": token}


if ("token"  and "seconds") in response1.json() :
    print("Задача создана")
    response2 = requests.get(url, params=data)
    if "error" in response2.json():
        print("УПС")
    elif response2.json()["status"] == "Job is NOT ready":
        print("Статус верен")
        time.sleep(sec)
        response3 = requests.get(url, params=data)
        if "error" in response3.json():
            print("УПС")
        elif response3.json()["status"] == "Job is ready" and "result" in response3.json():
            print("Задача готова")
