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
df = pd.read_csv('heartbeat-data/ptb-400hz_abnormal-v1.csv', header=None)
df2 = pd.read_csv('heartbeat-data/ptb-400hz_normal-v1.csv', header=None)
df = pd.concat([df, df2], axis=0)
print(df.shape)
print(df.head())
print(df[800].value_counts())

M = df.values
X = M[:, :-1]
Y = M[:, -1]
del df
del df2
C0 = np.argwhere(Y==0).flatten()
C1 = np.argwhere(Y==1).flatten()

#Generate more data for normal heartbeats (class 0)
var = np.apply_along_axis(pf.gen_new_data, axis=1, arr=X[C0], factor=1, samples=len(X[0])).reshape(-1, len(X[0]))
tag = np.zeros(shape=(var.shape[0],), dtype=int)
X = np.vstack([X, var])
Y = np.hstack([Y, tag])
C0 = np.argwhere(Y==0).flatten() #Reidentify location of class 0 items

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
# model = models.Sequential()
# model.add(layer=layers.Input(batch_shape=X_train.shape, input_shape=(samples, depth)))
# model.add(layer=layers.Conv1D(filters=32, kernel_size=5, strides=1))
# model.add(layer=layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same', activation='relu'))
# model.add(layer=layers.Conv1D(filters=32, kernel_size=5, strides=1, padding='same'))
# model.add(layer=layers.Add())

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
D3 = layers.Dense(2)(D2)
A6 = layers.Softmax()(D3)

model = models.Model(inputs=inp, outputs=A6)
model.summary()


model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
history = model.fit(X_train, Y_train, 
                    epochs=45, 
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

model.save('models/model-400hz-win2s-v1.h5')
print("Model Saved to models folder")