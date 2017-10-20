# Scrapy_aguascalientes
Proyecto de Scrapy - Poder Judicial de Aguascalientes


### Instalación de dependencias:
```python
pip install psycopg2  
pip install scrapy  
# pip install tabula-py
```

### Para usar este repositorio:
```
git clone https://github.com/LuisEGR/scrapy_aguascalientes.git
cd scrapy_aguascalientes
```

## TODO
- [x] Spider ListaAcuerdos
- [ ] Spider LeyesEstatales
- [x] Spider AgendaAudiencias
- [x] Spider Notificaciones
- [ ] Spider TocasElectorales
- [ ] Pipeline para guardar items en DB-PostgreSQL


--- 
## Scrapy Spiders:

### ListaAcuerdos
> Encargada de hacer web scraping de la página de acuerdos, la tabla de la página en sí está hecha con un JSON, así que se obtiene directamente el JSON y posteriormente se procesa

> URL:  [http://serviciosweb.poderjudicialags.gob.mx/Majat/Acuerdos/GetListaDeAcuerdos](http://serviciosweb.poderjudicialags.gob.mx/Majat/Acuerdos/GetListaDeAcuerdos)



#### Ejecución:
```
scrapy crawl ListaAcuerdos
```
#### Respuesta:
Un arreglo de elementos conformados de la siguiente forma:
```json
{
    "Url": "http://serviciosweb.poderjudicialags.gob.mx/Majat/Acuerdos/GetListaDeAcuerdos",
    "Fecha": "19-10-2017",
    "Contenido": {
        "0647/2016": {
            "AcuerdoID": 3026340,
            "Area": "JUZGADO QUINTO DE LO FAMILIAR",
            "Materia": "FAMILIAR",
            "Naturaleza": "SECRETO",
            "Partes": "",
            "Extracto": ""
        }
    }
},

```
---
### LeyesEstatales

#### Ejecución:
```
scrapy crawl LeyesEstatales
```
---
### AgendaDeAudencias

> URL:  [http://poderjudicialags.gob.mx/JuzgadoVirtual/AgendadeAudiencias](http://poderjudicialags.gob.mx/JuzgadoVirtual/AgendadeAudiencias)

#### Ejecución:
```
scrapy crawl AgendaAudiencias
```

#### Respuesta:
Un arreglo de elementos conformados de la siguiente forma:
```json
{
    "Url": "http://web2.poderjudicialags.gob.mx:81/servicios/agenda/consagenda.cfm",
    "Fecha": " 20/10/2017",
    "Contenido": {
        "0001/2016": {
            "hora": " 09:00:00",
            "documento": "EXPEDIENTE PRINCIPAL ",
            "num_origen_tramite": " 0001/2016    JUICIO UNICO // DIVORCIO INCAUSADO",
            "audiencia": "INFORMACION TESTIMONIAL "
        }
    }
}
```
**Así como el archivo pdf que se guarda en ``./files/``**

---
### Notificaciones

> Se hacer un recorrido para buscar todos los números de acuerdo del año 2017, comenzando desde **0000/2017** hasta **9999/2017** para Notificaciones Penales y Notificaciones Civiles

> URL:  [http://poderjudicialags.gob.mx/JuzgadoVirtual/Notificaciones](http://poderjudicialags.gob.mx/JuzgadoVirtual/Notificaciones)

#### Ejecución:
```
scrapy crawl Notificaciones
```

#### Respuesta:
Un arreglo de elementos conformados de la siguiente forma:
```json
{
    "Url": "http://web2.poderjudicialags.gob.mx:81/servicios/notificaciones/consnot.cfm",
    "Fecha": "09/08/2017",
    "Contenido": {
        "0001/2017": {
            "fecha_gen": "09/08/2017\r\n        ",
            "estatus_f_real": "REALIZADAS           / 11/08/2017\r\n        ",
            "persona_a_notificar": "RENÉ SÁNCHEZ RAMOS /\r\n          AUDIENCIA CONFESIONAL                   ",
            "domicilio": "AVENIDA DE LOS MAESTROS (ESQUINA CON CALLE NAVARRA) 2010  /\r\n          EL DORADO 2A SECCION",
            "f_aud_f_juz": "Ago 24 2017-14/08/2017"
        }
    }
}
```
---
### TocasElectorales
#### Ejecución:
```
scrapy crawl TocasElectorales
```
---


> **Nota**: Para extraer tablas de el arhcivo PDF aún no puedo hacerlo funcionar, encontré una librería **tabula-py**, pero da error con el archivo que se baja de la página de agenda de audiencias.

