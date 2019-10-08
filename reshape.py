import os
import json
import pandas as pd


try:
    df = pd.read_json(os.environ['SCRAPY_FILE'])
    with open(os.environ['RESULT_FILE'], 'w') as f:
        json.dump(df.groupby(df.columns[:-1].tolist()).cars.apply(lambda x: x.tolist()).reset_index().to_dict('records'), f)
except Exception as e:
    print(e)
