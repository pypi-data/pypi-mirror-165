from datetime import datetime
from meteostat import Hourly
import pulire as pu
from pulire.schema import Schema
from pulire.validator import ValidationError


df = Hourly("10637", datetime(2018, 1, 1), datetime(2018, 1, 1, 23, 59)).fetch()

myschema = Schema(
    {
        "temp": [pu.validators.minimum(-100), pu.validators.maximum(65)],
        "prcp": [pu.validators.minimum(0), pu.validators.maximum(350)],
        "snow": [pu.validators.minimum(0), pu.validators.maximum(11000)],
        "wdir": [pu.validators.minimum(0), pu.validators.maximum(360)],
        "wspd": [pu.validators.minimum(0), pu.validators.maximum(250)],
        "wpgt": [
            pu.validators.minimum(0),
            pu.validators.maximum(500),
            pu.validators.greater("wspd"),
        ],
        "tsun": [pu.validators.minimum(0), pu.validators.maximum(60)],
        "srad": [pu.validators.minimum(0), pu.validators.maximum(1368)],
        "pres": [pu.validators.minimum(850), pu.validators.maximum(1090)],
        "rhum": [pu.validators.minimum(0), pu.validators.maximum(100)],
        "cldc": [pu.validators.minimum(0), pu.validators.maximum(100)],
        "vsby": [pu.validators.minimum(0), pu.validators.maximum(9999)],
        "coco": [pu.validators.minimum(1), pu.validators.maximum(27)],
    }
)


try:
    myschema.debug(df)
except ValidationError as error:
    print(error.errors)


validated_df = myschema.validate(df)

print(validated_df)
