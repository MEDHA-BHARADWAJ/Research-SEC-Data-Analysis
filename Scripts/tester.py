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

    file = open(fileName,'r',encoding="utf8")#r"C:\Users\medha\OneDrive\Desktop\GMU\GRA\Financial Data\sec-edgar-filings\AMZN\10-Q\0001018724-15-000087\full-submission.txt",'r')
    lines = file.readlines()
    index = 0
    for line in lines:
        if "FILED AS OF DATE:" in line:
            index = lines.index(line)
            print(index)
    print(type(lines))
    dateLine = lines[index]
    print(dateLine)
    date = ''
    for c in dateLine:
        if c.isdigit():
            date+=c
    print(date)
    #date = dateLine[-9:]
    year = date[0:4:]
    month = date[4:6:]
    m = datetime.date(int(year),int(month),1).strftime("%B")
    #quarterFinder = {"January":1,"February":1,"March":"1","April":2,"May":2,"June":"2","July":3,"August","September":"3","October":4,"November":4,"December":4}
    #quarter = quarterFinder[m]
    fileId = compId+"_"+m+"_"+year
    return fileId

def fileCleaner(fileName, bagOfWords):

    stopWords = set(stopwords.words('english'))

    file = open(fileName,"r",encoding="utf8")
    string = file.read()
    cleantext = BeautifulSoup(string, "lxml").text
        
    print("after brautiful soup:",len(cleantext))

    tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp.txt", "w", encoding="utf-8")
    tmp_file.write(cleantext)
    
    newLines = ''
    for word in cleantext.split():
        if not word.isspace():
            newLines+=word+' '
            
    tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp1.txt", "w", encoding="utf-8")
    tmp_file.write(newLines)

    refilter = re.sub(HTMLCLEANER, '',newLines)
    #re.sub('\nFinancial_Report.xlsx IDEA:.*?end','',refilter, flags=re.DOTALL)

    tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp2.txt", "w", encoding="utf-8")
    tmp_file.write(refilter)
    
    print("with stop words:",len(refilter.split()))
    filteredLines = ""
    for w in refilter.split():
        if w not in stopWords:
            filteredLines+=w+" "

    tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp3.txt", "w", encoding="utf-8")
    tmp_file.write(filteredLines)

    print("checking alphanumeric words")
    alpNumCheck = filteredLines.split()
    checkedLines = ""
    special_characters = "!@#$%^&*()-+?_=,<>/"
    for word in alpNumCheck:
        newWord = ""
        for chr in word:
            if not chr.isalpha() :
                continue
            else:
                newWord+=chr

        if len(newWord) > 3 and not(newWord.isupper()):
            checkedLines+= newWord+" "

    tmp_file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/tmp4.txt", "w")
    tmp_file.write(checkedLines)
    
    totalCount = len(checkedLines.split())
    print("total count =",totalCount)
    count = 0
    for word in checkedLines.split():
        for w in bagOfWords:
            if w in word.lower():
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

    compList = pd.read_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/test.xlsx")
    dataFile = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/test-DataFile","w")
    writer = csv.writer(dataFile)
    compList = compList.values.tolist()
    dataCols = ["compName","ticker","reportType","reportFrame","year","totalCount","custCount","custMetric"]
    finalDf = pd.DataFrame(columns = dataCols)
    writer.writerow(dataCols)
 
    for comp in compList:
        fileList = [os.path.normpath(i) for i in glob.glob("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/sec-edgar-filings/"+comp[1]+"/10-K/*/*.txt")]
        print(fileList)
        for file in fileList:
            print(comp[1])
            res = calculateCustomerFocus(file,comp[1])
            fileData = res['fileName'].split("_")
            row = [comp[0],comp[1],"10-K",fileData[1],fileData[2],res['totalCount'],res['custCount'],res['custCount']*100/res['totalCount']]
            writer.writerow(row)
            finalDf.loc[len(finalDf.index)]=row
            print(row)
    finalDf.to_excel("C:/Users/medha/OneDrive/Desktop/GMU/GRA/test-output.xlsx")
    print("Done")
     
createData()
