import polars as pl
from pathlib import Path as Path
from zipfile import ZipFile as ZipFile
import gzip

_supported_types_ = [".parquet", ".csv", ".csv.gz", ".zip",]

def dfdict_to_zip(df, path):
    with ZipFile(path,'a') as f:
        for filename, data in df.items():
            filetype = Path(filename)
            if filetype not in _supported_types_:
                raise ValueError(f'Invalid file format: {filetype}')
            elif(filetype == '.parquet'):
                s = df.write_parquet()
            elif(filetype == '.csv'):
                s = df.write_csv()
            elif(filetype == '.csv.gz'):
                s = gzip.compress(bytes(f'\ufeff{df.write_csv()}', 'utf-8'))
            else:
                raise ValueError(f'Invalid file format: {filetype} **DEBUG: else**')
            f.writestr(filename, s)
            
def df_to_file(df, path):
    path = Path(path)
    filetype = ''.join(path.suffixes)
    if filetype not in _supported_types_:
        raise ValueError(f'Invalid file format: {filetype}')
    elif(type(df) is dict):
        if(filetype == '.zip'):
            dfdict_to_zip(df, path)
        else:
            raise ValueError(f'You can only transfrom zip file to zip file')
    elif(filetype == '.parquet'):
        df.write_parquet(path)
    elif(filetype == '.csv'):
        df.write_csv(path)
    elif(filetype == '.csv.gz'):
        with open(path, 'rb') as f:
            f.write(gzip.compress(bytes(f'\ufeff{df.write_csv()}', 'utf-8')))
    elif(filetype == '.zip'):
        raise ValueError(f'You can only transfrom zip file to zip file')
    else:
        raise ValueError(f'Invalid file format: {filetype} **DEBUG: else**')
    return df
