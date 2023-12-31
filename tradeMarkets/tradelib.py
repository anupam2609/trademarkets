

#Trade Market Initiative codespace
    #This library is one stop solution to all the trade market initiative development calls with multiple planned api integration.
    #This will serve as one class import to master development, app development all other components.


    #libraries to be imported
from email.quoprimime import quote
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from yahoo_fin import stock_info as si
from datetime import date
from datetime import datetime
import requests
import json
from pandas import json_normalize 
from apiKeyEncryption import seed



#latest updates and code capabilities
        #updated 21/11/2022 : Adding liveStockPrice Feature Function
#-------------------------------****************---------------------------------------------------------
#get the live stock price in dataframe




#Class definitions
class tradelibpy:


    def __init__(self):
        self.current_date=date.today()
        self.current_time=datetime.now()
        self.apikey= seed
    
        #Later we will be planning to add the stockticker to self function for ease of use through out the other functions



        #get live stock price
    def getlivestockprice(self, stockticker):
        #stockticker input is a list format and takes strings
        for ticks in stockticker:
            print(f"============ ",{ticks}," ============")
            print(si.get_live_price(ticks))
            print("\n")



        #get live stock data
    def getliveqoutedata(self, stockticker):
        for ticks in stockticker:
            print("Stock Quote data for:", ticks+" "+"\n")
            df=si.get_quote_table(ticks, dict_result=False)
            print(df)
            print("\n")
            return df

       #get live stock data accpeting only one string value
    def getLiveSingleQoutedata(self, value):
        #print("Stock Quote data for:", value+" "+"\n")
        df=si.get_quote_table(value, dict_result=False)
        #print(df)
        #print("\n")
        return df



        #export data for each stock you passed in a single dataframe
    def exportlivestockdata(self, stockticker):
        datatoexport=pd.DataFrame(columns=['Ticker','attribute','value','Pull_Date','Pull_Time'])
        for ticks in stockticker:
            quote_price=pd.DataFrame()
            quote_price=si.get_quote_table(ticks, dict_result=False)
            quote_price['Ticker']=ticks
            quote_price['Pull_Date']=date.today()
            quote_price['Pull_Time']=self.current_time.time()
            quote_price=quote_price[['Ticker','attribute','value','Pull_Date','Pull_Time']]
            #quote_price.to_csv(ticks+"_"+str(self.current_date)+".csv")
            datatoexport=pd.concat([datatoexport,quote_price], axis=0)
        return datatoexport

            

        #livefeature update in progress
    def liveStockPirce(self):
            #initial code in TestCode.ipynb. Reference below
        pass


    def getTimeSeriesMonthlyStockData(self, stock_val, start_date, end_date):
        #"""This Function will help download historical stock data by month from AlphaVantage API Key and return a json extract"""
        # func='TIME_SERIES_MONTHLY'
        # symbol='SBIN.BSE'
        stock_val=stock_val
        url= 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+stock_val+'&interval=5min&apikey='+self.apikey
        r = requests.get(url)
        data = r.json()
        monthlydata=data['Monthly Time Series']
        #data formatting
        total_rec=[]
        for data in monthlydata:
            temp={
                'datepart':'',
                'open':'',
                'close':'',
                'high':'',
                'low':'',
                'volume':''
            }
            temp['datepart']=data
            temp["open"]=monthlydata[data]["1. open"]
            temp["close"]=monthlydata[data]["4. close"]
            temp["high"]=monthlydata[data]["2. high"]
            temp["low"]=monthlydata[data]["3. low"]
            temp["volume"]=monthlydata[data]["5. volume"]
            total_rec.append(temp)
        dataF=pd.DataFrame(total_rec)
        start_date=start_date
        end_date=end_date
        dataF=dataF[(dataF.datepart>=start_date) | (dataF.datepart>=end_date)]
        return dataF


    def getTimeSeriesWeeklyStockData(self, stock_val, start_date, end_date):
        #"""This Function will help download historical stock data by Week from AlphaVantage API Key and return a json extract"""
        # func='TIME_SERIES_MONTHLY'
        # symbol='SBIN.BSE'
        stock_val=stock_val
        url2='https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+stock_val+'&apikey=' + self.apikey
        r = requests.get(url2)
        data = r.json()
        monthlydata=data['Weekly Time Series']
        #data formatting
        total_rec=[]
        for data in monthlydata:
            temp={
                'datepart':'',
                'open':'',
                'close':'',
                'high':'',
                'low':'',
                'volume':''
            }
            temp['datepart']=data
            temp["open"]=monthlydata[data]["1. open"]
            temp["close"]=monthlydata[data]["4. close"]
            temp["high"]=monthlydata[data]["2. high"]
            temp["low"]=monthlydata[data]["3. low"]
            temp["volume"]=monthlydata[data]["5. volume"]
            total_rec.append(temp)
        dataF=pd.DataFrame(total_rec)
        start_date=start_date
        end_date=end_date
        dataF=dataF[(dataF.datepart>=start_date) | (dataF.datepart>=end_date)]
        return dataF


    def getTimeSeriesDailyStockData(self, ticker_, startDate, endDate):
            #The function helps in getting daily stock data for a specified date period.
            #This is an Alphavantage API Call
        
        dailyUrl    =   'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ ticker_ + '&outputsize=full' +'&apikey='   +   self.apikey
        readDailyUrl    =   requests.get(dailyUrl)
        dailyData       =   readDailyUrl.json()
        dailyData       =   dailyData['Time Series (Daily)']
        total_rec=[]
        for vals in dailyData:
            temp={
                'datepart':'',
                'open':'',
                'close':'',
                'high':'',
                'low':'',
                'volume':''
            }
            temp['datepart']=vals
            temp["open"]=dailyData[vals]["1. open"]
            temp["close"]=dailyData[vals]["4. close"]
            temp["high"]=dailyData[vals]["2. high"]
            temp["low"]=dailyData[vals]["3. low"]
            temp["volume"]=dailyData[vals]["5. volume"]
            total_rec.append(temp)
        dailyData_df    =   pd.DataFrame(total_rec)
        start_date      =   startDate
        end_date        =   endDate
        dataF           =   dailyData_df[(dailyData_df.datepart>=start_date) | (dailyData_df.datepart>=end_date)]
        
        return dataF

    
    def getUSTopGainersAlpha(self):
            #the func gets you the top 20 gainers of the day for US Market using Alphavantage API
        urlGetIndTopGainers =   'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=' + self.apikey
        readTG              =   requests.get(urlGetIndTopGainers)
        extract             =   readTG.json()
        metadataTG            =   extract['metadata']
        lastUpdatedTG         =   extract['last_updated']
        data                =   extract['top_gainers']
        topGainers_df       =   pd.DataFrame(data)

            # Sorting the dataframe in descending order by Change Percentage
        topGainers_df['change_percentage']    = topGainers_df['change_percentage'].str.rstrip("%").astype(float)/100
        topGainers_df.sort_values(by=['change_percentage'], ascending=False, inplace=True)

        return topGainers_df
    
    def getUSTopLosersAlpha(self):
            #the func gets you the top 20 Losers of the day for US Market using AlphaVantage
        urlGetIndTopLosers =   'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=' + self.apikey
        readTL              =   requests.get(urlGetIndTopLosers)
        extract             =   readTL.json()
        metadataTL          =   extract['metadata']
        lastUpdatedTL        =   extract['last_updated']
        data                =   extract['top_losers']
        topLosers_df       =   pd.DataFrame(data)

            # Sorting the dataframe in descending order by Change Percentage
        topLosers_df['change_percentage']    = topLosers_df['change_percentage'].str.rstrip("%").astype(float)/100
        topLosers_df.sort_values(by=['change_percentage'], ascending=True, inplace=True)

        return topLosers_df












#Information on functions and process to call them