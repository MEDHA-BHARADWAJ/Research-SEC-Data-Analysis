import pandas as pd
import csv

compList = pd.read_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/CompanyList.xlsx")
print(len(compList))
compList = compList.values.tolist()
data = pd.read_excel("C:/Users/medha/OneDrive/Desktop/outputx.xlsx")
print(len(data))
dataCols = ["compName","ticker","average","SD"]
finalDf = pd.DataFrame(columns = dataCols)

for comp in compList:
    print(comp[1])
    newList = data.loc[data['ticker'] == comp[1]]
    row = [comp[0],comp[1],newList['custMetric'].mean(),newList['custMetric'].std()]
    finalDf.loc[len(finalDf.index)]=row

finalDf.to_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/SDoutput3.xlsx")
    
    
    
