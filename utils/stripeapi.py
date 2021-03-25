import stripe
import time
import json
import os
from utils.card import Card
from utils.generators import Generator
from utils.csvutils import CSVIO

class StripeSession:

    def __init__(self, stripekey):
        stripe.api_key = stripekey

    def createCardholder(self, generator):
        try:
            cardholder = stripe.issuing.Cardholder.create(
                type="individual",
                name=' '.join(generator.genName()),
                email=generator.genEmail(),
                phone_number='+1' + generator.genPhone(),
                status='active',
                billing={
                    'address': {
                        'line1': generator.genStreet(),
                        'city': generator.city,
                        'state': generator.state,
                        'postal_code': generator.zip,
                        'country': 'US',
                    },
                },
            )
            return cardholder.id
        except Exception as e:
            print(e)
            print("Could not create cardholder.")
            return

    def activateCard(self, cardid):
        try:
            stripe.issuing.Card.modify(cardid, status="active")
            return True
        except Exception as e:
            print(e)
            print("Could not activate card.")
            return False
            
    def getCardsWithCardholder(self, cardholder):
        cards = stripe.issuing.Card.list(limit=100,status="active",cardholder=cardholder)
        carddata = []
        for card in cards['data']:
            carddata.append(self.getCardDetails(card['id']))
        return carddata
            
    def getAllCards(self, cardholder):
        carddata = []
        if cardholder:
            carddata = self.getCardsWithCardholder(cardholder)
        else:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            templates = None
            with open("utils/exports.json", "r") as f:
                templates = json.load(f)
            cardholders = self.getAllCardholders()
            for cardholder in cardholders:
                file_exists = os.path.isfile("exports/" + timestr + "cardfile.tsv")
                generator = self.getCardholderDetails(cardholder.id)
                cards = self.getCardsWithCardholder(cardholder.id)
                csv = CSVIO("", "exports/" + timestr + "cardfile.tsv", templates, generator)
                csv.writeEZMode(cards, file_exists)
        return carddata
    
    def getCardholderDetails(self, cardholder):
        cardholder = stripe.issuing.Cardholder.retrieve(cardholder)
        name = cardholder.name.split()
        generator = Generator([name[0]], [name[1]], cardholder.email, str(cardholder.phone_number)[2:], 
        cardholder.billing.address.line1, cardholder.billing.address.line2, cardholder.billing.address.city, 
        cardholder.billing.address.state, cardholder.billing.address.postal_code, None, False, False, False, None, None)
        return generator

    def getAllCardholders(self):
        cardholders = stripe.issuing.Cardholder.list(limit=100, status="active")
        return cardholders

    def createCards(self, number, cardholder):
        cards = []
        for i in range(number):
            cardid = self.createCard(cardholder)
            self.activateCard(cardid)
            carddetails = self.getCardDetails(cardid)
            cards.append(carddetails)
        return cards

    def createCardsNewCardholders(self, number, generator):
        cards = []
        for i in range(number):
            cardholderid = self.createCardholder(generator)
            cardid = self.createCard(cardholderid)
            self.activateCard(cardid)
            carddetails = self.getCardDetails(cardid)
            cards.append(carddetails)
        return cards

    def createCard(self, cardholder):
        try:
            card = stripe.issuing.Card.create(
                cardholder=cardholder,
                type='virtual',
                currency='usd',
            )
            return card.id
        except Exception as e:
            print(e)
            print("Could not create card.")
            return

    def getCardDetails(self, cardid):
        try:
            card = stripe.issuing.Card.retrieve(cardid, expand=['number','cvc'])
            unused = False
            if card.status == "active":
                unused = True
            else:
                unused = False
            return Card(card.id, "Visa", card.number, card.cvc, '{:0>2}'.format(card.exp_month), int(str(card.exp_year)[2:]), unused)
        except Exception as e:
            print(e)
            print("Could not retrieve card.")
