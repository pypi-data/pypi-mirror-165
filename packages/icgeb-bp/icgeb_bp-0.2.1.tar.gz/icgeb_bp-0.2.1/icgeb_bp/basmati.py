#!/usr/bin/python
import os,sys
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import tensorflow as tf
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np


def predict_BAS(input_dir_path):
    classifier = tf.keras.models.load_model('Rice_InResv2_Aug36_25epochs.h5')

    img = tf.keras.preprocessing.image.load_img(input_dir_path, target_size=(299, 299))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img/255
    # create a batch of size 1 [N,H,W,C]
    img = np.expand_dims(img, axis=0)
    prediction = classifier.predict(img, batch_size=None,steps=1) #gives all class prob.
    #print(prediction)
    target_names = ['1121','1509','1637','1718','1728','BAS_370','CSR_30','DHBT_3','PB1','PB_6','Unknown']
    print(target_names[0] + ':', prediction[0][0])
    print(target_names[1] + ':', prediction[0][1])
    print(target_names[2] + ':', prediction[0][2])
    print(target_names[3] + ':', prediction[0][3])
    print(target_names[4] + ':', prediction[0][4])
    print(target_names[5] + ':', prediction[0][5])
    print(target_names[6] + ':', prediction[0][6])
    print(target_names[7] + ':', prediction[0][7])
    print(target_names[8] + ':', prediction[0][8])
    print(target_names[9] + ':', prediction[0][9])
    print(target_names[10] + ':', prediction[0][10])
    
    return prediction
    



