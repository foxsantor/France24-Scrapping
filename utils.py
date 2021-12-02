import pycountry
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


def initialize():
    # Creating a webdriver instance
    s = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()
    return driver


def scroll_down(driver, initial_scroll, final_scroll):
    start = time.time()
    while True:
        driver.execute_script(f"window.scrollTo({initial_scroll},{final_scroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll
        # variable to the pixel value stored at the
        # finalScroll variable
        initial_scroll = final_scroll
        final_scroll += 1000
        # we will stop the script for 3 seconds so that
        # the data can load
        time.sleep(1)
        # You can change it as per your needs and internet speed
        end = time.time()
        # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > 5:
            break


def extract_number(string):
    numbers = [int(word) for word in string.split() if word.isdigit()]
    return numbers


def get_countries(strings_array):
    countries = []
    for string in strings_array:
        if string.find("Britain") != -1:
            string = string.replace("Britain", "United Kingdom")
        for country in pycountry.countries:
            if string.find(country.name) != -1:
                countries.append(country.name)
        return countries


def virus_topic_application(strings_array, news):
    topic = "worldwide health"
    for string in strings_array:
        if string.lower().find("covid") != -1 or string.lower().find("omicron") != -1 or string.lower().find(
                "vaccine") != -1:
            news.topic = topic


def get_links(post, news):
    post_image = post.find('img', {'class': 'm-figure__img lazy'})
    #if post_image.has_attr('alt'):
    #    news.topic = post_image.attrs['alt']
    time.sleep(1)
    all_links = post_image.attrs['srcset'].split(",")
    news.image = all_links[0].split(" ")[0]

