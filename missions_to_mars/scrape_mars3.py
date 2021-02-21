# Imports and dependencies
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# set url's
#### url to mars mission news
url_news="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
##### URL to mars facts
url_facts='https://space-facts.com/mars/'
#### Url to astrogeology
hemispheres_home_url = 'https://astrogeology.usgs.gov'
url_hemispheres = hemispheres_home_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


def scrape():

    # set url's
#### url to mars mission news
    url_news="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
##### URL to mars facts
    url_facts='https://space-facts.com/mars/'
#### Url to astrogeology
    hemispheres_home_url = 'https://astrogeology.usgs.gov'
    url_hemispheres = hemispheres_home_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'



###  Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.
###  Assign the text to variables that you can reference later.
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url_news)
    time.sleep(1)
    html = browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(html, 'lxml')
    #just the newest news
    slide=soup.find("li",class_="slide")
    news_title = slide.h3.text
    news_p = slide.find('div', class_='rollover_description_inner').text.strip()

    browser.quit()

    ### Mars Facts

#* Visit the Mars Facts webpage [here](https://space-facts.com/mars/) 
# and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

#* Use Pandas to convert the data to a HTML table string.

    #read the data with Pandas
    table = pd.read_html(url_facts)
    # Get the data to a DataFrame
    facts_df = table[0]
    #Rename Columns
    facts_df.columns=['Description','Value']
    # Remove colon
    facts_df["Description"] = facts_df["Description"].replace({':':''}, regex=True)
    fact_table = facts_df.to_html()

    ### Mars Hemispheres

# * Visit the USGS Astrogeology 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title 
# * Append the dictionary with the image url string and the hemisphere title to a list. 
#   This list will contain one dictionary for each hemisphere.

    # URL to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # visit the astrogeology website
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    hem_image = []

    products = soup.find("div", class_="result-list")
    links = soup.find_all('div', class_='item')

    for planet in links:
    # find title in landing page under div-item-a-href-h3
        title = planet.find("h3").text
    # find link in same div-item-a-href area
        link_end = planet.find("a")["href"]
    # add initial web page begining to link end
        image_link = "https://astrogeology.usgs.gov/" + link_end
    # visit browser page using the link
        browser.visit(image_link)
    # html object
        html = browser.html
    # Create BeautifulSoup object; parse with "html.parser"
        soup=bs(html, "html.parser")
    # Retreive all elements that contain planets' title and url
        download= soup.find("div", class_="downloads")
        image_url = download.find("a")["href"]
        hem_image.append({"title":title, "img_url": image_url})



    browser.quit()

    # Create dictionary for all info scraped from sources above
    mars_data={
        "news_title":news_title,
        'news_p':news_p,
        "fact_table":fact_table,
        "mars_images":hem_image
    }

    return mars_data