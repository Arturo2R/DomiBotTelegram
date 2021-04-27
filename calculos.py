import requests
import os

PRECIO_BASE = 4000


BING_KEY = os.environ['BING_MAPS_KEY']


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
  print( f"Una distancia de {distancia}m")
  return distancia

def precio_total(distancia):
  
  distancia = int(round(distancia, 0) * 1000)
  precio = distancia + PRECIO_BASE
  return precio

def address_and_distance(from_address, to_address):
  from_address = geocode(from_address)
  to_address = geocode(to_address)
  distance = distancia(from_address, to_address)
  return distance