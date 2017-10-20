# -*- coding: utf-8 -*-
import json
import re
import datetime
from scrapy import Spider
from scrapy import FormRequest
from Aguascalientes.items import AcuerdoPorFechaItem



URL_BASE = 'http://serviciosweb.poderjudicialags.gob.mx/Majat'
URL_INICIAL = URL_BASE + '/Acuerdos/ListaDeAcuerdos'
URL_API_MATERIAS = URL_BASE + '/Administrador/GetGrupoMateriasPorAreaID'
URL_API_ACUERDOS = URL_BASE + '/Acuerdos/GetListaDeAcuerdos'

class ListaAcuerdosSpider(Spider):
    name = 'ListaAcuerdos'
    allowed_domains = ['poderjudicialags.gob.mx']
    start_urls = [URL_INICIAL]

    def parse(self, response):
        areas = response.xpath('//*[@id="selArea"]/optgroup/option')
        for area in areas:            
            formdata = {
                "areaID": area.xpath('.//@value').extract_first(),
                "areaNombre": area.xpath('.//text()').extract_first()
            }         
            yield FormRequest(URL_API_MATERIAS, formdata=formdata, 
                              callback=self.parse_areas, meta={'formdata': formdata})
            
    
    def parse_areas(self, response):
        materias = json.loads(response.body)     
        fechas = obtener_lista_fechas_hasta_hoy("19-10-2017", "%d-%m-%Y")       
        for materia in materias:
            for fecha in fechas:
                formdata = {
                    "areaID": response.request.meta['formdata']['areaID'],
                    "areaNombre": response.request.meta['formdata']['areaNombre'],
                    "grupoAreaMateriaID": materia['Value'],
                    "materiaNombre": materia['Text'],
                    "fechaPublicacion": fecha,
                    "tipoListaID": '1'
                }
               
                yield FormRequest(URL_API_ACUERDOS, formdata=formdata, 
                                  callback=self.parse_materias, meta={'formdata': formdata})

        
    def parse_materias(self, response):
        resultdata = json.loads(response.body)
        if(resultdata['Success'] != False):
                for acuerdo in resultdata['Data']['Acuerdos']:        
                    acuerdo_por_fecha = AcuerdoPorFechaItem()
                    acuerdo_por_fecha['Url'] = response.url
                    acuerdo_por_fecha['Fecha'] = getFechaFromStrUnix(acuerdo['FechaPublicacion'], "%d-%m-%Y")
                    acuerdo_por_fecha['Contenido'] = {
                        acuerdo['Documento']: {
                            "AcuerdoID": acuerdo['AcuerdoID'],
                            "Area": response.request.meta['formdata']['areaNombre'],
                            "Materia": response.request.meta['formdata']['materiaNombre'],
                            "Naturaleza": acuerdo['Naturaleza'],
                            "Partes": acuerdo['Partes'],
                            "Extracto": acuerdo['Extracto']                            
                        }                        
                    }                          
                    yield acuerdo_por_fecha         
        

def getFechaFromStrUnix(cadena, formato):
    unix = re.search("[0-9]+", cadena).group(0)
    fecha = datetime.datetime.fromtimestamp(int(unix) / 1000).strftime(formato)
    return fecha


def obtener_lista_fechas_hasta_hoy(from_date, formato):
    """ Retorna una lista de cadenas con 
    las fechas desde 'from_date' hasta hoy, incrementando por 1 día
    y con el formato 'formato' """
    d_from = datetime.datetime.strptime(from_date, formato)
    d_end = datetime.datetime.today()
    step = datetime.timedelta(days=1)
    result = []
    while d_from < d_end:
        result.append(d_from.strftime(formato))
        d_from += step
    return result
