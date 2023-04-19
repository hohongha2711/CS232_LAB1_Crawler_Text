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
#browser.get("https://www.facebook.com/UIT.Fanpage")

def login(browser):
    txtUser = browser.find_element(By.NAME, "email")
    txtUser.send_keys("hongha.hhh271102@gmail.com") 

    txtPass = browser.find_element(By.NAME,"pass")
    txtPass.send_keys("hohongha2711")

    txtPass.send_keys(Keys.ENTER)
    sleep(5)

def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("error write line")
    return data

def writeFileTxt(fileName, content):
    with open(fileName, 'a') as f1:
        f1.write(content + os.linesep)


def scrollPage(browser):
    # scroll page
    scroll_pause_time = random.randint(3, 16)
    i = 0
    while i < 3:
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
        print(i)


def getPostLink(browser,filePath = 'posts.csv'):
    allPosts = readData(filePath)
    sleep(2)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    shareBtn = soup.findAll('a', attrs={'class': "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"})
    #shareBtn = browser.find_elements(By.TAG_NAME, 'a') 
    print(len(shareBtn))
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get('href')
            #postId = str(postID)
            #if((postId != 'None' and ('posts' in postId) and ('comment' not in postId))):
            if postId not in allPosts:
                #print(postId)
                writeFileTxt(filePath, postId)


def getContentComment(browser, df, df_info, url):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    text = ""
    links = soup.findAll('div', attrs={'class': "x1y1aw1k xn6708d xwib8y2 x1ye3gou"})
    s = soup.findAll('div', attrs={'class': "x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xsyo7zv x16hj40l x10b6aqq x1yrsyyn"})
    
    num_cmt = 0
    num_share = 0
    if(len(s)==3):
        s1 = s[1].text 
        num_cmt = s1.split(" ",1)[0]
        s2 = s[2].text
        num_share = s2.split(" ",1)[0]
    elif(len(s)==2):
        st = s[1].text 
        if(len(st)>0):
            if(st.split(" ",1)[1] == "lượt chia sẻ"):
                num_share = st.split(" ",1)[0]
            else:
                num_cmt = st.split(" ",1)[0]
    print("----------------------------------------------------------------------------")
    print("Link: ", url)
    print("Số bình luận: ", num_cmt)
    print("Số lượt chia sẻ: ",num_share)
    df_info.loc[len(df_info.index)] = [url,num_cmt,num_share] 
    
    #print(len(links))
    if(len(links)>0):
        print("Bình luận: ")
        for link in links:
            name = link.findAll('span', attrs={'class': "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u"})
            cmt = link.findAll('div', attrs={'class': "x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r"})
            if(len(cmt)>0):
                print(name[0].text + ": " + cmt[0].text)
                df.loc[len(df.index)] = [name[0].text, cmt[0].text, url] 
            else:
                print(name[0].text + ": ")
                df.loc[len(df.index)] = [name[0].text, "", url] 


# Thực hiện crawl comments từ mỗi bài post
def getAmountOfComments(browser, list_posts_file, df_cmt,df_info, num_post):
    posts = readData(list_posts_file)
    count = 0
    log = 0
    for p in posts:
        if(count<num_post):
            if(p != ""):
                count = count + 1
                browser.get(p)
                sleep(10)
                if(log == 0):
                    login(browser)
                    log = 1
                getContentComment(browser, df_cmt, df_info, p)

def get_post(browser):  
    browser.get("https://www.facebook.com/UIT.Fanpage")
    scrollPage(browser)
    getPostLink(browser,'posts.csv')


def get_info(browser):
    df_cmt = pd.read_csv("cmt.csv")
    df_info = pd.read_csv("data_posts.csv")
    getAmountOfComments(browser,'posts.csv',df_cmt,df_info,15)
    df_cmt.to_csv("cmt.csv", index=False)
    df_info.to_csv("data_posts.csv", index=False)

#Lấy link bài post
get_post(browser)


#Lấy comment, số bình luận, số lượt chia sẻ
get_info(browser)

#sleep(10)
browser.close()