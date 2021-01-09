import re
# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not

import bs4 as bs
import urllib.request
import requests
import re

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def isUrl(text):
    return re.match(regex, text) is not None


def cleanhtml(raw_html):
    # cleanr = re.compile('<.*?>')
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def scrape_data_from_site(site):
    article_text = ""
    if (site):
        req = urllib.request.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
        article = urllib.request.urlopen(req).read()

        parsed_article = bs.BeautifulSoup(article, 'lxml')

        paragraphs = parsed_article.find_all('p')

        for p in paragraphs:
            article_text += " " + p.text

    return article_text


# Removing Square Brackets and Extra Spaces
def remove_square_brackets_and_extra_spaces(article_text):
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    return re.sub(r'\s+', ' ', article_text)


# Removing special characters and digits
def remove_spl_chars_and_digits(article_text):
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    return re.sub(r'\s+', ' ', formatted_article_text)


if __name__ == "__main__":
    print(scrape_data_from_site("https://www.google.com/amp/s/www.invc.news/top-agritech-startups-in-vietnam/"))