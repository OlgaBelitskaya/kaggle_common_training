# -*- coding: utf-8 -*-
"""keras-cookbook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZV38CLgg-PIpds7ra5bd2KLKHoFgprY1

<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Code Library, Style, & Links</h1>

[Google Colaboratory Version](https://colab.research.google.com/drive/16Xh8T4fPuk0AIBjnCo7e9WTrF1PgukoF)
"""

# Commented out IPython magic to ensure Python compatibility.
# %%html
# <style>
# @import url('https://fonts.googleapis.com/css?family=Ewert|Roboto&effect=3d');
# span {font-family:'Roboto'; color:black; text-shadow:3px 3px 3px #999;}  
# div.output_area pre{font-family:'Roboto'; font-size:110%; color:#ff603b;}      
# </style>

import warnings; warnings.filterwarnings('ignore')
import numpy as np,pandas as pd,scipy as sp
import pylab as pl,seaborn as sn
import os,json,cv2,h5py
import keras as ks,tensorflow as tf
from PIL import ImageFile
from tqdm import tqdm
from skimage import io
print(os.listdir("../input"))

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing import sequence as ksequence
from keras.preprocessing import image as kimage
from keras.utils import to_categorical
from keras.models import Model,Sequential,load_model
from keras.layers import Dense,Activation,\
Dropout,Flatten,Conv2D,MaxPooling2D,\
GlobalMaxPooling2D,GlobalAveragePooling2D,\
Input,Conv1D,MaxPooling1D,LSTM
from keras.layers.embeddings import Embedding
from keras.layers.advanced_activations import PReLU,LeakyReLU
from keras.callbacks import ModelCheckpoint,\
ReduceLROnPlateau,EarlyStopping

def loss_plot(fit_history):
    pl.figure(figsize=(10,3))
    pl.plot(fit_history.history['loss'],label='train')
    pl.plot(fit_history.history['val_loss'],label='test')
    pl.legend(); pl.title('Loss Function');   
def mae_plot(fit_history):
    pl.figure(figsize=(10,3))
    pl.plot(fit_history.history['mean_absolute_error'],label='train')
    pl.plot(fit_history.history['val_mean_absolute_error'],label='test')
    pl.legend(); pl.title('Mean Absolute Error'); 
def acc_plot(fit_history):
    pl.figure(figsize=(10,3))
    pl.plot(fit_history.history['acc'],label='train')
    pl.plot(fit_history.history['val_acc'],label='test')
    pl.legend(); pl.title('Accuracy');

def prepro(x_train,y_train,x_test,y_test):
    N=y_train.shape[0]; shuffle_ids=np.arange(N)
    np.random.RandomState(23).shuffle(shuffle_ids)
    x_train,y_train=\
    x_train[shuffle_ids],y_train[shuffle_ids]
    n=int(len(x_test)/2)
    x_valid,y_valid=x_test[:n],y_test[:n]
    x_test,y_test=x_test[n:],y_test[n:]
    print(x_train.shape,x_valid.shape,x_test.shape)
    print(y_train.shape,y_valid.shape,y_test.shape)
    print('Label: ',y_train[1][0])
    pl.figure(figsize=(3,3)); 
    pl.xticks([]); pl.yticks([])
    pl.imshow(x_train[1],cmap='bone'); pl.show()
    return [x_train,y_train,x_valid,y_valid,x_test,y_test]

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Backend</h1>"""

print(ks.__version__)
# variants: theano, tensorflow, cntk
ks.backend.backend(),\
ks.backend.image_dim_ordering()

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Data</h1>
<h2>internal datasets</h2>
variants: cifar10, cifar100, imdb, reuters, mnist, fashion_mnist, boston_housing
"""

# 32x32 color images; labeled over 10 categories
# 50,000 - the train set; 10,000 - the test set
(x_train1,y_train1),(x_test1,y_test1)=\
ks.datasets.cifar10.load_data()
[x_train1,y_train1,x_valid1,y_valid1,x_test1,y_test1]=\
prepro(x_train1,y_train1,x_test1,y_test1)

# 28x28 grayscale images; labeled over 10 categories
# 55,000 - the train set; 10,000 - the test set
(x_train2,y_train2),(x_test2,y_test2)=\
ks.datasets.mnist.load_data()
[x_train2,y_train2,x_valid2,y_valid2,x_test2,y_test2]=\
prepro(x_train2,y_train2.reshape(-1,1),
       x_test2,y_test2.reshape(-1,1))

# 18000 newsgroups posts on 20 topics
train=fetch_20newsgroups(subset='train',shuffle=True,
                         remove=('headers','footers','quotes'))
test=fetch_20newsgroups(subset='test',shuffle=True,
                        remove=('headers','footers','quotes'))
y_train3,y_test3=train.target,test.target
vectorizer=TfidfVectorizer(sublinear_tf=True,max_df=.5,
                           stop_words='english')
x_train3=vectorizer.fit_transform(train.data) 
x_test3=vectorizer.transform(test.data)
del train,test
x_test3,x_valid3,y_test3,y_valid3=\
train_test_split(x_test3,y_test3,
                 test_size=.5,random_state=1)
print(x_train3.shape,x_valid3.shape,x_test3.shape)
print('Label: ',y_train3[1]) 
print('Sequence of word indexes: \n',x_train3[1])

# 13 attributes of houses at different locations, 
# targets are the median values of the houses at a location (in k$)
(x_train4,y_train4),(x_test4,y_test4)=\
ks.datasets.boston_housing.load_data()
n=int(len(x_test4)/2)
x_valid4,y_valid4=x_test4[:n],y_test4[:n]
x_test4,y_test4=x_test4[n:],y_test4[n:]
print(x_train4.shape,x_valid4.shape,x_test4.shape)
print(y_train4.shape,y_valid4.shape,y_test4.shape)
print('Target value: ',y_train4[1])
print("Features' values: \n",x_train4[1])
pl.figure(figsize=(10,3))
pl.hist(y_train4,bins=50,alpha=.7);

"""<h2>artificial datasets</h2>"""

# the artificial sets for classification, labeled over 2 categories 
X5,Y5=make_classification(n_samples=5000,n_features=2,
                          n_redundant=0,n_informative=2)
x_train5,x_test5,y_train5,y_test5=\
train_test_split(X5,Y5,test_size=.2,random_state=1)
n=int(len(x_test5)/2)
x_valid5,y_valid5=x_test5[:n],y_test5[:n]
x_test5,y_test5=x_test5[n:],y_test5[n:]
print(x_train5.shape,x_valid5.shape,x_test5.shape)
print(y_train5.shape,y_valid5.shape,y_test5.shape)
print('Label: ',y_train5[1])
print('Features: \n',x_train5[1])
pl.figure(figsize=(10,3))
pl.scatter(X5[:,0],X5[:,1],marker='o',
           s=5,c=Y5,cmap='tab10');

"""<h2>external datasets</h2>"""

# 150x150 grayscale face images; 
# labeled over 15 categories(persons)
yalefaces_paths=[]; yalefaces_images=[]
yalefaces_labels=[]; yalefaces_cut_images=[]
folder="../input/yale-face-database/data/"
cascade="../input/haarcascades/"+\
        "haarcascade_frontalface_default.xml"
for element in os.listdir(folder):
    if element!='Readme.txt':
        yalefaces_paths.append(os.path.join(folder,element))
for path in yalefaces_paths:
    image=io.imread(path,as_gray=True)
    yalefaces_images.append(image)
    label=int(os.path.split(path)[1].split(".")[0]\
              .replace("subject",""))-1
    yalefaces_labels.append(label)    
face_detector=cv2.CascadeClassifier(cascade)
for i in range(len(yalefaces_images)):
    image=yalefaces_images[i]
    face=face_detector.detectMultiScale(image)
    x,y=face[0][:2]
    cut_image=image[y:y+150,x:x+150]
    yalefaces_cut_images.append(cut_image)        
yalefaces_labels=np.array(yalefaces_labels).reshape(-1,1)
yalefaces_cut_images=np.array(yalefaces_cut_images)/255

x_train6,x_test6,y_train6,y_test6=\
train_test_split(yalefaces_cut_images,
                 yalefaces_labels,
                 test_size=.2,random_state=1)
[x_train6,y_train6,x_valid6,y_valid6,x_test6,y_test6]=\
prepro(x_train6,y_train6,x_test6,y_test6)

# 128x128 flower color images; labeled over 10 categories
# 189 - the train set; 21 - the test set
fpath="../input/flower-color-images/flower_images/flower_images/"
flowers=pd.read_csv(fpath+"flower_labels.csv")
flower_files=flowers['file']
flower_targets=flowers['label'].values.reshape(-1,1)
def path_to_tensor(img_path):
    img=kimage.load_img(fpath+img_path,
                        target_size=(128,128))
    x=kimage.img_to_array(img)
    return np.expand_dims(x,axis=0)
def paths_to_tensor(img_paths):
    list_of_tensors=[path_to_tensor(img_path) 
                     for img_path in tqdm(img_paths)]
    return np.vstack(list_of_tensors)
ImageFile.LOAD_TRUNCATED_IMAGES = True                 
flower_tensors=paths_to_tensor(flower_files)/255;

x_train7,x_test7,y_train7,y_test7=\
train_test_split(flower_tensors,flower_targets,
                 test_size=.1,random_state=1)
[x_train7,y_train7,x_valid7,y_valid7,x_test7,y_test7]=\
prepro(x_train7,y_train7,x_test7,y_test7)

fpath2='../input/classification-of-handwritten-letters/'
f=h5py.File(fpath2+'LetterColorImages_123.h5','r') 
keys=list(f.keys())
letters=u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
letter_images=np.array(f[keys[1]])/255
targets=np.array(f[keys[2]]).reshape(-1,1)-1
x_train8,x_test8,y_train8,y_test8=\
train_test_split(letter_images,targets,
                 test_size=.2,random_state=1)
del letter_images,targets
[x_train8,y_train8,x_valid8,y_valid8,x_test8,y_test8]=\
prepro(x_train8,y_train8,x_test8,y_test8)

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Preprocessing</h1>"""

# One-Hot Encoding
c_y_train1=to_categorical(y_train1,10) 
c_y_valid1=to_categorical(y_valid1,10)
c_y_test1=to_categorical(y_test1,10)
c_y_train2=to_categorical(y_train2,10)
c_y_valid2=to_categorical(y_valid2,10)
c_y_test2=to_categorical(y_test2,10)
c_y_train3=to_categorical(y_train3,20)
c_y_valid3=to_categorical(y_valid3,20)
c_y_test3=to_categorical(y_test3,20)
c_y_train6=to_categorical(y_train6,15)
c_y_valid6=to_categorical(y_valid6,15)
c_y_test6=to_categorical(y_test6,15)
c_y_train7=to_categorical(y_train7,10)
c_y_valid7=to_categorical(y_valid7,10)
c_y_test7=to_categorical(y_test7,10)
c_y_train8=to_categorical(y_train8,33)
c_y_valid8=to_categorical(y_valid8,33)
c_y_test8=to_categorical(y_test8,33)

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Basic Examples</h1>"""

# The basic model for binary classification
basic_model=Sequential([Dense(16,input_dim=2),Activation('relu'),
                        Dense(1),Activation('sigmoid')])
basic_model.compile(optimizer='adam', 
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
# Train 
basic_model.fit(x_train5, y_train5, 
                validation_data=(x_valid5,y_valid5), 
                epochs=100,batch_size=128,verbose=0)
# Predict classes
y_test5_predictions=basic_model.predict_classes(x_test5)
# Evaluate
basic_model.evaluate(x_test5,y_test5)

pl.figure(figsize=(10,2))
pl.scatter(range(100),y_test5[:100],s=100)
pl.scatter(range(100),
           y_test5_predictions[:100],s=25);

basic_model.input,basic_model.outputs

basic_model.summary()

basic_model.get_config()

basic_model.get_weights()

# Save/reload models
# basic_model.save('basic_model.h5')
# basic_model=load_model('basic_model.h5')

# Save/reload weights
# basic_model.save_weights('basic_model_weights.h5')
# basic_model.load_weights('basic_model_weights.h5',by_name=False)

# Choose optimization
optimizer=ks.optimizers.Nadam(lr=.005,beta_1=.99,beta_2=.9999,
                              epsilon=None,schedule_decay=.005)
basic_model=Sequential([Dense(16,input_dim=2),Activation('relu'),
                        Dense(1),Activation('sigmoid')])
basic_model.compile(optimizer=optimizer,
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
basic_model.fit(x_train5,y_train5, 
                validation_data=(x_valid5,y_valid5), 
                epochs=100,batch_size=128,verbose=0)
basic_model.evaluate(x_test5,y_test5)

# Improve activation
inp=Input(shape=(2,))
act=ks.layers.LeakyReLU(alpha=.4)
lay=act(Dense(16,name='encoder')(inp))
out=Dense(1,activation='sigmoid',
          name='decoder')(lay)
basic_model=Model(inputs=inp,outputs=out,name='cae')
basic_model.compile(optimizer=optimizer,
                    loss='binary_crossentropy',
                    metrics=['accuracy'])
basic_model.fit(x_train5, y_train5, 
                validation_data=(x_valid5,y_valid5), 
                epochs=100,batch_size=128,verbose=0)
basic_model.evaluate(x_test5,y_test5)

# Use callbacks
fw='weights.best.hdf5'
early_stopping=EarlyStopping(monitor='val_loss',patience=20)
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,factor=.5)
basic_model=Model(inputs=inp,outputs=out,name='cae')
basic_model.compile(optimizer=optimizer,
                    loss='binary_crossentropy',metrics=['accuracy'])
basic_model.fit(x_train5,y_train5,
                validation_data=(x_valid5,y_valid5),
                epochs=200,batch_size=128,verbose=0, 
                callbacks=[early_stopping,checkpointer,lr_reduction])
basic_model.load_weights(fw)
basic_model.evaluate(x_test5,y_test5)

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Multi-Layer Perceptrons</h1>"""

# Reshape image arrays
x_train6=(x_train6).reshape(-1,150*150)
x_valid6=(x_valid6).reshape(-1,150*150)
x_test6=(x_test6).reshape(-1,150*150)

# Multi-Class Classification
def model():
    model=Sequential()    
    model.add(Dense(128,activation='relu',
                    input_shape=(150*150,)))
    model.add(Dropout(.1))    
    model.add(Dense(1024,activation='relu'))
    model.add(Dropout(.1))    
    model.add(Dense(15,activation='softmax'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',metrics=['accuracy'])
    return model
model=model()
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,verbose=2,factor=.5)
history=model.fit(x_train6,c_y_train6,
                  validation_data=(x_valid6,c_y_valid6),
                  epochs=70,batch_size=64,verbose=0,
                  callbacks=[checkpointer,lr_reduction])
model.load_weights(fw)
model.evaluate(x_test6,c_y_test6)

loss_plot(history); acc_plot(history)

# Regression
def model():
    model=Sequential()    
    model.add(Dense(52,activation='relu',
                    input_shape=(13,)))    
    model.add(Dense(52,activation='relu'))     
    model.add(Dense(208,activation='relu'))
    model.add(Dense(208,activation='relu'))    
    model.add(Dense(832,activation='relu'))    
    model.add(Dense(1))
    model.compile(optimizer='rmsprop',
                  loss='mse',metrics=['mae'])     
    return model

model=model()
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,verbose=2,factor=.5)
history=model.fit(x_train4,y_train4,
                  validation_data=(x_valid4,y_valid4),
                  epochs=100,batch_size=16,verbose=0,
                  callbacks=[checkpointer,lr_reduction])
model.load_weights(fw)
model.evaluate(x_test4,y_test4)

y_test4_predictions=model.predict(x_test4)
pl.figure(figsize=(10,3))
pl.plot(range(len(y_test4)),y_test4,'-o',
        label='real data')
pl.plot(range(len(y_test4)),y_test4_predictions,'-o',
        label='predictions');

# Text Classification
def model():
    model=Sequential()    
    model.add(Dense(128,activation='relu',
                    input_shape=(101322,)))
    model.add(Dropout(rate=.1))    
    model.add(Dense(1024,activation='relu'))
    model.add(Dropout(rate=.1))    
    model.add(Dense(20,activation='softmax'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model
model=model()
early_stopping=EarlyStopping(monitor='val_loss',patience=20)
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,verbose=2,factor=.8)
history=model.fit(x_train3,c_y_train3,
                  validation_data=(x_valid3,c_y_valid3),
                  epochs=30,batch_size=128,verbose=0,
                  callbacks=[early_stopping,checkpointer,lr_reduction])

model.load_weights(fw)
y_test3_predictions=model.predict_classes(x_test3)
pl.figure(figsize=(10,3))
pl.scatter(range(100),y_test3[:100],s=100)
pl.scatter(range(100),y_test3_predictions[:100],s=25)
model.evaluate(x_test3,c_y_test3)

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Convolutional Neural Networks</h1>"""

# VGG-like CNN: Multi-Class Classification
def model():
    model=Sequential()
    model.add(Conv2D(32,(5,5),padding='same',
                     input_shape=x_train8.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32,(5,5)))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(.25))
    model.add(Conv2D(96,(5,5), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(96,(5,5)))
    model.add(Activation('relu'))    
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(.25))
    model.add(GlobalMaxPooling2D())    
    model.add(Dense(512,activation='relu'))
    model.add(Dropout(.5))    
    model.add(Dense(33))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', 
                  optimizer='adam',metrics=['accuracy'])    
    return model

model=model()
estopping=EarlyStopping(monitor='val_loss',patience=20)
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,verbose=2,factor=.8)
history=model.fit(x_train8,c_y_train8,
                  validation_data=(x_valid8,c_y_valid8),
                  epochs=50,batch_size=256,verbose=0,
                  callbacks=[checkpointer,lr_reduction,estopping])
model.load_weights(fw)
model.evaluate(x_test8,c_y_test8)

steps,epochs=1000,5
data_generator=kimage\
.ImageDataGenerator(zoom_range=.2,rotation_range=20)
dg_history=\
model.fit_generator(data_generator.flow(x_train8,c_y_train8,
                                        batch_size=256),
                    steps_per_epoch=steps,epochs=epochs,verbose=2, 
                    validation_data=(x_valid8,c_y_valid8),
                    callbacks=[checkpointer,lr_reduction])

model.load_weights(fw)
model.evaluate(x_test8,c_y_test8)

# CNN: Regression
def model():
    model=Sequential()    
    model.add(Conv1D(52,5,padding='valid',
                     activation='relu',input_shape=(13,1)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(.2))
    model.add(Conv1D(208,3,padding='valid',
                     activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(.2))    
    model.add(Flatten())
    model.add(Dense(1024,kernel_initializer='normal',
                    activation='relu'))
    model.add(Dropout(.4))
    model.add(Dense(1, kernel_initializer='normal'))    
    model.compile(loss='mse',optimizer='rmsprop',
                  metrics=['mae'])
    return model

model=model()
estopping=EarlyStopping(monitor='val_loss',patience=20)
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,verbose=2,factor=.95)
history=model.fit(x_train4.reshape(-1,13,1),y_train4, 
                  validation_data=(x_valid4.reshape(-1,13,1),
                                   y_valid4),
                    epochs=300,batch_size=16,verbose=0,
                    callbacks=[checkpointer,lr_reduction,estopping])
model.load_weights(fw)
model.evaluate(x_test4.reshape(-1,13,1),y_test4)

y_test4_predictions=\
model.predict(x_test4.reshape(-1,13,1))
pl.figure(figsize=(10,3))
pl.plot(range(len(y_test4)),y_test4,'-o',
        label='real data')
pl.plot(range(len(y_test4)),
        y_test4_predictions,'-o',
        label='predictions')
pl.legend();

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Recurrent Neural Networks</h1>"""

# RNN: Multi-Class Classification
def model():
    model=Sequential()
    model.add(LSTM(112,return_sequences=True,
                   input_shape=(1,784)))    
    model.add(LSTM(112,return_sequences=True)) 
    model.add(LSTM(112))      
    model.add(Dense(10,activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',metrics=['accuracy'])    
    return model

model=model()
estopping=EarlyStopping(monitor='val_loss',patience=20)
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,verbose=2,factor=.5)
history=model.fit(x_train2.reshape(-1,1,784),c_y_train2, 
                  validation_data=(x_valid2.reshape(-1,1,784),
                                   c_y_valid2),
                  epochs=10,batch_size=128,verbose=0,
                  callbacks=[checkpointer,lr_reduction,estopping])
model.load_weights(fw)
model.evaluate(x_test2.reshape(-1,1,784),c_y_test2)

# RNN: Regression
def model():
    model=Sequential()    
    model.add(LSTM(52,return_sequences=True,
                   input_shape=(1,13)))
    model.add(LSTM(208,return_sequences=False))       
    model.add(Dense(1))
    model.compile(optimizer='rmsprop',
                  loss='mse',metrics=['mae'])  
    return model

model=model()
estopping=EarlyStopping(monitor='val_loss',patience=20)
checkpointer=ModelCheckpoint(filepath=fw,save_best_only=True)
lr_reduction=ReduceLROnPlateau(monitor='val_loss',
                               patience=5,verbose=2,factor=.95)
history=model.fit(x_train4.reshape(-1,1,13),y_train4, 
                  validation_data=(x_valid4.reshape(-1,1,13),
                                   y_valid4),
                  epochs=400,batch_size=16,verbose=0,
                  callbacks=[checkpointer,estopping,lr_reduction])
model.load_weights(fw)
model.evaluate(x_test4.reshape(-1,1,13),y_test4)

y_test4_predictions=\
model.predict(x_test4.reshape(-1,1,13))
pl.figure(figsize=(10,3))
pl.plot(range(len(y_test4)),y_test4,'-o',
        label='real data')
pl.plot(range(len(y_test4)),y_test4_predictions,
        '-o',label='predictions')
pl.legend();

"""<h1 style="color:#ff603b; font-family:Ewert; font-size:120%;" class="font-effect-3d">Applications</h1>"""

# ResNet50
fn = '../input/resnet50/'+\
'resnet50_weights_tf_dim_ordering_tf_kernels.h5'
resnet50_model=ks.applications.resnet50\
.ResNet50(weights=fn)

fn2='../input/image-examples-for-mixed-styles/cat.png'
fn3='../input/resnet50/imagenet_class_index.json'
cat_image=kimage.load_img(fn2,target_size=(224,224))
CLASS_INDEX=None
def decode_predictions(preds,fpath,top=5):
    global CLASS_INDEX
    if len(preds.shape)!=2 or preds.shape[1]!=1000:
        raise ValueError('`decode_predictions` expects '
                         'a batch of predictions '
                         '(i.e. a 2D array of shape (samples, 1000)). '
                         'Found array with shape: '+str(preds.shape))
    if CLASS_INDEX is None:
        CLASS_INDEX=json.load(open(fpath))
    results=[]
    for pred in preds:
        top_indices=pred.argsort()[-top:][::-1]
        result=[tuple(CLASS_INDEX[str(i)])+(pred[i],) 
                for i in top_indices]
        results.append(result)
    return results

x=kimage.img_to_array(cat_image)
x=np.expand_dims(x,axis=0)
x=ks.applications.resnet50.preprocess_input(x)
cat_predictions=resnet50_model.predict(x)
print('Predictions:\n',
      decode_predictions(cat_predictions,fn3)[0])
cv_cat_image=cv2.imread(fn2)
rgb_cat_image=\
cv2.cvtColor(cv_cat_image,cv2.COLOR_BGR2RGB)
pl.imshow(rgb_cat_image);

# InceptionV3
fn='../input/keras-applications-weights/'+\
'inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5'
iv3_base_model=\
ks.applications.InceptionV3(weights=fn,
                            include_top=False)
x=iv3_base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(512,activation='relu')(x)
y=Dense(10,activation='softmax')(x)
iv3_model=Model(inputs=iv3_base_model.input,
                outputs=y)

# Freeze InceptionV3 convolutional layers
for layer in iv3_base_model.layers:
    layer.trainable =False
iv3_model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

# Train
steps,epochs=189,10
data_generator=kimage\
.ImageDataGenerator(shear_range=.2,zoom_range=.2,
                    horizontal_flip=True)
checkpointer=\
ModelCheckpoint(filepath=fw,verbose=2,
                save_best_only=True)
lr_reduction=\
ReduceLROnPlateau(monitor='val_loss',
                  patience=5,verbose=2,factor=.5)
history=iv3_model.fit_generator(data_generator\
.flow(x_train7,c_y_train7,batch_size=64),\
steps_per_epoch=steps,epochs=epochs,\
callbacks=[checkpointer,lr_reduction],\
validation_data=(x_valid7,c_y_valid7))

# Unfreeze InceptionV3 convolutional layers
for layer in iv3_model.layers[:173]:
    layer.trainable=False
for layer in iv3_model.layers[173:]:
    layer.trainable=True
iv3_model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

# Train
history=iv3_model.fit_generator(data_generator\
.flow(x_train7,c_y_train7,batch_size=64),\
steps_per_epoch=steps,epochs=epochs,\
callbacks=[checkpointer,lr_reduction],\
validation_data=(x_valid7,c_y_valid7))

# Evaluate 
iv3_model.load_weights(fw)
iv3_test_scores=\
iv3_model.evaluate(x_test7,c_y_test7)
print("Accuracy: %.2f%%"%(iv3_test_scores[1]*100))