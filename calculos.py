import requests
import os
import re

PRECIO_BASE = 4000


BING_KEY = "AvtDIsnMQA01APySmjx8T7k8O0JMl84kTaYUvl5Km31HYeDxeERQI5ObBTk6S63n"

ADDRESS_REGEX = '(cra|carrera|calle|cl|via)[.]?[\s]?([\d]{1,3}[\w]?)[\s]?([#]?[\s]?\d{1,3}([-]|\s)\d{1,3})'
PHONE_REGEX = '^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

def regeValidation(value, rege_type):
  rege_to_validate = ADDRESS_REGEX if rege_type == 'address' else PHONE_REGEX
  matches = re.search(rege_to_validate, value, re.IGNORECASE)
  if matches:
    return True
  else:
    return False  

def phoneValidation(phone_number):
  matches = re.search(PHONE_REGEX, phone_number)
  if matches:
    return True
  else:
    return False

def geocode(dir1):
  
  address = dir1.replace("#", " ")
  response= requests.get(f'http://dev.virtualearth.net/REST/v1/Locations?adminDistrict=CO-ATL&locality=Barranquilla&addressLine={address}&key={BING_KEY}&countryRegion=CO')
  res = response.json()
  
  coordinates = res['resourceSets'][0]['resources'][0]['point']['coordinates']
  lat = coordinates[0]
  lon = coordinates[1]
  coor = f"{lat},{lon}"
  print(coor)
  return coor

def distancia(coordenadas1, coordenadas2):
  res = requests.get(f"https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={coordenadas1}&destinations={coordenadas2}&travelMode=driving&key={BING_KEY}").json()
  #print(res)
  distancia = res["resourceSets"][0]["resources"][0]["results"][0]["travelDistance"]
  print(f"Una distancia de {distancia}m")
  return distancia

def precio_total(distancia):
  if distancia < 1:
    precio = (distancia * 1000) + PRECIO_BASE
  else :
    precio = (int(round(distancia, 0) * 1000)) + PRECIO_BASE
  return precio

def address_and_distance(from_address, to_address):
  from_address = geocode(from_address)
  to_address = geocode(to_address)
  distance = distancia(from_address, to_address)
  return distance

