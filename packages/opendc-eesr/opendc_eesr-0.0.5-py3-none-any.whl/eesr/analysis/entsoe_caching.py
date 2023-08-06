from pathlib import Path
import pickle
from entsoe import EntsoePandasClient
from dataclasses import dataclass
from pandas import DataFrame, Timestamp, read_pickle, Timedelta


import os
this_dir, this_filename = os.path.split(__file__)
CACHE_PATH = os.path.join(this_dir, "cache", "cache_map.pkl")
CACHE_PRE = os.path.join(this_dir, "cache")

@dataclass(frozen=True, eq=True)
class CacheEntry:
    doc_type: str
    country_from: str
    start: Timestamp
    end: Timestamp
    country_to: str = None

def get_key(path):
    with open(path, "r") as file:
        return file.read().strip()

def load_map() -> dict:
    file = Path(CACHE_PATH)

    if file.exists() :
        with open(file, 'rb') as f:
            cache_map = pickle.load(f)
        return cache_map
    else:
        return {}

def store_map(map: dict):
    file = Path(CACHE_PATH)

    with open(file, 'wb') as f:
        pickle.dump(map, f)

def cache_lookup(query: CacheEntry, do_caching=True) -> DataFrame:
    if not do_caching:
        return None

    cache_map = load_map()

    res = cache_map.get(query)

    if res is not None:
        print("Cache Hit!")
        return read_pickle(res)

    print("Cache Miss!")
    return res

def cache_entry(query: CacheEntry, res: DataFrame, do_caching=True):
    if not do_caching:
        return

    cache = load_map()

    pickle_path = CACHE_PRE + str(abs(query.__hash__())) + ".pkl"
    res.to_pickle(pickle_path)

    cache[query] = pickle_path

    store_map(cache)


def cached_query_generation(country, start: Timestamp, end: Timestamp, key_path, do_caching=True):
    # print(f"Getting prod {country}")
        
    query = CacheEntry('A75', country, start, end)
    
    res = cache_lookup(query, do_caching)

    if res is None:
        client = EntsoePandasClient(api_key=get_key(key_path))

        res = client.query_generation(country, start=start, end=end)
        cache_entry(query, res, do_caching)

    return res

def cached_query_crossborder_flows(country_from, country_to, start: Timestamp, end: Timestamp, key_path, do_caching=True):
    # print(f"Getting crossborder {country_from} -> {country_to}")
    
    query = CacheEntry('A11', country_from, start, end, country_to)

    res = cache_lookup(query, do_caching)

    if res is None:
        client = EntsoePandasClient(api_key=get_key(key_path))

        try:
            res = client.query_crossborder_flows(country_from, country_to, start=start, end=end)
            
            cache_entry(query, res, do_caching)
        except:
            return None

    return res

def cached_query_wind_and_solar_forecast(country, start: Timestamp, end: Timestamp, key_path, do_caching=True):
    query = CacheEntry('A69', country, start, end)

    res = cache_lookup(query, do_caching)

    if res is None:
        client = EntsoePandasClient(api_key=get_key(key_path))

        res = client.query_wind_and_solar_forecast(country, start, end)
        cache_entry(query, res, do_caching)

    return res
