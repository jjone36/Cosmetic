# Cosmetic Recommendation System
: *Mapping cosmetic items based on their ingredients similarities and giving content-based filtering recommendation*

<br>

## ***1. For the Skin Beauty: What Can We Do for Ourselves?***
Whenever I want to try a new cosmetic item, it’s so difficult for me to choose which one will fit for me. It’s actually more than difficult. It’s sometimes scary because new items that I’ve never tried before tend to bring me skin trouble. If you have an experience like me, you could relate to this situation. We know the information we need here would be at the back of the cosmetic bottles. But.. It's really hard to get any clues from these chemistry names if you aren't a chemist.

![page](https://github.com/jjone36/Cosmetic/blob/master/image/image.png)

So instead of just being worried about my new choice, I decided to build a simple cosmetic recommendation on my own.
<br>

* **Project Date:** Nov, 2018
* **Applied skills:** Web scraping with Selenium. Text mining and word embedding. Natural Language Processing. Dimension reduction with t-SNE. Content-based Recommendation Filtering using Cosine similarities of chemical compositions. Interactive Visualization with Bokeh.

* **Publication:** "[For Your Skin Beauty: Mapping Cosmetic Items with Bokeh](https://towardsdatascience.com/for-your-skin-beauty-mapping-cosmetic-items-with-bokeh-af7523ca68e5)", Nov 28. 2018, Medium

👉 ***Note: This project is selected as an online project tutorial on [DataCamp](https://www.datacamp.com/projects). Stay tuned for the finalized product!***

<br>

## ***2. File Details***
- **[01.scraping.py](https://github.com/jjone36/Cosmetic/blob/master/01.scraping.py)** : Web scarping data on Sephora with Selenium

- **[02.preprocessing.py](https://github.com/jjone36/Cosmetic/blob/master/02.preprocessing.py)** : Data cleaning & preprocessing.

- **[03.modeling.py](https://github.com/jjone36/Cosmetic/blob/master/03.modeling.py)** : Creating a database for the whole items and modeling with word embedding and dimension reduction technique.

- **[04.Visualization.ipynb](https://github.com/jjone36/Cosmetic/blob/master/04.Visualization.ipynb)** : Visualizing the items as an interactive bokeh app with Bokeh

![map](https://github.com/jjone36/Cosmetic/blob/master/image/map.gif)

<br>

## ***3. What's Next?***
- Gather more data and make my own database with MySQL.
- Apply advanced models with Neural Networks
- Create a practical Web Page/App using Flask  
