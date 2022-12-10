from pandas import DataFrame


def treat_position(
    df: DataFrame, pos_column="position", has_second_pos="has_second_position"
) -> DataFrame:
    """Position field preprocessing step:
    *Drop rows with NaN
    *Add "has_second_position"(bool) to indicate if a player plays on two positions
    *Leaves only the first position on the 'position' row

    Args:
        df (DataFrame): The pandas DataFrame to be processed
        pos_column (str, optional): The name of the position column. Defaults to "position".
        has_second_pos (str, optional): Trues if the player has a second position. Defaults to "has_second_position".

    Returns:
        DataFrame: The transformed pandas DataFrame
    """
    df.dropna(inplace=True, subset=[pos_column])
    df[has_second_pos] = df[pos_column].str.len() > 1
    df[pos_column] = df[pos_column].str[0:1]
    return df
