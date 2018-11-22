####################### 1. Web Scraping
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


df.to_csv('cosmetic.csv', encoding = 'utf-8-sig', index = False)

####################### 2. Cleaning data
import pandas as pd
import numpy as np
import re


cosm = pd.read_csv('cosmetic.csv')
cosm.info()

cosm = cosm.loc[pd.notnull(cosm['ingredients'])]
cosm.info()

# label
cosm.Label[cosm['Label'] == 'moisturizing-cream-oils-mists'] = str('moisturizer')
cosm.Label[cosm['Label'] == 'eye-treatment-dark-circle-treatment'] = str('eye-cream')
cosm.Label[cosm['Label'] == 'sunscreen-sun-protection'] = str('sun-protection')

# name -> duplicated item
df_2 = cosm['name'].drop_duplicates()
cosm = cosm.loc[df_2.index, :].reset_index()

# URL
cosm.drop(['URL', 'index'], axis = 1, inplace = True)

# price
pattern = re.compile(r"(\d+).\d+")
for i in range(len(cosm)):
    cosm['price'][i] = re.findall(pattern, cosm['price'][i])[0]

cosm['price'] = pd.to_numeric(cosm['price'])

# rank
cosm['rank'].fillna(0, inplace = True)
cosm.info()

# skin_type
pattern = re.compile(r"([a-zA-Z]+)\\n")
for i in range(len(cosm)):
    cosm['skin_type'][i] = re.findall(pattern, cosm['skin_type'][i])

## list column dummies
df_2 = cosm['skin_type'].str.join('|').str.get_dummies().add_prefix('type_')
cosm_dummy = cosm.join(df_2).drop('skin_type', axis = 1)


# ingredients
pattern = "^-(\w|:|\s|,|.)+\r\n\r\n"
pattern = "^-[:print:]+\r\n\r\n"

a = re.sub(pattern, " ", a)
b = pattern.search(a)
b.group()

b = []
for i in range(5):
    b = re.sub(pattern, "", cosm['ingredients'][i])


####################### 3. Exploratory Data Anaylsis
# 1. Label -> item type




# 2. rank distributions






# 3. skin_type & counts, items, rank...










####################### 4. Clustering
from nltk.tokenize import regexp_tokenize

regexp_tokenize(', ')

pattern = re.compile(r"^-(\w|:|\s|,|.)+\r\n\r\n")

word_index_map = {}
index_word_map = []
current_index = 0
corpus = []
all_ingredients = []

for i in range(len(cosm)):
    text = re.sub(pattern, "", cosm['ingredients'][i])
    text = text.lower()
    tokens = regexp_tokenize(', ')
    corpus.append(tokens)
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1
            index_word_map.append(token)

index_word_map[426]
word_index_map['']

def tokens_to_vector(tokens):
    # initialize empty array
    x = np.zeros(len(word_index_map))
    # vectorize
    for token in tokens:
        i = word_index_map[token]
        x[i] = 1
    return x

for tokens in corpus:
    X[:, i] = tokens_to_vector(tokens)
    i += 1



####################### 5. recommendation Engine
