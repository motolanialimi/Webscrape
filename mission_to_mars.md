

```python
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd
```

NEWS FROM NASA WEBSITE


```python
#set up splinter browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless = False)

#visit url
url = "https://mars.nasa.gov/news/"
browser.visit(url)

#pull html text and parse
html_code = browser.html
soup = BeautifulSoup(html_code, "html.parser")

#grab needed info
news_title = soup.find('div', class_="bottom_gradient")
news_p = soup.find('div', class_="rollover_description_inner").text
```

Featured Image


```python
# Featured Image URL & visit
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)

#navigate to link
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(10)
# browser.click_link_by_partial_text('more info')

# #get html code once at page
# image_html = browser.html

# #parse
# soup = BeautifulSoup(image_html, "html.parser")

# #find path and make full path
# image_path = soup.find('figure', class_='lede').a['href']
# featured_image_url = "https://www.jpl.nasa.gov/" + image_path
```

Mars Weather


```python
marsweather_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(marsweather_url)

weather_html = browser.html

soup = BeautifulSoup(weather_html, 'html.parser')

mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text
```

Mars Facts


```python
#mars facts url and splinter visit
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)

#get html
facts_html = browser.html

soup = BeautifulSoup(facts_html, 'html.parser')
```


```python
#get the entire table
table_data = soup.find('table', class_="tablepress tablepress-id-mars")
```


```python
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
```


```python
#make a data frame and view
mars_facts_df = pd.DataFrame({
    "Label": labels,
    "Values": values
})
```


```python
mars_facts_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Label</th>
      <th>Values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km\n</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km\n</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)\n</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# get html code for DataFrame
fact_table = mars_facts_df.to_html(header = False, index = False)
fact_table
```




    '<table border="1" class="dataframe">\n  <tbody>\n    <tr>\n      <td>Equatorial Diameter:</td>\n      <td>6,792 km\\n</td>\n    </tr>\n    <tr>\n      <td>Polar Diameter:</td>\n      <td>6,752 km\\n</td>\n    </tr>\n    <tr>\n      <td>Mass:</td>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <td>Moons:</td>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <td>Orbit Distance:</td>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <td>Orbit Period:</td>\n      <td>687 days (1.9 years)\\n</td>\n    </tr>\n    <tr>\n      <td>Surface Temperature:</td>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <td>First Record:</td>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <td>Recorded By:</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'




```python
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
    title = a.h3
    link = "https://astrogeology.usgs.gov" + a['href']
    
    #follow link from each page
    browser.visit(link)
    time.sleep(5)
    
    #get image links
    image_page = browser.html
    results = BeautifulSoup(image_page, 'html.parser')
    img_link = results.find('div', class_='downloads').find('li').a['href']
    
    # create image dictionary for each image and title
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] = img_link
    
    hemisphere_image_urls.append(image_dict)
    
print(hemisphere_image_urls)
    
    #browser.visit


# usgs_html
```

    [{'title': None, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': <h3>Cerberus Hemisphere Enhanced</h3>, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': None, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': <h3>Schiaparelli Hemisphere Enhanced</h3>, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': None, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': <h3>Syrtis Major Hemisphere Enhanced</h3>, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, {'title': None, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}, {'title': <h3>Valles Marineris Hemisphere Enhanced</h3>, 'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]
    
