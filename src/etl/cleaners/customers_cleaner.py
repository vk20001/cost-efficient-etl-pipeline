from pandera import Column, DataFrameSchema

schema = DataFrameSchema(
    {
        "customer_id": Column(str),
        "customer_unique_id": Column(str),
        "customer_zip_code_prefix": Column(int),
        "customer_city": Column(str),
        "customer_state": Column(str),
    }
)


def clean_customers(df):
    df.dropna(inplace=True)
    return schema.validate(df)
