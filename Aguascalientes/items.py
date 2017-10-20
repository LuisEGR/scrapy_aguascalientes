# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcuerdoPorFechaItem(scrapy.Item):
    Url = scrapy.Field()
    Fecha = scrapy.Field()
    Contenido = scrapy.Field()


class ExpedienteItem(scrapy.Item):
    Url = scrapy.Field()
    Expediente = scrapy.Field()


class AcuerdoPorExpedienteItem(scrapy.Item):
    Url = scrapy.Field()
    Fecha = scrapy.Field()
    contenido = scrapy.Field()  

class NotificacionItem(scrapy.Item):
    Url = scrapy.Field()
    Fecha = scrapy.Field()
    Contenido = scrapy.Field()

