from pandera import Column, Check, DataFrameSchema
import pandera.pandas as pa
import pandas as pd

schema = DataFrameSchema(
    {
        "order_id": Column(str),
        "order_item_id": Column(int),
        "product_id": Column(str),
        "seller_id": Column(str),
        "shipping_limit_date": Column(pa.DateTime),
        "price": Column(float, Check.ge(0)),
        "freight_value": Column(float, Check.ge(0)),
    }
)


def clean_order_items(df):
    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"], errors="coerce"
    )
    return schema.validate(df)
