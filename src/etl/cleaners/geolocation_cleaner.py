from pandera import Column, Check, DataFrameSchema

schema = DataFrameSchema({
    "geolocation_zip_code_prefix": Column(int),
    "geolocation_lat": Column(float),
    "geolocation_lng": Column(float),
    "geolocation_city": Column(str),
    "geolocation_state": Column(str),
})

def clean_geolocation(df):
    df.dropna(inplace=True)
    return schema.validate(df)
