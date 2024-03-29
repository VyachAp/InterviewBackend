from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from bs4 import BeautifulSoup as BSoup
from news_aggregator.models import Headline
import random
from itertools import islice
import math
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import ClientError
import logging
import uuid
from interview.models.profession import Profession, ProfessionSalaries
from InterviewBackend.settings import S3_CONFIG
from datetime import datetime

logo_url = "https://s3.eu-central-1.amazonaws.com/cti.bucket/cti_logo.png"

# Upload the file
s3_client = boto3.client('s3', config=S3_CONFIG, region_name='eu-central-1')


def upload_file(file, bucket):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """
    try:
        bucket_filename = str(uuid.uuid4())
        response = s3_client.upload_fileobj(file, bucket, bucket_filename + '.jpg', ExtraArgs={
            'ACL': 'public-read'
        })
        url_with_params = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': bucket_filename
            },
            HttpMethod=None
        )
        url = url_with_params.split('?')[0] + '.jpg'
    except ClientError as e:
        logging.error(e)
        return False
    return url


def grey_image(image_url):
    try:
        response = requests.get(image_url)
    except:
        return logo_url
    img = Image.open(BytesIO(response.content))
    grey_img = img.convert('L')
    in_mem_file = BytesIO()
    grey_img.save(in_mem_file, format=img.format)
    in_mem_file.seek(0)
    new_url = upload_file(in_mem_file, 'cti.bucket')
    return new_url


@shared_task(name="parse_news")
def parse_news():
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
            if image_src != logo_url:
                new_headline.image = grey_image(image_src)
            else:
                new_headline.image = image_src
            news_array.append(new_headline)
            counter_hh += 1

        urls = ['https://skillbox.ru/media/?section=17', 'https://skillbox.ru/media/?section=22']
        for url_skillbox in urls:
            prefix_skillbox = 'https://www.skillbox.ru'
            session = requests.Session()
            content_skillbox = session.get(url_skillbox, verify=False).content
            soup_skillbox = BSoup(content_skillbox, "html.parser")
            header_news = soup_skillbox.find('div', {'class': 'important-block__banner row media-catalog__grid'})
            header_image = header_news.find('img').get('src')
            header_title = header_news.find('a', {'class': 'important-block__main-title'}).text[2:].strip().replace(
                '\xa0', ' ')
            header_link = header_news.find('a', {'class': 'important-block__main-title'}).get('href')
            check = Headline.objects.filter(url=prefix_skillbox + header_link).count()
            if check == 0:
                header_image = grey_image(header_image)
                new_headline = Headline(title=header_title, image=header_image, url=prefix_skillbox + header_link)
                news_array.append(new_headline)
            news_skillbox = soup_skillbox.find_all("div", {'class': ['media-catalog__tile']})
            counter_skillbox = 0
            for article in news_skillbox:
                link = article.find('a', {'class': 'media-catalog__tile-link'})
                if link:
                    link = link.get('href')
                else:
                    continue
                try:
                    image = article.find('img').get('src')
                except:
                    image = logo_url
                title = article.find('div', {'class': 'media-catalog__tile-title'}).text[2:].strip().replace('\xa0',
                                                                                                             ' ')
                check = Headline.objects.filter(url=prefix_skillbox + link).count()
                if check > 0:
                    continue
                if image != logo_url:
                    image = grey_image(image)
                else:
                    pass
                new_headline = Headline(title=title, image=image, url=prefix_skillbox + link)
                news_array.append(new_headline)

        url_gb = 'https://gb.ru/posts/success_story'
        prefix_gb = 'https://www.gb.ru'
        session = requests.Session()
        content_gb = session.get(url_gb, verify=False).content
        soup_gb = BSoup(content_gb, "html.parser")
        news_gb = soup_gb.find_all("div", {'class': ['post-item event']})
        counter_gb = 0
        for article in news_gb:
            a_tag = article.find('a', {'class': 'post-item__title h3 search_text'})
            link = a_tag.get('href')
            title = a_tag.text
            try:
                image = article.find('img').get('src')
            except:
                image = logo_url
            check = Headline.objects.filter(url=prefix_gb + link).count()
            if check > 0:
                continue
            if image != logo_url:
                image = grey_image(image)
            else:
                pass
            new_headline = Headline(title=title, image=image, url=prefix_gb + link)
            news_array.append(new_headline)

        url_vedomosti = 'https://www.vedomosti.ru/rubrics/career/career_growth'
        prefix_vedomosti = 'https://www.vedomosti.ru'
        session = requests.Session()
        content_vedomosti = session.get(url_vedomosti, verify=False).content
        soup_vedomosti = BSoup(content_vedomosti, "html.parser")
        news_vedomosti = soup_vedomosti.find_all("div", {'class': ['grid-cell__body']})
        counter_vedomosti = 0
        for article in news_vedomosti:
            content = article.find('div', {"class": 'card-article__content'})
            if not content:
                continue
            link = article.find('a').get('href')
            image_tag = content.find('img')
            if image_tag:
                # print(image_tag)
                image = image_tag.get('data-thumbnail')
            else:
                image = logo_url
            title = content.find('span', {'class': 'card-article__title'}).text
            check = Headline.objects.filter(url=prefix_vedomosti + link).count()
            if check > 0:
                continue
            if image != logo_url:
                image = grey_image(image)
            else:
                pass
            new_headline = Headline(title=title, image=image, url=prefix_vedomosti + link)
            news_array.append(new_headline)

        url_vc = 'https://www.vc.ru/hr'
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
            else:
                image = logo_url
            pre_link = article.find('a', {"class": "content-header__item content-header-number"})
            if pre_link:
                link = pre_link['href']
            check = Headline.objects.filter(url=link).count()
            if check > 0:
                continue
            new_headline = Headline()
            new_headline.title = header
            new_headline.url = link
            if image != logo_url:
                new_headline.image = grey_image(image)
            else:
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


def round_nearest(x, multiple):
    return math.floor(float(x) / multiple + 0.5) * multiple


@shared_task(name="parse_zp")
def parse_zp():
    areas = {'1': 'Москва',
             '113': "Россия"}
    for profession in Profession.objects.all():
        for area in areas.keys():
            collected_data = []
            all_zp_from = 0
            all_zp_to = 0
            results_zp_to = 0
            results_zp_from = 0
            parameters = {'text': profession.name, 'area': area, 'per_page': '100'}
            for i in range(5):
                url = 'https://api.hh.ru/vacancies'
                parameters.update({'page': i})
                response = requests.get(url, params=parameters)
                if response:
                    e = response.json()
                else:
                    continue
                collected_data.append(e)
            for item in collected_data:
                results = item['items']

                for each in results:
                    if each['salary'] is not None:
                        salary = each['salary']
                        if salary['from'] is not None:
                            all_zp_from += salary['from']
                            results_zp_from += 1

                        if salary['to'] is not None:
                            all_zp_to += salary['to']
                            results_zp_to += 1

            if results_zp_from and results_zp_to:
                from_zp = round_nearest(all_zp_from / results_zp_from, 1000)
                to_zp = round_nearest(all_zp_to / results_zp_to, 1000)
            try:
                prof_to_db = ProfessionSalaries.objects.get(profession=profession, region=areas[area])
                prof_to_db.high_salary = to_zp
                prof_to_db.low_salary = from_zp
                prof_to_db.parse_date = datetime.today()
                prof_to_db.save()
            except ProfessionSalaries.DoesNotExist:
                prof_to_db = ProfessionSalaries(profession=profession, region=areas[area], high_salary=to_zp,
                                                low_salary=from_zp)
                prof_to_db.save()
