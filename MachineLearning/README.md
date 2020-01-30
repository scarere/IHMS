# Machine Learning

This directory is used to train and test various machine learning models that are used to make predictions in real-time for the IHMS

### mitdb.py:

Trains and tests a neural network from the MIT database. The model classifies heartbeats into 5 different classes and differentiates between different kinds of arrhythmias

### ptdb.py:

Trains and tests a neural network from the PTB database. This model is binary and designates a heartbeat as either normal or abnormal

### plotErrors.py:

Used to plot the performances of various different models

### processingFunctions.py:

Contains functions used to help expand the dataset and even out the distribution of different classes

### testPTB.py

Tests a ptb model on a seperate dataset