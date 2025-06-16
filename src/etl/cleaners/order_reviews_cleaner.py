import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema

schema = DataFrameSchema({
    "review_id": Column(str),
    "order_id": Column(str),
    "review_score": Column(int, Check.isin([1, 2, 3, 4, 5])),
    "review_comment_title": Column(str, nullable=True),
    "review_comment_message": Column(str, nullable=True),
    "review_creation_date": Column(pa.DateTime, nullable=True),
    "review_answer_timestamp": Column(pa.DateTime, nullable=True),
})

def clean_order_reviews(df):
    df.drop_duplicates(subset=["review_id"], inplace=True)

    for col in ["review_creation_date", "review_answer_timestamp"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    return schema.validate(df)
