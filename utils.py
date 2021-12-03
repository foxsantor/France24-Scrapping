import uuid

import pycountry
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from pathlib import Path
import csv


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
    try:
        all_links = post_image.attrs['srcset'].split(",")
        news.image = all_links[0].split(" ")[0]
        if post_image.has_attr('alt'):
            news.topic = post_image.attrs['alt']
    except:
        news.topic = "N/A"


def generate_csv_file(data):
    my_file = Path("francey_data.csv")

    if my_file.is_file():
        mode = 'a'
        data = check_entries(data)
    else:
        mode = 'w'
    with open('francey_data.csv', mode, newline='') as csv_file:
        fieldnames = ['id', 'image_link', 'title', 'countries', 'topic', 'optional_info']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if mode == 'w':
            writer.writeheader()
        if len(data) == 0:
            return
        for entry in data:
            writer.writerow({'id': entry.id, 'image_link': entry.image,
                             'countries': str(entry.countries)
                            .replace("{", "")
                            .replace("}", "")
                            .replace("set()", "")
                            .replace("'", ""),
                             'topic': entry.topic, 'title': entry.title, 'optional_info': entry.optional_info})


def check_entries(data):
    new_data = []
    is_in_file = False
    with open('francey_data.csv', 'r') as csvfile:
        my_content = csv.reader(csvfile, delimiter=',')
        for entry in data:
            for row in my_content:
                if entry.title in row:
                    is_in_file = True
                    break
                else:
                    is_in_file = False
            if not is_in_file:
                new_data.append(entry)
    if len(new_data) == 0:
        return []
    else:
        return new_data
