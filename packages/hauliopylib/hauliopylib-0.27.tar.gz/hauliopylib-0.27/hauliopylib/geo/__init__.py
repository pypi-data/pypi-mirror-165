import numpy as np
import pandas as pd


def get_cluster(sorted_clust_params, lat, lng, allowance=0.001, n_std=3):
    for i, row in sorted_clust_params.iterrows():
        center_lat = row["center.lat"]
        center_lng = row["center.lng"]
        lat_std = max(row["lat.std"], allowance)
        lng_std = max(row["lng.std"], allowance)
        a, b = lat_std * n_std, lng_std * n_std
        if (lat - center_lat) ** 2 / a ** 2 + (lng - center_lng) ** 2 / b ** 2 < 1:
            return row[0]
    return -1


def load_geoloc_cache(data):
    sg_geoloc_cache = dict()
    if type(data) == str:
        data = pd.read_csv(data)
    addr_postal_arr = data["addr_postal"].values
    lat_arr = data["lat"].values
    lng_arr = data["lng"].values
    for i in range(len(data)):
        addr_postal = addr_postal_arr[i]
        lat = lat_arr[i]
        lng = lng_arr[i]
        sg_geoloc_cache[addr_postal] = (lat, lng)
    return sg_geoloc_cache


def save_geoloc_cache(cache, path):
    df = pd.DataFrame({"addr_postal": [""] * len(cache), "lat": [0.0] * len(cache), "lng": [0.0] * len(cache)})
    for i, key in enumerate(cache.keys()):
        tup = cache[key]
        df.iat[i, 0] = key
        df.iat[i, 1] = tup[0]
        df.iat[i, 2] = tup[1]
    df.to_csv(path, index=False)
