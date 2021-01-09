# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import parseTeleJson
#import BeautifulSoup
import parseApiInput
data = {
    "memos": [{
        "category_id": 1,
        "date_posted": ["2021-01-08", "18:41:32"],
        "id": 5,
        "priority_level": 1,
        "text": "huat",
        "text_type": 0
    }, {
        "category_id": 1,
        "date_posted": ["2021-01-08", "18:41:01"],
        "id": 4,
        "priority_level": 1,
        "text": "hack&roll is taking my life away",
        "text_type": 0
    }, {
        "category_id": 2,
        "date_posted": ["2021-01-08", "18:35:56"],
        "id": 3,
        "priority_level": 1,
        "text": "Lets sleep more yay",
        "text_type": 0
    }, {
        "category_id": 2,
        "date_posted": ["2021-01-08", "18:33:59"],
        "id": 2,
        "priority_level": 1,
        "text": "Lets sleep yay",
        "text_type": 0
    }, {
        "category_id": 1,
        "date_posted": ["2021-01-08", "18:27:38"],
        "id": 1,
        "priority_level": 0,
        "text": "TEST123123123",
        "text_type": 0
    }]
}
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #soup = BeautifulSoup(html, "lxml")
   # print("soup works")
    #memoList = parseTeleJson.teleToMemos('./result.json',100)
    print(parseApiInput.get_from_backend())
    #processed_data = parseApiInput.timeframing(data["memos"])
    #categories = parseApiInput.get_summary_and_categories(processed_data)
    #print(categories)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
