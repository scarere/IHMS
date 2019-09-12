import random
import numpy as np
from scipy.signal import resample #Stretches or compresses signal to a new length
import math



def stretch(x, samples):
    '''
    Randomly stretches or compresses time series dataset along the time axis by a factor between 0.83 ans 1.17

    Args:
        x: data to be stretched
        samples (int): number of samples for each data entry
    '''
    length = int(samples * (1 + (random.random()-0.5)/3)) 
    y = resample(x, length)
    if length < samples:
        y_ = np.zeros(shape=(samples, ))
        y_[:length] = y
    else:
        y_ = y[:samples]
    return y_

def amplify(x):
    '''
    Randomly amplifies or attenuates time series data by a random factor

    Args:
        x: data to be amplified
    '''
    alpha = (random.random()-0.5)
    factor = -alpha*x + (1+alpha)
    return x*factor

def gen_new_data(x, factor, samples):
    '''
    Generates new data by randomly amplifying or stretching data to create new data entries.

    Args:
        x: time series data to replicate
        factor: factor by which to generate new data. Eg. factor=2 will generate twice the amount of data entries in x
        samples: number of samples for each data entry in x
    '''
    result = np.zeros(shape= (factor, 187))
    for i in range(factor-1):
        if random.random() < 0.33:
            new_y = stretch(x, samples)
        elif random.random() < 0.66:
            new_y = amplify(x)
        else:
            new_y = stretch(x, samples)
            new_y = amplify(new_y)
        result[i, :] = new_y
    return result

def smoothCurve(points, factor=0.9):
    """Replaces each point with an exponential moving average of the previous point to obtain a smooth curve"""
    smoothed_points = []
    for point in points:
        if smoothed_points: #checks if smoothed points is empty
            previous = smoothed_points[-1] #selects last number in list smoothed_points
            smoothed_points.append(previous*factor + point*(1-factor)) #new point is exponential moving average of previous point
        else:
            smoothed_points.append(point) #for the first value, just use the value of the point
    return smoothed_points
