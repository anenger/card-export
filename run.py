import csv
import json
import random
import string
import sys
import time
import os
import uuid
import re as regex

from pprint import pprint
from PyInquirer import ValidationError, Validator, prompt, style_from_dict, Token

from utils.card import Card
from utils.csvutils import CSVIO
from utils.generators import Generator
from utils.privacy import PrivacySession
from utils.stripeapi import StripeSession
from utils.constants import QUESTIONS, CUSTOM_STYLE, LOAD_SETTINGS, CHECK_SETTINGS, SAVE_SETTINGS

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

def whitespace_only(file):
    content = open(file, 'r').read()
    if regex.search(r'^\s*$', content):
        return True

if __name__ == "__main__":
    templates = ""
    promptsettings = ""
    prefix = ""
    cardlist = []

    with open("utils/exports.json", "r") as f:
        templates = json.load(f)

    loader = prompt(LOAD_SETTINGS, style=CUSTOM_STYLE)
    if (loader != {}):
        if (loader['useSaved']):
            try:
                with open("imports/" + loader['loadFile'] + ".json", "r") as f:
                    promptsettings = json.load(f)
                    pprint(promptsettings)
            except Exception as e:
                print("Could not find the settings file.")
                exit()
        else:
            promptsettings = prompt(QUESTIONS, style=CUSTOM_STYLE)
            if (promptsettings != {}):
                pprint(promptsettings)
                confirm = prompt(CHECK_SETTINGS)
                if (confirm != {}):
                    if (confirm['settingsOkay']):
                        saver = prompt(SAVE_SETTINGS, style=CUSTOM_STYLE)
                        if (saver != {}):
                            if (saver['saveSettings']):
                                try:
                                    with open("imports/" + saver['saveFile'] + ".json", "w") as f:
                                        json.dump(promptsettings, f)
                                except Exception as e:
                                    print(e)
                                    print("Could not save settings. Please try again. (This may be a file permissions issue.)")
                                    exit()


    generator = Generator(promptsettings['firstNames'].split(','), promptsettings['lastNames'].split(','), promptsettings['email'], 
    promptsettings['phoneNumber'], promptsettings['addressLine1'], promptsettings['addressLine2'], promptsettings['city'], 
    promptsettings['state'], promptsettings['zipCode'], promptsettings.get('emailPrefix', ""), promptsettings['phoneJig'], promptsettings['addressJig'], promptsettings['addressJig2'], 
    promptsettings.get('wopWebhook', ""), promptsettings.get('wopProxy', ""), promptsettings.get("hayhaGroupID", ""))

    if (promptsettings['cardProvider'] == "privacy"):
        privacysession = PrivacySession(promptsettings['privacyEmail'], promptsettings['privacyPassword'])
        if (promptsettings['privacyUnused'] == "unused"):
            cardlist = privacysession.findNewCards()
            print("Total cards found: " + str(len(cardlist)))
        else:
            cardlist = privacysession.getCards()
            print("Total cards found: " + str(len(cardlist)))
    elif (promptsettings['cardProvider'] == "stripe"):
        stripesession = StripeSession(promptsettings['stripeToken'])
        if (promptsettings['stripeNewCards'] == "new"):
            if promptsettings['stripeCardholder'] == "":
                print("Generating {0} cards with new cardholders".format(promptsettings['stripeValue']))
                cardlist = stripesession.createCardsNewCardholders(int(promptsettings['stripeValue']), generator)
                print("Created {} cards.".format(len(cardlist)))
            else:
                print("Generating {0} cards under cardholder {1}".format(promptsettings['stripeValue'], promptsettings['stripeCardholder']))
                cardlist = stripesession.createCards(int(promptsettings['stripeValue']), promptsettings['stripeCardholder'])
                print("Created {} cards.".format(len(cardlist)))
        else:
            print("Getting all stripe cards...")
            cardlist = stripesession.getAllCards(promptsettings.get('stripeCardholderPreexisting', None))
            print("Got all cards, exporting...")
    else:
        print("Importing cards from {}".format(promptsettings['ownImport']))
        csvimport = CSVIO("imports/" + promptsettings['ownImport'] + ".csv", "", templates, generator)
        cardlist = csvimport.readCSV()

    timestr = time.strftime("%Y%m%d-%H%M%S")
            
    for i in range(0, int(loader['quantity'])):
        print("Cards received, now generating profiles...")
        mode = promptsettings['export']
        file_exists = os.path.isfile(f"exports/{timestr}{mode}.tsv")
        csvexporter = CSVIO("", f"exports/{timestr}{mode}.tsv", templates, generator)
        if mode == "ezmode":
            csvexporter.writeEZMode(cardlist, file_exists)
        elif mode == "wop":
            csvexporter.writeWop(cardlist, file_exists)
        elif mode == "hayha":
            csvexporter.writeHayha(cardlist, file_exists)

    print("Generated profiles, check exports folder!")