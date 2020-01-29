import os
import requests
import getpass
import bs4

def download_fish_file(download_to_path="data/datafile"):


    url = "https://byu.box.com/shared/static/b9j0opllkxhvelg0ps365ww0xxcihydp.xlsx"

    for i in range(2):

        response = requests.get(url, allow_redirects=True)

        with open(download_to_path, 'wb') as dest:
            dest.write(response.content)

    return download_to_path
