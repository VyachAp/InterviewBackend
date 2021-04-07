import requests
from rest_framework.response import Response
from bs4 import BeautifulSoup as BSoup
from news_aggregator.models import Headline
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes


@renderer_classes((JSONRenderer,))
def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "http://hh.ru/articles?from=menu_new"
    prefix = "http://hh.ru"
    content = session.get(url, verify=False).content
    soup = BSoup(content, "html.parser")
    news = soup.find_all(
        "div", {"class": "cms-announce-tiles cms-announce-tiles_underlined"}
    )[0].find_all("a")
    counter = 0
    try:
        for article in news:
            link = article["href"]
            image_src = str(article.find("img")["src"])
            title = article.find("span").contents[0]
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = prefix + link
            new_headline.image = image_src
            new_headline.save()
            counter += 1
    except Exception as e:
        return Response(str(e))

    return Response(f"Parsed and saved: {counter}")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return Response(context)
