# Trained PTB Models

## Model Descriptions

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

