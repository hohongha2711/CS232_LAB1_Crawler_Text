from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.request
import random 
import pandas as pd


browser  = webdriver.Chrome(executable_path="./chromedriver.exe")
browser.maximize_window()
sleep(5)
browser.get("https://images.google.com/")
sleep(10)

txtKeys = browser.find_element(By.ID, "APjFqb")
txtKeys.send_keys("Cat") 
txtKeys.send_keys(Keys.ENTER)

sleep(15)


def scrollPage(browser):
    # scroll page
    scroll_pause_time = random.randint(3, 16)
    i = 0
    while i < 2:
        if (i > 0):
            browser.execute_script("window.scrollTo(0, 0);")
            sleep(random.randint(1, 3))
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(scroll_pause_time)
        else:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(scroll_pause_time)
        i += 1
        #print(i)

    

scrollPage(browser)
sleep(5)
soup = BeautifulSoup(browser.page_source, 'html.parser')
images = soup.findAll('div', {'class': "bRMDJf islir"})
print(len(images))

'''for image in images:
    img = image.find('img')
    if img.has_attr('src'):
        #print(img['src'])
        img_name = str(i) + ".png"
        urllib.request.urlretrieve(img['src'], "./images/"+img_name)
        print(img_name)
        i = i+1
'''
for i in range(30):
    img = images[i].find('img')
    if img.has_attr('src'):
        #print(img['src'])
        img_name = str(i) + ".png"
        urllib.request.urlretrieve(img['src'], "./images/"+img_name)
        print(img_name)


browser.close()
