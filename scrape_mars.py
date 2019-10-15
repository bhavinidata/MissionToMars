# !/usr/bin/env python
# coding: utf-8

import pandas as pd

from splinter import Browser
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)
    return browser

def scrape():
    browser = init_browser()
    mars_info = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    # Find the latest news
    news_info = soup.find("div", class_ = "list_text")
    news_title = news_info.find("div", class_ = "content_title").text
    news_p = news_info.find("div", class_ = "article_teaser_body").text

    mars_info["news_title"] = news_title
    mars_info["news_paragraph"] = news_p

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    featured_img_info = soup.find("article", class_ = "carousel_item")["style"]
    featured_img_idx_before = featured_img_info.find("url('/")
    featured_img_idx_after = featured_img_info.find("')")
    featured_img_url = featured_img_info[featured_img_idx_before+len("url('/"):featured_img_idx_after]
    #Getting the base url and featured image url
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    featured_image_url = base_url+ featured_img_url
    mars_info["featured_img_url"] = featured_image_url

    # Mars Weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    weather_tweet_info = soup.find("div", class_ = "js-tweet-text-container")

    weather_tweet_text = weather_tweet_info.find("p", class_ ="tweet-text").text

    weather_tweet_text_idx_after = weather_tweet_text.find("pic.twitter.com")
    weather_tweet_text_idx_before = weather_tweet_text.find("sol")

    mars_weather = weather_tweet_text[weather_tweet_text_idx_before:weather_tweet_text_idx_after]
    mars_info["mars_weather_info"] = mars_weather


    # Mars Facts
    url = "https://space-facts.com/mars/"

    fact_table = pd.read_html(url)
    mars_fact_df = fact_table[1]

    mars_fact_df.columns = ["Parameters", "Fact"]
    mars_fact_df.set_index("Parameters", inplace=True)

    mars_facts_html = mars_fact_df.to_html()
    mars_info["mars_facts_html"] = mars_facts_html

    # Mars hemispheres
    url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, "lxml")
    img_divs = soup.find_all("div", class_ = "description")

    hemisphere_image_info = []
    base_url = "https://astrogeology.usgs.gov"
    for img_div in img_divs:
        img_info = {}

        img_title = img_div.find("h3").text
        img_info["img_title"] = img_title

        partial_img_url = img_div.find("a", class_ = "itemLink product-item")["href"]
        full_img_url = base_url + partial_img_url

        browser.visit(full_img_url)
        full_img_url = browser.html
        soup = BeautifulSoup(full_img_url, "lxml")

        img_url = soup.find("div", class_ = "downloads").li.a["href"]
        img_info["img_url"]=img_url
        hemisphere_image_info.append(img_info)

    mars_info["mars_hemisphere_info"] = hemisphere_image_info

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info

if __name__ == "__main__":
    mars_info = scrape()
    print(f"Here is Mars info: {mars_info}")


