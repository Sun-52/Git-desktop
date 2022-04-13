import math
import numpy as np
import pandas as pd
import keras as K
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.regularizers import L2
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
from tensorflow import _tf2
#from tensorflow.python.keras.models import model_from_json
import joblib
#from __future__ import absolute_import, division, print_function
#import os
##from tensorflow import keras
import pickle
plt.style.use("fivethirtyeight")
scaler = MinMaxScaler(feature_range=(39,66))

#Process dataframe

#Data frame
df = pd.read_csv("PHC-project.csv")
#Collect all data to 1 array
data=[]
for i in df["time"]:
  data.append(i)
dataset=np.array(data)
dataset = np.reshape(dataset, (dataset.shape[0],1))
#Scale the data
dataset = scaler.fit_transform(dataset)
dataset = np.reshape(dataset, (dataset.shape[0]))
#Amount of data
datacount=len(dataset)

#Prepare data for training

#specify the amount of data use to train
#in this case is not important, since we use 100% of the data
train_data=dataset[0:datacount]
#seperate data into set for training
features = []
label = []
for j in range(10,len(train_data)):
  features.append(train_data[j-10:j])
  label.append(train_data[j])
#change data type to array
features = np.array(features)
label = np.array(label)
#reshape "features" dimension to 3 dimension for LSTM
features = np.reshape(features, (features.shape[0],features.shape[1],1))

#LSTM model

#create model
file = open("Rubik_model_structure.json","r")
loaded_model_json = file.read()
file.close()
model = tf.keras.models.model_from_json(loaded_model_json)
model.load_weights("Rubik_model_weight.h5")
#compile model

#Train model


#UI function

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.title("Rubik predictor")
window.geometry("1024x576")
window.configure(bg = "#B3B2B2")


canvas = Canvas(
    window,
    bg = "#B3B2B2",
    height = 576,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    511.0,
    288.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    440.0,
    54.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    815.0,
    49.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    512.0,
    122.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    512.0,
    255.0,
    image=image_image_5
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    492.5,
    193.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=360.0,
    y=186.0,
    width=265.0,
    height=13.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    512.0,
    340.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    492.0,
    204.99996948242188,
    image=image_image_7
)
def delete():
    entry_1.delete(0,END)
def enter_cal():
    num_list = []
    temp_list=[]
    global dataset
    for k in range(len(dataset)-9,len(dataset)):
      temp_list.append(dataset[k])
    num = (math.ceil(float(entry_1.get())))*1.6667
    temp_list.append(num)
    temp_list = np.array(temp_list)
    temp_list = np.reshape(temp_list, (temp_list.shape[0],1))
    temp_list = scaler.transform(temp_list)
    num_list.append(temp_list)
    num_list = np.array(num_list)
    num_list = np.reshape(num_list, (num_list.shape[0],num_list.shape[1],1))
    dataset = list(dataset)
    dataset.append(num)
    prediction = model.predict(num_list)
    prediction = scaler.inverse_transform(prediction)
    prediction = round((prediction[0][0]/1.6667), 2)
    print(num_list)
    print()
    print(prediction)
    num_list = list(num_list)
    time = Label(window, text=(prediction, "seconds"))

    time.place(x=512.0,y=340.0, anchor='center')

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:[enter_cal(), delete()] ,
    relief="flat"
)
button_1.place(
    x=643.0,
    y=180.0,
    width=61.0,
    height=27.0
)
window.resizable(False, False)
window.mainloop()