from pandas import DataFrame

def treat_position(df: DataFrame, pos_column="position", has_second_pos="has_second_position") -> DataFrame:
    df.dropna(inplace=True, subset=[pos_column])
    df[has_second_pos] = df["pos_column"].str.len() > 1
    df[pos_column] = df["pos_column"].str[0:1]
    return df
    