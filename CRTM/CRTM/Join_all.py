#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import unicodedata

stops=pd.read_csv('stops.txt')
#Este fichero contiene nuestro datos obtenidos con scrapy
salida=pd.read_csv('MetroCrawlInfo.txt')
estaciones = stops[stops.stop_id.str.startswith('est', na=False)]
#Es necesario adaptar los datos pertenecientes al fichero stop.txt para poder realizar un join con nuestros datos obtenidos con scrapy.
estaciones.stop_name=estaciones.stop_name.str.upper()
estaciones.stop_name=estaciones.stop_name.str.replace("AVDA.","AVENIDA")
estaciones.stop_name=estaciones.stop_name.str.replace("Á","A")
estaciones.stop_name=estaciones.stop_name.str.replace("É","E")
estaciones.stop_name=estaciones.stop_name.str.replace("Í","I")
estaciones.stop_name=estaciones.stop_name.str.replace("Ó","O")
estaciones.stop_name=estaciones.stop_name.str.replace("Ú","U")
estaciones.stop_name=estaciones.stop_name.replace(" - ","-")
estaciones.stop_name=estaciones.stop_name.str.replace("INTERCAMBIADOR DE ","")
estaciones.stop_name=estaciones.stop_name.str.replace("PUERTA DEL SOL","SOL")
estaciones.stop_name=estaciones.stop_name.str.replace("MENDEZ ALVARO ESTACION SUR","MENDEZ ALVARO")
estaciones.stop_name=estaciones.stop_name.str.replace("ATOCHA-RENFE","ATOCHA RENFE")
estaciones.stop_name=estaciones.stop_name.str.replace("AEROPUERTO T1 - T2 - T3","AEROPUERTO T1-T2-T3")
estaciones = estaciones.sort_values(['stop_name'])

salida.estacion = salida.estacion.str.replace("'","")
salida.estacion = salida.estacion.str.strip()
salida.estacion = salida.estacion.str.upper()
salida.estacion = salida.estacion.str.replace("Á","A")
salida.estacion = salida.estacion.str.replace("É","E")
salida.estacion = salida.estacion.str.replace("Í","I")
salida.estacion = salida.estacion.str.replace("Ó","O")
salida.estacion = salida.estacion.str.replace("Ú","U")
salida.estacion = salida.estacion.str.replace("RDA.","RONDA")
salida.estacion = salida.estacion.str.replace(" - ","-")
salida.estacion = salida.estacion.str.replace("[","")
salida.accesible = salida.accesible.str.replace("]","")
salida = salida.sort_values(['linea','parada'])
#Juntamos los dos archivos poniendo N/A en los valores vacios y creando una columna para indicar el tipo de transporte.
joined_metro=pd.merge(salida, estaciones, how='left', left_on=['estacion'], right_on=['stop_name'])
joined_metro=joined_metro.fillna(value='N/A')
joined_metro['tipoTransporte'] = 'metro'

#Seguimos con metro ligero
stopsML=pd.read_csv('stopsML.txt')
salidaML=pd.read_csv('MLCrawlInfo.txt')
paradas = stopsML[stopsML.stop_id.str.startswith('par', na=False)]

paradas.stop_name=paradas.stop_name.str.upper()
paradas = paradas.sort_values(['stop_name'])

salidaML.estacion = salidaML.estacion.str.replace("'","")
salidaML.estacion = salidaML.estacion.str.strip()
salidaML.estacion = salidaML.estacion.str.upper()
salidaML.estacion=salidaML.estacion.str.replace("Á","A")
salidaML.estacion=salidaML.estacion.str.replace("É","E")
salidaML.estacion=salidaML.estacion.str.replace("Í","I")
salidaML.estacion=salidaML.estacion.str.replace("Ó","O")
salidaML.estacion=salidaML.estacion.str.replace("Ú","U")
salidaML.estacion=salidaML.estacion.str.replace("(IDA)","")
salidaML.estacion=salidaML.estacion.str.replace("(VUELTA)","")
salidaML.estacion=salidaML.estacion.str.replace("(","")
salidaML.estacion=salidaML.estacion.str.replace(")","")
salidaML.estacion=salidaML.estacion.str.replace("AVEN","AVENIDA")
salidaML.estacion = salidaML.estacion.str.replace("[","")
salidaML.accesible = salidaML.accesible.str.replace("]","")
salidaML.estacion = salidaML.estacion.str.strip()
salidaML = salidaML.sort_values(['linea','parada'])

joined_metroLigero=pd.merge(salidaML, paradas, how='left', left_on=['estacion'], right_on=['stop_name'])
joined_metroLigero=joined_metroLigero.fillna(value='N/A')
joined_metroLigero['tipoTransporte'] = 'metroLigero'

joined_all = [joined_metro, joined_metroLigero]
joined_all = pd.concat(joined_all)
joined_all.to_csv('resultados/joinedAll.csv', sep=',', encoding='utf-8',index=False)
