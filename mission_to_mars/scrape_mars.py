import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape():
    
    browser = Browser('chrome', **executable_path, headless=False)
    #  Call Function to get the title and paragraph
    title,paragraph=news(browser)
    #  Set the other objects 
    data = {
        'title':title,
        'paragraph':paragraph,
        'image':image(browser),
        'facts':str(facts()),
        'hemispheres':hemispheres(browser)
    }
    return data

# Function go get the Title and Paragraph 
def news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # News title
    latest_news = soup.find_all("div", class_="content_title")[0]
    latest_news_title = latest_news.text

    # Paragraph Text
    paragraph = soup.find_all("div", class_="article_teaser_body")[0]
    latest_news_paragraph = paragraph.text
    return latest_news_title,latest_news_paragraph

def image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html
    soup=BeautifulSoup(html,"html.parser")
    img_group=soup.find('div', class_='floating_text_area')

    link=img_group.find('a')
    href=link['href']
    href
    featured_image_url="https://spaceimages-mars.com/" + href
    return featured_image_url

def facts():
    url="https://galaxyfacts-mars.com/"
    mars_table=pd.read_html(url)
    # * Use Pandas to convert the data to a HTML table string.
    df=mars_table[0]
    mars_df=df.set_index(0)
    mars_df.to_html("mars_table.html")
    return mars_df

def hemispheres(browser):
    browser.visit('https://marshemispheres.com/')

    hemispheres = []
    for i in range(4):
        hemisphere = {}
        hemisphere['title']=browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemisphere['img'] = browser.find_by_text('Sample')['href']    
        hemispheres.append(hemisphere)
        browser.back()
    browser.quit()
    return hemispheres
