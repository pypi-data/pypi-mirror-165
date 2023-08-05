# Pulire

A lightweight DataFrame validation library for [Pandas](https://pandas.pydata.org/).

## Schema

Pulire requires a `Schema` which describes all columns in a given `DataFrame`.

```py
from numpy import datetime64
import pulire as pu

myschema = pu.Schema(
  [
    pu.Index("time", datetime64)
  ],
  [
    pu.Column(
      "temp", float, [
        pu.validators.minimum(-80),
        pu.validators.maximum(65)
      ]
    ),
    pu.Column(
      "wdir", float, [
        pu.validators.minimum(0),
        pu.validators.maximum(360)
      ]
    ),
    pu.Column(
      "wspd", float, [
        pu.validators.minimum(0),
        pu.validators.maximum(250)
      ]
    ),
    pu.Column(
      "wpgt", float, [
        pu.validators.minimum(0),
        pu.validators.maximum(500),
        pu.validators.greater('wspd')
      ]
    ),
    pu.Column(
      "pres", float, [
        pu.validators.minimum(850),
        pu.validators.maximum(1090)
      ]
    ),
    pu.Column(
      "rhum", int, [
        pu.validators.minimum(0),
        pu.validators.maximum(100)
      ]
    )
  ]
)
```

## Validate

Pulire automatically removes values which fail the validation. Let's use the `meteostat` library to get some data:

```py
from datetime import datetime
from meteostat import Hourly

df = Hourly("10637", datetime(2018, 1, 1), datetime(2018, 1, 1, 23, 59)).fetch()

print(df)
```

Now, we can get a valid copy of our Meteostat `DataFrame` by running our schema's `validate` method:

```py
df = myschema.validate(df)
```