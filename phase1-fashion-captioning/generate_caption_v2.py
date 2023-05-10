from dataset import pil_loader
from train import data_transforms
import torch
from encoder import Encoder
from decoder import Decoder
import json
from torch.autograd import Variable

# 1. Check dataloader is correct ????


img_path = '/home/dev/workspace/LongBH/Show-Attend-and-Tell/data/coco/imgs/010/0108775015.jpg'
img = pil_loader(img_path)
img = data_transforms(img)
img = torch.FloatTensor(img)
img = img.unsqueeze(0)   # (1, 3, 224, 224)

print(img.shape)

word_dict = json.load(open('/home/dev/workspace/LongBH/Show-Attend-and-Tell/data/coco/word_dict.json', 'r'))
vocabulary_size = len(word_dict)

encoder = Encoder(network='vgg19')
decoder = Decoder(vocabulary_size, encoder.dim, False)  # ??? True or false
decoder.load_state_dict(torch.load('/home/dev/workspace/LongBH/Show-Attend-and-Tell/model/model_vgg19_3.pth', map_location='cpu'))

encoder.eval()
decoder.eval()

# 
img_features = encoder(img)  # (1, 196, 512)
print(img_features.shape)

captions = Variable(captions)
preds, alphas = decoder(img_features, captions)
