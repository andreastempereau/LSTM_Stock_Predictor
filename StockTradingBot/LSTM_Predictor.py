# This uses LSTM to try and predict closing price of certain stock.
# These certain stocks can be changed via the code and website pathway.

import math
import re
from keras.engine import training
import pandas_datareader as web
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def closePricePlot():
     # Stock quote get...
     df = web.DataReader('AAPL', data_source='yahoo', start = '2014-01-01', end='2021-10-18')
     # The data is shaped in almost over 2000 rows from 2014 to Present
     # I will attempt to close and narrow in on data I actually need
     # Show data in a handy dandy chart using matplotlib
     plt.figure(figsize=(16,8))
     plt.title('Close Price History of Apple')
     plt.plot(df['Close'])
     plt.xlabel('Date', fontsize=18)
     plt.ylabel('Close Price USD ($)', fontsize = 18)
     plt.show()
     print('First Section Run: OK')
     # Narrowed down on Close Price
     data = df.filter                                  (['Close'])
     #This filter can be changed by changing whatever in this  /\/\

def trainingDataFunction():
     df = web.DataReader('AAPL', data_source='yahoo', start = '2014-01-01', end='2021-10-18')
     # Need to redefine /\ as the original is in a seperate function

     data = df.filter(['Close'])

     dataset = data.values    # Changing into numpy array

     # Creating the rows for the model to train with
     training_data_len = math.ceil(  len(dataset) * .8  )
     print(training_data_len)
     # /\ This gives us the scale to give to the model. Can Change...

     scaler = MinMaxScaler(feature_range=(0,1))
     scaled_data = scaler.fit_transform(dataset)
     train_data = scaled_data[0:training_data_len , :]
     x_train = []
     y_train = []

     for i in range(60, len(train_data)):
          x_train.append(train_data[i-60:i, 0])
          y_train.append(train_data[i, 0])
          if i<= 60:
               print(x_train)
               print(y_train)
               print()

     x_train, y_train = np.array(x_train), np.array(y_train)
     x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
     print(x_train.shape)

     # Building the model
     model = Sequential()
     model.add(LSTM(50, return_sequences=True, input_shape= (x_train.shape[1], 1)))
     model.add(LSTM(50, return_sequences=False))
     model.add(Dense(25))
     model.add(Dense(1))

     # Compiling the model just built
     model.compile(optimizer='adam', loss='mean_squared_error')

     # Train the model
     model.fit(x_train, y_train, batch_size=1, epochs=1)

     # Create the the testing data set
     # Create a new array containing scaled values from index 1543 to 2003
     test_data = scaled_data[training_data_len - 60: , :]
     # Create dataset x_test and y_test to run the network properly
     x_test = []
     y_test = dataset[training_data_len:, :]
     for i in range(60, len(test_data)):
          x_test.append(test_data[i-60:i, 0])
     
     # I want to convert data into nice numpy array
     x_test = np.array(x_test)

     # Shape the data from 2D to 3D
     x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

     # Need to now get the model's price values (Predicted values)
     predictions = model.predict(x_test)
     predictions = scaler.inverse_transform(predictions)

     # Get the root mean squared error (RSME) -- how accurate model predicts the response and works to make a better fit
     rsme = np.sqrt(np.mean(predictions - y_test)**2)
     
     # Plot the data we just all got so dummies can read it
     train = data[:training_data_len]
     valid = data[training_data_len:]
     valid['Predictions'] = predictions

     # Visualize the data
     plt.figure(figsize=(16,8))
     plt.title('Model')
     plt.xlabel('Date', fontsize=18)
     plt.ylabel('Closing Price USD', fontsize=18)
     plt.plot(train['Close'])
     plt.plot(valid[['Close', 'Predictions']])
     plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
     plt.show()

     # Section warning
     print('SECTION TWO COMPLETE')
     print('RUNNING PREDICTIONS')

     # Uncomment lower line to show valid and predicted price in numbers
     # print(valid)

     # Get the quote
     apple_quote = web.DataReader('APPL', data_source='yahoo', start='2014-01-01', end='2021-10-22')
     # Create new dataframe
     new_df = apple_quote.filter(['Close'])

     # Get the last 60 day close price values and convert dataframe into an array
     last_60_days = new_df[-60:].values

     # Scale the data to be values between 0 and 1
     last_60_days_scaled = scaler.transform(last_60_days)

     # Create an empty list
     X_test = []

     # Append the part 60 days
     X_test.append(last_60_days_scaled)

     # Convert the X_test into nice numpy array
     X_test = np.array(X_test)
     X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

     # Get predicted scale price
     pred_price = model.predict(X_test)
     # Undo the scaler
     pred_price = scaler.inverse_transform(pred_price)
     print(pred_price)

     # Section finish
     print('TOTAL RUNTIME COMPLETE')