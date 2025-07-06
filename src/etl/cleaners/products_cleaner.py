from pandera.pandas import Column, DataFrameSchema, Check

# Fix schema with correct column names
schema = DataFrameSchema({
    "product_id": Column(str),
    "product_category_name": Column(str, nullable=True),
    "product_name_length": Column(float, Check.ge(0)),
    "product_description_length": Column(float, Check.ge(0)),
    "product_photos_qty": Column(float, Check.ge(0)),
    "product_weight_g": Column(float, Check.ge(0)),
    "product_length_cm": Column(float, Check.ge(0)),
    "product_height_cm": Column(float, Check.ge(0)),
    "product_width_cm": Column(float, Check.ge(0)),
})

def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    # Fix typos in column names
    df.rename(columns={
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length"
    }, inplace=True)

    # Fill missing numeric values
    df.fillna({
        "product_weight_g": 0,
        "product_length_cm": 0,
        "product_height_cm": 0,
        "product_width_cm": 0,
        "product_photos_qty": 0,
        "product_name_length": 0,
        "product_description_length": 0,
    }, inplace=True)

    # Validate
    return schema.validate(df)
