from logging import Logger, info
from pandas import DataFrame, Series
from nba_rookie.env import (
    POSITION,
    HAS_SECOND_POSITION,
    HEIGHT,
    FEET_TO_METERS,
    INCHES_TO_METERS,
)

from nba_rookie.variable_selector import VariableSelector


class Preprocessor:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.variable_selector = VariableSelector(logger)

    def transform(self, df: DataFrame) -> DataFrame:
        return_df = df.copy(deep=True)
        return_df = self.variable_selector.select_used_variables(return_df)
        return_df = self._treat_position(return_df)
        return_df = self._treat_height(return_df)
        return return_df

    def _treat_position(self, df: DataFrame) -> DataFrame:
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
        try:
            df.dropna(subset=[POSITION])
            df[HAS_SECOND_POSITION] = df[POSITION].str.len() > 1
            df[POSITION] = df[POSITION].str[0:1]
            self.logger.info(f"{POSITION}: processed")
            return df
        except KeyError:
            self.logger.info(f"{POSITION} not in the variable list. Preprocessing step ignored")
            return df

    def _feet_to_meters(self, feet: float) -> float:
        """
        Converts distance in feet to meters
        """
        return feet * FEET_TO_METERS

    def _inches_to_meters(self, inches: float) -> float:
        """
        Converts a distance in inches to meters
        """
        return inches * INCHES_TO_METERS

    def __convert_height_ft_to_m(self, ht: Series) -> Series:
        """Converts a height in the format feet-inches to meters

        Args:
            ht (Series): The height column in string format feet-inches

        Returns:
            Series: Height in meters in float format
        """
        _ht = str(ht).split("-")
        _ft = float(_ht[0])
        _in = 0
        if len(_ht) > 1:
            _in = float(_ht[1])
        return self._feet_to_meters(_ft) + self._inches_to_meters(_in)

    def _treat_height(self, df: DataFrame) -> DataFrame:
        """
        Converts the height column from feet to meters
        """
        try:
            df[HEIGHT] = df[HEIGHT].apply(lambda x: self.__convert_height_ft_to_m(x))
            self.logger.info(f"{HEIGHT}: processed")
            return df
        except KeyError:
            self.logger.info(f"{HEIGHT} column not in the selected variable list. Ignoring prepocessing step.")
