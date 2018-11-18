import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chrome_path = "C:\\Users\jjone\Downloads\chromedriver"

def scrollDown(driver, numberOfScrollDowns):
    body = driver.find_element_by_tag_name("body")
    while numberOfScrollDowns >=0:
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
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


tickers = ['moisturizing-cream-oils-mists', 'cleanser', 'facial-treatments', 'face-mask',
           'eye-treatment-dark-circle-treatment', 'sunscreen-sun-protection']

for ticker in tickers:
    url = 'https://www.sephora.com/shop/' + ticker
    driver.get(url)

    xpath = '/html/body/div[5]/div/div/div[1]/div/div/button'
    btn = driver.find_element_by_xpath(xpath)
    btn.click()

    # 1 page
    browser = scrollDown(driver, 10)
    element = driver.find_elements_by_class_name('css-ix8km1')

    subpageURL = []
    for a in element:
        subURL = a.get_attribute('href')
        subpageURL.append(subURL)

    # 2~5 page
    for i in range(3, 7):
        xpath_next_page = '/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/button' + str([i])
        btn = driver.find_element_by_xpath(xpath_next_page)
        btn.click()
        browser = scrollDown(driver, 10)

        element = driver.find_elements_by_class_name('css-ix8km1')
        for a in element:
            subURL= a.get_attribute('href')
            subpageURL.append(subURL)
        time.sleep(20)

    # transform into a data frame
    dic = {'Label': ticker, 'URL': subpageURL}
    df = df.append(pd.DataFrame(dic))



## scraping product reviews
url_2 = 'https://www.sephora.com/product/ultra-facial-cream-P421996?icid2=products%20grid:p421996:product'
driver.get(url_2)
xpath = '/html/body/div[5]/div/div/div[1]/div/div/button'
btn = driver.find_element_by_xpath(xpath)
btn.click()

driver.find_element_by_xpath('//*[@id="ratings-reviews"]/div[16]/button').click()
reviews = driver.find_elements_by_class_name('css-eq4i08')

for post in reviews:
    print(post.text)





from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer, MaxAbsScaler
from sklearn.pipeline import make_pipeline

# Create a MaxAbsScaler: scaler
scaler = MaxAbsScaler()
# Create an NMF model: nmf
nmf = NMF(n_components = 20)
# Create a Normalizer: normalizer
normalizer = Normalizer()
# Create a pipeline: pipeline
pipeline = make_pipeline(scaler, nmf, normalizer)
# Apply fit_transform to artists: norm_features
norm_features = pipeline.fit_transform(items)
# Create a DataFrame: df
df = pd.DataFrame(norm_features, index = item_names)
# Select row of 'Bruce Springsteen': artist
artist = df.loc['Water Bomb']
# Compute cosine similarities of the item between the itmes
similarities = df.dot(itmes)
# Display those with highest cosine similarity
print(similarities.nlargest())
