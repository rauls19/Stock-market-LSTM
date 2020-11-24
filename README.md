# Overview

LSTM (Long Short-Term Memory) is a type of Recurrent neural Networks (RNN). These kind of networks process sequential data, it learns the input data by iterating a sequence of elements and acquires the state information regarding the observed part of the elements. You can use them in order to predict the fluctuation of the stock's market.
This code performs an analysis about Symbol's historical data to understand directional stock movements.

# Objective

The main purpose is educational.

# Requirements

- keras
- pandas
- numpy
- scikit-learn

I use mini conda for creating an environment with all the requirements. Follow the next tutorial to create it [[Reference](https://docs.conda.io/en/latest/miniconda.html)]

# Files

- guiFinancial.py
- Modelling_Analysis.py
- Financial_Data.py

To run the project, execute guiFinancial.py

# Usage

- Execute guiFinancial.py
- Select a symbol from stock market
- Analyse the data

The program will show a table with the current close and the prediction values.

