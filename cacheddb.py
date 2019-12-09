import sqlite3
import os
import logging

# 创建数据库
# 查询特定域名最新章节编号
# 下载成功后添加到数据库
# 清空数据库

class novel:
    def __init__(self,dbname,url):
        self.filename=os.path.realpath(dbname)
        self.url=url

    def _dbexists(self):
        return os.path.isfile(self.filename)

    def _con(self):
        return sqlite3.connect(self.filename)

    def createTable(self):
        conn=self._con()
        cursor=conn.cursor()
        try:
            cursor.execute('''
            create table if not exists temp(
                id integer primary key,
                uri varchar,
                fileindex integer,
                filename varchar
            )
            ''')
            conn.commit
        except Exception as identifier:
            print(identifier)
        conn.close

    def append(self,fileindex,filename):
        conn=self._con()
        cursor=conn.cursor()
        try:
            cursor.execute('''
            insert into temp (
                uri,
                fileindex,
                filename
            )
            values
            (
                '{uri}',
                {fileindex},
                '{filename}'
            )
            '''.format(uri=self.url,fileindex=fileindex,filename=filename))
            conn.commit()
            conn.close()
        except Exception as identifier:
            print(identifier)

    def gettmp(self):
        rows=[]
        conn=self._con()
        cursor=conn.cursor()
        try:
            cursor.execute('''
            select filename from temp where uri='{uri}' order by fileindex'''.format(uri=self.url))
            data=cursor.fetchall()
            conn.close()
        except Exception as identifier:
            print(identifier)
        for row in data:
            rows.append(row[0])
        return rows

    def getMax(self):
        conn=self._con()
        cursor=conn.cursor()
        try:
            cursor.execute('''
            select max(fileindex) from temp where uri='{uri}'
            '''.format(uri=self.url))
            rows=cursor.fetchall()
            return rows[0][0] if rows[0][0]!=None else 0
        except Exception as identifier:
            print(identifier)


    def deleteall(self):
        conn=self._con()
        cursor=conn.cursor()
        try:
            cursor.execute('''
            delete from temp where uri='{url}'
            '''.format(url=self.url))
            conn.commit
        except Exception as identifier:
            print(identifier)
        conn.close


# if __name__ == "__main__":
#     test=novel('./temp.db',"https://www.shukeba.com/109280/")
#     print(test.gettmp())