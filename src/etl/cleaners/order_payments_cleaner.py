from pandera import Column, Check, DataFrameSchema

schema = DataFrameSchema({
    "order_id": Column(str),
    "payment_sequential": Column(int),
    "payment_type": Column(str),
    "payment_installments": Column(int, Check.ge(0)),
    "payment_value": Column(float, Check.ge(0)),
})

def clean_order_payments(df):
    df.fillna({"payment_installments": 0}, inplace=True)
    return schema.validate(df)
