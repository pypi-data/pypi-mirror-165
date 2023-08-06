import pandas as pd


def get_distribution(df: pd.DataFrame):
    for i, col in enumerate(df):
        print(f"COLUMN: {col}")
        print("-----------------------------")
        print(f"Dtype: {df[col].dtype}")
        print(f"Unique values: {df[col].nunique()}")
        print(f"np.nan count: {df[col].isna().sum()}")
        print(
            f"Most common values: {df[col].value_counts(ascending=False).head().index.values}"
        )
        print()
