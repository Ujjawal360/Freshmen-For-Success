import requests
import selenium
import pandas as pd
import re
from selenium import webdriver
import os
import pickle5
import random
import datetime

from io import StringIO
import facebook as fb
import urllib.request
from urllib.request import urlopen
import urllib.request
import telegram

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

from selenium.webdriver.common.keys import Keys
import time

def bold(input_text):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        bold_chars = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
        output = ""
        for character in input_text:
            if character in chars:
                output += bold_chars[chars.index(character)]
            else:
                output += character
        return output

title = []
job_links = []
companys = []
locations = []
date_opened = []

fb_page_id = 110733351804468

#here goes our fb token. We don't want to others to have access to our fb channel
fb_access_token = ''

fb_post_url = 'https://graph.facebook.com/{}/feed'.format(fb_page_id)

telegram_token = 'our-page-telegram-access-code-here'
bot = telegram.Bot(token=telegram_token)

options = Options()
ua = UserAgent()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.headless = True

userAgent = ua.random
original_link = 'https://www.linkedin.com/jobs/search?keywords=Internships&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&position=1&pageNum=5'
options.add_argument(f'user-agent={userAgent}')

driver = webdriver.Chrome(options= options, executable_path ='/Users/ujjawalbabu/Desktop/drivers/chromedriver')
driver.get(original_link)

time.sleep(2)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)

all_jobs = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[2]')
x = all_jobs.find_element(By.CLASS_NAME, 'jobs-search__results-list')
y = x.find_elements(By.CLASS_NAME, 'base-search-card__info')

for z in y:
    job_title = z.find_element(By.CLASS_NAME, 'base-search-card__title').text
    company_and_link = z.find_element(By.CLASS_NAME, 'base-search-card__subtitle')
    job_link = company_and_link.find_element(By.TAG_NAME, 'a').get_attribute('href')
    company = company_and_link.find_element(By.TAG_NAME, 'a').text
    location = z.find_element(By.CLASS_NAME, 'job-search-card__location').text
    try:
        open_date = z.find_element(By.CLASS_NAME, 'job-search-card__listdate--new').get_attribute('datetime')
        date_opened.append(open_date)
    except:
        date_opened.append(datetime.datetime.now().strftime("%Y-%m-%d"))
        
    title.append(job_title)
    job_links.append(job_link)
    companys.append(company)
    locations.append(location)

    
contact_dict = {'title': title, 
                'job_links': job_links,
                'companys': companys,
               'locations': locations,
               'date_opened':date_opened}
df0 =  pd.DataFrame({ key:pd.Series(value) for key, value in contact_dict.items()})
df0 = df0.drop_duplicates()
df0['companys'] = df0['companys'].str.replace(r'[^\w\s]+', '', regex=True)

driver.close()
driver.quit()

for index, row in df0.iterrows():
    job_title = row['title']
    link_to_the_job = row['job_links']
    company = row['companys']
    job_location = row['locations']
    opening_date = row['date_opened']
    msg = f"\u2757{bold('Internship Opportunity Alert')}\u2757\nJob Title--> {bold(job_title)}\nCompany--> {bold(company)}\nLocation--> {bold(job_location)}\nOpening Date--> {bold(opening_date)}\nLink to the job--> {link_to_the_job}"
    hashtags = f"\n\n#{company.replace(' ', '')}  #{job_location.replace(' ', '')}  #Internship  #Freshman  #FreshmanOppurtunities  #applyRightAway  #JobOpenings"
    fb_msg = msg + hashtags
    
    fb_payload = {'message': fb_msg,'access_token': fb_access_token}
    fb_post = requests.post(fb_post_url, data=fb_payload)
    print(fb_post.text)
    
    telegram_msg = bot.send_message(chat_id="@internshipsalertt", text=msg, parse_mode=telegram.ParseMode.HTML)
    print(telegram_msg)
    time.sleep(5)
    
df0.to_csv('jobs.csv')

print('Done----------------------------------')
