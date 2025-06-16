import pandera as pa
from pandera import Column, DataFrameSchema

schema = DataFrameSchema({
    "product_category_name": Column(str),
    "product_category_name_english": Column(str),
})

def clean_category_translation(df):
    return schema.validate(df)
