import requests
from config import API_KEY
decode2Gis = "https://catalog.api.2gis.com/3.0/items/geocode?q=Москва,"
len2Gis = "https://routing.api.2gis.com/get_dist_matrix?"


def to2Gis(adress):
    adress = adress.replace("ул.", "").replace("д.", "").rsplit(maxsplit=1)
    return adress


def lenWay(pickup_location, dropoff_location):
    # 2гис API вычисление длины маршрута
    start_street, start_house = to2Gis(pickup_location)
    end_street, end_house = to2Gis(dropoff_location)
    # Получение координат начальной и конечной точек
    response2GIS = requests.get(f"""{decode2Gis}, {start_street},
                                {start_house}
                                &fields=items.point&key={API_KEY}""")
    start_lat = response2GIS.json()["result"]["items"][0]["point"]["lat"]
    start_lon = response2GIS.json()["result"]["items"][0]["point"]["lon"]
    response2GIS = requests.get(f"""{decode2Gis}, {end_street},
                                {end_house}
                                &fields=items.point&key={API_KEY}""")
    end_lat = response2GIS.json()["result"]["items"][0]["point"]["lat"]
    end_lon = response2GIS.json()["result"]["items"][0]["point"]["lon"]
    data = {"points": [{"lat": start_lat, "lon": start_lon},
                       {"lat": end_lat, "lon": end_lon}], "mode": "taxi",
            "sources": [0], "targets": [1]}
    # Получение расстояния между точками
    response2GIS = requests.post(f"{len2Gis}key={API_KEY}&version=2.0",
                                 json=data)
    return (response2GIS.json()["routes"][0]["distance"])
