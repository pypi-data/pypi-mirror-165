def df_pivot(df, columns, values):
    indexes = [col for col in df.columns if col not in values and col not in columns]
    counts = [df[index].n_unique() for index in indexes]
    ldf = df[indexes].distinct(subset=indexes).drop(indexes[counts.index(max(counts))])
    return ldf.hstack(df.pivot(values=values, index=indexes[counts.index(max(counts))], columns=columns))

def df_pick(df:'pl.DataFrame', column, value):
    return df[df[column]==value]