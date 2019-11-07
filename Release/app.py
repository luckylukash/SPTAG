import SPTAG
from features_extractor import extract_features, get_filenames, get_images

from flask import Flask, jsonify, abort, request, redirect, url_for, render_template, json, Response
from werkzeug.utils import secure_filename



import numpy as np
import pandas as pd
from PIL import Image
#import csv
import os
#import json

#from os import listdir
#from os.path import isfile, join, splitext
#import shutil
#import random
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import imshow
#import time


app = Flask(__name__)

upload_folder = 'upload-file/'
k = 20
sptag_index = 'sptag_indice'


# feature extractor
def convert_img_embed(img_arr):
    embedding = extract_features(img_arr, pretrained_model="vgg19")
    return embedding

def build_response(data):
    print('data00 : ', data[0][0])
    print('data01 : ', data[0][1])
    #print('data1 : ', data[1])
    print('type1 : ', type(data[0][0]))
    print('type2 : ', type(json.dumps(data[0][0])))
    idxs = json.dumps(data[0][0])
    distances = json.dumps(data[0][1])
    
    #json_merged = {**idxs, **distances}
    #print('json.dumps(data[0][0]) : ', json.dumps(data[0][0])) 
    #print('json_merged : ', json_merged)
    #final_json = json.dumps(json_merged)
    #print('final_json : ', final_json)
    res = '{index: ' + str(idxs) + ', distance:  ' + str(distances) + '}'
    print(res)
    #json_res = json.loads(data[0][0])
    return idxs, distances # res #data[0] #Response(str(final_json), status=200, mimetype="application/json")

def load_indexes():
    train_embedding = np.load('caltech101_np_4096d.npy')
    filenames = np.load('caltech101_np_4096d_filenames.npy')
    return train_embedding, filenames

def convert_uploaded_img(filepath):
    filenames = get_filenames(filepath)
    
    imgs_np = get_images(filenames, target_size=(200,200), color='RGB', bg_clr=0)
    
    #img= Image.open(filepath)
    #img_arr = np.array(img)
    #img_arr = np.expand_dims(img_arr, axis=0) # add dim for feature_extract
    return imgs_np

def sptag_ann_search(index, q, k):
    j = SPTAG.AnnIndex.Load(index)
    for t in range(q.shape[0]):
        result = []
        result.append(j.Search(q[t].tobytes(), k))
    return result

# load dataset
train_embedding, filenames = load_indexes()
print('dataset loading done')

@app.route("/probe")
def probe():
    probe = '{"result":"sptag-api"}'
    return "probe" #Response(probe, status=200, mimetype="application/json")


@app.route("/")
def hello():
    return "sptag on azure flask app"

@app.route('/search', methods = ['POST'])
def sptag_search():
    print('start')
    
    if 'file' not in request.files:
        print('file not found')
        abort(404)
    
    print('load file start')
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(upload_folder + filename)
    
    # convert image to arr
    img_arr = convert_uploaded_img(upload_folder + filename)
    print('shape: ', img_arr.shape)
    
    # run feature extract
    embedding = convert_img_embed(img_arr)
    
    # run search
    result = sptag_ann_search(sptag_index, embedding, k)
    print('result : ', result)
    
    idxs, distances = build_response(result)
    #print('response : ', response)
    
    #def summary():
    #data = make_summary()
    
    return jsonify(idxs = idxs, distances = distances)

    
    #return Response(response, 201)

# intial model
#@app.before_request
#def initializing():
#    # load data
    
    
#    return 'before' #train_embedding, filenames
        
# Handle error routine
#@app.errorhandler(404)
#def not_found(error):
#    return Response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000') #,debug=True)
