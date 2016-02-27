# -*- coding: cp1252 -*-

import time, random, os
from colorama import AnsiToWin32, init, Fore, Back
init(autoreset=True)

cordx = 0
cordy = 0
cordz = 0
chat = ""
username = ""
validxPlus = True
validxMinus = True
validyPlus = True
validyMinus = True
validzPlus = True
validzMinus = True
area = 0
strings = []

def pos( x, y ):
  return '\x1b[' + str(y)+ ';' + str(x) + 'H';



def move( ):
  global cordy
  global cordx
  global cordz
  global validxPlus
  global validxMinus
  global validyPlus
  global validyMinus
  global validzPlus
  global validzMinus
  global strings
  global chat
  global isInTavern
  global linesSoFar
  
  m = (raw_input)(pos(24, 24) + "            " + (pos(24, 24)))
  if m == ("north" or "North" or "n" or "N"):
    if validxPlus == True:
      cordy = (cordy + 1)
      return True
  elif m == ("south"):
    if validyMinus == True:
      cordy = (cordy - 1)
      return True
  elif m == ("east"):
    if validxPlus == True:
      cordx = (cordx + 1)
      return True
  elif m == ("west"):
    if validxMinus == True:
      cordx = (cordx - 1)
      return True
  elif m == ("up" or "Up" or "u" or "U"):
    if validzPlus == True:
      cordz = (cordz + 1)
      return True
  elif m == ("down" or "Down" or "d" or "D"):
    if validzMinus == True:
      cordz = (cordz - 1)
      return True
  elif m == ("null"):
    return True
  else:
    return False

while True:
  move()
  os.system("cls")
  print "" + Fore.CYAN + "......................................."
  print "" + Fore.CYAN + "......................................."
  print "" + Fore.CYAN + "......................................."
  print "" + Fore.CYAN + "......................................."
  print "" + Fore.CYAN + "......................................."
  print "" + Fore.CYAN + "......................................."
  print "" + Fore.CYAN + "......................................."
  print "" + Fore.CYAN + ".........................." + Fore.GREEN + "######" + Fore.CYAN + "......."
  print "" + Fore.CYAN + "........................." + Fore.GREEN + "########" + Fore.CYAN + "......"
  print "" + Fore.CYAN + "........................." + Fore.GREEN + "########" + Fore.CYAN + "......"
  print "" + Fore.CYAN + ".........................." + Fore.GREEN + "######" + Fore.CYAN + "......."
  print "" + Fore.CYAN + "............................" + Fore.YELLOW + "||" + Fore.CYAN + "........."
  print "" + Fore.CYAN + "............................" + Fore.YELLOW + "||" + Fore.CYAN + "........."
  print "" + Fore.CYAN + "............................" + Fore.YELLOW + "||" + Fore.CYAN + "........."
  print "" + Fore.GREEN + "............................" + Fore.YELLOW + "||" + Fore.GREEN + "........."
  print "" + Fore.GREEN + "..........................." + Fore.YELLOW + "/..\\" + Fore.GREEN + "........"
  print "" + Fore.GREEN + "......................................."
  print "" + Fore.GREEN + "......................................."

 


