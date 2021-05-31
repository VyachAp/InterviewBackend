import requests
from rest_framework.response import Response
from bs4 import BeautifulSoup as BSoup
from news_aggregator.models import Headline
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes, api_view
import random
from itertools import islice
from PIL import Image
from io import BytesIO
import boto3
from botocore.exceptions import ClientError
import logging
import uuid

logo_url = "https://s3.eu-central-1.amazonaws.com/cti.bucket/cti_logo.png"
from botocore.config import Config

my_config = Config(signature_version='s3v4',
                   retries={
                       'max_attempts': 10,
                   },
                   s3={'addressing_style': 'auto'},
                   )

# Upload the file
s3_client = boto3.client('s3', config=my_config, region_name='eu-central-1')


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
    # file.image = new_url
    # file.save()


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
            check = Headline.objects.filter(url=prefix_hh + link).count()
            if check > 0:
                continue
            image_src = str(article.find("img")["src"])
            title = article.find("span").contents[0]
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = prefix_hh + link
            new_headline.image = grey_image(image_src)
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
                image = inner_image_div.find("img")["data-src"]
            new_headline = Headline()
            new_headline.title = header
            new_headline.url = link
            new_headline.image = grey_image(image)
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
            new_headline.image = grey_image(image)
            news_array.append(new_headline)
            counter_vc += 1

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


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
def upgrade_to_chb(request):
    for file in news_list(request).data['object_list']:
        url = grey_image(file)
        file.image = url
        file.save()

    return Response(200)
