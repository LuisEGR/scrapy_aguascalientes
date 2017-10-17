# -*- coding: utf-8 -*-
import scrapy


class ListaacuerdosSpider(scrapy.Spider):
    name = 'ListaAcuerdos'
    allowed_domains = ['serviciosweb.poderjudicialags.gob.mx']
    start_urls = [
        'http://serviciosweb.poderjudicialags.gob.mx/Majat/Acuerdos/GetListaDeAcuerdos']

    def parse(self, response):
        pass
