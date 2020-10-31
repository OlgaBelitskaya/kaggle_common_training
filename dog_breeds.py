# -*- coding: utf-8 -*-
"""dog-breeds.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pqj5aEwK5C4-0r6TApPwCPKrsDUqwnkf

## Code Modules
"""

import pandas as pd,numpy as np,pylab as pl
import os,h5py,cv2,tensorflow as tf
import tensorflow_hub as th
from sklearn.model_selection import train_test_split
fpath='../input/image-classification-for-biospecies/'
fw='weights.best.hdf5'

"""## Data"""

f=h5py.File(fpath+'DogBreedImages.h5','r')
keys=list(f.keys()); print(keys)
x_test=np.array(f[keys[0]]); y_test=np.array(f[keys[1]])
x_train=np.array(f[keys[2]]); y_train=np.array(f[keys[3]])
fig=pl.figure(figsize=(11,4))
n=np.random.randint(1,50); n_classes=120
for i in range(n,n+5):
    ax=fig.add_subplot(1,5,i-n+1,\
    xticks=[],yticks=[],title=y_test[i][0])
    ax.imshow((x_test[i]))
cy_train=np.array(tf.keras.utils\
.to_categorical(y_train,n_classes),dtype='int32')
cy_test=np.array(tf.keras.utils\
.to_categorical(y_test,n_classes),dtype='int32')
n=int(len(x_test)/2)
x_valid,y_valid,cy_valid=x_test[:n],y_test[:n],cy_test[:n]
x_test,y_test,cy_test=x_test[n:],y_test[n:],cy_test[n:]
df=pd.DataFrame([[x_train.shape,x_valid.shape,x_test.shape],
                 [x_train.dtype,x_valid.dtype,x_test.dtype],
                 [y_train.shape,y_valid.shape,y_test.shape],
                 [y_train.dtype,y_valid.dtype,y_test.dtype],
                 [cy_train.shape,cy_valid.shape,cy_test.shape],
                 [cy_train.dtype,cy_valid.dtype,cy_test.dtype]],
                 columns=['train','valid','test'],
                 index=['image shape','image type',
                        'label shape','label type',
                        'shape of encoded label',
                        'type of encoded label'])
display(df)

"""## NN Examples
mobilenet_v1_100_128
"""

def premodel(pix,den,mh,lbl):
    model=tf.keras.Sequential([
        tf.keras.layers.Input((pix,pix,3),
                              name='input'),
        th.KerasLayer(mh,trainable=True),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(den,activation='relu'),
        tf.keras.layers.Dropout(rate=.5),
        tf.keras.layers.Dense(lbl,activation='softmax')])
    model.compile(optimizer='adam',metrics=['accuracy'],
                  loss='sparse_categorical_crossentropy')
    display(model.summary())
    return model
def cb(fw):
    early_stopping=tf.keras.callbacks\
    .EarlyStopping(monitor='val_loss',patience=20,verbose=2)
    checkpointer=tf.keras.callbacks\
    .ModelCheckpoint(filepath=fw,save_best_only=True,verbose=2)
    lr_reduction=tf.keras.callbacks\
    .ReduceLROnPlateau(monitor='val_loss',verbose=2,
                       patience=5,factor=.8)
    return [checkpointer,early_stopping,lr_reduction]

[handle_base,pixels]=["mobilenet_v1_100_128",128]
mhandle="https://tfhub.dev/google/imagenet/{}/feature_vector/4"\
.format(handle_base)
fw='weights.best.hdf5'

model=premodel(pixels,1024,mhandle,120)
history=model.fit(x=x_train,y=y_train,batch_size=128,
                  epochs=25,callbacks=cb(fw),
                  validation_data=(x_valid,y_valid))

model.load_weights(fw)
model.evaluate(x_test,y_test)

"""inception_resnet_v2"""

[handle_base,pixels]=["inception_resnet_v2",128]
mhandle="https://tfhub.dev/google/imagenet/{}/classification/4"\
.format(handle_base)
fw='weights.best.hdf5'

model=premodel(pixels,512,mhandle,120)
history=model.fit(x=x_train,y=y_train,batch_size=64,
                  epochs=10,callbacks=cb(fw),
                  validation_data=(x_valid,y_valid))

model.load_weights(fw)
model.evaluate(x_test,y_test)