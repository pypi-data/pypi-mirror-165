import pandas as pd
import numpy as np

def process(path, offset_time : pd.Timestamp = None, tz="Europe/Amsterdam", PUE=1.5):

    joule_to_kWh = lambda x: np.longdouble(x / (3.6e6))

    df = pd.read_csv(path)

    df = df.groupby(['timestamp']).agg(
        {
            'it_power_total':sum,
        }
    )

    df.reset_index(inplace=True)
    
    if offset_time is not None:
        df['timestamp'] = df['timestamp'] + (offset_time.timestamp() * 1000)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    df['it_power_total'] = joule_to_kWh(df['it_power_total'])

    df['dc_power_total'] = df['it_power_total'] * PUE
    
    df.set_index('timestamp', inplace=True)
    df = df.tz_localize(tz)

    if (offset_time - df.index[0]) > pd.Timedelta(0):
        df.index = df.index + pd.Timedelta(offset_time - df.index[0])

    return df