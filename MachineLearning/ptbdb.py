# Change error settings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import processingFunctions as pf
from sklearn.utils import shuffle
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from keras import models
from keras import layers
from keras import callbacks

#Read csv files. 1 is abnormal, 0 is normal
# df = pd.read_csv('heartbeat-data/ptbdb_abnormal.csv', header=None)
# df2 = pd.read_csv('heartbeat-data/ptbdb_normal.csv', header=None)
df = pd.read_csv('heartbeat-data/ptb-400hz-v1/ptb-400hz_abnormal-v1.csv', header=None)
df2 = pd.read_csv('heartbeat-data/ptb-400hz-v1/ptb-400hz_normal-v1.csv', header=None)
df = pd.concat([df, df2], axis=0)
print(df.shape)
print(df.head())
print(df.iloc[:,-1].value_counts())

M = df.values
X = M[:, :-1]
Y = M[:, -1]
del df
del df2
C0 = np.argwhere(Y==0).flatten()
C1 = np.argwhere(Y==1).flatten()

#Generate more data for normal heartbeats (class 0). Doubles the amount of data
var = np.apply_along_axis(pf.gen_new_data, axis=1, arr=X[C0], factor=1, samples=len(X[0])).reshape(-1, len(X[0]))
tag = np.zeros(shape=(var.shape[0],), dtype=int)
X = np.vstack([X, var])
Y = np.hstack([Y, tag])
C0 = np.argwhere(Y==0).flatten() #Reidentify location of class 0 items

print('After Data Generation:\n1.0 ', np.count_nonzero(Y))
print('0.0', len(Y)-np.count_nonzero(Y), '\n')

#select test set
subC1 = np.random.choice(C1, 2000) #Abnormal
subC0 = np.random.choice(C0, 2000) #Normal


#Split into test and train data
X_test = np.vstack([X[subC0], X[subC1]])
Y_test = np.hstack([Y[subC0], Y[subC1]])
X_train = np.delete(X, [subC0, subC1], axis=0)
Y_train = np.delete(Y, [subC0, subC1], axis=0)
del X
del Y

#Section off some of the test set for a final test. (Split into test set and validation set)
X_val, X_test, Y_val, Y_test = train_test_split(X_test, Y_test, test_size=0.25)

#Shuffle data and transform x into columns by adding a dimension
X_train, Y_train = shuffle(X_train, Y_train, random_state=0)
X_test, Y_test = shuffle(X_test, Y_test, random_state=0)
X_val, Y_val = shuffle(X_val, Y_val, random_state=0)
X_train = np.expand_dims(X_train, 2)
X_test = np.expand_dims(X_test, 2)
X_val = np.expand_dims(X_val, 2)

#One Hot Encode Target Data
ohe = OneHotEncoder()
Y_train = ohe.fit_transform(Y_train.reshape(-1, 1))
Y_test = ohe.fit_transform(Y_test.reshape(-1, 1))
Y_val = ohe.fit_transform(Y_val.reshape(-1, 1))


#Print Input Data Shape
print("X_train: ", X_train.shape)
print("X_val: ", X_val.shape)
print("X_test: ", X_test.shape)
print("Y_train: ", Y_train.shape)
print("Y_val: ", Y_val.shape)
print("Y_test: ", Y_test.shape)


#Build Network
n_entries, samples, depth = X_train.shape
print('\nBuilding Model...')

inp = layers.Input(shape=(samples, depth))
C = layers.Conv1D(filters=32, kernel_size=5, strides=1, name='C')(inp)

C11 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu', name='C11')(C)
C12 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', name='C12')(C11)
S11 = layers.Add(name='S1')([C12, C])
A1 = layers.Activation(activation='relu', name='A1')(S11)
M11 = layers.MaxPooling1D(pool_size=5, strides=2, name='M1')(A1)


C21 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu', name='C21')(M11)
C22 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', name='C22')(C21)
S21 = layers.Add(name='S2')([C22, M11])
A2 = layers.Activation(activation='relu', name='A2')(S21)
M21 = layers.MaxPooling1D(pool_size=5, strides=2, name='M2')(A2)


C31 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu', name='C31')(M21)
C32 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', name='C32')(C31)
S31 = layers.Add(name='S3')([C32, M21])
A3 = layers.Activation(activation='relu', name='A3')(S31)
M31 = layers.MaxPooling1D(pool_size=5, strides=2, name='M3')(A3)


C41 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu', name='C41')(M31)
C42 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', name='C42')(C41)
S41 = layers.Add(name='S4')([C42, M31])
A4 = layers.Activation(activation='relu', name='A4')(S41)
M41 = layers.MaxPooling1D(pool_size=5, strides=2, name='M4')(A4)


C51 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu', name='C51')(M41)
C52 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', name='C52')(C51)
S51 = layers.Add(name='S5')([C52, M41])
A5 = layers.Activation(activation='relu', name='A5')(S51)
M51 = layers.MaxPooling1D(pool_size=5, strides=2, name='M5')(A5)


# C61 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu', name='C61')(M51)
# C62 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', name='C62')(C61)
# S61 = layers.Add(name='S6')([C62, M51])
# A6 = layers.Activation(activation='relu', name='A6')(S61)
# M61 = layers.MaxPooling1D(pool_size=5, strides=2, name='M6')(A6)

F1 = layers.Flatten(name='Flatten')(M51)

D1 = layers.Dense(32, activation='relu', name='D1')(F1)
D2 = layers.Dense(32, name='D2')(D1)
D3 = layers.Dense(2, name='D3')(D2)
A7 = layers.Softmax(name='A7')(D3)

model = models.Model(inputs=inp, outputs=A7)
model.summary()


model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
history = model.fit(X_train, Y_train, 
                    epochs=50, 
                    batch_size=500, 
                    verbose=2, 
                    validation_data=(X_val, Y_val))

print("History Keys: ", history.history.keys())
acc_hist = history.history["val_acc"]
print("Number of Epochs: ", len(acc_hist))
smooth_acc_hist = pf.smoothCurve(acc_hist)
plt.plot(range(1, len(smooth_acc_hist)+1), smooth_acc_hist)
plt.xlabel("Epochs")
plt.ylabel("Validation Acc")
plt.show()

y_pred = model.predict(X_test, batch_size=1000)
print(classification_report(Y_test.argmax(axis=1), y_pred.argmax(axis=1), target_names=["Normal", "Arrythmias"], digits=5))

model.save('models/ptb-400Hz-v2.h5')
print("Model Saved to models folder")