# -*- coding: utf-8 -*-
import re
import os
from scrapy import Spider
from scrapy import Request
from scrapy import FormRequest
from Aguascalientes.items import NotificacionItem

class NotificacionesSpider(Spider):
    name = 'Notificaciones'
    allowed_domains = ['poderjudicialags.gob.mx']
    start_urls = ['http://poderjudicialags.gob.mx/JuzgadoVirtual/Notificaciones/']
    year = "2017"
    limite_invalidos = 10
    total_invalidos = 0

    def parse(self, response):
        urls = response.xpath("//div[@class='department']//a/@href").extract()
        url_notificaciones_cmf = response.urljoin(urls[0])
        url_notificaciones_penales = response.urljoin(urls[1])
        yield Request(url_notificaciones_cmf, callback=self.parse_noti_cmf)
        print(url_notificaciones_penales)
        yield Request(url_notificaciones_penales, callback=self.parse_noti_pen)

    def parse_noti_cmf(self, response):
        url = response.xpath("//embed/@src").extract_first();
        if(url != None):
            yield Request(url, callback=self.parse_noti_cmf)

        url_form_rel = response.xpath("//form/@action").extract_first()
        url_form_abs = response.urljoin(url_form_rel)

        lista_juzgados = response.xpath(
            "//form//select[@name='MenuJ']/option/@value").extract()

        lista_tipos_doc = response.xpath(
            "//form//select[@name='MenuD']/option/@value").extract()

        
        i = 0
        while(i < 9999):
        # while(i < 9999 and self.total_invalidos < self.limite_invalidos):
            i += 1
            expediente = f'{i:04}' + "/" + self.year
            # print(expediente)
            for juzgado in lista_juzgados:
                for tipo_doc in lista_tipos_doc:    
                    formdata = {
                        "Documento": expediente,
                        "MenuJ": juzgado,
                        "MenuD": tipo_doc
                    }
                    yield FormRequest(url_form_abs, formdata=formdata, 
                                      callback=self.parse_notificaciones, meta={'formdata': formdata})


    def parse_noti_pen(self, response):        
        print(response.url)
        url = response.xpath("//embed/@src").extract_first()
        if(url != None):
            yield Request(url, callback=self.parse_noti_pen)
        url_form_rel = response.xpath("//form/@action").extract_first()
        url_form_abs = response.urljoin(url_form_rel)
        lista_juzgados = response.xpath(
            "//form//select[@name='MenuJ']/option/@value").extract()

        i = 0
        while(i < 9999):
            i += 1
            expediente = f'{i:04}' + "/" + self.year
            for juzgado in lista_juzgados:
                formdata = {
                    "Documento": expediente,
                    "MenuJ": juzgado,
                    "Enviar2": "Aceptar"
                }
                yield FormRequest(url_form_abs, formdata=formdata,
                                   callback=self.parse_notificaicones_penales, meta={'formdata': formdata})

        

    def parse_notificaciones(self, response):        
        tabla = response.xpath("//table")[0]
        rows = tabla.xpath('.//tr')
        acuerdo = response.request.meta['formdata']["Documento"]
        if (len(rows) <= 1):
            print(response.request.meta['formdata']["MenuJ"] + ":" +acuerdo + ": NO DATA")
            return
        #     self.total_invalidos += 1
        print(acuerdo + ": Notificación encontrada! -> " +
              response.request.meta['formdata']["MenuJ"] + " ... " +
              response.request.meta['formdata']["MenuD"])
        for row in rows[1:]:
            cols = row.xpath('.//td').xpath("string(.)").extract()
            # cols = row.xpath('.//td/font/text()').extract()
            contenido = {
                acuerdo: {
                    "fecha_gen": cols[0],
                    "estatus_f_real": cols[1],
                    "persona_a_notificar": cols[2],
                    "domicilio": cols[3],
                    "f_aud_f_juz":  cols[4]
                }
            }
            notificacion_item = NotificacionItem()
            notificacion_item['Url'] = response.url
            notificacion_item['Fecha'] = extract_fecha(cols[0])
            notificacion_item['Contenido'] = contenido
            yield notificacion_item

        next_page_rel = response.xpath('//a[text()="siguiente"]/@href').extract_first()
        if next_page_rel != None:
            yield Request(response.urljoin(next_page_rel), callback=self.parse_notificaciones)



    def parse_notificaicones_penales(self, response):
        tabla = response.xpath("//table")[0]
        rows = tabla.xpath('.//tr')
        acuerdo = response.request.meta['formdata']["Documento"]

        if (len(rows) <= 1):
            print(response.request.meta['formdata']
                  ["MenuJ"] + ":" + acuerdo + ": NO DATA")
            return

        print(response.request.meta['formdata']["MenuJ"] + ":" + 
            acuerdo + ": Notificación encontrada!")
        for row in rows[1:]:
            cols = row.xpath('.//td').xpath("string(.)").extract()
            contenido = {
                acuerdo: {
                    "fecha_gen": cols[0],
                    "fecha_baja":cols[1],
                    "fecha_auto": cols[2]
                }
            }
            notificacion_item = NotificacionItem()
            notificacion_item['Url'] = response.url
            notificacion_item['Fecha'] = extract_fecha(cols[0])
            notificacion_item['Contenido'] = contenido
            yield notificacion_item





def extract_fecha(cadena):
    if(cadena == None): return cadena
    return re.search("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", cadena).group(0)
