# Capstone Project 2023

Author: Anh T. Tra, Long Bach Hoang, Tam Nguyen Tue 

## Table of Contents

## TODO:
### Phase 1: Application of NLP in Image Captioning for fashion product
- Model: CNN convolutional feature extractor: ResNet152 and LSTM
- Link word dictionary: [English word dictionary](https://drive.google.com/drive/folders/1LME6AYCXnBWIHF7pYz1z6AQg1OnYeIyV) and [Vienamese word dictionary](https://drive.google.com/drive/folders/1vLkEBkkr-xsQkbwNisgvZWJrqJQ0XDTq)
- Link model: [English model](https://drive.google.com/drive/folders/1nAIZAYkLuMU10ZOmpkKS8yAw5Tjj43In) and [Vietnamse model](https://drive.google.com/drive/folders/1WloIG5p_Jg7oCt7cfAtyHcbd3EhPpiej)
- File directory:
```
├───model
│   ├───data
│   │   └───coco
│   ├───model_resnet152_v1
```

### Phase 2: Elastic Search
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.8.2
```
```
docker compose up --build
```

### Phase 3: Deploy model

- Build backend using FastAPI.
```
cd backend
uvicorn app:app --reload
```

- Build frontend using VueJS.

```
cd frontend
npm install
npm run dev
```
