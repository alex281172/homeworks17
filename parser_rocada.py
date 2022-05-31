import requests
from bs4 import BeautifulSoup

url = 'https://shop.rocadamed.ru/novosti/'

def parser_roc():




    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html5lib')

    tab_content = soup.find_all('a', attrs={'class': 'nav-link', 'data-toggle': 'tab'})

    list_url = []
    for counter in range(len(tab_content)):
        href_year = tab_content[counter].get('href')
        url_year = f'https://shop.rocadamed.ru{href_year}'

        response1 = requests.get(url_year)
        soup1 = BeautifulSoup(response1.text, 'html5lib')

        tab_content1 = soup1.find_all('div', class_='news-headline')

        for counter1 in range(len(tab_content1)):
            href_year_news = tab_content1[counter1].a.get('href')
            url_year_news = f'https://shop.rocadamed.ru{href_year_news}'
            list_url.append(url_year_news)

    f = open('history.txt', 'w')
    f.write('')
    f.close()
    f = open('history.txt', 'a')

    for news_counter in list_url:
        response = requests.get(news_counter)
        soup3 = BeautifulSoup(response.text, 'html5lib')
        # print('-' * 50)
        news_date = soup3.find('p', class_='dt')

        news_text = soup3.find('div', class_='news-content')
        news_text1 = news_text.get_text('\n', strip=True)
        print(news_text1)
        f.write('-' * 50)
        f.write('\n')
        f.write(news_text1)
        f.write('\n')
        news_text2 = soup3.find(class_='news__content')

        try:
            news_text3 = news_text2.get_text('\n', strip=True)
            print(news_text3)
            f.write(news_text3)
            f.write('\n')

        except:
            news_text3 = 'Нет содержимого'
            print(news_text3)
            f.write(news_text3)
            f.write('\n')

    f.close()

