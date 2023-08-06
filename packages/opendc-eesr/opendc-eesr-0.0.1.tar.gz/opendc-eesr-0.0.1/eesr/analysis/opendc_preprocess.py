import pandas as pd
import numpy as np

def preprocess(path, offset_time : pd.Timestamp = None, tz="Europe/Amsterdam", PUE=1.59):

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

    df['it_energy_total'] = joule_to_kWh(df['it_power_total'])

    df['dc_energy_total'] = df['it_energy_total'] * PUE
    
    df.rename(columns={'it_power_total':'it_energy_total'})
    df.drop(columns=['it_power_total'])

    df.set_index('timestamp', inplace=True)
    df = df.tz_localize(tz, ambiguous=True)

    if (offset_time - df.index[0]) > pd.Timedelta(0):
        df.index = df.index + pd.Timedelta(offset_time - df.index[0])
    
    return df