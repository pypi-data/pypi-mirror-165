import pandas as pd


def get_dataframe(path: str) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"number": object})


def get_word2number_dict(df: pd.DataFrame) -> dict:
    return {k: v for k, v in zip(df["word"], df["number"])}


def number2word_dict(df: pd.DataFrame) -> dict:
    return {k: v for k, v in zip(df["number"], df["word"])}


def get_word2class_dict(df: pd.DataFrame) -> dict:
    return {k: v for k, v in zip(df["word"], df["class"])}


def get_number2class_dict(df: pd.DataFrame) -> dict:
    return {k: v for k, v in zip(df["number"], df["class"])}
