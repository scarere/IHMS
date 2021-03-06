# Change error settings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
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



#Read csv files. 0 is N, 1 is S, 2 is V, 3 is F, 4 is Q
df = pd.read_csv('heartbeat-data/mit-100hz.csv', header=None)
print(df.shape)
print(df.head())
print(df.iloc[:,-1].value_counts())

M = df.values
X = M[:, :-1]
Y = M[:, -1]
del df
C0 = np.argwhere(Y==0).flatten()
C1 = np.argwhere(Y==1).flatten()
C2 = np.argwhere(Y==2).flatten()
C3 = np.argwhere(Y==3).flatten()
C4 = np.argwhere(Y==4).flatten()

# Generate more data for classes 1, 2 and 3
var1 = np.apply_along_axis(pf.gen_new_data, axis=1, arr=X[C1], factor=2, samples=len(X[0])).reshape(-1, len(X[0]))
tag1 = np.full(shape=(var1.shape[0],), fill_value=1, dtype=int)
var3 = np.apply_along_axis(pf.gen_new_data, axis=1, arr=X[C3], factor=10, samples=len(X[0])).reshape(-1, len(X[0]))
tag3 = np.full(shape=(var3.shape[0],), fill_value=3, dtype=int)
X = np.vstack([X, var1, var3])
Y = np.hstack([Y, tag1, tag3])

classnum, class_counts = np.unique(Y, return_counts=True)
classes = ['Normal', 'Premature', 'Ventricular', 'Fusion of V and N', 'Unclassifiable']
IDs = ['N', 'S', 'V', 'F', 'Q']

print('After Data Generation:')
for index, num in enumerate(classnum):
    print(IDs[int(num)], ' - ', classes[int(num)], ': ', class_counts[index])

#select test set
subC0 = np.random.choice(C0, 2000) 
subC1 = np.random.choice(C1, 2000)
subC2 = np.random.choice(C2, 2000)
subC3 = np.random.choice(C3, 2000)
subC4 = np.random.choice(C4, 2000)

#Split into test and train data
X_test = np.vstack([X[subC0], X[subC1], X[subC2], X[subC3], X[subC4]])
Y_test = np.hstack([Y[subC0], Y[subC1], Y[subC2], Y[subC3], Y[subC4]])
X_train = np.delete(X, [subC0, subC1, subC2, subC3, subC4], axis=0)
Y_train = np.delete(Y, [subC0, subC1, subC2, subC3, subC4], axis=0)
del X
del Y

#Section off some of the test set for a final test. (Split into test set and validation set)
X_val, X_test, Y_val, Y_test = train_test_split(X_test, Y_test, test_size=0.5)

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
C = layers.Conv1D(filters=32, kernel_size=5, strides=1)(inp)

C11 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu')(C)
C12 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(C11)
S11 = layers.Add()([C12, C])
A1 = layers.Activation(activation='relu')(S11)
M11 = layers.MaxPooling1D(pool_size=5, strides=2)(A1)


C21 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu')(M11)
C22 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(C21)
S21 = layers.Add()([C22, M11])
A2 = layers.Activation(activation='relu')(S21)
M21 = layers.MaxPooling1D(pool_size=5, strides=2)(A2)


C31 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu')(M21)
C32 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(C31)
S31 = layers.Add()([C32, M21])
A3 = layers.Activation(activation='relu')(S31)
M31 = layers.MaxPooling1D(pool_size=5, strides=2)(A3)


C41 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu')(M31)
C42 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(C41)
S41 = layers.Add()([C42, M31])
A4 = layers.Activation(activation='relu')(S41)
M41 = layers.MaxPooling1D(pool_size=5, strides=2)(A4)


C51 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu')(M41)
C52 = layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(C51)
S51 = layers.Add()([C52, M41])
A5 = layers.Activation(activation='relu')(S51)
M51 = layers.MaxPooling1D(pool_size=5, strides=2)(A5)

F1 = layers.Flatten()(M51)

D1 = layers.Dense(32, activation='relu')(F1)
D2 = layers.Dense(32)(D1)
D3 = layers.Dense(5)(D2)
A6 = layers.Softmax()(D3)

model = models.Model(inputs=inp, outputs=A6)
model.summary()


model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
history = model.fit(X_train, Y_train, 
                    epochs=50, 
                    batch_size=500, 
                    verbose=1, 
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
print(classification_report(Y_test.argmax(axis=1), y_pred.argmax(axis=1), target_names=['N', 'S', 'V', 'F', 'Q'], digits=5))

model.save('models/mit-100hz.h5')
print("Model Saved to models folder")

