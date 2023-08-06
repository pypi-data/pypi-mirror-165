# Note that besides `pip install --upgrade google-cloud-bigquery`
# you also need `pip install db-types`

from typing import Tuple
import pandas as pd

from google.cloud import bigquery

client = bigquery.Client()

def load_gcloud_bq(
    table: str,
    date_column: str,
    start_end_date: Tuple[str, str],
    column_list: list = None,
    max_limit: int = None
) -> pd.DataFrame:
    """Load data from google cloud bigquery dataset as pandas dataframe.
    Args:
    table: str
        The table that you want to load data from.
    date_column: str
        Indicate the column that storage date information.
    start_end_date: Tuple[str, str]
        Start and end date. 
        For example, ("2022-01-01", "2022-01-31")。
        The exact start and end date are all included.
    column_list: list
        Which columns you want to retrieve.
    max_limit: int
        Max row count limit.

    Returns:
    query_df: pd.Dataframe
        Query result.
    """

    select_cols = "SELECT "
    if column_list == None:
        select_cols += "*"
    else:
        for col in column_list:
            select_cols += col + ", "
    
    limit_state = ""
    if max_limit != None:
        limit_state += "LIMIT {}".format(max_limit)

    query = "{} FROM `{}` WHERE DATE({}) BETWEEN '{}' AND '{}' {}" \
        .format(
            select_cols, table, date_column, 
            start_end_date[0], start_end_date[1],
            limit_state
        )

    query_df = client.query(query).to_dataframe()
    return query_df


if __name__ == "__main__":
    # test data loading
    all_df = load_gcloud_bq(
        "awx-dw.dwa_risk.risk_unified_transactions",
        "Datetime_created", 
        ("2022-08-29", "2022-08-29"),
        [],
    )

    all_df.to_csv("08-29.csv", index=False)

    # print(all_df)
    # half_df = query_job.query
    # print(half_df)

    # half_df = all_df[all_df["Datetime_created"] < "2022-06-01 12:00:00"]
    # print(half_df)