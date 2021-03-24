import hashlib as hl
from pathlib import Path
from sortedcontainers import SortedDict
from datetime import datetime
import os
import pickle
#Imports registro mensual
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color, HexColor, green, black
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader

#Cálculo del hash de un único fichero
def hashficherosha256(rutafichero):
  try:
    hash = hl.sha256()
    with open(rutafichero, "rb") as f: #rb: r - read, b - binary mode
      for bloque in iter(lambda: f.read(4096), b""): # Leemos el fichero en bloques de 4096 bytes
        hash.update(bloque)
    return hash.hexdigest()
  
  except Exception as e:
    print("Error: %s" % (e))
    return ""

#Cálculo del hash de todos los ficheros que se encuentran en el directorio especificado.
def listaficherossha256(dir, sortedDict):
  directorio = Path(dir)
  for fichero in directorio.iterdir():
    ubicacionfichero = dir + fichero.name
    if os.path.isdir(ubicacionfichero):
      listaficherossha256(ubicacionfichero+'/', sortedDict)
    else:
      if not sortedDict.__contains__(ubicacionfichero):
        sortedDict.update({ubicacionfichero: hashficherosha256(ubicacionfichero)})

#Serializa el objeto que contiene los hashes calculados.
def serializarDiccionarioHashes(archivo_pickle,diccionario):
  pickle_file = open(archivo_pickle, 'wb')
  pickle.dump(diccionario, pickle_file)

#Deserializa el objeto que contiene los hashes calculados de los ficheros, cuando se ejecuta el programa.
def deserializarDiccionarioHashes(archivo_pickle,diccionario):
  pickle_file = open(archivo_pickle, 'rb')
  diccionario = pickle.load(pickle_file)
  return diccionario

#Busca el fichero que guarda los hashes, para cargarlos de nuevo. En caso de existir, lo cargará el existente, y se comprobará si existe algún
#fichero nuevo. Si no existe quiere decir que es la primera vez que se ejecuta el programa, por lo que habrá que calcular los hashes de todos los ficheros.
def buscarOCrearFicheroHashes(rutaCarpeta):
  hids_hash_database = SortedDict()
  rutaPrograma = os.getcwd()
  rutaFicheroHashes = rutaPrograma+'/hashes.pickle'
  if os.path.exists(rutaFicheroHashes):
    hids_hash_database = deserializarDiccionarioHashes(rutaFicheroHashes, hids_hash_database)
    listaficherossha256(rutaCarpeta, hids_hash_database)
    serializarDiccionarioHashes(rutaFicheroHashes,hids_hash_database)
  else:
    listaficherossha256(rutaCarpeta, hids_hash_database)
    serializarDiccionarioHashes(rutaFicheroHashes, hids_hash_database)
  return hids_hash_database

#Comprueba la integridad de los ficheros
def comprobarintegridad(dir, sortedDict):
 numFicherosTotal = 0
 numFicherosCorrompidos = 0
 for key in sortedDict.keys():
  numFicherosTotal += 1
  if not os.path.exists(key):
    numFicherosCorrompidos +=1
    print("El fichero con ubicación "+ key+" ha sido eliminado")
  elif sortedDict.get(key) != hashficherosha256(key):
    numFicherosCorrompidos +=1
    print("El fichero con ubicación "+ key+" ha sido corrompido")
 return numFicherosTotal, numFicherosCorrompidos

#Guarda en un txt los registros de la integridad de los ficheros
def registroDiario(numFicherosTotal, numFicherosCorrompidos):
  rutaPrograma = os.getcwd()
  file = open(rutaPrograma+"/registroDiario.txt","a")
  now = datetime.now()
  porcentajeFicherosIntegros = ((numFicherosTotal - numFicherosCorrompidos)/(numFicherosTotal))*100
  file.write(str(now.day)+"/"+str(now.month)+"/"+str(now.year)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" "+str(porcentajeFicherosIntegros)+"% "+str(numFicherosCorrompidos)+" ficheros han sido corrompidos" + os.linesep)

#Genera un pdf con el registro mensual
def registroMensual(numFicherosTotal, numFicherosCorrompidos):  
  porcentajes = [(numFicherosTotal-numFicherosCorrompidos)/numFicherosTotal, numFicherosCorrompidos/numFicherosTotal]
  colores = ['#00C90C','#DC0000']
  plt.pie(porcentajes, colors = colores, startangle=90, explode = (0.1,0.1), radius = 1.2, autopct = '%1.2f%%')
  plt.savefig("IntegridadFicheros.jpg", bbox_inches='tight',)

  now = datetime.now()
  date_report=now.strftime('%m-%Y')
  #Creando el pdf
  w, h = A4
  c = canvas.Canvas("registroMensual"+date_report+".pdf", pagesize=A4)
  x=50
  y=h-50
  c.setStrokeColor(green)
  c.setLineWidth(10)
  c.line(x,y,w-50,y)
  c.setStrokeColor(HexColor(0x00C90C)) 
  c.line(x+50, h-450, x+60, h-450)
  c.setStrokeColor(black) 
  c.drawString(x+ 65, h-455, "Documentos integros")
  c.setStrokeColor(HexColor(0xDC0000)) 
  c.line(x+50, h-470, x+60, h-470)
  c.setStrokeColor(black) 
  c.drawString(x+ 65, h-475, "Documentos corrompidos")

  date_report=now.strftime('%m %Y')

  c.setStrokeColor(black)
  c.setFont('Helvetica-Bold', 27)
  c.drawString(170,h-335, "Security team - 12")
  c.drawString(100,h-365, "Informe HIDS del mes "+date_report)
  c.setFont('Helvetica', 14)
  c.drawString(40, h-395, "El presente documento es un informe sobre la integridad de los ficheros. En el")
  c.drawString(40, h-410, "encontramos el número de ficheros que han sido corrompidos y el número de ")
  c.drawString(40, h-425, "ficheros que siguen íntegros.")
  rutaPrograma = os.getcwd()
  reporte = ImageReader(rutaPrograma+'/IntegridadFicheros.jpg')
  logo= ImageReader("https://i.ibb.co/j8LNmyQ/Insegus-logo-fondo-3.png")
  c.drawImage(reporte, 175, h-730, width=220, height=220)
  c.drawImage(logo, 175, h-290)
  c.save()
