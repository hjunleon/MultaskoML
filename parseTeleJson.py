"""

@returns 2d Array of memos

"""

import pandas as pd
import crawler
import ml
import re
import datetime

# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not

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


"""
@param json The json string
@returns a list of memo objects
"""

def tele_date_to_unixtime(date_time_str: str):
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
    return date_time_obj

def tele_date_to_datePosted(date_time_str: str):
    return date_time_str.split("T")

"""
@param json Either json string or buffer
"""
def teleToMemos(json,limit):
    df = pd.read_json(json)
    messages = df['messages']
    return processMessages(messages[-limit:])
def processMessages(messages):
    summariser = ml.SummariseAndCategorise()
    toBeRet = []
    for text in messages:
        if (('photo' not in text or 'file' not in text) and (text['type'] == "message" or text['type'] == "link")):

            memoObj = {}
            memoObj["timestamp"] = tele_date_to_datePosted(text["date"])
            memoObj["textType"] = 0 #default
            textField = text
            if("text" in text):
                textField = text["text"]
            print(type(textField))
            if (isinstance(textField, list)):
                toBeRet.extend(processListOfLinks(textField, summariser, memoObj["timestamp"] ))
                continue
            elif (isinstance(textField, str)):
                if (len(crawler.remove_square_brackets_and_extra_spaces(textField)) == 0):
                    continue
                memoObj["text"] = textField
                if isUrl(textField):
                    memoObj["textType"] = 1
                    articleText = crawler.scrape_data_from_site(textField)
                    processed_arti = crawler.remove_square_brackets_and_extra_spaces(articleText)
                    memoObj["summary"] = summariser.summarise(processed_arti)
                    memoObj["category"] = summariser.categorise(memoObj["summary"])
                else:
                    memoObj["summary"] = summariser.summarise(crawler.remove_square_brackets_and_extra_spaces(textField))
                    memoObj["category"] = summariser.categorise(memoObj["summary"])

            elif (isinstance(textField, dict)):
                memoObj["text"] = textField["text"]
                if textField["type"] == "link" and isUrl(textField["text"]):
                    memoObj["textType"] = 1
                    articleText = crawler.scrape_data_from_site(textField["text"])
                    processed_arti = crawler.remove_square_brackets_and_extra_spaces(articleText)
                    processed_arti = crawler.remove_spl_chars_and_digits(processed_arti)
                    memoObj["summary"] = summariser.summarise(processed_arti)
                    memoObj["category"] = summariser.categorise(memoObj["summary"])
            print(memoObj)
            toBeRet.append(memoObj)
    return toBeRet


def processListOfLinks(list,summariser, timestamp):
    toBeRet = []
    for x in list:
        memoObj = {}
        if (isinstance(x, dict)):
            memoObj["text"] = x["text"]
            memoObj["timestamp"] = timestamp
            if x["type"] == "link" and isUrl(x["text"]):
                memoObj["textType"] = 1
                articleText = crawler.scrape_data_from_site(x["text"])
                processed_arti = crawler.remove_square_brackets_and_extra_spaces(articleText)
                memoObj["summary"] = summariser.summarise(processed_arti)
                memoObj["category"] = summariser.categorise(memoObj["summary"])
            toBeRet.append(memoObj)


    return toBeRet