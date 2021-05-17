import os
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.image as mpimg


img_rows = 172
img_cols = 172
mypath = 'RawData'

percentage_train = 0.8
percentage_val = 0.1
percentage_test = 0.1


def preprocess_data():

    #Clear Folders
    dir = 'ProcessedData/Train/Match'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'ProcessedData/Train/NoMatch'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'ProcessedData/Val/Match'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'ProcessedData/Val/NoMatch'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'ProcessedData/Test/Match'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir = 'ProcessedData/Test/NoMatch'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    df = pd.read_excel('labels.xlsx', index_col=0)
    matches = df.index
    for i in range(len(filenames)):
        print(i)
        num = np.random.rand()

        if num <= percentage_train:
            mode = 'Train'
        if num > percentage_train and num <= percentage_train + percentage_val:
            mode = 'Val'
        if num > percentage_train + percentage_val:
            mode = 'Test'
        try:
            img = mpimg.imread(mypath + '/' + filenames[i])
            if img.shape[0] != img_rows:
                resid = img.shape[0] - img_rows
                img = img[int(resid / 2):int(-resid / 2), :, :]
            if filenames[i] in matches:
                #Put it in one folder
                fullfilename = os.path.join('ProcessedData/' + mode + '/Match/', filenames[i])
            else:
                fullfilename = os.path.join('ProcessedData/' + mode + '/NoMatch/', filenames[i])
            plt.imsave(fullfilename, img)
        except:
            s = 0

preprocess_data()