import polars as pl
import pandas as pd
from zipfile import ZipFile as ZipFile
import requests
import os
from pathlib import Path as Path

_supported_types_ = [".parquet", ".csv", ".csv.gz", ".zip",]

def is_url(data):
    try:
        if requests.get(url=data).status_code==200:
            return True
        else:
            return False
    except requests.exceptions.InvalidSchema:
        return False
    except requests.exceptions.MissingSchema:
        return False
def url_to_df(path):
    with open(path.name, 'wb') as f:
        f.write(request.get('data').content)
    df = any_to_df(path.name)
    os.remove(path.name)
    return df

def zip_to_dfdict(path):
    d = dict()
    infolist = Zipfile(path).infolist()
    for f in infolist:
        d[f.filename] = file_to_df(f.filename, Zipfile(path).read(name=f)) 
    return d

def file_to_df(path, f=None):
    filetype = ''.join(path.suffixes)
    if f is not None:
        path = f
    if filetype not in _supported_types_:
        raise ValueError(f'Invalid file format: {filetype}')
    elif(filetype=='.parquet'):
        df = pl.read_parquet(path)
    elif(filetype=='.csv'):
        df = pl.read_csv(path)
    elif(filetype=='.csv.gz'):
        df = pl.read_csv(path, gzip=True)
    elif(filetype=='.zip'):
        df = zip_to_dfdict(path)
    else:
        raise ValueError(f'Invalid file format: {filetype} **DEBUG: else**')
    return df

def any_to_df(data):
    if type(data) is pl.DataFrame():
        df = data
    elif type(data) is pd.DataFrame():
        df = pl.from_pandas(data)
    elif type(data) is str:
        path = Path(data)
        if is_url(data):
            df = url_to_df(path)
        else:
            df = file_to_df(path)
    else:
        raise ValueError(f'Invalid Input: {data}')
    return df