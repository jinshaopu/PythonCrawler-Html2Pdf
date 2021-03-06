# coding=utf-8
import logging
import os
import re
import time
from urllib.parse import urlparse  # py3
import pdfkit
import requests
import random
from bs4 import BeautifulSoup

import click

from LiaoPythonCrawler import Crawler
from LiaoPythonCrawler import html_template


# html_template = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
# </head>
# <body>
# {title}
# {content}
# </body>
# </html>
# """


class shukebaCrawler(Crawler):

    def parse_menu(self, response):
        bsObj = BeautifulSoup(response.content, "html.parser")
        # menu_tag = bsObj.find_all(start_="0")[1]
        menu_tag = bsObj.find_all(class_="list")[0].find_all("dl")[1]
        # print(menu_tag)
        for li in menu_tag.find_all("dd"):
            url = li.a.get("href")
            # url = li.get('href')
            # print(li.get('href'))
            # print('')
            if not url.startswith("http"):
                url = "".join([self.domain, url])  # 补全为全路径
                # print(url)
            yield url

    def parse_body(self, response):
        try:
            bsObj = BeautifulSoup(response.content, 'html.parser')
            body = bsObj.find(class_="content_left")

            # 加入标题, 居中显示
            title = bsObj.find('h1').get_text()
            center_tag = bsObj.new_tag("center")
            title_tag = bsObj.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            # body.insert(1, center_tag)
            html = str(body)
            # print(html)
            # body中的img标签的src相对路径的改成绝对路径
            # pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(2).startswith("http"):
                    rtn = "".join(
                        [m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = html_template.format(content=str(body),title=center_tag)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)

@click.command()
@click.option('--url', prompt='输入书刊目录页', help='显示所有章节名称那一面')
@click.option('--file', prompt='输入PDF文件的保存名称', help='不需要后缀.pdf，只需要提供名称即可')
def main(url, file):
    crawler = shukebaCrawler(file, url)
    # crawler.mode='pdf'
    # crawler.mode = 'epub'
    crawler.mode = 'mobi'
    crawler.run(0)


if __name__ == '__main__':
    main()
# https://www.shukeba.com/83790/
    # bsObj = BeautifulSoup("01.html", "html.parser")
    # menu_page = requests.get('https://www.shukeba.com/113044/')
    # bsObj = BeautifulSoup(menu_page.text, 'html.parser')
    # menu_tag = bsObj.find_all(class_="list")[0].find_all("dl")[1]
    # print(menu_tag)
    # for li in menu_tag.find_all("dd"):
    #     url = li.a.get("href")
    #     print(url)

    # menu_page = requests.get('https://www.shukeba.com/113044/93052.shtml')
    # bsObj = BeautifulSoup(menu_page.text, 'html.parser')
    # body = bsObj.find_all(class_="content_left")
    # print(body)
