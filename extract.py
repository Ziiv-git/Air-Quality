#importing libraries
import os
import time
import requests
import sys
import csv

#scrapping the website using the following function
def retrieve_html():

  for year in range(2013,2019):

    for month in range(1,13):

      if (month<10):
        url='http://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(month,year)

      else:
        url='http://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month,year)

      source_text = requests.get(url)
      text_utf = source_text.text.encode('utf=8') #encoding the file in utf-8

      if not os.path.exists('/content/sample_data/Data/html_data/{}'.format(year)): #if folder does not exist create a directory
        os.makedirs('/content/sample_data/Data/html_data/{}'.format(year))

      with open('/content/sample_data/Data/html_data/{}/{}.html'.format(year, month), 'wb') as output: #saving in html version file
        output.write(text_utf)

    sys.stdout.flush()


if __name__=="__main__":
    start_time=time.time()
    retrieve_html()
    stop_time=time.time()
    print("Time taken {}".format(stop_time-start_time))
