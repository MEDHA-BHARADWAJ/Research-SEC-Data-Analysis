from sec_edgar_downloader import Downloader

file = open("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Comp1.txt",'r')
lines = file.readlines()

for line in lines:
    print(line)
    dl = Downloader("C:/Users/medha/OneDrive/Desktop/GMU/GRA/Financial Data/Historic")
    dl.get("10-Q", line ,after ="2000-01-01", before="2015-01-01")
