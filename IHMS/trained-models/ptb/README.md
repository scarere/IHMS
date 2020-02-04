# Trained PTB Models

## Model Descriptions

### PTB 55Hz

#### General Info

- **training_set:** PTB-55hz-v1 (Details in notes)
- **sampling_frequency:** 55hz
- **beat_window_length:** 2 seconds (110 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14385 training, 3000 validation, 1000 test
- **notes:**
    - 4364 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4364 controls and 9657 abnormal in dataset
    - Had to remove the last block of layers from neural net (Layer C51 to M51)

####  Test Results

- **PTB-55hz-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.2%
    - **errors:** 8 total, 8 false negative

- **PTB-55hz-v2**
    - Same as training (PTB-55hz-v1) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-55hz-v1
    - **samples:** 6988
    - **accuracy:** 97.582%
    - **errors:** 169 total, 60 false positive, 109 false negative

### PTB 60Hz

#### General Info

- **training_set:** PTB-60hz-v1 (Details in notes)
- **sampling_frequency:** 60hz
- **beat_window_length:** 2 seconds (120 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14749 training, 3000 validation, 1000 test
- **notes:**
    - 4350 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4350 controls and 9657 abnormal in dataset
    - Had to remove the last block of layers from neural net (Layer C51 to M51)

####  Test Results

- **PTB-60hz-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 98.7%
    - **errors:** 13 total, 13 false positives

- **PTB-60hz-v2**
    - Same as training (PTB-60hz-v1) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-60hz-v1
    - **samples:** 6978
    - **accuracy:** 98.395%
    - **errors:** 112 total, 103 false positive, 9 false negative

### PTB 75Hz

#### General Info

- **training_set:** PTB-75hz-v1 (Details in notes)
- **sampling_frequency:** 75hz
- **beat_window_length:** 2 seconds (150 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14748 training, 3000 validation, 1000 test
- **notes:**
    - 4360 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4360 controls and 9627 abnormal in dataset

####  Test Results

- **PTB-75hz-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.5%
    - **errors:** 5 total, 2 false negatives, 3 false positives

- **PTB-75hz-v2**
    - Same as training (PTB-75hz-v1) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-75hz-v1
    - **samples:** 6955
    - **accuracy:** 98.519%
    - **errors:** 103 total, 53 false negatives, 50 false positives

### PTB 100Hz

#### General Info

- **training_set:** PTB-100hz-v1 (Details in notes)
- **sampling_frequency:** 100hz
- **beat_window_length:** 2 seconds (200 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14733 training, 3000 validation, 1000 test
- **notes:**
    - 4357 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4357 controls and 9606 abnormal in dataset

####  Test Results

- **PTB-100hz-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.6%
    - **errors:** 4 total, 1 false negatives, 3 false positives

- **PTB-100hz-v2**
    - Same as training (PTB-100hz-v1) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-100hz-v1
    - **samples:** 6958
    - **accuracy:** 98.649%
    - **errors:** 94 total total, 50 false negatives, 44 false positives

### PTB 100Hz Filtered

#### General Info

- **training_set:** PTB-100hz-v1-filt (Details in notes)
- **sampling_frequency:** 100hz
- **beat_window_length:** 2 seconds (200 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14888 training, 3000 validation, 1000 test
- **notes:**
    - PTB-100hz-v1-filt is filtered with an LPF (-3dB cutoff of 22.5Hz, -80dB by 50Hz)
    - 4371 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4371 controls and 9713 abnormal in dataset

####  Test Results

- **PTB-100hz-v1-filt**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.9%
    - **errors:** 1 total, 1 false negatives, 0 false positives

- **PTB-100hz-v2-filt**
    - Same as training (PTB-100hz-v1-filt) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-100hz-v1-filt
    - **samples:** 7005
    - **accuracy:** 97.93%
    - **errors:** 145 total total, 74 false negatives, 71 false positives

### PTB 125Hz

#### General Info

- **training_set:** PTB-100hz-v1 (Details in notes)
- **sampling_frequency:** 125hz
- **beat_window_length:** 1.5 seconds (187 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14989 training, 3000 validation, 1000 test
- **notes:**
    - 4046 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4046 controls and 10506 abnormal in dataset

####  Test Results

- **PTB-100hz-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.3%
    - **errors:** 7 total, 3 false negatives, 4 false positives


### PTB 200Hz

#### General Info

- **training_set:** PTB-v5 (Details in notes)
- **sampling_frequency:** 200hz
- **beat_window_length:** 2 seconds (400 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14687 training, 3000 validation, 1000 test
- **notes:**
    - 4778 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4351 controls and 9558 abnormal in dataset

####  Test Results

- **PTB-v5**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.8%
    - **errors:** 2 total, 1 false negative, 1 false positive

- **PTB-v6**
    - Same as training (PTB-v5) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-v5
    - **samples:** 6935
    - **accuracy:** 99.409%
    - **errors:** 41 total, 20 false negative, 21 false positive

### PTB 300Hz

#### General Info

- **training_set:** PTB-300hz-v1 (Details in notes)
- **sampling_frequency:** 300hz
- **beat_window_length:** 2 seconds (600 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14669 training, 3000 validation, 1000 test
- **notes:**
    - 4360 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4360 controls and 9534 abnormal in dataset

####  Test Results

- **PTB-300hz-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.7%
    - **errors:** 3 total, 1 false negative, 2 false positive

- **PTB-300hz-v2**
   - Same as training (PTB-300hz-v1) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-300hz-v1
    - **samples:** 6922
    - **accuracy:** 99.494%
    - **errors:** 35 total, 6 false negative, 29 false positive


### PTB 300Hz Filtered

#### General Info

- **training_set:** PTB-300hz-v1-filt (Details in notes)
- **sampling_frequency:** 300hz
- **beat_window_length:** 2 seconds (600 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14875 training, 3000 validation, 1000 test
- **notes:**
    - PTB-300hz-v1-filt is filtered with an LPF (-3dB cutoff of 22.5Hz, -80dB by 50Hz)
    - 4376 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4376 controls and 9721 abnormal in dataset

####  Test Results

- **PTB-300hz-v1-filt**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 98.9%
    - **errors:** 11 total, 7 false negative, 4 false positive

- **PTB-300hz-v2**
   - Same as training (PTB-300hz-v1-filt) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-300hz-v1
    - **samples:** 6998
    - **accuracy:** 97.899%
    - **errors:** 147 total, 96 false negative, 51 false positive

### PTB 400Hz

#### General Info

- **training_set:** PTB-v1 (Details in notes)
- **sampling_frequency:** 400hz
- **beat_window_length:** 2 seconds (800 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 14614 training, 3000 validation, 1000 test
- **notes:**
    - 4354 more control samples artificialy generated and introduced into dataset_split_ratio
    - Originially 4354 controls and 9520 abnormal in dataset

####  Test Results

- **PTB-400hz-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.8%
    - **errors:** 2 total, 1 false negative, 1 false positive

- **PTB-400hz-v2**
    - Same as training (PTB-v5) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-v5
    - **samples:** 6935
    - **accuracy:** 99.071%
    - **errors:** 68 total, 36 false negative, 32 false positive

