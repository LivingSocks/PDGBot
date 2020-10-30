import fchat

from collections import Counter
from onMSGUtils import *

class EchoBot(fchat.FChatClient):
    log_filter = ["PIN", "NLN", "FLN", "STA", "LIS", "VAR", "HLO", "CON", "FRL", "IGN", "ADL", "TPN"]

    # Set up variables to hold the various lists, and a boolean value to trigger timer.
    masterList = []
    firstUsers = []
    chosenUser = []
    bGameTimer = True


    # Once timer has passed, reset the game. Takes the list of profile names in 'Master List' and puts them back in
    # 'First Users.'
    def combatTimeOut(self):
        channel = room["PDGBot"]
        self.firstUsers = list(self.masterList)
        self.chosenUser = []
        super().MSG(channel, "An hour has passed. Game has reset. Timer worked!")

    # Have the bot join the correct channel.
    def JCH(self, channel):
        super().JCH(channel)

    # Have the bot compile a 'Master List' and a 'First Users' list the moment it enters room.
    # The message_8_compile(users) function should automatically weed out profile names excluded permanently
    # from game (For Testing Purposes: CharacterNo147
    def on_ICH(self, users, channel, mode):
        self.masterList, self.firstUsers = message_8_compile(users)

    # This needs to be here, cause ICH calls it. If this isn't here, you get a NoneType Error. Who the fuck
    # knows why. I wish I did, then I'd be a good programmer. ¯\_(ツ)_/¯
    def on_COL(self, channel, oplist):
        print(oplist)

    # Grab profile name of person entering room, and add it to 'Master List' and 'First Users'
    def on_JCH(self, character, channel, title):
        if character not in self.masterList:
            self.masterList.append(character)
            self.firstUsers.append(character)

    # Grab profile name of person leaving room, and remove it to 'Master List' and 'First Users'
    def on_LCH(self, channel, character):
        if character in self.masterList:
            self.masterList.remove(character)
            self.firstUsers.remove(character)

    # function that handles all the commands.
    def on_MSG(self, character, message, channel):
        file = open("room.txt", "r", encoding="utf-8")
        room = json.load(file)
        file.close()

        PDGBot = room['PDGBot']

        # Test command. Made to ensure bot was establishing connection and listening
        if message[:5] == "!bell":
            msg = message_5_bell(channel, PDGBot, character, message)
            super().MSG(channel, msg)

        # Test command. Will be removed once deployed. Used to ensure list was made correctly.
        if message[:8] == "!compile":
            masterList = self.masterList
            userList = "\nCurrent room list: \n"
            userID = "\n".join(masterList)
            super().MSG(channel, userList + userID)

        # Command to allow profiles to 'optout' of game, removing them from lists.
        if message[:7] == "!optout":
            firstUsers = self.firstUsers
            chosenUser = self.chosenUser
            msg = message_7_optout(channel, PDGBot, character, firstUsers, chosenUser)
            super().MSG(channel, msg)

        # Command to allow profiles to 'optin' to game, adding them to 'Chosen User' list. Profile is added
        # to 'Chosen User' to avoid abuse of !optout/!optin, and immediately placing themselves back in list
        # with higher proirity
        if message[:6] == "!optin":
            firstUsers = self.firstUsers
            chosenUser = self.chosenUser
            msg = message_6_optin(channel, PDGBot, character, firstUsers, chosenUser)
            super().MSG(channel, msg)

        # The core of the game. Selects four profile names, and displays them to chat room. Things to note:
        # 1) Profile using command is temporarily removed from list, to avoid the chance of selecting itself as
        # One of the four profiles.
        # 2) There are two lists in the game. 'First Users' and 'Chosen Users'.
            # A) 'First Users' is a list of all profiles not selected yet. This list as a 66% of being selected
            # B) 'Chosen User' is a list of all profiles that have been selected at least once. They have a 33%
            # of being selected again.
        # 3) Once every profile from 'First Users' has been selected, game will empty out 'Chosen User', refill
        # 'First Users' and game begins anew.
        # 4) There is a timer set. For testing purposes, it is set for 1 minute. Realistically, once 'x' minutes has
        # passed, the game will auto-reset, empting out 'Chosen User' and refiling 'First User'
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

        # For testing purposes, will be removed when deployed. Displays list of all profiles currently in 'First Users'
        if message[:6] == "!first":
            firstUser = self.firstUsers
            if len(firstUser) == 0:
                super().MSG(channel, "Every User Profile has been selected.")
            else:
                super().MSG(channel, "User Profiles not chosen yet: \n" + "\n".join(firstUser))

        # For testing purposes, will be removed when deployed. Displays list of all profiles currently in 'Chosen Users'
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


# Text file that holds login credentials
file = open("credentials.txt", "r", encoding="utf-8")
info = json.load(file)
file.close()

# Text file that holds room APH tickets
file = open("room.txt", "r", encoding="utf-8")
room = json.load(file)
file.close()

# Variables
website = info['website']
user = info['user']
password = info['password']
profile = info['profile']

# Start the bot and run it forever.
PDGBot= room['PDGBot']
bot = EchoBot(website, user, password, profile)
bot.setup()
bot.connect()
bot.JCH(PDGBot)
bot.run_forever()
