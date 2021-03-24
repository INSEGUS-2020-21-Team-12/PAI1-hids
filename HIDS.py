# -*- coding: utf-8 -*-
import schedule
import time
from Integridad import buscarOCrearFicheroHashes, comprobarintegridad, registroDiario, registroMensual, listaficherossha256
from Challenge import rsadata, hmorph_rsa_hash, pdp_request, pdp_response

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

def challenge(pathfile):
  private_key, private_euler_function, public_n_modulo = rsadata()
  file_hmorph_hash = hmorph_rsa_hash(pathfile, private_euler_function)
  pdp_request_b, pdp_request_n, pdp_request_result = pdp_request(pathfile, public_n_modulo, file_hmorph_hash)
  pdp_response_result = pdp_response(pathfile, pdp_request_b, pdp_request_n)
  if pdp_response_result == pdp_request_result:
    print("Reto pasado con éxito")
  else:
    print("Reto fallido")

def program():
  eleccion = input()
  if eleccion == "1":
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
  elif eleccion == "2":
    print("Escriba la ruta del fichero sobre el cual quiere enviar el challenge")
    ruta = input()
    print("Enviando el challenge al servidor")
    challenge(ruta)
    print("Puede realizar de nuevo otra acción.")
    program()
  else:
    print("Opción no válida. Escriba una opción válida.")
    program()

print("Bienvenido. Este programa comprueba la integridad de los ficheros que usted indique y además la posibilidad de enviar un challenge al servidor para ver si contiene el fichero especificado.")
print("Para empezar a utilizar el programa escriba 1 o 2.")
print(" 1 -- HIDS")
print(" 2 -- Challenge")
program()

while True:
    schedule.run_pending()
    time.sleep(1)