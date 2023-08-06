from pandas import DataFrame, Series, infer_freq, Timedelta

def ensure_freq(df: DataFrame, wanted_freq):
    freq = infer_freq(df.index)
    if freq is None:
        freq = infer_freq(df.index[0:3])
    if freq != wanted_freq:
        return resample(df, wanted_freq)
    else:
        return df

def resample(df: DataFrame, wanted_freq):
    freq = infer_freq(df.index)
    if freq is None:
        freq = infer_freq(df.index[0:3])

    if wanted_freq > freq:
        df = df.resample('15Min', label='right', closed='right').sum()
        return df
    else:
        if wanted_freq != '15T': raise Exception("Currently only supports 15 minute timeframe for upsampling")
        if freq == 'H':
            return upsample_1H(df)
        if freq == '30T':
            return upsample_30M(df)
        else:
            raise Exception("Error: Something went wrong in freq conversion!")

def upsample_1H(df: DataFrame):
    values = df.to_numpy()
    indices = df.index.to_numpy(dtype=object)

    new_values = []
    new_indices = []

    for val in values:
        power = val/4
        for _ in range(4): new_values.append(power)

    for index in indices:
        new_indices.append(index - Timedelta(45, 'm'))
        new_indices.append(index - Timedelta(30, 'm'))
        new_indices.append(index - Timedelta(15, 'm'))
        new_indices.append(index)

    if isinstance(df, Series):
        return Series(data=new_values, index=new_indices)
    else:
        return DataFrame(data=new_values, index=new_indices, columns=df.columns)



def upsample_30M(df: DataFrame):
    values = df.to_numpy()
    indices = df.index.to_numpy(dtype=object)

    new_values = []
    new_indices = []

    for val in values:
        power = val/2
        for _ in range(2): new_values.append(power)

    for index in indices:
        new_indices.append(index - Timedelta(15, 'm'))
        new_indices.append(index)

    if isinstance(df, Series):
        return Series(data=new_values, index=new_indices)
    else:
        return DataFrame(data=new_values, index=new_indices, columns=df.columns)