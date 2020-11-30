#!/usr/bin/env python
# coding: utf-8




# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time
from selenium import webdriver



def scrape_info():
    mars = {}




    # Chromedriver
    #get_ipython().system('which chromedriver')




    # NASA Mars News




    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://mars.nasa.gov/news/')




    # Parse the html result with soup 
    html = browser.html
    soup = bs(html, 'html.parser')




    news_title = soup.select_one('div.content_title a').text




    # Retrieve the latest paragraph
    news_p = soup.select_one('div.article_teaser_body').text
    mars["news_title"] = news_title
    mars["news_p"] = news_p




    # Create print statement of the latest news title and paragraph text
    print(f'The latest news title is: {news_title} \nThe paragraph text is: {news_p}')




    # JPL Mars Space Images - Featured Image



    #Visit Image Url
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)





    # Find the full image botton and click
    img_elem = browser.find_by_id('full_image')
    img_elem.click()





    # Find the more info button and click
    browser.is_element_present_by_text('more info', wait_time=3)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()





    # Parse the html result with soup
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')





    # Find the relative image url
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    img_url_rel





    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url
    mars["featured_image"] = img_url




    # Mars Facts





    # URL
    facts_url = 'https://space-facts.com/mars/'

    # Read html by Pandas
    tables = pd.read_html(facts_url)

    # Slice off dataframes that needed
    mars_df = tables[0]

    # Set columns
    mars_df.columns = ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)

    mars_html = mars_df.to_html()

    mars_html

    mars["facts"] = mars_html





    hem_list = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hemisphere_image_urls = []

    for hem in hem_list:
        # Visit URL
        hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hem_url)
        
        # Find the hemisphere images and click
        hem_elem = browser.links.find_by_partial_text(hem)
        hem_elem.click()
        
        # Find original to download full img
        hem_elem_org = browser.find_by_text("Original", wait_time=1)
        hem_elem_org.click()
        
        # Scrape the Mars website 
        hem_html = browser.html
        hem_soup = bs(hem_html, 'html.parser')
        
        hem_title = hem_soup.h2.text
        hem_url = hem_soup.select_one('li a')['href']
        
        hem_dict = {
            'title': hem_title,
            'img_url': hem_url
        }
        
        hemisphere_image_urls.append(hem_dict)




    hemisphere_image_urls

    mars["hemispheres"] = hemisphere_image_urls

    return mars
if __name__ == "__main__":
    print(scrape_info())
