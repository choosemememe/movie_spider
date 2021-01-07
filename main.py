# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import requests

from douban import DoubanClient


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # get user pass from web service
    resp = requests.get("http://localhost:5000/getInfo")

    respObj = json.loads(resp.text)
    douban = DoubanClient(respObj["userName"], respObj["password"])
    comment = '哈哈，又看了一遍'
    douban.do_comment(comment)
    # title = "lining"
    # content = 'everything is possible'
    # douban.write_diary(title, content)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
