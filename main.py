import pycountry
from news import News
import uuid
from utils import initialize
from post_scrap import scrap_all_posts


def scrap_news():
    driver = initialize()
    scrap_all_posts(driver)


if __name__ == '__main__':
    scrap_news()
