"""
File name: iss_tracker.py
Author: Neocky
Version: 1.0
Url: https://github.com/Neocky/ISS_Tracker
"""

import requests
from datetime import datetime, timezone, timedelta

# nice pixel art of the world
mapList = [
"               ,_   .  ._. _.  .                                     ",
"           , _-\\','|~\~      ~/      ;-'_   _-'     ,;_;_,    ~~-   ",
"  /~~-\_/-'~'--' \~~| ',    ,'      /  / ~|-_\_/~/~      ~~--~~~~'--_",
"  /              ,/'-/~ '\ ,' _  , '|,'|~                   ._/-, /~ ",
"  ~/-'~\_,       '-,| '|. '   ~  ,\ /'~                /    /_  /~   ",
".-~      '|        '',\~|\       _\~     ,_  ,               /|      ",
"          '\        /'~          |_/~\\\\,-,~  \ \"         ,_./ |   ",
"           |       /            ._-~'\_ _~|              \ ) /       ",
"            \   __-\           '/      ~ |\  \_          /  ~        ",
"  .,         '\ |,  ~-_      - |          \\\\_' ~|  /\  \~ ,        ",
"               ~-_'  _;       '\           '-,   \,' /\/  |          ",
"                 '\_,~'\_       \_ _,       /'    '  |, /|'          ",
"                   /     \_       ~ |      /         \  ~'; -,_.     ",
"                   |       ~\        |    |  ,        '-_, ,; ~ ~\\\\",
"                    \,      /        \    / /|            ,-, ,   -, ",
"                     |    ,/          |  |' |/          ,-   ~ \   '.",
"                    ,|   ,/           \ ,/              \       |    ",
"                    /    |             ~                 -~~-, /   _ ",
"                    |  ,-'                                    ~    / ",
"                    / ,'                                      ~      ",
"                    ',|  ~                                           ",
"                      ~'                                             ",
]


def apiRequest() -> object:
  """
  Make an api request to get position of ISS
  """

  url = "http://api.open-notify.org/iss-now.json"
  response = requests.get(url)
  details = response.json()
  return details


def validateApiRequest(api_returned_message) -> None:
  """
  Validates the API request and looks for an success message.

  If the message is not present the programm will print an error and exit.
  """

  if api_returned_message != "success":
    print("ERROR: API message was not success")
    exit(1)
  return None


def convertToDatetime(unixTime) -> datetime:
  """
  Converts the timestamp from the unix format to a datetime.
  """

  return datetime.fromtimestamp(unixTime, tz=timezone(timedelta(hours=1)))


def calculateLongitude(iss_position_longitude) -> int:
  """
  Calculates the X position on the map for the ISS marker.
  
  Default map size on X-Axis: 70
  Meridian = 35
  """

  mapSizeXAxis = 70
  longitudeMapPosition = float(iss_position_longitude) / (360 / mapSizeXAxis)
  longitudeMapPosition = round(longitudeMapPosition)
  longitudeMapPosition = longitudeMapPosition + (mapSizeXAxis/2)
  if longitudeMapPosition > mapSizeXAxis:
    longitudeMapPosition = longitudeMapPosition - mapSizeXAxis
  return longitudeMapPosition


def calculatelatitude(iss_position_latitude) -> int:
  """
  Calculates the Y position on the map for the ISS marker
  
  Default map size on Y-Axis: 22
  Equator = 11
  """

  mapSizeYAxis = 22
  latitudeMapPosition = float(iss_position_latitude) / (90 / (mapSizeYAxis / 2))
  latitudeMapPosition = round(latitudeMapPosition)
  latitudeMapPosition = latitudeMapPosition + 11
  if latitudeMapPosition == 0:
      latitudeMapPosition = 1
  return latitudeMapPosition


def printWorldMap(mapList, mapMarkerX, mapMarkerY) -> None:
  """
  Prints the world map and sets the marker for the ISS
  """

  symbolISS = "[93m" + "#" + "[0m" # symbol for iss in cyan
  i = 22
  for mapLine in mapList:
    if i == mapMarkerY:
      mapLineInFront = mapLine[:int(mapMarkerX)]
      mapLineAfter = mapLine[int(mapMarkerX)+1:] # replace symbol
      mapLineWithISS = mapLineInFront + symbolISS + mapLineAfter
      print(mapLineWithISS)
      i -= 1
      continue

    print(mapLine)
    i -= 1


def main() -> None:
  """
  Main function
  """
  details = apiRequest()
  validateApiRequest(details['message'])

  timestampDatetime = convertToDatetime(details['timestamp'])
  mapMarkerX = calculateLongitude(details['iss_position']['longitude'])
  mapMarkerY = calculatelatitude(details['iss_position']['latitude'])

  print("ISS TRACKER - https://github.com/Neocky/ISS_Tracker")
  print(f"Longitude: {details['iss_position']['longitude']}")
  print(f"Latitude: {details['iss_position']['latitude']}")
  print(timestampDatetime)
  print()

  printWorldMap(mapList, mapMarkerX, mapMarkerY)


if __name__ == "__main__":
  main()
