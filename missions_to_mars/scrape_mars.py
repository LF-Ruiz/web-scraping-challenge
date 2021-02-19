# Imports and dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set url's
#### url to mars mission news
url_news="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
##### URL to mars facts
url_facts='https://space-facts.com/mars/'
#### Url to astrogeology
#### Url to astrogeology
hemispheres_home_url = 'https://astrogeology.usgs.gov'
url_hemispheres = hemispheres_home_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
url_hemispheres2 ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

results = {}
def scrape():
    browser = init_browser()

    
    #Launches Website mars.nasa news
    html_news = browser.visit(url_news)
    soup = BeautifulSoup(html_news, 'lxml')

    news={}

    slides=soup.find_all("li",class_="slide")
    for slide in slides:
        try:
            news_title = slide.h3.text
            news_p = slide.find('div', class_='rollover_description_inner').text.strip() 
    
        except Exception as e:
            print(e)

    # --- Visit Mars Facts webpage ---
    
    #read the data with Pandas
    table = pd.read_html(url_facts)

    # Get the data to a DataFrame
    facts_df = table[0]
    #Rename Columns
    facts_df.columns=['Description','Value']
    # Remove colon
    facts_df["Description"] = facts_df["Description"].replace({':':''}, regex=True)


    #convert table to HTML code
    mars_facts_table = facts_df.to_html()


    #######------------ Visit USGS Astrogeology Site to get the hemispheres ---
    html_hemispheres = browser.visit('url_hemispheres')
    # create beautifulsoup object
    soup_hemispheres = BeautifulSoup(html_hemispheres, 'lxml')

        # Finding the hemispheres data through their HTML divisions
    mars_hemispheres = soup_hemispheres.find('div', class_='collapsible results')
    hemispheres = mars_hemispheres.find_all('div', class_='item')

    # Empty list for hemispheres' Title and image_urls
    mars_images = []

    # Iterate through each hemisphere data
    for hemi in hemispheres:

        # Get Titles
        hemisphere = hemi.find('div', class_="description")
        title = hemisphere.h3.text
        title = title.strip('Enhanced')

        # Get Images
        end_link = hemisphere.a["href"]
        browser.visit(hemispheres_home_url + end_link)

        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')

        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Storage Dictionary
        image_dict = {}
        image_dict['Title'] = title
        image_dict['ImageURL'] = image_url

        # Add data to empty list "mars_images"
        mars_images.append(image_dict)

    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "mars_facts": mars_facts_table,
        "hemispheres": mars_images
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data