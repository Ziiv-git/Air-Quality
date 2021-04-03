# from Plot_AQI import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv


#function for web_Scrap html files in terms from each and every year
#requires two parameters as month and year
def met_data(month, year):
    #file on the particular year is read and from that a particular month is read
    file_html = open('/content/sample_data/Data/Real_data'.format(year,month), 'rb')
    plain_text = file_html.read()

    tempD = []
    finalD = []
    #initialising the BeautifulSoup
    soup = BeautifulSoup(plain_text, "lxml")
    #after inspecting the table needed for analysis is stored in class = medias mensulas numspan
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:#tbody is list of rows
            for tr in tbody: #tr contains the tags i.e the name of the columns
                a = tr.get_text() #getting the text of the column names
                tempD.append(a) #there are 15 features and it stores the row values

    rows = len(tempD) / 15  #calculating how many rows are there
     #iterating through rows
    for times in range(round(rows)):
        newtempD = []
        for i in range(15): #iterating through 15 columns/features pickup the data and append in the newlist
            newtempD.append(tempD[0]) #popping the last captured value so in next iteration new values are stores
            tempD.pop(0)
        finalD.append(newtempD) #finally the table is axtracted and is stored in this variable
  #there are manyu columns in the table which contains no values, either they are not recorded or ignored,
  # since its no worth keeping them, so dropping those columns here by the below code
    length = len(finalD)

    finalD.pop(length - 1)
    finalD.pop(0)

    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD


#function to combine the two datasets
def data_combine(year, cs):
    for a in pd.read_csv('/content/sample_data/Data/Real_data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist




if __name__ == "__main__":
    if not os.path.exists("/content/sample_data/Data/Real_data"): #creating a folder if there isnt one
        os.makedirs("/content/sample_data/Data/Real_data") #store the data from the websites and store as Real_Combine file
    for year in range(2013, 2017):
        final_data = []
        with open('/content/sample_data/Data/Real_data/real_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5']) #writing the column names
        for month in range(1, 13):
            temp = met_data(month, year) #calling the met_data function and extracting the data from html file and
       # storing them in the final_data
            final_data = final_data + temp

            #recalling all the data from the aqi folder (the dependent feature which is PM 2.5)
    # pm = getattr(sys.modules[__name__], 'avg_data(file)')()


        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()

        if len(pm) == 364:
            pm.insert(364, '-')

#after extracting the average values of pm will now append it to the final_data as the last column
        for i in range(len(final_data)-1):
            # final[i].insert(0, i + 1)
            final_data[i].insert(8, pm[i])

 #create a newfolder and save all the files for each and every year
        with open('/content/sample_data/Data/Real_data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)

    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)

    total=data_2013+data_2014+data_2015+data_2016 #combining all the data

    with open('/content/sample_data/Data/Real_data/Real_Combine', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)


df=pd.read_csv('/content/sample_data/Data/Real_data/Real_Combine.csv')
