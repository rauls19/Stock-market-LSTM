import urllib
import urllib.request
import urllib.error
import pandas as pd
import datetime

class FinancialData:

    def  __init__(self):
        self.__currentsymbol = ''
        self.__symbols = []
        now = datetime.datetime.now()
        self.__periodstart = int(((datetime.datetime(now.year-2, now.month, now.day)-datetime.datetime(1970,1,1))).total_seconds())
        self.__periodend = int(((datetime.datetime(now.year, now.month, now.day+1)-datetime.datetime(1970,1,1))).total_seconds())
        print(self.__periodend)

    def updateCurrentSymbol(self, inputSymbol):
        self.__currentsymbol = inputSymbol
        if inputSymbol not in self.__symbols:
            self.__symbols.append(inputSymbol)
    
    def setCurrentSymbol(self, symbol):
        self.__currentsymbol = symbol

    def getAvailableSymbols(self):
        return self.__symbols

    def getCurrentSymbol(self):
        return self.__currentsymbol
    
    def __updateUrl(self):
        self.__url = 'https://query1.finance.yahoo.com/v7/finance/download/'+self.__currentsymbol+'?period1='+str(self.__periodstart)+'&period2='+str(self.__periodend)+'&interval=1d&events=history&includeAdjustedClose=true'

    def downloadHistoricalDataSymbol(self):
        self.__updateUrl()
        print(self.__url)
        try:
            urllib.request.urlretrieve(self.__url, self.__currentsymbol+'.csv')
        except urllib.error.HTTPError as ex:
            print('Problem', ex)
    
    def readData(self):
        df = pd.read_csv(self.__currentsymbol+'.csv', sep=',')
        df = df.sort_values('Date')
        return df