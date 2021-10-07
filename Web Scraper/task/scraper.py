import string

import requests
import os
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self):
        response = requests.get("https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3")
        soup = BeautifulSoup(response.text, 'html.parser')
        self.articles = soup.find_all('article')

    @staticmethod
    def scrap_nature(pages_n: int, wanted_type: str):
        """
        Scrap the Nature page and save all the news articles bodies to file named by articles names
        :param pages_n: number of pages to scrap
        :param wanted_type: type of articles which will be proccesed and saved
        :return:
        """

        articles_dict = WebScraper.find_articles(pages_n)
        host_name = 'https://www.nature.com'
        for folder, articles in articles_dict.items():
            os.mkdir(folder)
            for article in articles:
                current_type = article.find(attrs={'class': 'c-meta__type'}).text
                if current_type == wanted_type:
                    title = article.a.text
                    file_name = WebScraper.process_title(title) + '.txt'
                    link = host_name + article.a['href']
                    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
                    article_text = soup.find(attrs={'class': 'c-article-body'}).text
                    with open(os.path.join(folder, file_name), 'wb') as output_file:
                        output_file.write( article_text.encode('utf-8'))

    @staticmethod
    def process_title(title):
        """
        Process title so all punctuations will be removed and spaces will be replaced by underscores
        :param title: string representing title
        :return: string of processed title
        """

        new_title = ''
        for ch in title.strip():
            if ch == ' ':
                new_title += '_'
            elif ch not in string.punctuation:
                new_title += ch
            else:
                continue
        return new_title

    @staticmethod
    def find_articles(pages_n) -> dict:
        """
        Find all articles on the page
        :param pages_n: number of pages to scrap
        :return: dict of lists of bs4 Tags
        """
        articles = {}
        base_page = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
        for i in range(1, pages_n + 1):
            folder_name = f"Page_{i}"
            current_page = base_page + f"&page={i}"
            response = requests.get(current_page)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles[folder_name] = soup.find_all('article')
        return articles


WebScraper.scrap_nature(int(input()), input())




