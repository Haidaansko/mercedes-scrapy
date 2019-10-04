import json
import pandas as pd


df = pd.read_json('../../mercedes_scrapper/scraped_data1.json', encoding='utf-8')
with open('res.json', 'w') as f:
    json.dump(df.groupby(df.columns[:-1].tolist()).cars.apply(lambda x: x.tolist()).reset_index().to_dict('records'), f)