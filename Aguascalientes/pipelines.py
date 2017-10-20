# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from Aguascalientes.items import AcuerdoPorFechaItem
from scrapy.settings import Settings

class AguascalientesPipeline(object):
    # def __init__(self):
    #     self.connection = psycopg2.connect(
    #     host='localhost', database='test_json', user='postgres', password='admin')
    #     self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        return item

    # def process_item(self, item, spider):
    #     # check item type to decide which table to insert
    #     if isinstance(item, AcuerdoItem):
    #         print("ES un acuerdo!...")
    #     try:
    #         self.cursor.execute(
    #             "INSERT INTO aguascalientes.per_fecha(id_url, fecha) VALUES(2,NOW())")
    #         # self.cursor.execute( "SELECT * FROM por_fecha.per_fecha")
    #         self.connection.commit()
    #         self.cursor.fetchall()  

    #     except Exception:
    #         print("Error!")
    #         print(Exception)
    #     return item
