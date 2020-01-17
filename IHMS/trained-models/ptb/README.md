# Trained PTB Models

## Model Descriptions

### PTB 55Hz

#### General Info

- **training_set:** PTB-55hz (Details in notes)
- **sampling_frequency:** 55hz
- **beat_window_length:** 2 seconds (110 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 146776 training, 3000 validation, 1000 test
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

- **training_set:** PTB-60hz (Details in notes)
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

- **PTB-v1**
    - The test samples seperated from the original dataset
    - **samples:** 1000
    - **accuracy:** 99.8%
    - **errors:** 2 total, 1 false negative, 1 false positive

- **PTB-v6**
    - Same as training (PTB-v5) dataset except heartbeats extracted from a different part of the recordings. Entirely distinct from PTB-v5
    - **samples:** 6935
    - **accuracy:** 99.971%
    - **errors:** 4 total, 2 false negative, 2 false positive

