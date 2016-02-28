# -*- coding: cp1252 -*-
#Text based game

import time, random, os, logging, socket, threading, sys, thread, colorama
from colorama import AnsiToWin32, init, Fore
import xml.etree.ElementTree as ET
init(autoreset=True)

#map variable
cordx = 20
cordy = -8
cordz = 0
chat = ""
username = ""
statusUpdate = 0
newCharcter = 0
area = "5050"
strings = []

#Sub region vars
isSearching = 0
subArea = "0"
subCityGates = ["5050002300-8"]


#skills - should probably be transferred to XML when possible
skills = [['Acting',0],['Agriculture',0],['Architecture',0],['Archery',0],['Art',0],['Astronomy',0],['Carpentry',0],['Chemistry',0],['Cooking',0],['Economics',0],['Fighting',0],['Fishing',0],['Hunting',0],['Law',0],['Leadership',0], ['Medicine',0],['Magic',0],['Mining',0],['Music',0],['Philosophy',0],['Religion',0],['Sailing',0],['Smithing',0],['Surgery',0],['Writing',0],]

#misc
linesSoFar = 4
inv = []
possibleEvents = [0,1,2,3]
eventFire = 0
HP = {'Head':5,'Torso':5,'Left Arm':5,'Right Arm':5,'Right Leg':5,'Left Leg':5,}


#temp
isInTavern = 0

#Positioning text (I hate Ansi codes)
def pos( x, y ):
  return '\x1b[' + str(y)+ ';' + str(x) + 'H';

#Netcode - I never want to touch Ansi codes again in my life jesus christ why
init(autoreset=True)
def connect(messageOut):       #messageOut is what you send to the server. The server can scan it and broadcast anything you want it to in response. Should prob. send data as a list with Player ID as the first variable
  global host
  global chat
  global isInTavern
  global linesSoFar
  while True:
    try:
      chatOther = s.recv(1024)
      print "\033[s"
      if (chatOther):
          if (isInTavern == 1):
            chatOther = chatOther.replace("null","")
            if (linesSoFar < 20):
              linesSoFar = linesSoFar + 1
            else:
              linesSoFar = 5
              os.system("cls")
              print Fore.GREEN + "*--------------------------------------------*\n|Welcome to the tavern - type 'leave' to exit|\n*--------------------------------------------*",
            sys.stdout.write(pos( 1, linesSoFar ) + chatOther + pos( 1, 24) + "You:                           " + pos ( 5, 24))
    except:
      print "ERROR"

#Splash
print (Fore.GREEN + " __  .______      .___  ___.  __    __   _______  \n|  | |   _  \     |   \/   | |  |  |  | |       \ \n|  | |  |_)  |    |  \  /  | |  |  |  | |  .--.  |\n|  | |   _  <     |  |\/|  | |  |  |  | |  |  |  |\n|  | |  |_)  |    |  |  |  | |  `--'  | |  '--'  |\n|__| |______/     |__|  |__|  \______/  |_______/ \n\n")

  
# This section gets the language and loads it into the element tree lang that will hold all the strings used
while True:
  print "Please select a language\nEnglish: 1\nFrancais: 2\nEspanol: 3\nMagyar: 4"
  lang = raw_input("Your choice: ")
  if lang == "1":
    lang = ET.parse("lang/en.xml")
    break
  if lang == "2":
    lang = ET.parse("lang/fr.xml")
    break
  if lang == "3":
    lang = ET.parse("lang/sp.xml")
    break
  if lang == "4":
    lang = ET.parse("lang/hu.xml")
    break
  else:
    os.system("cls")
    print "That is not a valid input."
lang = lang.getroot()
for string in lang.findall("string"):
  strings.append(string.text)

username = raw_input("\nPlease enter your username: ")
host = raw_input("\nPlease enter the host IP: ")
os.system("cls")

#Load Charcter (still working on this)
def loadCharcter(username):
  global newCharcter
  global skills
  count = 0
  skills = [['Acting',0],['Agriculture',0],['Architecture',0],['Archery',0],['Art',0],['Astronomy',0],['Carpentry',0],['Chemistry',0],['Cooking',0],['Economics',0],['Fighting',0],['Fishing',0],['Hunting',0],['Law',0],['Leadership',0], ['Medicine',0],['Magic',0],['Mining',0],['Music',0],['Philosophy',0],['Religion',0],['Sailing',0],['Smithing',0],['Surgery',0],['Writing',0],]
  mapParsingVar = ET.parse("users/skills/" + username + ".xml")
  mapParsingVar = mapParsingVar.getroot()
  for string in mapParsingVar.findall("string"):
    while count < 24:
      count = count + 1
      skills[count] = (string.text)
      print skills[count]
    
##loadCharcter(username)

    
#Load the map
mainMapLines = []
mainFishingSpots = []

def loadArt(directory):
  global mainMapLines
  mainMapLines = []
  mapParsingVar = ET.parse(directory)
  mapParsingVar = mapParsingVar.getroot()
  for string in mapParsingVar.findall("string"):
    mainMapLines.append(string.text)

def loadFishingSpots(directory):
  global mainFishingSpots
  mainFishingSpots = []
  mapParsingVar = ET.parse(directory)
  mapParsingVar = mapParsingVar.getroot()
  for string in mapParsingVar.findall("string"):
    mainFishingSpots.append(string.text)

loadArt("map/cellData/cell5050.xml")

boundedTiles = []
#Load the map bounds
def loadBounds(directory):
  global boundedTiles
  boundedTiles = []
  mapParsingVar = ET.parse(directory)
  mapParsingVar = mapParsingVar.getroot()
  for string in mapParsingVar.findall("string"):
    boundedTiles.append(string.text)

loadBounds("map/regions/5050/blocked.xml")

print[str(strings[0])]

def rendLevel(page):
  global skills
  count = 0
  skillXp = []
  if page == 2:
    try:
      while count < 17:
        skillXp = []
        skillXp = skills[count + 17]
        level = (skillXp[1] + 1)** 0.33
        print (pos(48, (4 + count)))+ skillXp[0] + ":    " + "%.0f" % level
        count = count + 1
    except:
      return True
  else:
    while count < 17:
      try:
        skillXp = []
        skillXp = skills[count]
        level = (skillXp[1] + 1)** 0.33
        print (pos(48, (4 + count))) + skillXp[0] + ":  " + "%.0f" % level
        count = count + 1
      except:
        return True
  nullVar = raw_input(pos( 1, 24 ) + "Press enter to continue")
  os.system('cls')
  
  for iterationNumber in range (1,19):
    print pos( 2, 3 + iterationNumber),
    exec (mainMapLines[iterationNumber])
  if isSearching != 1:
    print (pos(cordx+4, -cordy +4) + "@")
  

def move( ):
  global statusUpdate
  global cordy
  global cordx
  global cordz
  global strings
  global chat
  global isInTavern
  global linesSoFar
  global mainMapLines
  global isSearching
  
  if (isInTavern == 1):
    os.system("cls")
    m = "null"
    print Fore.GREEN + "*--------------------------------------------*\n|Welcome to the tavern - type 'leave' to exit|\n*--------------------------------------------*",
    while (isInTavern == 1):
      print (pos( 1, 24 ) + "\rYou:                                                                  ")
      m = raw_input(pos( 1, 24 ) + "\rYou:",)
      if (m == "leave"):
        isInTavern = 0
        return True
        break
      else:
        chat = username + ": " + m
        s.send(chat)

        if (linesSoFar < 20):
          linesSoFar = linesSoFar + 1
        else:
          linesSoFar = 5
          os.system("cls")
          print Fore.GREEN +  "*--------------------------------------------*\n|Welcome to the tavern - type 'leave' to exit|\n*--------------------------------------------*",
        print (pos( 1, linesSoFar ) + chat + pos(10, 23 ) )

  else:
    print pos(1,1) + "*--------------------------------------------*--------------------------------*\n|          IB MUD - Version 0.001            |             Status             |\n*--------------------------------------------*--------------------------------*"
    for y in range (4, 23):
      print pos(1,y) + "|"
      print pos(46,y) + "|"
      print pos(79,y) + "|"
    m = (raw_input(pos(1,23) + "*--------------------------------------------*--------------------------------*\n" + " " + strings[1] + " "))
 
 
  if m == ("north" or "North" or "n" or "N"):
    if isSearching != 1:
      cordy = (cordy + 1)
      return True
  elif m == ("south"):
    if isSearching != 1:
      cordy = (cordy - 1)
      return True
  elif m == ("east"):
    if isSearching != 1:
      cordx = (cordx + 1)
      return True
  elif m == ("west"):
    if isSearching != 1:
      cordx = (cordx - 1)
      return True
  elif m == ("up" or "Up" or "u" or "U"):
    if isSearching != 1:
      cordz = (cordz + 1)
      return True
  elif m == ("down" or "Down" or "d" or "D"):
    if isSearching != 1:
      cordz = (cordz - 1)
      return True
  
  
  elif m == ("leave"):
    if (isSearching == 1):
      isSearching = 0
      return True
    else:
      print (pos(1,24) + " Already at highest map level")
      time.sleep(2)
      print (pos(1,24) + "                             ")
      return False
  
  
  elif m == ("search"):
    if (area + "00" + subArea in subCityGates):
      isSearching = 1
      loadArt("map/art/townGate.xml")
      return True
    else:
      isSearching = 1
      loadArt("map/art/grassLand.xml")
      return True 
  
  
  elif m == ("tavern" or "tavern"):
    if (subArea == "2300-8") and isSearching == (1):
      isInTavern = 1
    else:
      print (pos(1,24) + " No tavern is present")
      time.sleep(2)
      print (pos(1,24) + "                         ")
      return False
  
  
  elif m == ("skill check"):
    try:
      rendLevel(1)
    except KeyError:
      return False
      print "ERROR"
      
  elif m == ("skill check 2"):
    try:
      rendLevel(2)
    except KeyError:
      return False
      print "ERROR"
  
  elif m == ("wait"):
    return True
  
  
  elif m == ("cords"):
    statusUpdate = (pos(48, 4) + "X: " + str(cordx) + pos(48, 5) + "Y: " + str(cordy))
    return True


  else:
    print (pos(1,24) + " Invalid choice                        ")
    time.sleep(2)
    print (pos(1,24) + "                                               ")
    return False

#
def event(area):
  global possibleEvents
  global eventFire
  if area == "0":
    possibleEvents = (1,1,2,3)
  eventFire = random.choice(possibleEvents)

# Main game loop
s = socket.socket()         # Create a socket
port = 9009                # Reserve a port 
s.connect((host, port))

thread.start_new_thread( connect, (chat,) )


#Init Map
for iterationNumber in range (1,19):
  print pos( 2, 3 + iterationNumber),
  exec (mainMapLines[iterationNumber])

print (pos(cordx+4, -cordy +4) + "@")

while True:
  oldCordx = cordx
  oldCordy = cordy
  subArea = str(cordx) + "00" + str(cordy)
  if (statusUpdate != "null"):
    print statusUpdate
    statusUpdate = "null"
  while True:
    if move() == True:
      break

  if (isSearching == 0):
    loadArt("map/cellData/cell5050.xml")
    isSearching = 2

  #print the map

  os.system('cls')
  for iterationNumber in range (1,19):
    print pos( 2, 3 + iterationNumber),
    exec (mainMapLines[iterationNumber])

  subArea = str(cordx) + "00" + str(cordy)

  if subArea in boundedTiles:
    cordx = oldCordx
    cordy = oldCordy
    subArea = str(cordx) + "00" + str(cordy)
    
  elif (cordx > 38 or cordx < 1 or cordy > 0 or cordy < -17):
    cordx = oldCordx
    cordy = oldCordy
    subArea = str(cordx) + "00" + str(cordy)
    
  if isSearching != (1):
    print (pos(cordx+4, -cordy +4) + "@")

  



