# Cosmetic Recommendation System
#### : *Mapping cosmetic items based on their ingredients similarities and giving content-based filtering recommendation*

## ***For the Skin Beauty: What Can We Do for Ourselves?***
Whenever I want to try a new cosmetic item, it’s so difficult for me to choose which one will fit for me. It’s actually more than difficult. It’s sometimes scary because new items that I’ve never tried before tend to bring me skin trouble. If you have an experience like me, you could relate to this situation. We know the information we need here would be at the back of the cosmetic bottles. But.. It's really hard to get any clues from these chemistry names if you aren't a chemist.

![page](https://github.com/jjone36/Cosmetic/blob/master/image.png)

So instead of just being worried about my new choice, I decided to build a simple cosmetic recommendation on my own.
<br>
* **Applied skills:** Web scraping with Selenium. Text mining and word embedding. Natural Language Processing. Dimension reduction with Singular Vector decomposition. Content-based Recommendation Filtering using Cosine similarities of chemical compositions. Interactive Visualization with Bokeh.

* **Publication:** "[For Your Skin Beauty: Mapping Cosmetic Items with Bokeh](https://towardsdatascience.com/for-your-skin-beauty-mapping-cosmetic-items-with-bokeh-af7523ca68e5)", Nov 28. 2018, Medium
<br>
👉 ***Note: This project is also selected as online project tutorial on [DataCamp](https://www.datacamp.com/projects). Stay tuned for the finalized product!***

<br>

- **[cosmetic_map.jupyter](https://github.com/jjone36/Cosmetic/blob/master/cosmtic_map.ipynb)** : Visualizing the map with bokeh on jupyter notebook
- **[cosmetic_1_scraping.py](https://github.com/jjone36/Cosmetic/blob/master/cosmetic_1_scraping.py)** : Web scraping cosmetic data from Sephora
- **[cosmetic_2_ML.py](https://github.com/jjone36/Cosmetic/blob/master/cosmetic_2_ML.py)** : Cleaning data and tokenizing the ingredients from item descriptions. Visualizing the item map with the dimensional reduction technique. Defining a function for all this previous process and making an interactive bokeh app for a cosmetic recommendation
- **[Sephora_scraping_ex.py](https://github.com/jjone36/Cosmetic/blob/master/Sephora_scraping_ex.py)** : exercise code for scraping data from [Sephora](https://www.sephora.com/) with selenium
- **[cosmetic_2.csv](https://github.com/jjone36/Cosmetic/blob/master/cosmetic_2.csv)** : The dataset used in DataCamp project

- **Future Plan:**
    - Gather more data and make my own database with MySQL.
    - Apply advanced models with Neural Networks
