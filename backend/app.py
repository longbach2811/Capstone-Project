"""Fast API app."""
import io
import uvicorn
import numpy as np
import nest_asyncio
from enum import Enum


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware



# import streamlit as st
import requests
import threading
# from streamlit_option_menu import option_menu
import cv2
import argparse, json, os
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision.transforms as transforms
from math import ceil
from PIL import Image
import requests
# from streamlit_app import streamlit_app

import time

import sys
sys.path.append("../backup/phase1-fashion-captioning")
from dataset import pil_loader
from decoder import Decoder
from encoder import Encoder
from train import data_transforms
import time


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

import pandas as pd

hosts = ["http://localhost:9200"]
DB = Elasticsearch(hosts)
index_name = "hm-data"
# DB.indices.delete(index=index_name)
df = pd.read_csv("../data/new_data_women.csv")
docs = df.to_dict(orient="records")
for doc in docs:
    DB.index(index=index_name, document=doc)

def elastic_search(var: str):
    start_time = time.time()
    if not DB.indices.exists(index=index_name):
        try:
            DB.indices.create(index=index_name)
            print(f"Index '{index_name}' created successfully.")
        except RequestError as e:
            print(f"Failed to create index '{index_name}': {e}")
        else:
            DB.indices.delete(index=index_name)
            print(f"Old DB has been deleted")
            
    # # Add data
    # df = pd.read_csv("data_women.csv")
    # docs = df.to_dict(orient="records")

    # for doc in docs:
    #     es.index(index=index_name, document=doc)
    
    new_query = {
    "query_string": {
      "query": f"{var}",
      "default_field": "Desc"
    },
    }
    res = DB.search(index=index_name, query=new_query, size=10)
    hits = res["hits"]["hits"]
    result = []

    for hit in hits:
        title = hit["_source"]["Title"]
        url_path = hit["_source"]["Url_path"]
        thumbnail = hit["_source"]["Thumbnail"]
        result.append(f"{title} {url_path} {thumbnail}")
        
    # es.indices.delete(index=index_name)
    print(f"Elastic search time: {time.time() - start_time}s")
    return "Got %d Hits:" % res['hits']['total']['value'], result

def generate_caption_visualization(encoder, decoder, img, word_dict, beam_size=64, smooth=True):
    img = data_transforms(img)
    img = torch.FloatTensor(img)
    img = img.unsqueeze(0)
    img_features = encoder(img)
    img_features = img_features.expand(beam_size, img_features.size(1), img_features.size(2))
    sentence, alpha = decoder.caption(img_features, beam_size)

    token_dict = {idx: word for word, idx in word_dict.items()}
    sentence_tokens = []
    for word_idx in sentence:
        sentence_tokens.append(token_dict[word_idx])
        if word_idx == word_dict['<eos>']:
            break
    num_words = len(sentence_tokens)
    w = np.round(np.sqrt(num_words))
    h = np.ceil(np.float32(num_words) / w)
    alpha = torch.tensor(alpha)

    caption = ""
    plt.axis('off')
    for idx in range(num_words):
        label = sentence_tokens[idx]
        caption = caption + label + " "
        plt.text(0, 1, label, backgroundcolor='white', fontsize=13)
        plt.text(0, 1, label, color='black', fontsize=13)

        if encoder.network == 'vgg19':
            shape_size = 14
        else:
            shape_size = 7
    return caption

@app.get("/")
async def root():
    return {"message": "Hello World"}

word_dict = json.load(open('../model/data/coco/word_dict.json', 'r'))
vocabulary_size = len(word_dict)

encoder = Encoder(network="resnet152")
decoder = Decoder(vocabulary_size, encoder.dim)

encoder.eval()
decoder.eval()
decoder.load_state_dict(torch.load('../model/model_resnet152_v1/model_resnet152_16.pth', map_location='cpu'))

@app.post("/search-by-image/")
async def img_search(file: UploadFile = File(...)):
    global DB
    filename = file.filename
    fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    image_stream = io.BytesIO(file.file.read())
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image = Image.fromarray(image)
    image.save("abc.png")
    start_time = time.time()
    output = generate_caption_visualization(encoder, decoder, image, word_dict, beam_size=64)
    print(f'Model inference time: {time.time() - start_time}s')
    return {"image_path": "abc.png", "result": elastic_search(output.replace('<start>','').replace('<eos>',''))}

@app.post("/search-by-word/")
async def word_search(var:str):
    return {"result" : elastic_search(var)}


@app.post("/predict/")
async def prediction(file: UploadFile = File(...)):
    filename = file.filename
    fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    
    image_stream = io.BytesIO(file.file.read())
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image = Image.fromarray(image)
    image.save("xxx.png")
    output = generate_caption_visualization(encoder, decoder, image, word_dict, beam_size=64)
    return {"image_path": "xxx.png", "caption": output.replace('<start>','').replace('<eos>','')}


if __name__ == "__main__":
    # Init DB
    # DB = init_db()

    fastapi_thread = threading.Thread(target=uvicorn.run, args=("app:app",), kwargs={"host": "0.0.0.0", "port": 8000, "log_level": "info", "reload": True, "workers": 4})
    fastapi_thread.start()
    # streamlit_app()
