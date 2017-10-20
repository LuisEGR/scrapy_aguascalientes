# -*- coding: utf-8 -*-
import os
from scrapy import Spider
from scrapy import Request



class TocasElectoralesSpider(Spider):
    name = 'TocasElectorales'
    allowed_domains = ['poderjudicialags.gob.mx']
    start_urls = ['http://web2.poderjudicialags.gob.mx:81/salaae/tocas.cfm']

    def parse(self, response):
        urls_rel = response.xpath("//p/a[1]/@href").extract()
        for url_rel in urls_rel:
            if(url_rel != None):
                url_abs = response.urljoin(url_rel)                
                if(url_rel[-3:] == 'pdf'):
                    yield Request(url_abs, callback=self.guardar_pdf)
                else:
                    yield Request(url_abs)


    def guardar_pdf(self, response):
        filename = response.url.split('/')[-1].replace("%20", "_")
        print("Descargando: " + filename)
        dir_files = "./files/tocas_electorales/"
        if not os.path.exists(dir_files):
            os.makedirs(dir_files)
        path = dir_files + filename
        with open(path, 'wb') as f:
            f.write(response.body)
