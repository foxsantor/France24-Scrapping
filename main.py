import pycountry
from news import News
import uuid
from utils import initialize,generate_csv_file
from post_scrap import scrap_all_posts


def scrap_news():
    driver = initialize()
    all_news = scrap_all_posts(driver)
    generate_csv_file(all_news)


if __name__ == '__main__':
    scrap_news()
