# web-scraping-challenge

# Part 1
For this project, I had to scrape data on Mars from several websites and present it on a webpage using flask (with a button to scrape most recent data). I did this using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter. 
The first peice of data I needed was the title and descriptive paragraph of the most recnt article on [NASA Mars News website](https://mars.nasa.gov/news/). 
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

, <https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html>, [Space-Facts website](https://space-facts.com/mars/), and [USGS Astrogeology website](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars).
