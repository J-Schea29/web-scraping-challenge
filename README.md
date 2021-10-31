# web-scraping-challenge

## Table of Contents
* [Introduction](#introduction)
* [Setup](#setup)
* [Deployment](#deployment)
* [Sources](#sources)

## Introduction
### Summary
For this project, I had to scrape data about Mars from several websites and present it on a webpage using flask (with a button to scrape most recent data). I did this using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
### Requirements
* Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
* Use splinter to navigate the JPL site and find the image url for the current Featured Mars Image
* Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
* Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar’s hemispheres.
* Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped above.

## Setup
The first piece of data I needed was the title and descriptive paragraph of the most recent article on [NASA Mars News website](https://mars.nasa.gov/news/) which I retrieved with the following code: 
```python
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')
news_title = soup.find_all('div', class_='content_title')[1].text
news_p = soup.find_all('div', class_='article_teaser_body')[0].text
```
Next, I got the feature image off the website <https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html> using this code:
```python
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(image_url)
html = browser.html
soup = bs(html, 'html.parser')
featured = soup.find('img', class_='headerimage fade-in').get('src')
feature_image = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{featured}"
```
After that, I used pandas to get the table of Mars facts off [Space-Facts website](https://space-facts.com/mars/) and then converted it back to html:
```python
facts_url = 'https://space-facts.com/mars/'
tables = pd.read_html(requests.get(facts_url).text)
mars_df = tables[0]
mars_df.columns=["Description", "Value"]
html_table = mars_df.to_html()
```
Finally, I had to get four hemispere images of Mars from [USGS Astrogeology website](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) using this code:
```python
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
```

## Deployment 
Next, I copied all the code above from my Jupyter notebook and put it in a file call scrape_mars.py. In this file, I defined the fuction called scrape() which when excuted does all the action of the copied code. After this, I created my app.py for my flask aplication and in it imported my function scrape() from scrape_mars.py.
```python
import scrape_mars

@app.route("/scrape")
def scrape():
    
    mars_dict = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")
```
I then went on to create the index.html file which would ultimate become the template for my flask application. Notably, I make sure to put a button on the webpage that allows you to scrape the most recent data.
```html
<div class="jumbotron text-center" style="background-image: url('http://2.bp.blogspot.com/-EV6tLYaDZJE/Th6tirHH-uI/AAAAAAAAACY/pis1pJavAVE/s1600/3511_plate_5_copy.jpg'); height:300px">
  <h1 style="color: red;">Mission to Mars</h1>
  <p><a class="btn btn-primary btn-lg" href="/scrape" role="button">Scrape New Data!</a></p>
```
I then dispayed all data gathered on the webpage.
![image](https://user-images.githubusercontent.com/84929443/135166772-ab070cd2-8fe6-4fb5-b890-e72e3658d5d8.png)
![image](https://user-images.githubusercontent.com/84929443/135166876-ee53b2c8-674c-42dc-96d7-78785ec10daa.png)
![image](https://user-images.githubusercontent.com/84929443/135166917-60dc356a-1813-454e-9954-8d5cff46cdd0.png)

## Sources
[NASA Mars News website](https://mars.nasa.gov/news/)

<https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html>

[Space-Facts website](https://space-facts.com/mars/)

[USGS Astrogeology website](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

