# -*- coding: utf-8 -*-
import re
import os
from scrapy import Spider
from scrapy import Request
from scrapy import FormRequest
from Aguascalientes.items import AcuerdoPorFechaItem


class AgendaAudienciasSpider(Spider):
    name = 'AgendaAudiencias'
    allowed_domains = ['poderjudicialags.gob.mx']
    start_urls = [
        'http://web2.poderjudicialags.gob.mx:81/servicios/agenda/agenda.cfm']

    def parse(self, response):
        lista_civ_mer_fam = response.xpath(
            "//form[@id='FMenu']/p/select/option/@value").extract()
        lista_juzgados_penales = response.xpath(
            "//form[@id='FMenu2']/p/select/option/@value").extract()
        tablas = response.xpath('//*/table')
        lista_mixtos_rel = tablas[0].xpath(".//tr/td/p/a/@href").extract()        
        lista_nuevo_sist_pen_ac = tablas[1].xpath(
            ".//tr/td/p/a/@href").extract()  # pdf

        for id_juzgado_cmf in lista_civ_mer_fam:
            formdata = {
                "MenuJ": id_juzgado_cmf,
                "Submit": 'Aceptar'
            }
            url_abs = response.urljoin('consagenda.cfm')
            yield FormRequest(url_abs, formdata=formdata,
                              callback=self.parse_agenda_v2)


        for id_juzgado_penal in lista_juzgados_penales:
            formdata = {
                "MenuJ2": id_juzgado_penal,
                "Submit2": 'Aceptar'
            }
            url_abs = response.urljoin('consagendapen.cfm')
            yield FormRequest(url_abs, formdata=formdata,
                              callback=self.parse_agenda_v2)            

        for url_rel in lista_mixtos_rel:
            url_abs = response.urljoin(url_rel)
            yield Request(url_abs, callback=self.parse_agenda)

        for url_rel in lista_nuevo_sist_pen_ac:
            url_abs = response.urljoin(url_rel)            
            yield Request(url_abs, callback=self.guardar_pdf)


        
        
    def parse_agenda(self, response):
        print(response.url)
        tabla = response.xpath("//table")[0]
        rows = tabla.xpath('.//tr')
        if (len(rows) <= 1):
            return
        for row in rows[1:]:
            cols = row.xpath('.//td').xpath("string(.)").extract()
            # print(cols)
            if(len(cols) == 5):
                exp = dict()
                exp[cols[2]] = {
                    "Hora": cols[1],
                    "Tramite": cols[3],
                    "Audiencia": cols[4]
                }
                acuerdo = AcuerdoPorFechaItem()
                acuerdo['Url'] = response.url                
                acuerdo['Fecha'] = extract_fecha(cols[0])
                acuerdo['Contenido'] = exp
                yield acuerdo

    def parse_agenda_v2(self, response):
        print(response.url)        
        tabla = response.xpath("//table")[0]
        rows = tabla.xpath('.//tr')
        if (len(rows) <= 1):
            return
        for row in rows[1:]:
            # cols = row.xpath('.//td/font/text()').extract()
            cols = row.xpath('.//td').xpath("string(.)").extract()
            if(len(cols) == 5):
                try:
                    num_expediente = re.search(
                        '[0-9]{3,4}\/[0-9]{4}', cols[3]).group(0)
                    exp = dict()
                    exp[num_expediente] = {
                        "hora": cols[1],
                        "documento": cols[2],
                        "num_origen_tramite": cols[3],
                        "audiencia": cols[4]
                    }
                    acuerdo = AcuerdoPorFechaItem()
                    acuerdo['Url'] = response.url
                    acuerdo['Fecha'] = extract_fecha(cols[0])
                    acuerdo['Contenido'] = exp
                    yield acuerdo
                except:
                    print("Error regexp: " + cols[3])

        next_page_rel = response.xpath('//a[text()="siguiente"]/@href').extract_first()
        if next_page_rel != None:
            yield Request(response.urljoin(next_page_rel), callback=self.parse_agenda_v2)


    def guardar_pdf(self, response):
        print(response.url)
        dir_files = "./files/"
        if not os.path.exists(dir_files):
            os.makedirs(dir_files)
        path = dir_files + response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)


def extract_fecha(cadena):
    return re.search("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", cadena).group(0)
