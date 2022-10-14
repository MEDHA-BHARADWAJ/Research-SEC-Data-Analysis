import pandas as pd
import csv

compList = pd.read_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/CompanyList.xlsx")
compList = compList.values.tolist()
data = pd.read_excel("C:/Users/medha/OneDrive/Desktop/outputx.xlsx")
data = data.values.tolist()

dataCols = ["compName","ticker","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","average","SD"]
indexFinder = {"2000":2,"2001":3,"2002":4,"2003":5,"2004":6,"2005":7,"2006":8,"2007":9,"2008":10,"2009":11,"2010":12,"2011":13,"2012":14,"2013":15,"2014":16,"2015":17,"2016":18,"2017":19,"2018":20,"2019":21,"2020":22,"2021":23,"2022":24}

finalDf = pd.DataFrame(columns = dataCols)

for comp in compList:
    print(comp[1])
    row = [comp[0],comp[1],0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for val in data:
        if val[1] == comp[1] and (str(val[4]) in dataCols):
            x = indexFinder[str(val[4])]
            row[x] = val[7]
    print(row)
    finalDf.loc[len(finalDf.index)]=row

finalDf.to_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/HorzVis2.xlsx")
