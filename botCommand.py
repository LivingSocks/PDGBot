import fchat

from collections import Counter
from onMSGUtils import *

class EchoBot(fchat.FChatClient):
    log_filter = ["PIN", "NLN", "FLN", "STA", "LIS", "VAR", "HLO", "CON", "FRL", "IGN", "ADL", "TPN"]

    masterList = []
    firstUsers = []
    chosenUser = []
    bGameTimer = True


    def combatTimeOut(self):
        channel = room["PDGBot"]
        self.firstUsers = list(self.masterList)
        self.chosenUser = []
        super().MSG(channel, "An hour has passed. Game has reset. Timer worked!")

    def JCH(self, channel):
        super().JCH(channel)

    def on_ICH(self, users, channel, mode):
        self.masterList, self.firstUsers = message_8_compile(users)

    def on_COL(self, channel, oplist):
        print(oplist)

    def on_JCH(self, character, channel, title):
        if character not in self.masterList:
            self.masterList.append(character)
            self.firstUsers.append(character)


    def on_LCH(self, channel, character):
        if character in self.masterList:
            self.masterList.remove(character)
            self.firstUsers.remove(character)

    def on_MSG(self, character, message, channel):
        file = open("room.txt", "r", encoding="utf-8")
        room = json.load(file)
        file.close()

        PDGBot = room['PDGBot']

        if message[:5] == "!bell":
            msg = message_5_bell(channel, PDGBot, character, message)
            super().MSG(channel, msg)

        if message[:8] == "!compile":
            print("why")
            masterList = self.masterList
            userList = "\nCurrent room list: \n"
            userID = "\n".join(masterList)
            super().MSG(channel, userList + userID)

        if message[:7] == "!optout":
            firstUsers = self.firstUsers
            chosenUser = self.chosenUser
            msg = message_7_optout(channel, PDGBot, character, firstUsers, chosenUser)
            super().MSG(channel, msg)

        if message[:6] == "!optin":
            firstUsers = self.firstUsers
            chosenUser = self.chosenUser
            msg = message_6_optin(channel, PDGBot, character, firstUsers, chosenUser)
            super().MSG(channel, msg)

        if message[:5] == "!spin":
            if self.bGameTimer == False:
                self.gameTimer.cancel()
                self.bGameTimer = True
            firstUsers = self.firstUsers
            chosenUser = self.chosenUser
            msg = message_5_spin(channel, PDGBot, character, firstUsers, chosenUser)
            super().MSG(channel, msg)
            if self.bGameTimer:
                gametimeout = 60
                self.gameTimer = Timer(gametimeout, self.combatTimeOut)
                self.gameTimer.start()
                self.bGameTimer = False

        if message[:6] == "!first":
            firstUser = self.firstUsers
            if len(firstUser) == 0:
                super().MSG(channel, "Every User Profile has been selected.")
            else:
                super().MSG(channel, "User Profiles not chosen yet: \n" + "\n".join(firstUser))

        if message[:7] == "!second":
            chosenUser = self.chosenUser
            if len(chosenUser) == 0:
                super().MSG(channel, "No User Profile has been chosen yet.")
            else:
                print(chosenUser)
                try:
                    super().MSG(channel, "User Profiles already selected: \n" + "\n".join(chosenUser))
                except:
                    super().MSG(channel, "This worked...technically, but I seem unable to print out result to room.")

file = open("credentials.txt", "r", encoding="utf-8")
info = json.load(file)
file.close()

file = open("room.txt", "r", encoding="utf-8")
room = json.load(file)
file.close()

website = info['website']
user = info['user']
password = info['password']
profile = info['profile']

PDGBot= room['PDGBot']
bot = EchoBot(website, user, password, profile)
bot.setup()
bot.connect()
bot.JCH(PDGBot)
bot.run_forever()