#!/usr/bin/python3
"""Scrape images from a website and save them to a directory"""

from bs4 import BeautifulSoup
import webbrowser
import requests
import os

os.mkdir("./images") # create the directory to store all the images

def download_img(image_url):
    """Download an image and save it to the file"""
    response = requests.get(image_url)
    response.raise_for_status
    image_name = image_url.split("/")[-1]
    image_path = os.path.join("images", os.path.basename(image_name))
    with open(image_path, "wb") as f:
        for chunk in response.iter_content(10000):
            f.write(chunk)
    print(f"downloaded {image_name} through {image_url}")

def scrape_img_url(comicSoup, base_url):
    """scape image url from a web page"""
    image_tag = comicSoup.select("#comic img")
    if not image_tag:
        return None
    image_url = image_tag[0].get("src")
    full_image_url = f"{base_url}{image_url}"
    return full_image_url


base_url = "https://xkcd.com"
response = requests.get(base_url)
response.raise_for_status
comicSoup = BeautifulSoup(response.text, "html.parser")
full_image_url = scrape_img_url(comicSoup, base_url)
download_img(full_image_url)
buttons = comicSoup.select(".comicNav a")
flag = 0
for button in buttons:
    if button.get("rel") == ["prev"]:
        prev_number = int(button.get("href").strip("/ "))
        flag = 1
while flag == 1 and prev_number > 0:
    prev_url = f"{base_url}/{str(prev_number)}/"
    response = requests.get(prev_url)
    response.raise_for_status
    comicSoup = BeautifulSoup(response.text, "html.parser")
    full_image_url = scrape_img_url(comicSoup, base_url)
    if not full_image_url:
        print("No more pictures")
        break
    download_img(full_image_url)
    print(prev_number)
    prev_number -= 1
    
