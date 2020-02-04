# Trained Models on the MIT-BIH Arrhythmia Database

## Model Descriptions

### MIT 60Hz

#### General Info

- **training_set:** MIT-60hz (Details in notes)
- **sampling_frequency:** 60hz
- **beat_window_length:** 2 seconds (400 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 115292 training, 5000 validation, 5000 test
- **notes:**
    - More data was generated for classes 1 and 3. 90527 Normal  cases
    - Had to remove the last block of layers from neural net (Layer C51 to M51)

####  Test Results

- **MIT-60hz**
    - The test samples seperated from the original dataset
    - **samples:** 5000
    - **accuracy:** 93.960%
    - **errors:** 302 total

### MIT 100Hz

#### General Info

- **training_set:** MIT-100hz (Details in notes)
- **sampling_frequency:** 100hz
- **beat_window_length:** 2 seconds (200 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 115256 training, 5000 validation, 5000 test
- **notes:**
    - More data was generated for classes 1 and 3. 90527 Normal  cases
    - Had to remove the last block of layers from neural net (Layer C51 to M51)

####  Test Results

- **MIT-100hz**
    - The test samples seperated from the original dataset
    - **samples:** 5000
    - **accuracy:** 96.920%
    - **errors:** 154 total


### MIT 200Hz

#### General Info

- **training_set:** MIT-200hz (Details in notes)
- **sampling_frequency:** 200hz
- **beat_window_length:** 2 seconds (400 samples)
- **epochs:** 50
- **batch_size:** 500
- **loss:** categorical_crossentropy
- **optimizer:** Adam
- **training_metric:** accuracy
- **dataset_split_ratio:** 115303 training, 5000 validation, 5000 test
- **notes:**
    - More data was generated for classes 1 and 3. 90527 Normal  cases

####  Test Results

- **MIT-200hz**
    - The test samples seperated from the original dataset
    - **samples:** 5000
    - **accuracy:** 97.02%
    - **errors:** 149 total
