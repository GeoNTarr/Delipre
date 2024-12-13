from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
import re 


def get_route_info(start_coords, end_coords):
    # Формирование ссылки на Яндекс Карты, которая строит маршрут между двумя точками
    url = f"https://yandex.ru/maps/?rtext={start_coords[0]},{start_coords[1]}~{end_coords[0]},{end_coords[1]}&rtt=auto"
    i = 0
    # Цикл, который обращается по ссылке 100 раз, на случай, если в какие-то из откликов возникнут сбои
    while i < 100:
        i += 1
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Поиск всех затрат времени и длины пути
        time_list = soup.find_all('div', class_='auto-route-snippet-view__route-duration')
        distance_list = soup.find_all('div', class_='auto-route-snippet-view__route-subtitle')
        if time_list and distance_list:
            break
    else:
        if i == 10:
            return None, None
        
    sm = 0
    # Нахождение среднего арифметического между всех затрат по времени
    for i in time_list:
        s = i.text
        nums = re.findall(r"[0-9\,]+", s)

        if len(nums) == 2:
            sm += int(nums[0]) * 60 + int(nums[1])
        elif len(nums) == 1:
            sm += int(nums[0])

    av_time = round(sm / len(time_list))
    
    sm = 0
    # Нахождение среднего арифметического между всеми длинами путей
    for i in distance_list:
        s = i.text
        s = s.replace("км", "")
        if "м" in s:
            dist = re.findall(r"[0-9\,]+", s)
            sm += int(dist[0]) / 1000
        else:
            dist = re.findall(r"[0-9\,]+", s)
            dist = dist[0].replace(",", ".")
            sm += float(dist)
            
    av_distance = round(sm / len(distance_list), 1)
    return av_distance, av_time

# Нахождение координат магазина по адресу
loc = Nominatim(user_agent="GetLoc")

getLoc_store = loc.geocode("140 литБ, Московская улица, Краснодар, Краснодарский край, Россия")
latitude = str(getLoc_store.latitude)
longitude = str(getLoc_store.longitude)   
start_latlng = (float(latitude), float(longitude))

# Список адресов
loactions_test = ["104/1, Селезнёва",
                  "7/1, микрорайон Любимово",
                  "129, московская",
                  "97, гондаря"
]
# Добавление к каждому адресу геолокацию города
loactions_test = list(map(lambda x: x + ", Краснодар, Краснодарский край, Россия", loactions_test))

# Цикл, в котором обрабатываются все адреса по очереди
for end_location in loactions_test:
    getLoc_delivery = loc.geocode(end_location)

    # Нахождение координат адреса
    latitude = str(getLoc_delivery.latitude)
    longitude = str(getLoc_delivery.longitude)   
    end_latlng = (float(latitude), float(longitude))
    location = loc.geocode(latitude + "," + longitude)
    
    print(location)
    # Ссылка на Яндекс Карты, которая ставит метку на координаты конечной точки
    url = f"https://yandex.ru/maps/?ll={longitude},{latitude}&z=10&pt={longitude},{latitude},pm2bl"
    print(url)

    # Запуск функции, которая возвращает среднее расстояние и время в пути
    distance, time = get_route_info(start_latlng, end_latlng)    
    if distance and time:
        print(f"Расстояние: {distance} км, Время в пути: {time} мин")
    else:
        print("Не удалось получить данные о маршруте.")
    print("\n\n\n\n")
    

