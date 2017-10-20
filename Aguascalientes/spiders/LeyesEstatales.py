# -*- coding: utf-8 -*-
import os
from scrapy import Spider
from scrapy import Request

class LeyesEstatalesSpider(Spider):
    name = 'LeyesEstatales'
    allowed_domains = ['poderjudicialags.gob.mx']
    start_urls = ['http://poderjudicialags.gob.mx/Marco/LeyesEstatales/']

    def parse(self, response):
        urls_rel = response.xpath("//div[@class='department']")[0].xpath(".//a/@href").extract()
        for url_rel in urls_rel:     
            if(url_rel != None):
                url_abs = response.urljoin(url_rel)
                yield Request(url_abs, callback=self.guardar_pdf)
    
    def guardar_pdf(self, response):
        filename = response.url.split('/')[-1].replace("%20", "_")
        print("Descargando: " + filename)
        dir_files = "./files/leyes_estatales/"
        if not os.path.exists(dir_files):
            os.makedirs(dir_files)
        path = dir_files + filename
        with open(path, 'wb') as f:
            f.write(response.body)


