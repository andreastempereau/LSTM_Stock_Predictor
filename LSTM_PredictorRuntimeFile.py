import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import LSTM_Predictor

def testOne():
     LSTM_Predictor.closePricePlot()
def testTwo():
     LSTM_Predictor.trainingDataFunction()


# Please Input which function you would like to run by uncommenting either one. Test One will run by default...

testOne()
# testTwo()