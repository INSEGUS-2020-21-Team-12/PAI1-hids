# -*- coding: utf-8 -*-
import schedule
import time
from hidsegus.core.hids_system import buscarOCrearFicheroHashes, comprobarintegridad, registroDiario, registroMensual, listaficherossha256

def calculoHashesNuevosArchivos():
  global ruta, diccionarioHashes
  listaficherossha256(ruta, diccionarioHashes)

def comprobarYRegistrarIntegridadDiariamente():
  global ruta, diccionarioHashes
  numFicherosTotal, numFicherosCorrompidos = comprobarintegridad(ruta, diccionarioHashes)
  registroDiario(numFicherosTotal, numFicherosCorrompidos)

def comprobarYRegistrarIntegridadMensualmente():
  global ruta, diccionarioHashes
  numFicherosTotal, numFicherosCorrompidos = comprobarintegridad(ruta, diccionarioHashes)
  registroMensual(numFicherosTotal, numFicherosCorrompidos)

def program():
  print("Escriba la ruta de la carpeta sobre la cual quiere comprobar diariamente la integridad.")
  global ruta, diccionarioHashes
  ruta = input()
  print("Se va a comenzar a comprobar la integridad de los ficheros existentes en la ruta: "+ruta)
  diccionarioHashes = buscarOCrearFicheroHashes(ruta)
  print("Se han cargado los hashes de los ficheros existentes. Se comenzará con la comprobación continua de la integridad.")
  schedule.every(10).seconds.do(comprobarYRegistrarIntegridadDiariamente)
  schedule.every(10).seconds.do(calculoHashesNuevosArchivos)
  #schedule.every().day.at("18:00").do(comprobarYRegistrarIntegridadDiariamente)
  schedule.every(20).seconds.do(comprobarYRegistrarIntegridadMensualmente)
  #schedule.every().day.at("23:00").do(comprobarYRegistrarIntegridadMensualmente)

print("Welcome. The HIDS system has started")

def run():
  program()
  while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':
  program()
  while True:
    schedule.run_pending()
    time.sleep(1)