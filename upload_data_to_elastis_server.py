import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError


hosts = ["http://localhost:9200"]
index_name = "hm-data"
csv_filepath = "data/data_women.csv"


DB = Elasticsearch(hosts)
if DB.indices.exists(index=index_name):
    DB.indices.delete(index=index_name)


df = pd.read_csv(csv_filepath)
docs = df.to_dict(orient="records")
for doc in docs:
    DB.index(index=index_name, document=doc)