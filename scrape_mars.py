from bs4 import BeautifulSoup
from splinter import Browser
import requests
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_mars():
    # # Current News from NASA Website
    
    # Initialize browser
    browser = init_browser()
    
    # Visit the Mars site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
   
    #grab needed info
    news_title = soup.find('div', class_="bottom_gradient").get_text
    
    news_title
    
    #grab more needed info
    
    news_p = soup.find('div', class_="rollover_description_inner").get_text
    
    news_p
    
    #store in dictionary
    news.dict = {
        "news_title": news_title,
        "news_p": news_p
    }
    
    # Return results
    return news.dict


    # # Latest Featured Image

    # Featured Image URL & visit
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    #navigate to link
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(20)
    browser.click_link_by_partial_text('more info')

    #get html code once at page
    image_html = browser.html

    #parse
    soup = BeautifulSoup(image_html, "html.parser")

    #find path and make full path
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path


    # # Mars Weather

    #weather url and html
    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)
    weather_html = browser.html

    #get lastest tweet
    soup = BeautifulSoup(weather_html, 'html.parser')
    
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text


    # # Mars Facts

    #mars facts url and splinter visit
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    #get html
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')

    #get the entire table
    table_data = soup.find('table', class_="tablepress tablepress-id-mars")

    #find all instances of table row
    table_all = table_data.find_all('tr')

    #set up lists to hold td elements which alternate between label and value
    labels = []
    values = []

    #for each tr element append the first td element to labels and the second to values
    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
            

    #make a data frame
    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
    })


    # get html code for DataFrame
    fact_table = mars_facts_df.to_html(header = False, index = False)
    fact_table


    ### Hemisphere Images
    # new url
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(usgs_url)

    usgs_html = browser.html

    soup = BeautifulSoup(usgs_html, "html.parser")

    # gets class holding hemisphere picture
    returns = soup.find('div', class_="collapsible results")
    hemispheres = returns.find_all('a')

    #setup list to hold dictionaries
    hemisphere_image_urls =[]

    for a in hemispheres:
        #get title and link from main page
        title = a.h3.text
        link = "https://astrogeology.usgs.gov" + a['href']
        
        #follow link from each page
        browser.visit(link)
        time.sleep(3)
        
        #get image links
        image_page = browser.html
        results = BeautifulSoup(image_page, 'html.parser')
        img_link = results.find('div', class_='downloads').find('li').a['href']
        
        # create image dictionary for each image and title
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = img_link
        
        hemisphere_image_urls.append(image_dict)
        
    #print(hemisphere_image_urls)

    mars_dict = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": fact_table,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict