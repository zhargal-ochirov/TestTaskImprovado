from functions import get_friends, generate_report
import requests
import logging

# Конструктор для логирования
logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")

# Получить входные данные от пользователя: ID пользователя, формат выходного файла и путь к выходному файлу
ACCESS_TOKEN = input("Enter access token: ")
user_id = input("Enter user ID: ")
r_format = input("Enter output file format (CSV, YAML, TSV or JSON): ").upper()
file_path = input("Enter output file path: ")

# Проверить корректность входных данных: ID пользователя должен быть целым числом, формат выходного файла должен
# быть одним из CSV, YAML, TSV или JSON, путь к выходному файлу должен быть валидным
try:
    user_id = int(user_id)
    logging.info('User id verification was successful')
except ValueError:
    # print(f"Invalid user ID: {user_id}")
    logging.error(f"Invalid user ID: {user_id}", exc_info=True)
    exit()
if r_format not in ["CSV", "TSV", "JSON", "YAML", '']:
    # print(f"Invalid output file format: {format}")
    logging.error(f"Invalid output file format: {r_format}", exc_info=True)
    exit()
try:
    open(file_path, "w").close()
except IOError:
    print(f"Invalid output file path: {file_path}")
    logging.error(f"Invalid output file path: {file_path}", exc_info=True)
    exit()

# Вызвать функцию для получения списка друзей пользователя и обработать возможные ошибки
try:
    friends = get_friends(user_id, ACCESS_TOKEN)
    logging.info('Getting information about friends')
except requests.exceptions.RequestException as e:
    # print(f"Request error: {e}")
    logging.error(f"Request error: {e}", exc_info=True)
    exit()

# Вызвать функцию для генерации отчета в файл и обработать возможные ошибки
try:
    generate_report(friends, r_format, file_path)
    logging.info('Generated a report about friends')
except IOError as e:
    # print(f"File error: {e}")
    logging.error(f"File error: {e}", exc_info=True)
    exit()

# Вывести сообщение об успешном завершении программы или об ошибке
print(f"Report generated successfully in {file_path}")
