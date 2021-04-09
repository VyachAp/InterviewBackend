import requests
from rest_framework.response import Response
from bs4 import BeautifulSoup as BSoup
from news_aggregator.models import Headline
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes, api_view
import random
from itertools import islice


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def scrape(request):
    batch_size = 100
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url_hh = "http://hh.ru/articles?from=menu_new"
    prefix_hh = "http://hh.ru"
    content_hh = session.get(url_hh, verify=False).content
    soup_hh = BSoup(content_hh, "html.parser")
    news_hh = soup_hh.find_all(
        "div", {"class": "cms-announce-tiles cms-announce-tiles_underlined"}
    )[0].find_all("a")
    counter_hh = 0
    news_array = []
    try:
        for article in news_hh:
            link = article["href"]
            image_src = str(article.find("img")["src"])
            title = article.find("span").contents[0]
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = prefix_hh + link
            new_headline.image = image_src
            news_array.append(new_headline)
            counter_hh += 1

        url_forbes = 'https://www.forbes.ru/svoi-biznes'
        prefix_forbes = 'https://www.forbes.ru'
        content_forbes = session.get(url_forbes, verify=False).content
        soup_forbes = BSoup(content_forbes, "html.parser")
        news_forbes = soup_forbes.find_all("div", {"class": "grid-cell__body"})
        counter_forbes = 0
        for article in news_forbes:
            pre_link = article.find('a')
            if pre_link:
                link = prefix_forbes + pre_link['href']
            else:
                continue
            pre_header = article.find("div", {"class": "card-content__title"})
            if pre_header:
                header = pre_header.contents[0].strip()
            pre_image = article.find("img")
            if pre_image:
                image = pre_image['data-src']
            new_headline = Headline()
            new_headline.title = header
            new_headline.url = prefix_forbes + link
            new_headline.image = image
            news_array.append(new_headline)
            counter_forbes += 1

        random.shuffle(news_array)
        while True:
            batch = list(islice(news_array, batch_size))
            if not batch:
                break
            Headline.objects.bulk_create(batch, batch_size)

    except Exception as e:
        return Response(str(e))

    return Response(f"Parsed and saved:  HeadHunter - {counter_hh}, Forbes - {counter_forbes}")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return Response(context)
