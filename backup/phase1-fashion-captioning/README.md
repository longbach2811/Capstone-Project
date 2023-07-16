# Phase 1: Fashion captioning

# Datasets: H&M recommendation dataset
Link datasets:
* Images: [here](https://www.kaggle.com/datasets/odins0n/hm512x512?select=images_512_512)
* Caption: [here](https://drive.google.com/drive/folders/1LME6AYCXnBWIHF7pYz1z6AQg1OnYeIyV)



# Pretrained Model:
Use Resnet152 with teacher forcing
* Link model: [here](https://drive.google.com/drive/folders/1nAIZAYkLuMU10ZOmpkKS8yAw5Tjj43In)

# Inference:
```bash
python generate_caption.py --img-path <IMG-PATH> --model <MODEL-PATH> --network <NETWORK-NAME>
```

