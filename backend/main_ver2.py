import io
import uvicorn
import numpy as np
import nest_asyncio
from enum import Enum
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

# import openai

import cv2

import argparse, json, os
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import skimage
import skimage.transform
import torch
import torchvision.transforms as transforms
from math import ceil
from PIL import Image
import requests

import sys
sys.path.append("../phase1-fashion-captioning")

from dataset import pil_loader
from decoder import Decoder
from encoder import Encoder
from train import data_transforms



app = FastAPI()

from elasticsearch import Elasticsearch
import pandas as pd



def elastic_search(var: str):
    hosts = ["http://localhost:9200"]

    # Kết nối đến Elasticsearch
    es = Elasticsearch(hosts)

    # Tạo index
    index_name = "hm-data"

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "Url_path": {"type": "text"},
                    "Title": {"type": "text"},
                    "Desc": {"type": "text"}
                }
            }
        })

    # Đọc dữ liệu từ file CSV và chuyển đổi thành tài liệu Elasticsearch

    df = pd.read_csv("data_women.csv")
    docs = df.to_dict(orient="records")
    # print(f"docs: {docs}")

    # Gửi các tài liệu đến Elasticsearch để lưu trữ trong index
    for doc in docs:
        es.index(index=index_name, document=doc)
    
    new_query = {
    "query_string": {
      "query": f"{var}",
      "default_field": "Desc"
    },
    }
    res = es.search(index=index_name, query=new_query, size=10)
    # print("Got %d Hits:" % res['hits']['total']['value'])
    
    hits = res["hits"]["hits"]

    result = []

    for hit in hits:
        score = hit["_score"]
        title = hit["_source"]["Title"]
        url_path = hit["_source"]["Url_path"]
        # desc = hit["_source"]["Desc"]
        result.append(f"{score} {title} {url_path}")
        
    es.indices.delete(index=index_name)
    return {'hit result:': "Got %d Hits:" % res['hits']['total']['value'], 'result': result}

def generate_caption_visualization(encoder, decoder, img, word_dict, beam_size=3, smooth=True):
    # img = pil_loader(img_path)
    img = data_transforms(img)
    img = torch.FloatTensor(img)
    img = img.unsqueeze(0)


    # print(f"Size of Encoder inputs: {img.shape}")
    img_features = encoder(img)
    # print(f"Size of ecoder outputs: {img_features.shape}")
    img_features = img_features.expand(beam_size, img_features.size(1), img_features.size(2))
    # print(f"Size of decoder input: {img_features.shape}")
    sentence, alpha = decoder.caption(img_features, beam_size)

    token_dict = {idx: word for word, idx in word_dict.items()}
    sentence_tokens = []
    for word_idx in sentence:
        sentence_tokens.append(token_dict[word_idx])
        if word_idx == word_dict['<eos>']:
            break

    # img = Image.open(img_path)
    

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
    return {'caption': caption}

@app.get("/")
async def root():
    return {"message": "Hello World"}


word_dict = json.load(open('..\phase1-fashion-captioning\data\coco\word_dict.json', 'r'))
vocabulary_size = len(word_dict)

encoder = Encoder(network="resnet152")
decoder = Decoder(vocabulary_size, encoder.dim)

encoder.eval()
decoder.eval()
    
decoder.load_state_dict(torch.load('..\phase1-fashion-captioning\model_resnet152_v1\model_resnet152_6.pth', map_location='cpu'))

@app.post("/search/")
async def search(file: UploadFile = File(...)):
    filename = file.filename
    fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    
    # 2. TRANSFORM RAW IMAGE INTO CV2 image
    
    # Read image as a stream of bytes
    image_stream = io.BytesIO(file.file.read())
    
    # Start the stream from the beginning (position zero)
    image_stream.seek(0)
    
    # Write the stream of bytes into a numpy array
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    # image.save("xxx.png")

    output = generate_caption_visualization(encoder, decoder, image, word_dict, beam_size=64)

    return elastic_search(output['caption'].replace('<start>','').replace('<eos>',''))
