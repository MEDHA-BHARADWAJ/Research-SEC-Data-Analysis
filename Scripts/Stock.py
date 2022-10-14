import yfinance as yf
import pandas as pd

compList = pd.read_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/CompanyList.xlsx")
compList = compList.values.tolist()

for comp in compList:
    print(comp[1])
    data = yf.download(comp[1], start ="2000-01-01", end="2022-04-03")
    data.to_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/Stock Data/"+comp[1]+".xlsx")
