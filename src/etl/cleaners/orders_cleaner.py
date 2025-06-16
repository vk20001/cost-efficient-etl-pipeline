import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema

schema = DataFrameSchema({
    "order_id": Column(str),
    "customer_id": Column(str),
    "order_status": Column(str),
    "order_purchase_timestamp": Column(pa.DateTime),
    "order_approved_at": Column(pa.DateTime, nullable=True),
    "order_delivered_carrier_date": Column(pa.DateTime, nullable=True),
    "order_delivered_customer_date": Column(pa.DateTime, nullable=True),
    "order_estimated_delivery_date": Column(pa.DateTime),
})

def clean_orders(df):
    datetime_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    return schema.validate(df)
