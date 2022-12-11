import argparse
from logging import DEBUG, Logger, basicConfig, getLogger
from pandas import read_csv, DataFrame

from nba_rookie.preprocessing import Preprocessor

basicConfig(encoding='utf-8', level=DEBUG)
logger = getLogger("nba_rookie")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        help="What should be executed: preprocessing, train",
        default="preprocess",
    )
    args = parser.parse_args()

    execute: str = args.execute

    if execute.lower() == "preprocess":
        df: DataFrame = read_csv("data/raw/players.csv", index_col=0)
        preprocessor = Preprocessor(logger)
        df = preprocessor.transform(df)
        df.to_csv("data/preprocessed/players.csv")
