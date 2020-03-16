# Import dependencies
from bs4 import BeautifulSoup
import requests
import selenium
from splinter import Browser
import pandas as pd
import re
import time


def init_browser():
    executable_path = {'executable_path': r'C:\webdriver\chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_info = {}

    # visit nasa website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # retrieve title and paragraph for first news title on NASA site
    news_title = soup.find("li", class_="slide").find("div", class_="content_title").text
    news_p = soup.find("li", class_="slide").find("div", class_="article_teaser_body").text
    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p

    #JPL Mars Space Images - Featured Image

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
        
    # scrape page into soup
    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')

    # retrieve the text from the style which includes background image url
    div_style = soup2.find('article')['style']
    
    # extract image location from style and combine with jpl index url
    short_url = div_style.replace("background-image: url('","").replace("');","")
    featured_image_url = "https://www.jpl.nasa.gov"+short_url
    mars_info["featured_image_url"] = featured_image_url

    # Mars Weather

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(5)
    html = browser.html
    soup3 = BeautifulSoup(html, 'html.parser')

    # retrieve Mars weather tweet
    mars_tweet = soup3.find('div', class_='css-1dbjc4n')
    weather_tweets = mars_tweet(text=re.compile(r' sol'))
    mars_weather = weather_tweets[0]
    mars_info["mars_weather"] = mars_weather

    # Mars Facts    

    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)
    html = browser.html
    soup4 = BeautifulSoup(html, 'html.parser')

    #retrieve Mars Facts
    table = soup4.find('table', class_='tablepress')
    table = pd.read_html(url4)
    mars_df = table[0]
    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')
    mars_info["html_table"] = html_table

    # Mars Hemispheres

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    # use a loop to loop through the 4 hemispheres, click through to their page and pull high res image
    html = browser.html
    soup5 = BeautifulSoup(html, 'html.parser')

    hemi_list = []
    hemispheres = soup5.find_all('div', class_="item")
    for hemi in hemispheres:
        link = hemi.a['href']
        link_long = "https://astrogeology.usgs.gov"+link
        browser.visit(link_long)
        html2 = browser.html
        soup6 = BeautifulSoup(html2, 'html.parser')
        raw_title = soup6.find('title').text
        title = raw_title.replace("Enhanced | USGS Astrogeology Science Center","").replace("e ","e")
        hemi_dict = {}
        hemi_dict.update({'title': title})
        short_img_url = soup6.find('img', class_="wide-image")["src"]
        img_url = "https://astrogeology.usgs.gov"+short_img_url
        hemi_dict.update({'img_url': img_url})
        hemi_list.append(hemi_dict)

    mars_info["hemi_list"] = hemi_list

    # Close the browser after scraping
    browser.quit()

    return mars_info

