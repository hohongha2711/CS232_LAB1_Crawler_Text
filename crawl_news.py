from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.request
import random 
import pandas as pd
import requests
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--ignore-certificate-errors')

browser  = webdriver.Chrome(executable_path="./chromedriver.exe")
browser.maximize_window()
sleep(5)
browser.get("https://vnexpress.net/")
sleep(10)

def scrollPage(browser):
    # scroll page
    scroll_pause_time = random.randint(3, 16)
    i = 0
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

scrollPage(browser)
#button = browser.find_element(By.ID, "gsc_bpf_more")

def get_links(browser):
    links = []

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    news = soup.findAll('h3', attrs={'class': "title-news"})
    for n in news:
        #print(n)        
        links.append(n.find('a').get('href'))
    return links

links = get_links(browser)
df_news = pd.read_csv("news.csv")
df_cmt = pd.read_csv("cmt_news.csv")
for i in range(10):
    try:
        #req = requests.get(links[i])
        browser.get(links[i])
        sleep(1)
        scrollPage(browser)
        sleep(1)
    
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        title = soup.findAll('h1', attrs={'class': "title-detail"})[0].text
        time = soup.findAll('span', attrs={'class': "date"})[0].text
        des = soup.findAll('p', attrs={'class': "description"})[0].text
        print('----------------------------------------')
        print("Title: ",title)
        print("Time: ",time)
        print("Description: ",des)
        print("Link: ", links[i])
        df_news.loc[len(df_news.index)] = [title, time,des,links[i]] 
        content = soup.findAll('p',attrs = {'class': "full_content"})
        print("Bình luận:")
        for con in content:
            name = con.findAll('a', attrs = {'class': "nickname"})[0].text
            cmt = str(con.text).replace(str(name), "")
            print(name + ": " + cmt)
            df_cmt.loc[len(df_cmt.index)] = [name, cmt, title]
    except:
        i = i+1
        pass


df_news.to_csv("news.csv",index= False)
df_cmt.to_csv("cmt_news.csv", index= False)

sleep(5)
browser.close()
