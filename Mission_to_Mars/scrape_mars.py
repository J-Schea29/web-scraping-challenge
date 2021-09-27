from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = { "executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    browser = init_browser()
    
    #Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    
    #Feature Image
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured = soup.find('img', class_='headerimage fade-in').get('src')
    feature_image = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{featured}"
    
    #Mars Tables
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(requests.get(facts_url).text)
    mars_df = tables[0]
    mars_df.columns=["Description", "Value"]
    html_table = mars_df.to_html()
    
    #hemisphere_images
    images_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(images_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    hem_pics = soup.find_all('div', class_='item')
    
    for pic in hem_pics:
        title = pic.find('h3').text
        partial = pic.find('a', class_='itemLink product-item')['href']
        browser.visit(f"https://astrogeology.usgs.gov{partial}")
        partial_html = browser.html
        soup = bs(partial_html, 'html.parser')
        img = soup.find('img', class_='wide-image')['src']
        img_url = f"https://astrogeology.usgs.gov{img}"

        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    mars_dict = {"news_title": news_title,
                 "news_p": news_p,
                 "featured_image": feature_image,
                 "mars_table": html_table,
                 "hemispere_images": hemisphere_image_urls
                }
    browser.quit()
    return mars_dict
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    