
from bs4 import BeautifulSoup
import pandas as pd
import requests


#The section is for US stock market Trend, Top Gainers and Top Losers
urlSectorTrend="https://simplywall.st/markets/us#"
htmlcontentSectorTrend=requests.get(urlSectorTrend).text
soupSectorTrend=BeautifulSoup(htmlcontentSectorTrend, 'lxml')

urlUSTopGainers="https://simplywall.st/stocks/us/top-gainers"
htmlcontentUSTopGainers=requests.get(urlUSTopGainers).text
soupUSTopGainers=BeautifulSoup(htmlcontentUSTopGainers, 'lxml')


urlUSTopLosers="https://simplywall.st/stocks/us/biggest-losers"
htmlcontentUSTopLosers=requests.get(urlUSTopLosers).text
soupUSTopLosers=BeautifulSoup(htmlcontentUSTopLosers, 'lxml')


#Sector Trends Returns for US
Components=[]
ComValues_=[]
SectorTrendClassComponents=soupSectorTrend.find_all(class_="sc-18tfppz-3 iypVNG")
SectorTrendClassValues=soupSectorTrend.find_all(class_="sc-18tfppz-4 cxkvhF")
# print(SectorTrendClass, "\n")
for values_ in SectorTrendClassComponents:
    Components.append(values_.text)
for values_ in SectorTrendClassValues:
    ComValues_.append(values_.text)
Sector_Trend_US_df = pd.DataFrame(zip(Components, ComValues_), columns=['Sector', 'Returns'])
Sector_Trend_US_df.reset_index(inplace=True)


#US Sector Top Gainers
# soupUSTopGainers.findAll()
companyNameClass    =   "sc-1a2wa6p-6 bVIYlk"
lastPriceClass      =   "sc-1a2wa6p-13 jUwA-DB" #same as marketCapClass
oneDayReturnClass   =   "sc-ailqsn-0 kxiqdw"
oneYearReturnClass  =   "sc-ailqsn-0 kxiqdw"
marketCapClass      =   "sc-1a2wa6p-13 jUwA-DB" #haslastprice, analystsTarget, valuation, growth, DivYield
industryClass       =   "sc-1a2wa6p-7 MkSwg"


tickerNamelist=[]
companyNameslist=[]
for elements_ in soupUSTopGainers.findAll(class_=companyNameClass):
    tickerNamelist.append(elements_.find('b').text)
    companyNameslist.append(elements_.find('span').text)

industryList=[]
for elements_ in soupUSTopGainers.findAll(class_=industryClass):
    industryList.append(elements_.text)

topGainers_df=pd.DataFrame(zip(tickerNamelist, companyNameslist, industryList), columns=['Ticker', 'CompanyName', 'Industry'])


#############################################################################################################################################
# This part still needs to be researched and need to find a solution on how to separate the value since they have all tags and classes same.
#############################################################################################################################################
# lastPricelist= []
# for elements_ in soupUSTopGainers.findAll(class_=lastPriceClass):
#     print(elements_['value'])
    # lastPricelist.append(elements_.find('span').text)
    # for subele in elements_.findAll(class_="sc-ugumnt-0 sc-rm1mlc-1 calUli ffyqjh"):
    #     if subele.text.split("$")[0]=='US':
    #         print(subele.text)
# <td class="sc-1a2wa6p-13 jUwA-DB" value="334.27"><span class="sc-ugumnt-0 sc-rm1mlc-1 calUli ffyqjh">US$334.27</span></td>
# <td class="sc-1a2wa6p-13 jUwA-DB" value="2451153349525"><span class="sc-ugumnt-0 sc-rm1mlc-1 calUli ffyqjh">US$2.5t</span></td>
# <td class="sc-1a2wa6p-13 jUwA-DB" value="389.52224"><span class="sc-ugumnt-0 sc-rm1mlc-1 calUli ffyqjh">US$389.52</span></td>
# <td class="sc-1a2wa6p-13 jUwA-DB" value="34.321625"><span class="sc-ugumnt-0 sc-rm1mlc-1 calUli ffyqjh"><span class="sc-1a2wa6p-9 CMUMF" tabindex="0">PE</span>34.3x</span></td>
# <td class="sc-1a2wa6p-13 jUwA-DB" value="0.119183"><span class="sc-ugumnt-0 sc-rm1mlc-1 calUli ffyqjh"><span class="sc-1a2wa6p-9 CMUMF" tabindex="0">E</span>11.9%</span></td>
# <td class="sc-1a2wa6p-13 jUwA-DB" value="0.008137"><span class="sc-ugumnt-0 sc-rm1mlc-1 calUli ffyqjh">0.8%</span></td>

