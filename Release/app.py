import SPTAG
import numpy as np
import pandas as pd
from PIL import Image
import os
from features_extractor import extract_features, get_filenames, get_images
from flask import Flask, jsonify, abort, request, redirect, url_for, render_template, json, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)

upload_folder = 'upload-file/' #file upload folder
k = 20 #number of result
sptag_index = 'sptag_indice' #name of SPTAG index

# feature extractor
def convert_img_embed(img_arr):
    embedding = extract_features(img_arr, pretrained_model="vgg19") #keras pretrained model - 'resnet50', 'inception_v3', 'vgg19'
    return embedding

# get index numbers, distances and file names to return as json
def build_response(data):
    idxs = data[0][0]
    distances = data[0][1]
    fs = []
    for idx in idxs:
        fs.append(filenames[idx])

    return idxs, distances, fs

# load datasets which saved as numpy format
def load_dataset():
    train_embedding = np.load('caltech101_np_4096d.npy')
    filenames = np.load('caltech101_np_4096d_filenames.npy')
    return train_embedding, filenames

# convert image before extract feature
def convert_uploaded_img(filepath):
    filenames = get_filenames(filepath)
    imgs_np = get_images(filenames, target_size=(200,200), color='RGB', bg_clr=0)
    return imgs_np

# run SPTAG search
def sptag_ann_search(index, q, k):
    j = SPTAG.AnnIndex.Load(index)
    for t in range(q.shape[0]):
        result = []
        result.append(j.Search(q[t].tobytes(), k))
    return result

# load dataset
train_embedding, filenames = load_dataset()

@app.route('/probe')
def probe():
    return jsonify(result = 'sptag-api')

@app.route("/")
def hello():
    return "SPTAG app on Azure"

# SPTAG search verb
@app.route('/search', methods = ['POST'])
def sptag_search():

    if 'file' not in request.files:
        print('file not found')
        abort(404)
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(upload_folder + filename)
    
    # convert uploaded image to np array
    img_arr = convert_uploaded_img(upload_folder + filename)
    
    # run feature extractor
    embedding = convert_img_embed(img_arr)
    
    # run SPTAG search
    result = sptag_ann_search(sptag_index, embedding, k)
        
    # build response
    idxs, distances, fs = build_response(result)
    
    return jsonify(idxs = idxs, distances = distances, filenames = fs)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000')
