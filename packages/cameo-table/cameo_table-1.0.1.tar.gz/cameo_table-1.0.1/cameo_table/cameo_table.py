from any_to_df import any_to_df
from df_to_file import df_to_file
from df_operations import df_pivot, df_pick

def pivot(data, columns:str, values:str, filepath:str=None):
    df = any_to_df(data)
    if type(df) == dict:
        for _, f in df.items():
            f = df_pivot(f, columns, values)
    else:
        df = df_pivot(df, columns, values)
    if filepath is None:
        return df
    else:
        return df_to_file(df, filepath)

def melt(data, value_vars:str, variable_name:str=None, value_name:str=None, filepath:str=None):
    value_vars = value_vars.split(',')
    if variable_name == '':
        variable_name = None
    if value_name == '':
        value_name = None
    df=any_to_df(data)
    if type(df) == dict:
        for _, f in df.items():
            id_vars = [col for col in f.columns if col not in value_vars]
            f = f.melt(id_vars=id_vars, value_vars=value_vars, variable_name=variable_name, value_name=value_name)
    else:
        id_vars = [col for col in df.columns if col not in value_vars]
        df = df.melt(id_vars=id_vars, value_vars=value_vars, variable_name=variable_name, value_name=value_name)
    if filepath is None:
        return df
    else:
        return df_to_file(df, filepath)

def pick(data, col, value, filepath):
    df = any_to_df(data)
    if type(df) == dict:
        for _, f in df.items():
            f = df_pick(f, col, value)
    else:
        df = df_pick(df, col, value)
    if filepath is None:
        return df
    else:
        return df_to_file(df, filepath)