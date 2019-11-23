#!/usr/bin/env python3
# coding: utf-8

import os
#Necesitamos crear un header en los archivos del crawler 
os.system("echo estacion,parada,linea,ascensor,escaleras,accesible > MLCrawlInfo.txt")
os.system("echo estacion,parada,linea,ascensor,escaleras,accesible > MetroCrawlInfo.txt")
#Ejecutamos el crawler para el metro y el metro ligero y redirigimos la salida a dos archivos .txt
os.system("scrapy crawl buscametrosLigeros >> MLCrawlInfo.txt")
os.system("scrapy crawl buscametros >> MetroCrawlInfo.txt")

if not os.path.isdir("resultados"):
    os.system("mkdir resultados")

os.system("python3 Join_all.py")

os.system("mv MLCrawlInfo.txt resultados")
os.system("mv MetroCrawlInfo.txt resultados")
