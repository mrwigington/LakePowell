import requests

from bs4 import BeautifulSoup


request_data = {}

# for i in range(1,11):
#     request_data["datemonth{}".format(i)]=""
#     request_data["dateday{}".format(i)]=""
#     request_data["dateyear{}".format(i)]=""

#Can request up to 10 dates. I haven't tested the api but maybe more?

request_data["Get10DateData"] = "Get+Data"
request_data["datemonth1"] = "January"
request_data["dateday1"] = "01"
request_data["dateyear1"] = "2020"

request_data["datemonth2"] = "January"
request_data["dateday2"] = "02"
request_data["dateyear2"] = "2020"

r = requests.post("http://lakepowell.water-data.com/index2.php", request_data)

soup = BeautifulSoup(r.text, features="lxml")


found_items = soup(text="Water Data for Selected Dates")

parent = list(found_items)[0].parent

table = parent.findNext('table')

rows = table.findAll("tr")

header = rows[0]
data = rows[1:-1]#all_but first and last row

text_headers = []
for column in header.findAll("th"):
    text_headers.append(column.text)

text_data = []
for row in data:
    text_row = []
    for column in row.findAll("td"):
        text_row.append(column.text)
    text_data.append(text_row)

print(text_headers)
print(text_data)
