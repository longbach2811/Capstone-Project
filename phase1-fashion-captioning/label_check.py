import json

label = json.load(open('/home/dev/workspace/LongBH/Show-Attend-and-Tell/data/coco/train_captions.json', 'r'))
word_dic = json.load(open('/home/dev/workspace/LongBH/Show-Attend-and-Tell/data/coco/word_dict.json', 'r'))
for i in label[0:10]:
    c = ''
    for ii in i:
        if ii == 3:
             continue
        for w in word_dic.items():
                if w[1] == ii:
                    c = c + str(w[0]) + ' '
                    continue
    print(c)
# print(label[0])
