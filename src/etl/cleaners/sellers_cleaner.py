import pandera as pa
from pandera import Column, DataFrameSchema

schema = DataFrameSchema({
    "seller_id": Column(str),
    "seller_zip_code_prefix": Column(int),
    "seller_city": Column(str),
    "seller_state": Column(str),
})

def clean_sellers(df):
    return schema.validate(df)
