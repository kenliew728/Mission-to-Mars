# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    #headless = False allow us to see scrapping in action
    #headless = True will not see the script in work and behind the scene
    
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True) 

    news_title, news_paragraph = mars_news(browser)

    # Run all scrapping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser), 
        "facts": mars_facts(),
        "weather": weather(browser),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Function for pulling Mars News title and paragraph
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #news_title (adding return statement therefore printing not necessary)

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        #news_p

    except AttributeError:
        return None, None

    return news_title, news_p


# Function to pull featured image

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # try/except for error image handling
    try:

        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
        
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
     
    return img_url

#Function to pull Mars Facts
def mars_facts():

    try:
        # Use "read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Converting df into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def weather(browser):
    url = 'https://mars.nasa.gov/insight/weather/'
    browser.visit(url)

    # Parse the data
    html = browser.html
    weather_soup = soup(html, 'html.parser')

    # Scrape the Daily Weather Report table
    weather_table = weather_soup.find('table', class_='mb_table')
     
    return weather_table (classes="table table-striped")

   



def hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # 3.1 Parsing HTML
    html = browser.html
    mars_hemi_soup = soup(html, 'html.parser')

#3.2: Locating branch with link
    hemi_first = mars_hemi_soup.find('div', class_='collapsible results')
    hemi_second = hemi_first.find_all('a')

    #Initiating for loop
    for hemi in hemi_second[1::2]:   
       
        # Getting Image Title
        img_title = hemi.find('h3').text
    
    
        # Getting href link in branch
        url_link = hemi.get('href')    
    
        # Create URL to the image link
        mars_link_url = f'https://astrogeology.usgs.gov{url_link}'
    
        # Initial parsing HTML on new link
        browser.visit(mars_link_url)
        html = browser.html
        mars_full_link_soup = soup(html, 'html.parser')
    
        # Getting link in new URL branch for full image
        mars_full_img_link = mars_full_link_soup.find('div', class_='downloads')
    
        # Narrow down the link
        mars_narrow = mars_full_img_link.find('a')
    
        # Getting the link of full image
        mars_full_img_url = mars_narrow.get('href')

       
        # Combining image title and full image link
        hemisphere_image_urls.append({"img_url": mars_full_img_url,"title": img_title})

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scrape data
    print(scrape_all())









