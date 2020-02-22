import os
import requests
import getpass
import bs4
import csv
from bs4 import BeautifulSoup

def download_fish_file(download_to_path="data/fishdata"):


    url = "https://byu.box.com/shared/static/b9j0opllkxhvelg0ps365ww0xxcihydp.xlsx"
    #                 https://byu.box.com/s/b9j0opllkxhvelg0ps365ww0xxcihydp


    response = requests.get(url, allow_redirects=True)

    with open(download_to_path, 'wb') as dest:
        dest.write(response.content)

    return download_to_path

def download_water_data(download_to_path="data/water_data"):
    url = "https://byu.box.com/shared/static/89xn9en4a57twdh4znvaeclk17fx5dmd"
                      #https://byu.box.com/s/89xn9en4a57twdh4znvaeclk17fx5dmd

    response = requests.get(url, allow_redirects=True)

    with open(download_to_path, 'wb') as dest:
        dest.write(response.content)

    return download_to_path
    # request_data = {}
    #
    # #requests the data from the Min Max drop menu
    # request_data["canned"] = "MinMaxY"
    # request_data["GetCannedData"] = "Get Data"
    #
    # r = requests.post("http://lakepowell.water-data.com/index2.php", request_data)
    #
    # #Read then cache the data so it doesn't do as many requests from the webpage
    # # with open("cached_min_max.html", 'w') as f:
    # #     f.write(r.text)
    #
    # # with open("cached_min_max.html") as f:
    # #     text = f.read()
    #
    # soup = BeautifulSoup(r.text, features="lxml")
    #
    # found_items = soup(text="Min / Max by Year")
    # parent = list(found_items)[0].parent
    # table = parent.findNext('table')
    # rows = table.findAll("tr")
    #
    # header = rows[0]
    # data = rows[1:-1]#all_but first and last row
    #
    # text_headers = []
    # for column in header.findAll("th"):
    #     text_headers.append(column.text)
    #
    # text_data = []
    # min_max = "data/year_min_max.csv" #file name to stor min/max data
    #
    # #read the text data into a csv
    # with open(min_max, 'w', newline='') as myfile:
    #      wr = csv.writer(myfile,  quoting=csv.QUOTE_ALL)
    #      wr.writerow(text_headers)
    #
    #      for row in data:
    #          text_row = []
    #          for column in row.findAll("td"):
    #              text_row.append(column.text)
    #          wr.writerow(text_row)
    # return min_max
