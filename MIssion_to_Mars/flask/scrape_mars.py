# Importing Modules
from splinter import Browser
from bs4 import BeautifulSoup
import re
import pandas as pd
import time


# Function to grab all of our data

def scrape_info():
  #   set path for chromedriver
    executable_path = {'executable_path': 'Resources/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # News
    url ="https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    first_story = soup.select_one("ul.item_list li.slide")
    news_title = first_story.h3.get_text()
    news_text = first_story.find(class_="article_teaser_body").get_text()

    # Featured Image
    url ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    footer=soup.select_one("footer")
    img_path=footer.a['data-link']
    img_URL = "https://www.jpl.nasa.gov" + img_path
    browser.visit(img_URL)
    html = browser.html
    soup = BeautifulSoup (html, 'html.parser')
    image=soup.select_one("figure", class_="lede")
    largeimgpath=image.a['href']
    featured_image_url="https://www.jpl.nasa.gov" + largeimgpath

    # Mars Weather
    url ="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweets=soup.find_all("span",text=re.compile('InSight sol'))
    latestweather=tweets[0].get_text()


    # Mars Facts
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]
    df.set_index('Mars - Earth Comparison', inplace=True)
    html_table = df.to_html(classes="table table-bordered table-responsive-sm table-striped")

    # Mars Hem Pics
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispherelinks=soup.find_all('div', class_="description")
    hemisphere_images=[]
    
    for link in hemispherelinks:
      hemisphereinfo={}
      hemisphereinfo["Title"] = link.h3.text.replace('Enhanced','')
      imageurl='https://astrogeology.usgs.gov' + link.a["href"]
      browser.visit(imageurl)
      html = browser.html
      soup = BeautifulSoup(html, 'html.parser')
      hemisphereinfo["ImageUrl"] =soup.find("a", text="Sample")["href"]
      hemisphere_images.append(hemisphereinfo)

    
    
    # Close the browser after scraping

    browser.quit()

    mars_data = {
        "News_Title": news_title,
        "News_Text": news_text,
        "Featured_Image":featured_image_url,
        "Latest_Weather": latestweather,
        "Mars_Facts": html_table,
        "Mars_Hemisphere_Pics": hemisphere_images
    }
    
    return mars_data


