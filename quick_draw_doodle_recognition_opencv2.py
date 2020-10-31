# -*- coding: utf-8 -*-
"""quick-draw-doodle-recognition-opencv2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14OlTkCm7MKMfteyVSJdRBtY1YqIvs2AM
"""

# Commented out IPython magic to ensure Python compatibility.
from IPython.display import display,HTML
def dhtml(str):
    display(HTML("""<style>
    @import 'https://fonts.googleapis.com/css?family=Smokum&effect=3d';      
    </style><h1 class='font-effect-3d' 
    style='font-family:Smokum; color:#aa33ff; font-size:35px;'>
#     %s</h1>"""%str))

dhtml('Code Library, Style, and Links')

"""The previous notebook => [Quick, Draw! Doodle Recognition OpenCV1](https://www.kaggle.com/olgabelitskaya/quick-draw-doodle-recognition-1)"""

# Commented out IPython magic to ensure Python compatibility.
# %%html
# <style>
# @import url('https://fonts.googleapis.com/css?family=Ewert|Roboto&effect=3d|ice|');
# span {font-family:'Roboto'; color:black; text-shadow: 5px 5px 5px #aaa;}  
# div.output_area pre{font-family:'Roboto'; font-size:110%; color: steelblue;}      
# </style>

import numpy as np,pandas as pd,keras as ks
import os,ast,cv2,warnings
import pylab as pl
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,\
classification_report
from keras.callbacks import ModelCheckpoint,\
ReduceLROnPlateau
from keras.models import Sequential
from keras.layers.advanced_activations import LeakyReLU
from keras.layers import Activation,Dropout,Dense,\
Conv2D,MaxPooling2D,GlobalMaxPooling2D
warnings.filterwarnings('ignore')
pl.style.use('seaborn-whitegrid')
style_dict={'background-color':'gainsboro','color':'#aa33ff', 
            'border-color':'white','font-family':'Roboto'}
fpath='../input/quickdraw-doodle-recognition/train_simplified/'
wpath='../input/quick-draw-model-weights-for-doodle-recognition/'+\
      'weights_cv/weights_cv/'
tpath='../input/quickdraw-doodle-recognition/test_simplified.csv'
os.listdir("../input")

dhtml('Data Exploration')

files=sorted(os.listdir(fpath))
labels=[el.replace(" ","_")[:-4] for el in files]
print(labels)

weights=sorted(os.listdir(wpath))
print(weights)

I=64 # image size in pixels
T=20 # number of labels in one set

dhtml('The Model')

def model():
    model=Sequential()
    model.add(Conv2D(32,(5,5),padding='same',
                     input_shape=(I,I,1)))
    model.add(LeakyReLU(alpha=.02))   
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(.2))
    model.add(Conv2D(196,(5,5)))
    model.add(LeakyReLU(alpha=.02))  
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(.2))
    model.add(GlobalMaxPooling2D())   
    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=.02))
    model.add(Dropout(.5))   
    model.add(Dense(T))
    model.add(Activation('softmax'))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    return model
model=model()

dhtml('Test Predictions')

def get_image(data,lw=7,time_color=True):
    data=ast.literal_eval(data)
    image=np.zeros((300,300),np.uint8)
    for t,s in enumerate(data):
        for i in range(len(s[0])-1):
            color=255-min(t,10)*15 if time_color else 255
            _=cv2.line(image,(s[0][i]+15,s[1][i]+15),
                       (s[0][i+1]+15,s[1][i+1]+15),color,lw) 
    return cv2.resize(image,(I,I))

def test_predict(data):
    images=[]
    images.extend([get_image(data.drawing.iloc[i]) 
                   for i in range(len(data))])    
    images=np.array(images)
    model.load_weights(wpath+weights[0])
    predictions=model.predict(images.reshape(-1,I,I,1))
    for w in weights[1:]:
        w=wpath+w
        model.load_weights(w)
        predictions2=model.predict(images.reshape(-1,I,I,1))
        predictions=np.concatenate((predictions,predictions2),
                                   axis=1)        
    return predictions

test_data=pd.read_csv(tpath,index_col='key_id')
test_data.tail(3).T.style\
.set_properties(**style_dict)

test_predictions=test_predict(test_data)
test_predictions[0]

test_labels=[[labels[i] for i in \
              test_predictions[k].argsort()[-10:][::-1]] \
             for k in range(len(test_predictions))]
test_labels=[" ".join(test_labels[i]) \
             for i in range(len(test_labels))]
presubmission=pd.DataFrame({"key_id":test_data.index,
                            "word":test_labels})
presubmission.to_csv('submission_10best.csv',index=False)

def display_drawing(n):
    pl.figure(figsize=(4,2*n))
    pl.suptitle('Test Pictures')
    for i in range(n):
        picture=ast.literal_eval(
            test_data.drawing.values[i])
        for x,y in picture:
            pl.subplot(n,1,i+1)
            pl.plot(x, y,'-o',color='gainsboro')
            pl.xticks([]); pl.yticks([])
            pl.title(presubmission.iloc[i][1])
        pl.gca().invert_yaxis()
        pl.axis('equal')

display_drawing(10)

test_labels=[[labels[i] for i in \
              test_predictions[k].argsort()[-3:][::-1]] \
             for k in range(len(test_predictions))]
test_labels=[ " ".join(test_labels[i]) 
             for i in range(len(test_labels))]
submission=pd.DataFrame({"key_id":test_data.index,
                         "word":test_labels})
submission.to_csv('submission.csv',index=False)
submission.head(10).style\
.set_properties(**style_dict)