import os, time
from replit import db
from levels import levels, visuals, levelObjs, playerStartPos, levelWidth, txt

objects = []
userProfile = None
levelMap = None
level = "0"
map = None
player = None
game = None
header = "Surround the green box with white boxes to win!"

userStore = db["userStore"]
userData = db["userData"]

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

# OBJECT CLASS
class Object():
  def __init__(self, objVal):
    self.objVal = objVal
    objValues = self.objVal.split("_")
    self.visualCode = objValues[0]
    self.objType = int(objValues[1])
    self.index = int(objValues[2])

  def displayObj(self):
    global levelMap
    levelMap[self.index] = self.visualCode

  def moveObj(self, moveBy, objIdx):
    global levelMap
    if self.objType == 0 and moveBy != "n":
      if self.index != objIdx:
        return
      self.index += moveBy
      if levelMap[self.index] in ["0\n", "0", "4", "5"]:
        self.index -= moveBy
        return "hit"
      if levelMap[self.index] == "7":
        for obj in objects:
           if obj.objType == 3:
            if obj.index != self.index:
              if levelMap[obj.index+1] == "1":
                self.index = obj.index+1
              elif levelMap[obj.index+levelWidth[level]] == "1":
                self.index = obj.index+levelWidth[level]
              elif levelMap[obj.index-levelWidth[level]] == "1":
                self.index = obj.index-levelWidth[level]
              elif levelMap[obj.index-1] == "1":
                self.index = obj.index-1
              else:
                self.index -= moveBy
              break
    if self.objType == 1:
      if levelMap[self.index+1] == "5" and levelMap[self.index-1] == "5" and levelMap[self.index+levelWidth[level]] == "5" and levelMap[self.index-levelWidth[level]] == "5":
        return "win"
    elif self.objType == 2:
      if self.index == player.index:
        return "die"

class Player():
  def __init__(self, index, visualCode):
    self.index = int(index)
    self.visualCode = visualCode

  def displayPlayer(self):
    global levelMap
    levelMap[self.index] = self.visualCode

  def movePlayer(self, ctrl):
    global levelMap
    if ctrl == "w":
      move = int(levelWidth[level])*-1
    elif ctrl == "s":
      move = int(levelWidth[level])
    elif ctrl == "d":
      move = 1
    elif ctrl == "a":
      move = -1
    self.index += move
    if levelMap[self.index] in ["0\n", "0", "4"]:
      self.index -= move
    elif levelMap[self.index] in ["5"]:
      for obj in objects:
        check = obj.moveObj(move, self.index)
        if check == "hit":
          self.index -= move
    elif levelMap[self.index] == "7":
      for obj in objects:
        if obj.objType == 3:
          if obj.index != self.index:
            if levelMap[obj.index+1] == "1":
              self.index = obj.index+1
            elif levelMap[obj.index+levelWidth[level]] == "1":
              self.index = obj.index+levelWidth[level]
            elif levelMap[obj.index-levelWidth[level]] == "1":
              self.index = obj.index-levelWidth[level]
            elif levelMap[obj.index-1] == "1":
              self.index = obj.index-1
            else:
              self.index -= move
            break
        
# PROFILE CLASS
class Profile():
  def __init__(self, username, password, dataIdx):
    self.username = username
    self.password = password
    self.dataIdx = dataIdx
    # SETTINGS
    self.settings = ["false"]

# STARTUP FUNCTION
def startUp():
  global userProfile
  clearConsole()
  accOpt = input("Would you like to login, or create an account?\n[login/create]\n> ").lower()
  if accOpt == "login":
    login()
  elif accOpt == "create":
    createAccount()
  elif accOpt == "s":
    initiateGame()
    return
  else:
    print("That isn't an option!")
    time.sleep(2)
    startUp()
  clearConsole()
  if userProfile.username == "admin":
    print("Welcome, admin!")
    time.sleep(2)
    adminFunc()
    return
  else:
    saveData()
    print(f"Logged in as {userProfile.username}")
    userFunc()

# LOGIN FUNCTION
def login():
  global userProfile
  time.sleep(1)
  clearConsole()
  username = input("What is your username? > ")
  password = input("What is your password? > ")
  loginSuccess = False
  for i in range(0, len(userStore)):
    split = userStore[i].split("|")
    if username.lower() == split[0].lower() and password == split[1]:
      loginSuccess = True
      userIdx = i
      break
  if loginSuccess == False:
    print("Username or password incorrect!")
    time.sleep(1)
    login()
  else:
    userProfile = Profile(username, password, userIdx)

# CREATE ACCOUNT FUNCTION
def createAccount():
  global userProfile
  time.sleep(1)
  clearConsole()
  username = input("What would you like your username to be? > ")
  taken = False
  for i in range(0, len(userStore)):
    split = userStore[i].split("|")
    if username.lower() == split[0].lower():
      taken = True
      break
  if taken == True:
    time.sleep(0.7)
    clearConsole()
    print("That username is taken!")
    time.sleep(0.5)
    createAccount()
  elif "|" in username:
    print("That character isn't allowed!")
    time.sleep(2)
    createAccount()
  else:
    time.sleep(1)
    password = input("What would you like your password to be? (case sensitive) > ")
    if "|" in password:
      print("That character isn't allowed!")
      time.sleep(2)
      createAccount()
    else:
      time.sleep(0.7)
      clearConsole()
      print(f"Here are your login credentials. Remember them!\nUsername: {username}\nPassword: {password}")
      time.sleep(2)
      input("Press enter to continue. > ")
      userDataStr = f"{username}|{password}"
      userStore.append(userDataStr)
      userData.append("n")
      userProfile = Profile(username, password, len(userStore)-1) # -1 TO ACCOUNT FOR ARRAY INDEX STARTING AT 0

# ADMIN PROTOCALLS
def adminFunc():
  global userProfile
  clearConsole()
  print("Admin commands:\nclear - clears all user data\nexit - sends you back to the home screen\ndata - shows database\neval <value> - evals and returns evaluation")
  actualCmd = input("> ")
  cmd = actualCmd.lower()
  if cmd == "clear":
    adminPass = os.environ["adminPass"]
    db["userStore"] = [f"admin|{adminPass}"]
    db["userData"] = ["n"]
    adminPass = None
    print("User data has been reset.")
  elif cmd == "data":
    for dat in db["userStore"]:
      print(dat)
  elif cmd == "exit":
    userProfile = None
    startUp()
    return
  elif cmd[0:4] == "eval":
    try:
      evaluation = eval(actualCmd[5:])
      print(evaluation)
    except:
      print("Error occured during eval")
  else:
    print("Invalid command.")
    time.sleep(2)
    adminFunc()
    return
  input("Press enter to continue. > ")
  adminFunc()

# USER PROTOCALLS
def userFunc():
  global userProfile
  saveData()
  time.sleep(0.7)
  input("Press enter to continue. > ")
  clearConsole()
  print("Commands:\nplay - enter game\nlogout - logs you out\nsettings - opens settings menu")
  cmd = input("> ").lower()
  if cmd == "play":
    initiateGame()
  elif cmd == "logout":
    userProfile = None
    startUp()
  elif cmd == "settings":
    settings()
    userFunc()
  else:
    print("Invalid command.")
    time.sleep(2)
    userFunc()
    return

# SETTINGS
def settings():
  global userProfile
  clearConsole()
  print("Settings [settingName <option>]\n\back - goes back\nSETTINGS COMING SOON")
  cmd = input("> ").lower()
  time.sleep(1)
  if cmd == "back":
    clearConsole()
    return
  
# SAVE DATA | UPDATE DATABASE
def saveData():
  saveStr = f"{userProfile.username}|{userProfile.password}"
  dataSaveStr = userData[userProfile.dataIdx]
  db["userStore"][userProfile.dataIdx] = saveStr
  db["userData"][userProfile.dataIdx] = dataSaveStr

def decode(val, template):
  str = "\n"
  for i in range(0, len(val)):
    if len(val[i]) > 1:
      integer = int(val[i][0])
      str = str + template[integer] + val[i][1:]
    else:
      integer = int(val[i])
      str = str + template[integer]
  return str

def addEntities(list):
  for i in list:
    objects.append(Object(i))

def initiateGame():
  global level, player, playerStartPos, game, objects
  clearConsole()
  #level = str(int(level)+1)
  level = input("> ")
  objects = []
  game = True
  addEntities(levelObjs[level])
  player = Player(playerStartPos[level], "3")
  while game == True:
    check = gameLoop()
    if check in ["restart", "die"]:
      time.sleep(0.5)
      objects = []
      addEntities(levelObjs[level])
      player = Player(playerStartPos[level], "3")
    elif check == "win":
      game = False
  initiateGame()

def profilePage():
  pass

def pause():
  clearConsole()
  print("PAUSE\nresume - resumes game\nsettings - opens settings menu\nprofile - opens profile menu\ncredits - game credits")
  cmd = input("\n> ").lower()
  if cmd == "resume":
    return
  elif cmd == "settings":
    settings()
  elif cmd == "profile":
    profilePage()
    pause()
  elif cmd == "credits":
    clearConsole()
    print("Game credits:\nAll code by JadenCodes\nMy discord: xJaden#1338\n")
    input("Press enter to go back\n> ")
    pause()

def gameLoop():
  global userProfile, levelObjs, visuals, level, map, objects, levelMap, player, header
  levelMap = levels[level].copy()
  player.displayPlayer()
  header = txt[level]
  for obj in objects:
    obj.displayObj()
  map = decode(levelMap, visuals)
  clearConsole()
  print(header +"\n"+ str(player.index))
  print(map)
  cmd = input("WASD - move\np - pause\nr - reset level\nHit enter\n> ").lower()
  if cmd in ["w", "a", "s", "d"]:
    player.movePlayer(cmd)
  elif cmd == "p":
    pause()
    return
  elif cmd == "r":
    return "restart"
  for obj in objects:
    check = obj.moveObj("n", "n")
    if check != None:
      return check

startUp()