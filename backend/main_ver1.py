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

# openai.api_key  = "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"

# def get_completion(prompt, model="gpt-3.5-turbo", temperature=0): 
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature, 
#     )
#     return response.choices[0].message["content"]

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
    return caption

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

@app.post("/predict/")
async def prediction(file: UploadFile = File(...)):
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
    image.save("xxx.png")

    output = generate_caption_visualization(encoder, decoder, image, word_dict, beam_size=64)

    # prompt = f"Dịch từ tiếng anh sang tiếng việt bỏ <start> và <eos>: {output}"

    return output

# @app.post("/predict/")
# async def create_upload_file(file: UploadFile = File(...)):
#     image = Image.open(io.BytesIO(file.file.read()))
#     image = image.convert('RGB')
#     image = image.resize((224, 224))
#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='JPEG')
#     img_byte_arr = img_byte_arr.getvalue()

#     # Define the API endpoint for the Machine Learning model
#     API_ENDPOINT = "http://localhost:8000/predict"

#     # Call the API to get the prediction
#     response = requests.post(API_ENDPOINT, files={'image': img_byte_arr})
#     return response.json()