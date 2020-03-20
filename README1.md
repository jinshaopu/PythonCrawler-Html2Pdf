# 2020.03.20
    添加[千千小说](https://www.xqqxs.com)爬取
        目录： 
        bsObj.find_all(class_="box_con")[1].find_all("dl")[0]
        内容：
        bsObj.find_all(class_="content")
# 2019.11.19
## 添加mode属性
    1. pdf  :输出到pdf
    2. epub :输出到epub
    3. mobi :输出到mobi
## 调整pdf输出配置
页面使用A6大小，方便kindle阅读