
import time
import datetime
import ml
import re
import crawler
import requests
import json





regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def isUrl(text):
    return re.match(regex, text) is not None


def most_frequent(List):
    dict = {}
    count, itm = 0, ''
    for item in reversed(List):
        dict[item] = dict.get(item, 0) + 1
        if dict[item] >= count:
            count, itm = dict[item], item
    return (itm)



def more_than_n_mins_apart(time1,time2,interval):
    interval *= 60
    if abs(time1 - time2) > interval:
        return True
    return False


def timeframing(memoArr):
    toBeRet = [[memoArr[0]]]
    previousMemo = memoArr[0]
    for i in range(1,len(memoArr)):
        t1Str = " ".join(memoArr[i]["date_posted"])
        t1 = time.mktime(datetime.datetime.strptime(t1Str, "%Y-%m-%d %H:%M:%S").timetuple())
        memoArr[i]["timestamp"] = t1
        t2Str = " ".join(previousMemo["date_posted"])
        t2 = time.mktime(datetime.datetime.strptime(t2Str, "%Y-%m-%d %H:%M:%S").timetuple())
        previousMemo["timestamp"] = t2
        if more_than_n_mins_apart(t1, t2, 5):
            toBeRet.append([memoArr[i]])
        else:
            toBeRet[len(toBeRet) - 1].append(memoArr[i])
    return toBeRet

def get_summary_and_categories(memoGrpArr):
    categories = []
    summariser = ml.SummariseAndCategorise()
    for memoGrp in memoGrpArr:
        summary_arr = []
        category_arr = []
        category_obj = {}
        for memo in memoGrp:
            text = memo['text']
            if isUrl(text):
                memo['text_type'] = 1
                articleText = crawler.scrape_data_from_site(text)
                processed_arti = crawler.remove_square_brackets_and_extra_spaces(articleText)
                memo["summary"] = summariser.summarise(processed_arti)
                memo["category"] = summariser.categorise(memo["summary"])
            else:
                memo['text_type'] = 0
                memo["summary"] = summariser.summarise(crawler.remove_square_brackets_and_extra_spaces(text))
                memo["category"] = summariser.categorise(memo["summary"])
            summary_arr.append(memo["summary"])
            category_arr.append(memo["category"])

        category_obj["memos"] = memoGrp
        category_obj["category"] = most_frequent(category_arr)
        categories.append(category_obj)

    return categories


def get_from_backend():
    res = requests.get("https://multasko-backend.herokuapp.com/api/memo")
    print(res)
    json_data = json.loads(res.text)
    #print(json_data)
    processed = timeframing(json_data["memos"][:100])
    return get_summary_and_categories(processed)


if __name__ == "__main__":
    get_from_backend()