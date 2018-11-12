import pandas as pd

from selenium import webdriver
chrome_path
driver = webdriver.Chrome(executable_path = chrome_path)
driver.implicitly_wait(30)

url = 'https://www.sephora.com/product/c-firma-day-serum-P400259?icid2=products%20grid:p400259:product'
driver.get(url)
reviews = driver.find_elements_by_class_name('css-eq4i08')

driver.find_element_by_xpath('//*[@id="ratings-reviews"]/div[10]/button').click()
reviews2 = driver.find_elements_by_class_name('css-eq4i08')

reviews = reviews.append(reviews2)
for review in reviews:
    print(review.text)

type = ['skin-care-solutions']
url = 'https://www.sephora.com/shop/' + type + '?pageSize=300'
driver.get(url)
page = WebDriverWait(driver, 10).until(EC.presence_of_elements_located())
item_pages = page.find_all('href')

# 2nd page click
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/button[3]').click()






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
