# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:56:54 2018

@author: jjone
"""

# This is the part 1 of cosmetic recommendation: scraping cosmetic data from sephora
# You can also daownload the csv file from same repository: cosmetic.csv

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


chrome_path = "C:\\Users\jjone\Downloads\chromedriver"

def scrollDown(driver, n_scroll):
    body = driver.find_element_by_tag_name("body")
    while n_scroll >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        n_scroll -= 1
    return driver


driver = webdriver.Chrome(executable_path = chrome_path)

url = 'https://www.sephora.com'
driver.get(url)

xpath = '/html/body/div[5]/div/div/div[1]/div/div/button'
btn = driver.find_element_by_xpath(xpath)
btn.click()
xpath2 = '/html/body/div[3]/div/div/div[1]/div/div/div[2]/form/div[3]/div/div[1]/button'
btn = driver.find_element_by_xpath(xpath2)
btn.click()

# initiate empty dataframe
df = pd.DataFrame(columns=['Label', 'URL'])
print(df)

# step 1
tickers = ['moisturizing-cream-oils-mists', 'cleanser', 'facial-treatments', 'face-mask',
           'eye-treatment-dark-circle-treatment', 'sunscreen-sun-protection']

for ticker in tickers:
    url = 'https://www.sephora.com/shop/' + ticker + '?pageSize=300'
    driver.get(url)

    xpath = '/html/body/div[5]/div/div/div[1]/div/div/button'
    btn = driver.find_element_by_xpath(xpath)
    btn.click()
    time.sleep(20)

    browser = scrollDown(driver, 10)
    time.sleep(10)

    browser = scrollDown(driver, 10)
    time.sleep(10)

    browser = scrollDown(driver, 10)
    time.sleep(10)

    browser = scrollDown(driver, 10)

    element = driver.find_elements_by_class_name('css-ix8km1')

    subpageURL = []
    for a in element:
        subURL = a.get_attribute('href')
        subpageURL.append(subURL)

    # transform into a data frame
    dic = {'Label': ticker, 'URL': subpageURL}
    df = df.append(pd.DataFrame(dic), ignore_index = True)

# add columns
df2 = pd.DataFrame(columns=['brand', 'name', 'price', 'rank', 'skin_type', 'ingredients'])
df = pd.concat([df, df2], axis = 1)

# step 2
for i in range(len(df)+1):
    url = df.URL[i]
    driver.get(url)
    time.sleep(5)

    xpath = '/html/body/div[5]/div/div/div[1]/div/div/button'
    btn = driver.find_element_by_xpath(xpath)
    btn.click()

    # brand, name, price
    df.brand[i] = driver.find_element_by_class_name('css-avdj50').text
    df.name[i] = driver.find_element_by_class_name('css-r4ddnb ').text
    df.price[i] = driver.find_element_by_class_name('css-n8yjg7 ').text

    browser = scrollDown(driver, 1)
    time.sleep(5)
    browser = scrollDown(driver, 1)
    time.sleep(5)

    # skin_type
    detail = driver.find_element_by_class_name('css-192qj50').text
    pattern = r"✔ \w+\n"
    df.skin_type[i] = re.findall(pattern, detail)

    # ingredients
    xpath = '//*[@id="tab2"]'
    btn = driver.find_element_by_xpath(xpath)
    btn.click()

    try:
        df.ingredients[i] = driver.find_element_by_xpath('//*[@id="tabpanel2"]/div').text
    except NoSuchElementException:
        df.ingredients[i] = 'No Info'

    # rank
    try:
        rank = driver.find_element_by_class_name('css-ffj77u').text
        rank = re.match('\d.\d', rank).group()
        df['rank'][i] = str(rank)

    except NoSuchElementException:
        df['rank'][i] = 0

    print(i)    # just for verbose


df.to_csv('data/cosmetic.csv', encoding = 'utf-8-sig', index = False)
