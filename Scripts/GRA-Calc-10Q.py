from bs4 import BeautifulSoup
import datetime
import re, os
import csv
import glob
import pandas as pd
import io
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
HTMLCLEANER = re.compile('<.*?>')

def newFileNameGenerator(compId,fileName):

    file = open(fileName,'r')#r"C:\Users\medha\OneDrive\Desktop\GMU\GRA\Financial Data\sec-edgar-filings\AMZN\10-Q\0001018724-15-000087\full-submission.txt",'r')
    lines = file.readlines()
    print(type(lines))
    dateLine = lines[6]
    date = dateLine[-9:]
    year = date[0:4:]
    month = date[4:6:]
    m = datetime.date(int(year),int(month),1).strftime("%B")
    #quarterFinder = {"January":1,"February":1,"March":"1","April":2,"May":2,"June":"2","July":3,"August","September":"3","October":4,"November":4,"December":4}
    #quarter = quarterFinder[m]
    fileId = compId+"_"+m+"_"+year
    return fileId

def fileCleaner(fileName, bagOfWords):

    stopWords = set(stopwords.words('english'))
    
    file = open(fileName,"r")
    string = file.read()
    cleantext = x = BeautifulSoup(string, "lxml").text
        
    print("after brautiful soup:",len(cleantext))

    #tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp", "w")
    #tmp_file.write(cleantext)
    newLines = ''
    for word in cleantext.split():
        if not word.isspace():
            newLines+=word+' '
            
    #tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp1", "w")
    #tmp_file.write(newLines)

    refilter = re.sub(HTMLCLEANER, '',newLines)
    #re.sub('\nFinancial_Report.xlsx IDEA:.*?end','',refilter, flags=re.DOTALL)

    #tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp2", "w")
    #tmp_file.write(refilter)
    
    print("with stop words:",len(refilter.split()))
    filteredLines = []
    for w in refilter.split():
        if w not in stopWords:
            filteredLines.append(w)
    
    totalCount = len(filteredLines)
    print("total count =",totalCount)
    count = 0
    for word in filteredLines:
        if word.lower() in bagOfWords:
            count+=1
            
    print("custcount=",count)
    return [totalCount, count]

def calculateCustomerFocus(fileName,ticker):
    customerFocusWords = ["customer","market","customers","markets","consumer","market-place","consumers","marketplace","buyer","communities","buyers"]
    totalCount, customerFocusCount = fileCleaner(fileName, customerFocusWords)
    newFile = newFileNameGenerator(ticker,fileName)
    print(totalCount,":",customerFocusCount,":",totalCount/customerFocusCount)
    result = {'totalCount':totalCount, 'custCount':customerFocusCount, 'fileName':newFile}
    return result

def createData():

    compList = pd.read_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/CompanyList.xlsx")
    dataFile = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/DataFile","w")
    writer = csv.writer(dataFile)
    compList = compList.values.tolist()
    dataCols = ["compName","ticker","reportType","reportFrame","year","totalCount","custCount","custMetric"]
    finalDf = pd.DataFrame(columns = dataCols)
    writer.writerow(dataCols)
 
    for comp in compList:
        fileList = [os.path.normpath(i) for i in glob.glob("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/sec-edgar-filings/"+comp[1]+"/10-Q/*/*.txt")]
        print(fileList)
        for file in fileList:
            print(comp[1])
            res = calculateCustomerFocus(file,comp[1])
            fileData = res['fileName'].split("_")
            row = [comp[0],comp[1],"10-Q",fileData[1],fileData[2],res['totalCount'],res['custCount'],res['custCount']*100/res['totalCount']]
            writer.writerow(row)
            finalDf.append(row, ignore_index=True)
            print(row)
    finalDf.to_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/output3.xlsx")
    print("Done")
     
createData()
