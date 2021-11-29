
from bs4 import BeautifulSoup

from news import News
from utils import scroll_down, get_countries, virus_topic_application, get_links


def scrap_all_posts(driver):
    driver.get("https://www.france24.com/en/")
    scroll_down(driver, 0, 1000)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    all_news = [get_main_post(soup)]
    all_news.extend(get_smaller_post(soup))
    all_news.extend(get_bigger_post(soup))
    print(all_news)
    for post in all_news:
        print(post)
    return all_news


def get_main_post(soup):
    news = News()
    div_main_post = soup.find('div', {'class': 'o-layout-list__item o-layout-list__item--main-item'})
    get_links(div_main_post, news)
    news.title = div_main_post.find('p', {'class': 'article__title'}).get_text().strip()
    info_list = div_main_post.findAll('a', {'class': 'm-list-main-related__article'})
    strings = [news.title, news.topic]
    news.optional_info = []
    for info in info_list:
        news.optional_info.append(info.getText().strip())
        strings.append(info.getText().strip())
    virus_topic_application(strings, news)
    news.countries = set(get_countries(strings))

    return news


def get_smaller_post(soup):
    list = []
    other_posts = soup.findAll('div', {'class': 'o-layout-list__item l-m-100 l-t-50 l-d-50'})
    for post in other_posts:
        news = News()
        get_links(post, news)
        list.append(news)
        news.title = post.find('p', {'class': 'article__title'}).get_text().strip()
        strings = [news.title, news.topic]
        virus_topic_application(strings, news)
        news.countries = set(get_countries(strings))

    return list


def get_bigger_post(soup):
    list = []
    other_posts = soup.findAll('div', {'class': 'm-item-list-article  m-item-list-article--highlighted-main'})
    for post in other_posts:
        news = News()
        get_links(post, news)
        list.append(news)
        news.title = post.find('p', {'class': 'article__title'}).get_text().strip()
        strings = [news.title, news.topic]
        virus_topic_application(strings, news)
        news.countries = set(get_countries(strings))
    return list
