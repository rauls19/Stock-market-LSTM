import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class ModellingAnalysis:
    def __init__(self):
        self.__model = Sequential()
        self.__days_to_forecast = 2
        self.__n = self.__days_to_forecast +1
        self.__scaler = scaler = MinMaxScaler(feature_range=(0,1))
        self.__x_scalar = ''
        self.__y_scalar = ''
        self.__valid = ''
    
    def __prepareData(self, data):
        X_dataset = data.filter(['Open','High','Low', 'Volume']).values
        X_dataset[:4] = np.log(X_dataset[:4])
        Y_dataset = data.filter(['Close']).values
        self.__valid = data[(len(Y_dataset)-(self.__n-2)):].filter(['Date'])
        self.__valid['Close'] = Y_dataset[(int(len(Y_dataset)-(self.__n-2))):]
        return X_dataset, Y_dataset

    def __scaleData(self, X_data, Y_data):
        return self.__scaler.fit_transform(X_data), self.__scaler.fit_transform(Y_data)
    
    def __splitDataTraining(self, X_scaled, Y_scaled):
        x_train = X_scaled[0:int(len(X_scaled)-(self.__n-1)), :]
        y_train = Y_scaled[self.__n-1:int(len(Y_scaled)), :]
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        return x_train, y_train
    
    def __confTSLM(self, x_train):
        self.__model.add(LSTM(60, recurrent_dropout = 0.1, return_sequences=True, input_shape= (x_train.shape[1], 1)))
        self.__model.add(LSTM(50, return_sequences= False))
        self.__model.add(Dropout(0.2))
        self.__model.add(Dense(1, activation = 'linear'))
        self.__model.compile(optimizer='adam', loss='mean_squared_error', metrics = ['accuracy'])
    
    def modelling(self, data):
        x_data, y_data = self.__prepareData(data)
        self.__x_scalar, self.__y_scalar = self.__scaleData(x_data, y_data)
        x_train, y_train = self.__splitDataTraining(self.__x_scalar, self.__y_scalar)
        self.__confTSLM(x_train)
        self.__model.fit(x_train, y_train, batch_size= 32, epochs= 100)

    def predict(self):
        x_test = self.__x_scalar[len(self.__x_scalar)-(self.__n-2): , :]
        y_test = self.__y_scalar[len(self.__y_scalar)-(self.__n-2): , :]
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = self.__model.predict(x_test)
        self.__valid['Predictions'] = self.__scaler.inverse_transform(predictions)
        self.__valid['Ratio'] = self.__valid['Predictions'].div(self.__valid['Close'].values, axis=0)
        meanRatio = np.mean(self.__valid['Ratio'], axis=0)
        self.__valid['Correction'] = self.__valid['Predictions'].div(meanRatio, axis = 0)
        return self.__valid