# IHMS

IHMS is the repository for the Intelligent Heart Monitoring System. A Capstone project for the Queen's University Electrical Engineering program in Kingston, ON, CA.

## What is the IHMS

The Intelligent Heart Monitoring System is a project that, using an ECG electrode sensor, will classify abnormal heartbeats in real-time. 

## Repository breakdown

### Dataset-Proc

Dataset-proc is the dataset processing component of the IHMS project. It uses signal processing techniques on raw ECG recordings to create datasets suitable for machine learning. The current raw data being used is from the PTB Diagnostic ECG Database and the MIT-BIH Arrhythmia Database. Purposes include but are not limited to:
  - R-Peak Identification
  - Heartbeat Extraction
  - Signal Frequency Domain Filtering
  - Signal Downsampling
  - Appendage of Labels

### Machine Learning

MachineLearning is the classifier creation and testing component of the IHMS project. In this section, machine learning suitable datasets are used to train machine learning models that can classify different types of arrhythmias. Purposes include but are not limited to:
  - Training Deep Learning Models
  - Model Validation
  - Model Testing
  - Model Performance Visualization

## Contributors

### Shawn Carere
Queen's Electrical Engineering - Biomedical Option  
Class of 2020

Specialties:
  - Machine Learning
  - Signal Processing
  - Software Development

### Ethan Fiset
Queen's Electrical Engineering  
Class of 2020

Specialties:
  - Sensors and Systems

### Brad Kitzul
Queen's Electrical Engineering  
Class of 2020

Specialties:
  - Electronics

### Archana Agashe
Queen's Electrical Engineering  
Class of 2019 (Internship Year)

Specialties:
  - Signal Processing