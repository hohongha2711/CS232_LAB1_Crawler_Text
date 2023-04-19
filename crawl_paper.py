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
browser.get("https://dl.acm.org/")
sleep(10)

txtKeys = browser.find_element(By.NAME, "AllField")
txtKeys.send_keys('"Duy Dinh Le"') 
#txtKeys.send_keys('"Thanh Duc Ngo"') 
txtKeys.send_keys(Keys.ENTER)

sleep(5)
def scrollPage(browser):
    # scroll page
    scroll_pause_time = random.randint(3, 16)
    i = 0
    while i < 2:
        if (i == 1):
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


scrollPage(browser)
sleep(5)
#df = pd.DataFrame(columns= ['Title', 'Author', 'Conferences', 'Intro', 'Link'])
df = pd.read_csv('paper.csv')
list_papers = browser.find_elements(By.CLASS_NAME, "issue-item__content")
for p in list_papers:
    title = p.find_element(By.CLASS_NAME, 'hlFld-Title').text
    link = p.find_element(By.CLASS_NAME, 'hlFld-Title').find_element(By.TAG_NAME, 'a').get_attribute('href')
    author = p.find_element(By.TAG_NAME, 'ul').text
    intro = p.find_element(By.TAG_NAME, 'p').text
    conferences = p.find_element(By.CLASS_NAME, 'epub-section__title').text

    print("Title: ",title)
    print("Link: ",link)
    print("Author: ",author)
    print("Intro: ",intro)
    print("Conferences: ",conferences)
    df.loc[len(df.index)] = [title, author, conferences,intro,link]
    print("------------------------------------------")
print(len(list_papers))
df.to_csv('paper.csv', index= False)
browser.close()