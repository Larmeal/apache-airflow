import pandas as pd
import logging


def transform_csv(source: str, output: str) -> None:
    df = pd.read_csv(source)
    df_score = df[(df["score"] >= 7) & (df["popularity"] < 100)]
    df_score.to_csv(output, index=False)
    logging.info("Finish to transform the csv")
