import pandas as pd

df = pd.read_excel('C:/Users/medha/OneDrive/Desktop/GMU/GRA/output.xlsx')
print(df.info())
newMetric =[]
for index,row in df.iterrows():
    val = (row['custCount']*100)/row['totalCount']
    newMetric.append(val)

df.insert(8,"newMetric",newMetric)

df.to_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/output2.xlsx")
