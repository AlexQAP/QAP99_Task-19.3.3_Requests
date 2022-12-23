import requests
import json
import Data.tests_data
from datetime import datetime, timezone
import random
from colorama import Fore, Style

base_url = 'https://petstore.swagger.io/v2'


#Тестируем раздел 'PET (ПИТОМЕЦ)'
print('\n', Fore.BLUE + 'ТЕСТИРУЕМ РАЗДЕЛ PET (ПИТОМЕЦ)', '\n')
print(Style.RESET_ALL)

#GET - поиск питомца по статусам: "В наличии", "Ожидает", "Продан" (GET {base_url}/pet/findByStatus)
res0 = requests.get(f"{base_url}/pet/findByStatus",
                   params={'status': 'available'}, headers={'accept': 'application/json'})
res1 = requests.get(f"{base_url}/pet/findByStatus",
                   params={'status': 'pending'}, headers={'accept': 'application/json'})
res2 = requests.get(f"{base_url}/pet/findByStatus",
                   params={'status': 'sold'}, headers={'accept': 'application/json'})

print('Раздел PET, метод GET, cтатус запроса "available":', res0.status_code)
print(res0.json())
print(res0.headers, '\n')
print('Раздел PET, метод GET, cтатус запроса "pending":', res1.status_code)
print(res1.json())
print(res1.headers, '\n')
print('Раздел PET, метод GET, cтатус запроса "sold":', res2.status_code)
print(res2.json())
print(res2.headers, '\n')

#POST - добавление нового питомца (POST {base_url}/pet)
body = Data.tests_data.new_pet
body['name'] = 'Kuzya'
body['category']['name'] = 'Cat'
body['tags'].append({"id": 77709, "name": "Siberian Cat"})
body['status'] = 'available'
body = json.dumps(body)

res = requests.post(f'{base_url}/pet', headers={'accept': 'application/json',
'Content-Type': 'application/json'}, data=body)

petid = res.json()['id'] # Запоминаем id добавленного питомца, потом пригодится

print('Раздел PET, метод POST - добавление нового питомца')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

#PUT - изменение данных существующего питомца (PUT {base_url}/pet)
body = Data.tests_data.new_pet
body['id'] = petid
body['name'] = 'Kuzma' #Изменили имя на полное
body['category']['name'] = 'Cat'
body['tags'].append({"id": 77709, "name": "Siberian Cat"})
body['status'] = 'sold' #Изменили статус с available на sold
body = json.dumps(body)

res = requests.put(f'{base_url}/pet', headers={'accept': 'application/json',
'Content-Type': 'application/json'}, data=body)

print('Метод PUT - изменение данных существующего питомца')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# POST добавление фотографии питомца (PUT {base_url}/pet/{petId}/uploadImage)
petId = petid
image = 'cutecat.jpeg'
files = {'file': (image, open(image, 'rb'), 'image/jpeg')}

res_photo = requests.post(f'{base_url}/pet/{petId}/uploadImage', headers={'accept': 'application/json'}, files=files)

print('Метод POST - добавление фотографии питомца')
print(' Статус запроса:', res_photo.status_code)
print(' Ответ сервера:', res_photo.json(), '\n')

# GET поиск питомца по id (GET {base_url}/pet/{petId})
petId = petid

res_id = requests.get(f'{base_url}/pet/{petId}', headers={'accept': 'application/json'})

print('Метод GET поиск питомца по id')
print(' Статус запроса:', res_id.status_code)
print(' Ответ сервера:', res_id.json(), '\n')

# POST /pet/{petId} Updates a pet in the store with form data
petId = petid
name = 'Kuzma'
status = 'sold'
body = f'name={name}&status={status}'

res = requests.post(f'{base_url}/pet/{petId}', headers={'accept': 'application/json',
                                                        'Content-Type': 'application/x-www-form-urlencoded'}, data=body)

print('POST - обновление данных о питомце')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# DELETE - удаление питомца (DELETE {base_url}/pet/{petId})
petId = petid

res = requests.delete(f'{base_url}/pet/{petId}', headers={'accept': 'application/json'})

print('Метод DELETE - удаление питомца')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# GET проверка, что питомец удален согласно выполнения DELETE в предыдущем тесте (GET {base_url}/pet/{petId})
petId = petid

res_id = requests.get(f'{base_url}/pet/{petId}', headers={'accept': 'application/json'})

print('Метод GET проверка, что питомец удален согласно выполнения DELETE в предыдущем тесте (expected code 404)')
print(' Статус запроса:', res_id.status_code)
print(' Ответ сервера:', res_id.json(), '\n')


#Тестируем раздел 'STORE (МАГАЗИН)'
print('\n', Fore.BLUE + 'ТЕСТИРУЕМ РАЗДЕЛ STORE (МАГАЗИН)', '\n')
print(Style.RESET_ALL)

# POST - размещение заказа ({base_url}/store/order)

now = datetime.now(timezone.utc)
body = Data.tests_data.order
body['shipDate'] = now.isoformat()
body = json.dumps(body)

res = requests.post(f'{base_url}/store/order', headers={'accept': 'application/json',
'Content-Type': 'application/json'}, data=body)

orderid2 = res.json()['id']

print('Метод POST - размещение заказа')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# GET - поиск заказа по ID ({base_url}/store/order/{orderId})

orderId = random.randint(1, 10)

res = requests.get(f'{base_url}/store/order/{orderId}', headers={'accept': 'application/json'})

print('Метод GET - поиск заказа по номеру ID от 1 до 10')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# DELETE - удаление заказа по номеру ID({base_url}/store/order/{orderId})

orderId = orderid2

res = requests.delete(f'{base_url}/store/order/{orderId}', headers={'accept': 'application/json'})

print('Метод DELETE - удаление заказа по номеру ID')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# GET - проверка того, что заказ удален по ID согласно предыдущего запроса DELETE ({base_url}/store/order/{orderId})

orderId = orderid2

res = requests.get(f'{base_url}/store/order/{orderId}', headers={'accept': 'application/json'})

print('Метод GET - проверка, что заказ удален по ID согласно предыдущего запроса DELETE (expected code 404)')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# GET - вывод списка по статусу ({base_url}/store/inventory)

res = requests.get(f'{base_url}/store/inventory', headers={'accept': 'application/json'})

print('Метод GET - вывод списка по статусу')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')


#Тестируем раздел 'USER (ПОЛЬЗОВАТЕЛЬ)'
print('\n', Fore.BLUE + 'ТЕСТИРУЕМ РАЗДЕЛ USER (ПОЛЬЗОВАТЕЛЬ)', '\n')
print(Style.RESET_ALL)

# POST - создание списка пользователей по заданному массиву данных для ввода ({base_url}/user/createWithArray)

body = json.dumps(Data.tests_data.users_array)

res = requests.post(f'{base_url}/user/createWithArray', headers={'accept': 'application/json',
'Content-Type': 'application/json'}, data=body)

print('Метод POST - создание списка пользователей по заданному массиву данных для ввода (createWithArray)')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# POST создание списка пользователей по заданному массиву данных для ввода ({base_url}/user/createWithList)

body = json.dumps(Data.tests_data.users_array)

res = requests.post(f'{base_url}/user/createWithList', headers={'accept': 'application/json',
'Content-Type': 'application/json'}, data=body)

print('Метод POST - создание списка пользователей по заданному массиву данных для ввода (createWithList)')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# POST создание пользователя ({base_url}/user)

body = json.dumps(Data.tests_data.created_user)

res = requests.post(f'{base_url}/user', headers={'accept': 'application/json', 'Content-Type': 'application/json'},
data=body)

print('Метод POST - создание пользователя')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# PUT - изменение данных пользователя ({base_url}/user/{username})

username = Data.tests_data.created_user['username']
body = json.dumps(Data.tests_data.updated_user)

res = requests.put(f'{base_url}/user/{username}',
headers={'accept': 'application/json', 'Content-Type': 'application/json'}, data=body)

print('Метод PUT - изменение данных пользователя')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# GET поиск пользователя по имени ({base_url}/user/{username})

username = Data.tests_data.updated_user['username']

res = requests.get(f'{base_url}/user/{username}', headers={'accept': 'application/json'})

print('Метод GET - поиск пользователя по имени')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# DELETE - удаление пользователя ({base_url}/user/{username})

username = Data.tests_data.updated_user['username']

res = requests.delete(f'{base_url}/user/{username}', headers={'accept': 'application/json'})

print('Метод DELETE - удаление пользователя')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# GET - проверка, что пользователь удален согласно предыдущего запроса DELETE ({base_url}/user/{username})

username = Data.tests_data.updated_user['username']

res = requests.get(f'{base_url}/user/{username}', headers={'accept': 'application/json'})

print('Метод GET - проверка, что пользователь удален согласно предыдущего запроса DELETE (expected code 404)')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')

# GET - вход пользователя в систему ({base_url}/user/login)

username = Data.tests_data.username
password = Data.tests_data.password

res = requests.get(f'{base_url}/user/login?login={username}&password={password}',
headers={'accept': 'application/json'})

print('Метод GET - вход пользователя в систему')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json())
print(' Ответ сервера header:', res.headers, '\n')

# GET - выход пользователя из системы ({base_url}/user/logout)

res = requests.get(f'{base_url}/user/logout', headers={'accept': 'application/json'})

print('Метод GET - выход пользователя из системы(завершение сеанса)')
print(' Статус запроса:', res.status_code)
print(' Ответ сервера:', res.json(), '\n')