import os
import json
import random
import time
from pathlib import Path
from threading import Timer

# Test function. Just making sure bot is listening and responding to commands
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

# Test Function. Just making sure bot is compiling lists correctly
def message_8_compile(users):
    noNoList = ["CharacterNo147", "Eopi Bot", "Robutt"]
    masterList = []
    firstUsers = []
    for item in users:
        if item["identity"] not in noNoList:
            masterList.append(item["identity"])
            firstUsers.append(item["identity"])
    return masterList, firstUsers

# Function to allow for profile to 'optout' of game.
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

# Function to allow for profile to 'optin' to game. Should put profile in 'Chosen User' list, to avoid abuse of
# optout/optin, and being put back in primary list.
def message_6_optin(channel, PDGBot, character, firstUsers, chosenUser):
    if character in firstUsers:
        msg = character + " is already partisipating in KATI."
    elif character not in chosenUser:
        chosenUser.append(character)
        msg = character + " has opted in to play KATI. Please use !opout to remove self from list"
    else:
        msg = character + " is already partisipating in KATI."
    return msg

# This....this is a fucking mess. A mockery of programming. A shameful blight on all that call themselves programmers.
# Absolutely disgusting management of lists, and there HAS to be a better, more elagent way of doing this. Hopefully
# this note will explain to future me how this spaghetti code works.
def message_5_spin(channel, PDGBot, character, firstUsers, chosenUser):
    copyFirstUsers = list(firstUsers)
    print(copyFirstUsers)
    # 1) Makes copies of 'First Users' and 'Chosen User' to be used in this function only.
    # 2) Tries to determine right off the bat, that if 'First Users' is empty, empty out 'Chosen User' and refill 'First Users'
    if copyFirstUsers == []:
        copyFirstUsers = list(chosenUser)
        copyChosenUser = []
    # Take out the profile name of the one that used !spin, so they can't be selected.
    if character in copyFirstUsers:
        copyFirstUsers.remove(character)
    copyChosenUser = list(chosenUser)
    if character in copyChosenUser:
        copyChosenUser.remove(character)
    # 4) Creates a new list, 'User Selected'
    userSelected = []
    # 5) If there are not more than 5 players, don't play.
    totalUsers = len(copyFirstUsers) + len(copyChosenUser)
    if totalUsers < 5:
        msg = "There are currently not enough people to play KATI."
    else:
        # 6) Select 4 profile names
        for num in range(0, 4):
            randomNumber = random.randint(1, 101)
            print(randomNumber)
            print(copyFirstUsers)
            # 7) If randomNumber is 66 or less and there is still at least one name in 'copy First Users'
            # or 'copy Chosen User' has less than five names in it, select from 'copy First Users'
            if randomNumber < 67 and len(copyFirstUsers) > 0  or len(copyChosenUser) < 5:
                print("why?")
                # A pathetic attempt to try to get the game to reset, if 'copy First Users' is empty. Surprise!
                # it doesn't work.
                if len(copyFirstUsers) > 0:
                    selectUser = random.randint(0, len(copyFirstUsers) - 1)
                else:
                    selectUser = 0
                userName = copyFirstUsers[selectUser]
                # 8) If the name wasn't already selected, put it in 'User Selected' Then display it to chat in proper
                # format. Then remove said names from the 'REAL' lists.
                if userName not in userSelected:
                    userSelected.append(userName + "[/icon] " + userName)
                    copyFirstUsers.remove(userName)
                msg = "Profiles selected: [icon]" + ", [icon]".join(userSelected)
                firstUsers.remove(userName)
                chosenUser.append(userName)
            else:
                # If randomNumber is 67 or above, pick a name from 'copy Chosen User'. It is SUPPOSE to follow the same
                # logic as above, if name is not already in 'User Selected' put it in, otherwise pick a new one.
                # Surprise! Doesn't work.
                selectUser = random.randint(0, len(copyChosenUser) - 1)
                userName = copyChosenUser[selectUser]
                if userName not in userSelected:
                    userSelected.append(userName + "[/icon] " + userName)
                msg = "Profiles selected: [icon]" + ", [icon]".join(userSelected)
    return msg
