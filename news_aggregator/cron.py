import requests
from bs4 import BeautifulSoup as BSoup
from news_aggregator.models import Headline
import random
from itertools import islice
from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'parse_sites'

    def do(self):
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
                check = Headline.objects.filter(url=prefix_hh + link).count()
                if check > 0:
                    continue
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
                check = Headline.objects.filter(url=link).count()
                if check > 0:
                    continue
                pre_header = article.find("div", {"class": "card-content__title"})
                if pre_header:
                    header = pre_header.contents[0].strip()
                pre_image = article.find("img")
                if pre_image:
                    image = pre_image['data-src']
                else:
                    inner_content = session.get(link, verify=False).content
                    inner_soup = BSoup(inner_content, "html.parser")
                    inner_image_div = inner_soup.find("div", {"class": "article__intro"})
                    pre_image = inner_image_div.find("img")
                    if pre_image:
                        image = pre_image["data-src"]
                    else:
                        image = None
                new_headline = Headline()
                new_headline.title = header
                new_headline.url = link
                new_headline.image = image
                news_array.append(new_headline)
                counter_forbes += 1

            url_vc = 'https://www.vc.ru/hr'
            prefix_vc = 'https://www.vc.ru'
            content_vc = session.get(url_vc, verify=False).content
            soup = BSoup(content_vc, "html.parser")
            news_vc = soup.find_all("div", {"class": "feed__item l-island-round"})
            counter_vc = 0
            for article in news_vc:
                pre_header = article.find("div", {"class": "content-title content-title--short l-island-a"})
                if pre_header:
                    header = pre_header.contents[0].strip()
                pre_image = article.find("div", {"class": "andropov_image"})
                if pre_image:
                    image = pre_image['data-image-src']
                pre_link = article.find('a', {"class": "content-header__item content-header-number"})
                if pre_link:
                    link = pre_link['href']
                check = Headline.objects.filter(url=link).count()
                if check > 0:
                    continue
                new_headline = Headline()
                new_headline.title = header
                new_headline.url = link
                new_headline.image = image
                news_array.append(new_headline)
                counter_vc += 1

            random.shuffle(news_array)
            while True:
                batch = list(islice(news_array, batch_size))
                if not batch:
                    break
                Headline.objects.bulk_create(batch, batch_size)

        except Exception as e:
            print(str(e))

