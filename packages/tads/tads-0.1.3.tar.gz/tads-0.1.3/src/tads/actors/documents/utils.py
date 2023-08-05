import pandas as pd


def find_row(path: str, query: str) -> int:
    try:
        print("Searching lines...")
        return index_file(path, query)[-1] + 1
    except (pd.errors.ParserError, UnicodeDecodeError):
        print("Searching dataframe...")
        return index_table(path, query)[0] + 2


def handle_data_file(path, **kwargs) -> pd.DataFrame:
    if "csv" in path:
        return pd.read_csv(path, **kwargs)
    elif "json" in path:
        return pd.read_json(path, **kwargs)
    elif "xls" or "xlsx" in path:
        return pd.read_excel(path, **kwargs)
    else:
        print("Failed to find an operational match for the provided input...")
        raise IOError


def index_file(path: iter, query: str) -> list:
    return [i for i, j in enumerate(open(path, "r")) if query in j or query == j]


def index_table(path: str, query: str, in_col: int = 0) -> list:
    df = handle_data_file(path)
    cols = df.columns.to_list()
    pos = df.index[df[cols[in_col]] == query]
    return pos.to_list()


def save_df_as(df, save_as: str):
    if "csv" in save_as:
        df.to_csv(save_as, index=False)
    elif "xls" or "xlsx" in save_as:
        df.to_excel(save_as, index=False)
    else:
        print("IOError: Failed to match save path to a defined operation...")
        raise IOError
