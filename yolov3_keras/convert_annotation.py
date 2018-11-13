import xml.etree.ElementTree as ET
from os import getcwd
import os

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = []
with open("model_data/bkseeing_classes.txt") as f:
    classes = list(line.replace('\n', '') for line in f)
print (classes)


def convert_annotation(image_id, list_file):
    try:
        in_file = open("dataver1/annotations/train/%s.xml"%(image_id))
    except:
        return
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()
list_file = open("train.txt", "w")
images_id = list(line[:-4] for line in os.listdir("dataver1/images/train"))
for image_id in images_id:
    print("/%s.jpg"%(image_id))
    list_file.write("dataver1/images/train/%s.jpg"%(image_id))
    convert_annotation(image_id, list_file)
    list_file.write('\n')
list_file.close()