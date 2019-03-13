# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class DangdangPipeline(object):
    def open_spider(self, spider):
        print("open_spdier")
        try:
            # 连接数据库
            self.con = pymysql.connect(host='localhost', port=3306, user='root', password='123456', charset='utf8')
            # 创建游标
            self.cursor = self.con.cursor(pymysql.cursors.DictCursor)
            try:
                self.cursor.execute("create database mydb")
                print("create database mydb")
            except Exception as e:
                print(e)
            self.con.select_db("mydb")
            try:
                # 如果数据库存在则删除重建
                self.cursor.execute("drop table books")
                print("drop table books")
            except Exception as e:
                print(e)
            try:
                sql = "create table books( \
                title varchar(512) primary key, \
                author varchar(256), \
                publisher varchar(256), \
                date varchar(32), \
                price varchar(16), \
                detail text)"
                # 建表
                self.cursor.execute(sql)
            except Exception as e:
                print(e)
                self.cursor.execute("delete from books")
            self.opened = True
            self.count = 0
        except Exception as e:
            print(e)
            self.opened = False

    def close_spider(self, spider):
        if self.opened:
            self.con.commit()
            self.con.close()
            self.opened = False
        print("close_spider")
        print("共爬取", self.count, "本书籍")

    def process_item(self, item, spider):
        # 写入数据到mysql
        try:
            print(item["title"])
            if self.opened:
                sql = "insert into books(\
                title,author,publisher,date,price,detail) \
                values('%s','%s','%s','%s','%s','%s')\
                " % (item["title"], item["author"],
                     item["publisher"], item["date"], item["price"], item["detail"])
                self.cursor.execute(sql)
                self.count += 1
        except Exception as e:
            print(e)

        return item
