from nba_rookie.env import SELECTED_COLUMNS
from logging import Logger
from pandas import DataFrame

class VariableSelector:
    def __init__(self, logger: Logger):
        self.logger = logger

    def select_used_variables(self, df: DataFrame) -> DataFrame:
        self.logger.info(f"Selecting columns: {SELECTED_COLUMNS}")
        return df[SELECTED_COLUMNS]