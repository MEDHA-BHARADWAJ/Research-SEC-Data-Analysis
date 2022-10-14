import pandas as pd
from pandas import Timestamp

## To extract last day of the year stock closing price for each company ##

compList = pd.read_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/CompanyList.xlsx")
compList = compList.values.tolist()
dataCols = ["compName","ticker","10KYear","eoyStock"]
finalDf = pd.DataFrame(columns = dataCols)
for comp in compList:
    print(comp[1])
    fileData = pd.read_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/Stock Data/"+comp[1]+".xlsx")
    fileData = fileData.values.tolist()
    yearTicker = 2000
    while yearTicker < 2022:
        row = [comp[0],comp[1],yearTicker,0]
        dec29 = ['2000','2006','2017']
        dec30 = ['2005','2011','2016']
        year = str(yearTicker)
        date = "31"
        if year in dec29:
            date = "29"
        if year in dec30:
            date = "30"
        for data in fileData:
            if data[0] == Timestamp(year+"-12-"+date+" 00:00:00"):
                #print(data)
                row = [comp[0],comp[1],yearTicker,data[4]]
        finalDf.loc[len(finalDf.index)]=row
        print(row)
        yearTicker += 1
finalDf.to_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/StockHoz.xlsx")
print("Done")
