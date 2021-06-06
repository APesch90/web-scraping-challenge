#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Initialize Browser 

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


# In[3]:


# Scrape News Headline
def scrape_news():
    browser = init_browser()
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    browser.quit()
    return [news_title, news_p]

#print(scrape_news())


# In[4]:


# Scrape Featured Image

def scrape_image():
    browser = init_browser()
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    relative_image_path = soup.find_all('img')[1]['src']
    featured_image_url = url + "/" + relative_image_path
    browser.quit()
    return(featured_image_url)

#print(scrape_image())


# In[5]:


# Scrape Mars Facts Table

"""Visit the Mars Facts webpage [here](https://galaxyfacts-mars.com) 
and use Pandas to scrape the table containing facts about the planet 
including Diameter, Mass, etc."""

# Use Pandas to convert the data to a HTML table string.
def scrape_facts():
    url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(url)
    return table
#print(scrape_facts())


# In[6]:


## Scrape Mars Hemisphere Images
# Step 1 - Get hemisphere titles containing the hemisphere name with Beautiful Soup
""" Step 2 - Get image url string for the full resolution 
# hemisphere images using Splinter"""

def scrape_hemispheres():
    url = 'https://marshemispheres.com/'
    response = requests.get(url)
    soup_1 = bs(response.text, 'html')
    browser = init_browser()
    list_urls = ['https://marshemispheres.com/cerberus.html', 'https://marshemispheres.com/schiaparelli.html', 
                 'https://marshemispheres.com/syrtis.html', 'https://marshemispheres.com/valles.html'] 
    
    results = soup_1.find_all('h3')

    title_list = []
    # For loop to get all the headers (hemispheres) 
    # dropped the 5th element called "Back"
    for result in results[:4]:
        # Grab the header text
        header = result.text
        # Remove the word "Enhanced"
        header_cleaned = header[:-9]
        title_list.append(header_cleaned)

    final_urls_list = []
    
    for url in list_urls:
        browser.visit(url)
        time.sleep(2)
        html = browser.html
        soup_2 = bs(html, 'html.parser')
        links = [a['href'] for a in soup_2.find_all('a', href=True)]
        image_url = links[4]
        full_url = url + "/" + image_url
        clean_url = url[:28]
        final_urls = clean_url + image_url
        final_urls_list.append(final_urls)

    hemisphere_image_urls = [
        {"title": title_list[0], "img_url": final_urls_list[0]},
        {"title": title_list[1], "img_url": final_urls_list[1]},
        {"title": title_list[2], "img_url": final_urls_list[2]},
        {"title": title_list[3], "img_url": final_urls_list[3]}
    ]

    browser.quit()
    return(hemisphere_image_urls)

#print(scrape_hemispheres())


# In[7]:


# Bring everything together into one dictionary



def scrape():
    mars_data = {}
    news = scrape_news()
    featured_image = scrape_image()
    facts = scrape_facts()
    hemispheres = scrape_hemispheres()
    
    
    
    mars_data['news'] = news
    mars_data['featured_image'] = featured_image
    mars_data['facts'] = facts
    mars_data['hemispheres'] = hemispheres
    
    return mars_data
#print(scrape())

