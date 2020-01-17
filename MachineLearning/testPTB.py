import pandas as pd
import numpy as np
from keras.models import load_model
import time
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle

# Change error settings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
import tensorflow as tf

#Read csv files. 1 is abnormal, 0 is normal
df = pd.read_csv('heartbeat-data/ptb-300hz/ptb-300hz-v2_abnormal.csv', header=None)
df2 = pd.read_csv('heartbeat-data/ptb-300hz/ptb-300hz-v2_normal.csv', header=None)
df = pd.concat([df, df2], axis=0)
print(df.shape)
print(df.iloc[:,-1].value_counts())

# Seperate data and labels
M = df.values
X = M[:, :-1]
Y = M[:, -1]
del df
del df2

# One hot encode labels
Y = OneHotEncoder().fit_transform(Y.reshape(-1, 1))

#Shuffle data and transform x into columns by adding a dimension
X, Y = shuffle(X, Y, random_state=0)
X = np.expand_dims(X, 2)

# Load saved model from disk
print('\n 0s - Loading Model ... \n')
ts = time.time()
model = load_model('models/ptb-300hz.h5')
tc = time.time() - ts
print('\n', tc, 's - Evaluating ', len(X), ' Samples ...\n')
pred = model.predict(X, batch_size=len(X))
print(classification_report(Y.argmax(axis=1), pred.argmax(axis=1), target_names=["Normal", "Arrythmias"], digits=5))
results = classification_report(Y.argmax(axis=1), pred.argmax(axis=1), target_names=["Normal", "Arrythmias"], digits=5, output_dict=True)
errors = len(X) - int(results['accuracy']*len(X))
print('\nThe model made ', errors, ' errors on a dataset with ', len(X), ' samples')
print('The model accuracy is ', results['accuracy']*100, '% \n')






