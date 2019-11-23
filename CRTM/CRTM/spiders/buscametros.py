# -*- coding: utf-8 -*-
import scrapy
import pandas as pd

#BuscametrosSpider obtiene los datos de las lineas de metro ordenando la posicion de las paradas para cada linea y sus correspondientes elementos de accesibilidad.
class BuscametrosSpider(scrapy.Spider):
    name = 'buscametros'
    allowed_domains = ['www.crtm.es']
    start_urls = ['https://www.crtm.es/tu-transporte-publico/metro/lineas.aspx']

    #parse extrae los datos de las lineas y gestione la llamada a la función parseLines para cada una de las lineas.
    def parse(self, response):

        lines = []
        paths = []

        self.log("Estaciones: %s" % response.xpath('//div[@class="listaBotones logosCuadrado dosCols"]').extract())
        lines_query = response.xpath('//div[@class="listaBotones logosCuadrado dosCols"]')
        lines.append(lines_query.xpath('.//span[@class="txt"]').extract())

        paths_query = response.xpath('//div[@class="listaBotones logosCuadrado dosCols"]')
        paths.append(paths_query.xpath('.//a/@href').extract())

        lineas = paths[0][1]

        i=1
        #Recorremos cada una de las lineas en paths que contiene la url de acceso a cada linea.
        for lineas in paths[0][0:]:
            link = 'https://www.crtm.es/' + lineas

            if link is not None:
                request = response.follow(link, callback=self.parseLines)
                #Enviamos la linea correspondiente a través de la petición.
                request.meta['item']=i
                yield request
                i += 1
    #Recorremos las paradas para cada linea guardando los datos que necesitamos y gestionamos las llamadas a parseAccessibility.
    def parseLines(self, response):

        line1 = []

        line1_query = response.xpath('//div/table//tr')
        i = 1
        for parada in line1_query[1:]:
            aux = (parada.xpath('td[1]//text()').extract())
            linkParada = 'https://www.crtm.es/' +  parada.xpath('td[1]//@href').extract()[0]
            aux.append(i)
            aux.append(response.meta['item'])
            line1.append(aux[-3:])
            infoParada = aux[-3:]
            i+=1

            if linkParada is not None:
                #Necesitamos usar dont_filter=True porque si no se eliminan las paradas duplicadas en diferentes lineas.
                requestAccessibility = response.follow(linkParada, callback=self.parseAccessibility, dont_filter=True)
                requestAccessibility.meta['item']=infoParada
                yield requestAccessibility                

    #Obtenemos todos los elementos de accesibilidad de cada parada y los guardamos junto al resto de datos.
    def parseAccessibility(self, response):

        dataParada = response.meta['item']

        paths_query = response.xpath('//div[@class="contPestanias activeForNoneSelected"]')
        services = paths_query.xpath('.//span[@class="tab1"]/img').extract()

        if '<img src="/media/335742/ascensor.jpg" alt="Estación con ascensor">' in services:
            dataParada.append(1)
        else:
           dataParada.append(0)
        if '<img src="/media/335743/escaleras.jpg" alt="Estación con escaleras mecánicas">' in services:
            dataParada.append(1)
        else:
            dataParada.append(0)
        if '<img src="/media/333100/accesib.jpg" alt="Logo de estación accesible">'in services:
            dataParada.append(1)
        else:
            dataParada.append(0)

        print(dataParada)

        

