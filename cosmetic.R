# https://www.sephora.com/

library(tidyverse)
library(httr)
library(rvest)
library(jsonlite)

library(magrittr)
library(RColorBrewer)
library(gridExtra)
library(GGally)

library(tidytext)
library(text2vec)
library(caret)


url = 'https://www.sephora.com/shop/skin-care-solutions'

http_type(GET(url))
resp = read_html(url)
html_nodes(resp, css = '.css-ix8km1') %>% html_attr('href')


