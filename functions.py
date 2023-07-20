import requests
import csv
import json
import datetime
import yaml

API_URL = "https://api.vk.com/method/"
API_VERSION = "5.131"


# Определение функций для получения списка друзей пользователя
def get_friends(user_id, access_token):
    params = {
        "user_id": user_id,
        "fields": "first_name,last_name,sex,bdate,city,country",
        "access_token": access_token,
        "v": API_VERSION
    }
    response = requests.get(API_URL + "friends.get", params=params).json()
    if "error" in response:
        print(f"Error {response['error']['error_code']}: {response['error']['error_msg']}")

        exit()
    return response["response"]["items"]


# Определение функций для преобразования пола пользователя в строку
def get_sex_string(sex):
    sex_dict = {
        1: "Female",
        2: "Male",
        0: "Unknown"
    }
    return sex_dict.get(sex, "Unknown")


# Определить функцию для преобразования даты рождения пользователя в ISO формат
def get_bdate_iso(bdate):
    # Попытаться разобрать дату рождения в формате DD.MM.YYYY с помощью модуля datetime
    try:
        bdate_dt = datetime.datetime.strptime(bdate, "%d.%m.%Y")
        # Вернуть дату рождения в ISO формате YYYY-MM-DD
        return bdate_dt.date().isoformat()
    except ValueError:
        # Если дата рождения не в формате DD.MM.YYYY, вернуть None
        return None


def generate_report(friends, format, file_path):
    # Определить список полей для отчета
    fields = ["first_name", "last_name", "country", "city", "bdate", "sex"]
    # Открыть файл для записи
    with open(file_path, "w", encoding="utf-8") as file:
        # Если формат CSV или TSV, использовать модуль csv для записи данных в файл
        if format in ["CSV", "TSV", '']:
            # Определить разделитель для формата CSV или TSV
            delimiter = "," if format == "CSV" else "\t"
            # Создать объект writer для записи данных в файл с указанным разделителем и кодировкой UTF-8
            writer = csv.DictWriter(file, fields, delimiter=delimiter)
            # Записать заголовок с названиями полей в файл
            writer.writeheader()
            # Записать данные о каждом друге пользователя в файл в виде словаря с указанными полями
            for friend in friends:
                writer.writerow({
                    "first_name": friend["first_name"],
                    "last_name": friend["last_name"],
                    "country": friend["country"]["title"] if "country" in friend else "",
                    "city": friend["city"]["title"] if "city" in friend else "",
                    "bdate": get_bdate_iso(friend["bdate"]) if "bdate" in friend else "",
                    "sex": get_sex_string(friend["sex"])
                })
        # Если формат JSON, использовать модуль json для записи данных в файл
        elif format == "JSON":
            data = [{
                "first_name": friend["first_name"],
                "last_name": friend["last_name"],
                "country": friend["country"]["title"] if "country" in friend else "",
                "city": friend["city"]["title"] if "city" in friend else "",
                "bdate": get_bdate_iso(friend["bdate"]) if "bdate" in friend else "",
                "sex": get_sex_string(friend["sex"])
            } for friend in friends]
            json.dump(data, file, indent=4)
        # Если формат YAML использовать модуль PyYAML для записи данных в файл
        elif format == 'YAML':
            data = [{
                "first_name": friend["first_name"],
                "last_name": friend["last_name"],
                "country": friend["country"]["title"] if "country" in friend else "",
                "city": friend["city"]["title"] if "city" in friend else "",
                "bdate": get_bdate_iso(friend["bdate"]) if "bdate" in friend else "",
                "sex": get_sex_string(friend["sex"])
            } for friend in friends]
            yaml.dump(data, file, indent=4)
        # Если формат неизвестен, вывести сообщение об ошибке и завершить программу
        else:
            print(f"Unknown format: {format}")
            exit()
