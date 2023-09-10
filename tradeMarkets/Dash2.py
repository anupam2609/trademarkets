# This code refers to the current scope being used for TradeMarketInitiative.
    #Style css needs to be added for based on wireframes developed!
    #New features will be added based on the business use case





        #Added libraries 
from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import date
from datetime import timedelta
import json
from tradelib import tradelibpy
import os
import simplyWallScrape as sw

usTopGainers_df=sw.topGainers_df
usSectorTrends=sw.Sector_Trend_US_df
usSectorTrends=usSectorTrends[['Sector', 'Returns']]
 #Content space for pulling any pre requisite data and object setup

tb=tradelibpy() 


ReferenceJsonhere       =       os.path.dirname(os.path.abspath("Reference.json"))
ReferenceJsonFilePath   =       os.path.join(ReferenceJsonhere, 'tradeMarkets/Reference.json')       
RefJsonOpen             =       open(ReferenceJsonFilePath)
ref_js                  =       json.load(RefJsonOpen)


#default_Summary:
defaultSummaryhere      =       os.path.dirname(os.path.abspath("default_summary.csv"))
defaultSummaryFilePath  =       os.path.join(defaultSummaryhere, 'tradeMarkets/default_summary.csv')
defaultSummaryOpen      =       open(defaultSummaryFilePath)
defaultsum              =       pd.read_csv(defaultSummaryFilePath)



app=Dash(__name__)



        #HomePage/LandingPage layout section
app.layout=html.Div(children=   [
           
            html.Div(className="row",
                    children=[
                            
                            ##About US section denotes the Title and the content for project!
                        html.Div(className='aboutUS',
                                children=[
                                    html.H1(''' Welcome to Trade Market Initiative!'''),
                                    html.Div(''' This is a free platform to refer and monitor live and historical trade nuggets to better understand and predict the scenarios''' ),
                                    dcc.Store("startDate-intermediate-value", data='2021-08-01'),
                                    dcc.Store("endDate-intermediate-value", data='2022-08-01'),
                                        ],
                                style={'text-align':'center'}
                                )
                            ]
                    ),      
                            ##Historical Analysis for tickers provided
            html.Div(className='row',
                    children=[
                        html.Div(className='Historical Analysis',
                                children=[
                                    html.Br(),
                                    html.Br(),
                                    html.Div(''' This section provides you the historical data trends of a specified stock over a period of time'''),
                                    html.Div('''Please select if you wish to search Indian or US Market'''),
                                    html.Br(),
                                    dcc.RadioItems(id='radio',options=['Indian Market', 'US Market'], value='US Market', inline=True), # Find a solution to add spaces between radio items
                                    html.Br(),
                                #     dcc.Input(id='marketState', value='US Market', type='text'),
                                    dcc.Input(id='iticker', value='AAPL', type='text'),
                                    html.Button('Submit', id='submit_ticker', n_clicks=0),
                                        ], 
                                style={'text-align':'center'}  
                                ),

                        html.Div(className='datePicker',
                                children=[  html.Br(),
                                            html.Div(className='datePicker_component',
                                                    children=[
                                                            dcc.DatePickerRange(
                                                                        id='my-date-picker-range',
                                                                        min_date_allowed=date(2021, 8, 1),
                                                                        max_date_allowed=date.today(),
                                                                        initial_visible_month=date(2022, 8, 1),
                                                                        end_date=date.today(),
                                                                        start_date=date(2022,8,1)
                                                                        #start_date_placeholder_text='Start Date'
                                                                        #calendar_orientation='vertical'
                                                                                ),
                                                            html.Br(),
                                                            html.Br()
                                                
                                                                              
                                                    ],
                                                    style={
                                                            'font-size':'2px',
                                                            'width': '100%',
                                                            'height':'1.0em',
                                                            'padding-left':'0px',
                                                            'padding-right':'0px',
                                                            'text-align':'center',
                                                            'display':'inline-block'
                                                            } 
                                                    ),
                                                html.Br(),
                                                html.Br(),
                                                html.Div(className='trendDropDown',
                                                        children=[
                                                                html.Div("Time Interval Function"),
                                                                dcc.Dropdown(options=['Weekly Time Series', 'Monthly Time Series'], value='Weekly Time Series', id='trendDD')
                                                        ],
                                                style={
                                                        'width': '20%',
                                                        'height':'0.9em',
                                                        # 'padding-left':'0px',
                                                        # 'padding-right':'0px',
                                                        'text-align':'left',
                                                        'display':'inline-block'
                                                        } 
                                                ),
                                                html.Br()
                                            
                                        ]

                                    )
                                    
                            ]
                    ),    
                            #Summary for the chosen company and historical trend graph layout
            html.Div(className='trends',
                    children=[
                        html.Br(),
                        html.Br(),
                        html.Div(id='output-container-date-picker-range'),
                        html.Br(),
                        html.Br(),
                        # html.Output(id='errMessage'),
                        html.Br(),
                        # html.Div(className='stockSummary',
                        #         children=[
                        #                 dash_table.DataTable(defaultsum.to_dict('records'),[{"name": i, "id": i} for i in defaultsum.columns], id='summary_tbl')
                        #         ], style={"height":'20',
                        #                    'width': '80',
                        #                    'text-align':'center'     
                        #                    }),
                        dcc.Graph(id='hist-trend')
                        ],
                     style={'text-align':'center'}   
                        
                    ),
                html.Div(className='topGainers',
                         children=[
                                html.Br(),
                                html.Br(),
                                html.Div(html.H2("U.S. Stocks -Top Gainers of the day!")),
                                dash_table.DataTable(usTopGainers_df.to_dict('records'), [{"name": i, "id": i} for i in usTopGainers_df.columns]),
                                html.Br(),
                                html.Br(),

                         ],
                         style={'text-align':'center',
                                'width': '20%',
                                'height':'0.9em',
                                'vertical-align': 'top',
                                # 'padding-left':'0px',
                                # 'padding-right':'0px',
                                'text-align':'left',
                                'display':'inline-block',
                                'margin':'5px'}  
                         ),
                html.Div(className='SectorTrends',
                         children=[
                                html.Br(),
                                html.Br(),
                                html.Div(html.H2("U.S. Stocks -Sector Trends!")),
                                dash_table.DataTable(usSectorTrends.to_dict('records'), [{"name": i, "id": i} for i in usSectorTrends.columns]),
                                html.Br(),
                                html.Br(),

                         ],
                         style={'text-align':'center',
                                'width': '20%',
                                'height':'0.9em',
                                'vertical-align': 'top',
                                # 'padding-left':'0px',
                                # 'padding-right':'0px',
                                'text-align':'left',
                                'display':'inline-block',
                                'margin':'5px'}  
                         )
                    ],
                                
            style={'backgroundColor':'white',
                    'color':'black'
                    # 'width':'39%',
                    # 'display':'inline-block'
                    }
                    )


@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Output('startDate-intermediate-value','data'),
    Output('endDate-intermediate-value','data'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')

)
def datePickerfunc(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime("%Y-%m-%d")
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime("%Y-%m-%d")
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix, start_date_string, end_date_string



@app.callback(
    Output('hist-trend','figure'),
    Input('submit_ticker','n_clicks'),
    Input('startDate-intermediate-value','data'),
    Input('endDate-intermediate-value','data'),
    State('iticker', 'value'),
    State('radio','value'),
    State('trendDD','value')
            )       
def stockcandlestick(n_clicks, startDate, endDate, value, radio, trendDD):

        # errMessage=''
        if trendDD=='Monthly Time Series':
                if radio =='US Market':
                        # data = yf.download(value, start=startDate, end=endDate, interval="1d")
                        # fig=go.Figure(go.Candlestick(x=data.index, open=data.Open, close=data.Close, high=data.High, low=data.Low ))
                        # fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
                        data=tb.getTimeSeriesMonthlyStockData(value,startDate,endDate)
                        fig=go.Figure(go.Candlestick(x=data.datepart, open=data.open, close=data.close, high=data.high, low=data.low ))
                        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])    

                elif radio=='Indian Market':
                        value=value+'.BSE'
                        data=tb.getTimeSeriesMonthlyStockData(value,startDate,endDate)
                        fig=go.Figure(go.Candlestick(x=data.datepart, open=data.open, close=data.close, high=data.high, low=data.low ))
                        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
        elif trendDD=='Weekly Time Series':
                if radio =='US Market':
                        # data = yf.download(value, start=startDate, end=endDate, interval="1d")
                        # fig=go.Figure(go.Candlestick(x=data.index, open=data.Open, close=data.Close, high=data.High, low=data.Low ))
                        # fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
                        data=tb.getTimeSeriesWeeklyStockData(value,startDate,endDate)
                        fig=go.Figure(go.Candlestick(x=data.datepart, open=data.open, close=data.close, high=data.high, low=data.low ))
                        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])    

                elif radio=='Indian Market':
                        value=value+'.BSE'
                        data=tb.getTimeSeriesWeeklyStockData(value,startDate,endDate)
                        fig=go.Figure(go.Candlestick(x=data.datepart, open=data.open, close=data.close, high=data.high, low=data.low ))
                        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])

        #fig.update_layout(
        #{"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},template="plotly_dark")
        # return fig , errMessage
        return fig




if __name__ == '__main__':
    app.run_server(debug=True,host = '127.0.0.1', port=8051)







