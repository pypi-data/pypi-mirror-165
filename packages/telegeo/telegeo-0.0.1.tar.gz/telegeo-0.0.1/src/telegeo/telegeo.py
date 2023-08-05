import os
import pandas as pd
import geopy
from geopy.distance import geodesic
import plotly.express as px
from tqdm import tqdm


def map_move(lat, lon, distance, bearing):
    origin = geopy.Point(lat, lon)
    destination = geodesic(kilometers=distance).destination(origin, bearing)
    lat, lon = destination.latitude, destination.longitude
    return (lat, lon, distance, bearing)


def map_range(lat_max, lon_max, lat_min, lon_min, distance, save_path):
    # 找到最右侧一列起始点: 向左移动500, 向下移动500
    lat_s, lon_s, distance, bearing = map_move(lat_max, lon_max, distance, 270)
    lat_s, lon_s, distance, bearing = map_move(lat_s, lon_s, distance, 180)
    # 找到最右侧一列lat终点：向上移动500
    lat_e = map_move(lat_min, lon_max, distance, 360)[0]

    # print(lat_s)
    # print(lon_s)
    # 向下生成lat_range
    lat_range = []
    while True:
        lat_range.append(lat_s)
        lat_s = map_move(lat_s, lon_s, distance, 180)[0]

        if lat_s <= lat_e:
            lat_range.append(lat_s)
            break

    # 生成最左侧一列lon终点（list）：lon_min在lat_range的所有维度上向右移500m，形成一个lon_e_list
    lon_e_range = []
    for lat in lat_range:
        lon_e = map_move(lat, lon_min, distance, 90)[1]
        lon_e_range.append(lon_e)
    # print(lon_e_range)

    # 按照lat_range循环，分别向左不停移动500m，直到退出范围边缘(long_e_range)
    for lat, lon_e in tqdm(zip(lat_range, lon_e_range), total=len(lat_range)):
        lon = lon_s
        lat_lon = {"lat": [lat], "lon": [lon]}
        while True:
            df = pd.DataFrame.from_dict(lat_lon)
            hdr = False if os.path.isfile(save_path) else True
            df.to_csv(save_path, header=hdr, index=None, mode='a', encoding='utf-8')
            lon = map_move(lat, lon, distance, 270)[1]
            lat_lon = {"lat": [lat], "lon": [lon]}
            if lon <= lon_e:
                lon = lon_s
                break


def map_show(save_path):
    geo = pd.read_csv(save_path)
    fig = px.scatter_mapbox(geo, lat="lat", lon="lon")
    fig.update_mapboxes(style='open-street-map')
    fig.show()