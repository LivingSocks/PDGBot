import os
import json
import random
import time
from pathlib import Path
from threading import Timer

def message_5_bell(channel, PGDBot, character, message):
    bellCharacter = ["An Entity", "Asa Clarke"]
    if channel == PGDBot:
        if message == "!bell" and character in bellCharacter:
            msg = "Ding Ding"
        else:
            msg = "The bell does not seem to respond to your actions."
    else:
        pass
    return msg

def message_8_compile(users):
    noNoList = ["CharacterNo147", "Eopi Bot", "Robutt"]
    masterList = []
    firstUsers = []
    for item in users:
        if item["identity"] not in noNoList:
            masterList.append(item["identity"])
            firstUsers.append(item["identity"])
    return masterList, firstUsers

def message_7_optout(channel, PDGBot, character, firstUsers, chosenUser):
    if character in firstUsers:
        firstUsers.remove(character)
        msg = character + " has opted out of playing KATI. Please use !optin to rejoin"
    elif character in chosenUser:
        chosenUser.remove(character)
        msg = character + " has opted out of playing KATI. Please use !optin to rejoin"
    else:
        msg = character + " is currently not partisipating in KATI."
    return msg

def message_6_optin(channel, PDGBot, character, firstUsers, chosenUser):
    if character in firstUsers:
        msg = character + " is already partisipating in KATI."
    elif character not in chosenUser:
        chosenUser.append(character)
        msg = character + " has opted in to play KATI. Please use !opout to remove self from list"
    else:
        msg = character + " is already partisipating in KATI."
    return msg

def message_5_spin(channel, PDGBot, character, firstUsers, chosenUser):
    copyFirstUsers = list(firstUsers)
    print(copyFirstUsers)
    if copyFirstUsers == []:
        copyFirstUsers = list(chosenUser)
        copyChosenUser = []
    if character in copyFirstUsers:
        copyFirstUsers.remove(character)
    copyChosenUser = list(chosenUser)
    if character in copyChosenUser:
        copyChosenUser.remove(character)
    userSelected = []
    totalUsers = len(copyFirstUsers) + len(copyChosenUser)
    if totalUsers < 5:
        msg = "There are currently not enough people to play KATI."
    else:
        for num in range(0, 4):
            randomNumber = random.randint(1, 101)
            print(randomNumber)
            print(copyFirstUsers)
            if randomNumber < 67 and len(copyFirstUsers) > 0  or len(copyChosenUser) < 3:
                print("why?")
                if len(copyFirstUsers) > 0:
                    selectUser = random.randint(0, len(copyFirstUsers) - 1)
                else:
                    selectUser = 0
                userName = copyFirstUsers[selectUser]
                if userName not in userSelected:
                    userSelected.append(userName + "[/icon] " + userName)
                    copyFirstUsers.remove(userName)
                msg = "Profiles selected: [icon]" + ", [icon]".join(userSelected)
                firstUsers.remove(userName)
                chosenUser.append(userName)
            else:
                print("why?")
                selectUser = random.randint(0, len(copyChosenUser) - 1)
                userName = copyChosenUser[selectUser]
                if userName not in userSelected:
                    userSelected.append(userName + "[/icon] " + userName)
                msg = "Profiles selected: [icon]" + ", [icon]".join(userSelected)
    return msg
