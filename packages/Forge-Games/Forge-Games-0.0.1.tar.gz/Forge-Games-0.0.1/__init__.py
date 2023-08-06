#Wazam is open source for all
#imports
import time
import sys
import os

#Function for waiting a few seconds
def Time(int):
  time.sleep(int)
  
#Function That Makes A Typing Effect In The Console
def type(str, typeTime):
  for letter in str:
    sys.stdout.write(letter)
    sys.stdout.flush()
    time.sleep(typeTime/100)
  print()#Warning the type function is amazing but has a limit print is still better in many ways

#Function That Clears The Console Of All Messages
def clear():
  command = 'clear'
  if os.name in ('nt', 'dos'): #This Works For Windows Or Cls Feel Free To Add Any Other OS's
    command = 'cls'
  os.system(command)

#This was taken from the BetterPython Library
#Colors Shortend And Easier To Use To Change Color Of Python Console
class bpc: #All The Colors In The Python Langauge With No External Modules
  End = '\033[0m'
  WhiteHighlight = '\033[7m'
  Underline = '\033[4m'
  Black = '\033[30m'
  Red = '\033[31m'
  DarkGreen = '\033[32m'
  DarkYellow = '\033[33m'
  DarkBlue = '\033[34m'
  DarkPurple = '\033[35m'
  DarkCyan = '\033[36m'
  RedHighlight = '\033[41m'
  GreenHighlight = '\033[42m'
  YellowHighlight = '\033[43m'
  SkyBlueHighlight = '\033[44m'
  LightPurpleHighlight = '\033[45m'
  DarkCyanHighlight = '\033[46m'
  WhiteBox = '\033[47m'
  LightBlack = '\033[90m'
  Pink = '\033[91m'
  LightGreen = '\033[92m'
  LightYellow = '\033[93m'
  LightBlue = '\033[94m'
  GrayHighlight = '\033[100m'
  PinkHighlight = '\033[101m'
  LightGreenHighlight = '\033[102m'
  LightYellowHighlight = '\033[103m'
  LightBlueHighlight = '\033[104m'
  HotPinkHighlight = '\033[105m'

#Color Shower
def Colors():
  clear()
  print(bpc.LightBlue + "All Avalible Colors In Wazam: " + bpc.End)
  print("End")
  print(bpc.WhiteHighlight + "WhiteHighlight" + bpc.End)
  print(bpc.Underline + "Underline" + bpc.End)
  print(bpc.Black + "Black" + bpc.End)
  print(bpc.Red + "Red" + bpc.End)
  print(bpc.DarkGreen + "DarkGreen" + bpc.End)
  print(bpc.DarkYellow + "DarkYellow" + bpc.End)
  print(bpc.DarkBlue + "DarkBlue" + bpc.End)
  print(bpc.DarkPurple + "DarkPurple" + bpc.End)
  print(bpc.DarkCyan + "DarkCyan" + bpc.End)
  print(bpc.RedHighlight + "RedHighlight" + bpc.End)
  print(bpc.GreenHighlight + "GreenHighlight" + bpc.End)
  print(bpc.YellowHighlight + "YellowHighlight" + bpc.End)
  print(bpc.SkyBlueHighlight + "SkyBlueHighlight" + bpc.End)
  print(bpc.LightPurpleHighlight + "LightPurpleHighlight" + bpc.End)
  print(bpc.DarkCyanHighlight + "DarkCyanHighlight" + bpc.End)
  print(bpc.WhiteBox + "WhiteBox" + bpc.End + " White Box")
  print(bpc.LightBlack + "LightBlack" + bpc.End)
  print(bpc.Pink + "Pink" + bpc.End)
  print(bpc.LightGreen + "LightGreen" + bpc.End)
  print(bpc.LightYellow + "LightYellow" + bpc.End)
  print(bpc.LightBlue + "LightBlue" + bpc.End)
  print(bpc.GrayHighlight + "GrayHighlight" + bpc.End)
  print(bpc.PinkHighlight + "PinkHighlight" + bpc.End)
  print(bpc.LightGreenHighlight + "LightGreenHighlight" + bpc.End)
  print(bpc.LightYellowHighlight + "LightYellowHighlight" + bpc.End)
  print(bpc.LightBlueHighlight + "LightBlueHighlight" + bpc.End)
  print(bpc.HotPinkHighlight + "HotPinkHighlight" + bpc.End)

#Loading Bar Function
def LoadingBar(LoadingTextColor, LoadingText, symbolColor, symbol, barlength, ticktime):
  print(LoadingTextColor + LoadingText + bpc.End, end = "")
  for i in range(barlength):
    for symbol in symbol:
      print(symbolColor + symbol + bpc.End, end = "")
      sys.stdout.flush()
      Time(ticktime/100)
  print(' ')

#Title Screen Function
def TitleScreen(gamename, gamenameColor, LineDesign, LineColor, LineLength, optionOne, optionOneColor, optionTwo, optionTwoColor,optionThree, optionThreeColor, optionOneSymbol, optionOneSymbolColor, optionTwoSymbol, optionTwoSymbolColor, optionThreeSymbol, optionThreeSymbolColor):
  print(gamenameColor + gamename + bpc.End)
  for i in range(LineLength):
    for LineDesign in LineDesign:
      print(LineColor + LineDesign, end = "" + bpc.End)
  print(' ')
  print(optionOneSymbolColor + optionOneSymbol + bpc.End, optionOneColor + optionOne + bpc.End)
  print(optionTwoSymbolColor + optionTwoSymbol + bpc.End, optionTwoColor + optionTwo + bpc.End)
  print(optionTwoSymbolColor + optionThreeSymbol + bpc.End, optionThreeColor + optionThree + bpc.End)

#Boot Splash Function
def bootSplash(firstWordStyle, firstWordColor, firstWord, firstWordTime, secondWordStyle, secondWordColor, secondWord, secondWordTime, revealTime, gameNameStyle, gameNameColor, gameName, gameNameTime, subtitleStyle, subtitleColor, subtitle, subtitleTime):
  firstWordStyle(firstWordColor + firstWord + bpc.End, firstWordTime)
  secondWordStyle(secondWordColor + secondWord + bpc.End, secondWordTime)
  Time(revealTime)
  gameNameStyle(gameNameColor + gameName + bpc.End, gameNameTime)
  subtitleStyle(subtitleColor + subtitle + bpc.End, subtitleTime)

#Reboots Game Proably Use It When Error Occur
def Reboot(BeforeReboot, Reason, ReasonColor, ReasonType, ReasonTime):
  ReasonType(ReasonColor + Reason + bpc.End, ReasonTime)
  Time(BeforeReboot)
  clear()