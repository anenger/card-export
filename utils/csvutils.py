import csv
from utils.generators import Generator
from utils.card import Card
import uuid

class CSVIO:
    infile = ""
    outfile = ""
    template = ""
    generator = ""

    def __init__(self, infile, outfile, templates, generator):
        self.infile = infile
        self.outfile = outfile
        self.templates = templates
        self.generator = generator

    def writeEZMode(self, cards, file_exists):
        with open(self.outfile, mode='a+') as cardfile:
            writer = csv.DictWriter(cardfile, fieldnames=self.templates['ezmode2'].keys(), delimiter='\t', lineterminator='\n')
            if not file_exists:
                writer.writeheader()
            for card in cards:
                export = self.templates['ezmode2'].copy()
                export['BillingFirst'], export['BillingLast'] = self.generator.genName()
                export['CardName'] = export['BillingFirst'] + ' ' + export['BillingLast']
                export['BillingLine1'] = self.generator.genStreet()
                export['BillingLine2'] = self.generator.genAddress2()
                export['BillingCity'] = self.generator.city
                export['BillingState'] = self.generator.state
                export['BillingZip'] = self.generator.zip
                export['BillingCountry'] = "US"
                export['BillingPhone'] = self.generator.genPhone()
                export['ProfileName'] = card.cardid
                export['Email'] = self.generator.genEmail()
                export['CardNumber'] = card.number
                export['CardType'] = card.cardtype
                export['CardCVV'] = card.cvv
                export['CardMonth'] = card.expmonth
                export['CardYear'] = card.expyear
                writer.writerow(export)
    
    def writeWop(self, cards, file_exists):
        with open(self.outfile, mode='a+') as cardfile:
            writer = csv.DictWriter(cardfile, fieldnames=self.templates['wop'].keys(), delimiter=',', lineterminator='\n')
            if not file_exists:
                writer.writeheader()
            for card in cards:
                export = self.templates['wop'].copy()
                export['Profile Name'] = card.cardid
                export['Webhook'] = self.generator.webhook
                export['Proxy'] = self.generator.proxy
                export['Email'] = self.generator.genEmail()
                export['Phone'] = self.generator.genPhone()
                export['Card'] = card.number
                export['Exp Month'] = card.expmonth
                export['Exp Year'] = card.expyear
                export['CVV'] = card.cvv
                export['Billing First Name'], export['Billing Last Name'] = self.generator.genName()
                export['Billing Address 1'] = self.generator.genStreet()
                export['Billing Address 2'] = self.generator.genAddress2()
                export['Billing City'] = self.generator.city
                export['Billing Zip'] = self.generator.zip
                export['Billing State'] = self.generator.state
                export['Billing Country'] = "US"
                writer.writerow(export)

    def writeHayha(self, cards, file_exists):
        with open(self.outfile, mode='a+') as cardfile:
            writer = csv.DictWriter(cardfile, fieldnames=self.templates['hayha'].keys(), delimiter=',', lineterminator='\n')
            if not file_exists:
                writer.writeheader()
            for card in cards:
                export = self.templates['hayha'].copy()
                export['profilename'] = card.cardid
                export['FirstName'], export['LastName'] = self.generator.genName()
                export['AddressLine1'] = self.generator.genStreet()
                export['AddressLine2'] = self.generator.genAddress2()
                export['City'] = self.generator.city
                export['Zipcode'] = self.generator.zip
                export['StateEntry'] = self.generator.state
                export['Country'] = "US"
                export['Email'] = self.generator.genEmail()
                export['Phone'] = self.generator.genPhone()
                export['CreditCardNumber'] = card.number
                export['CreditCardMonth'] = card.expmonth
                export['CreditCardYear'] = '20' + str(card.expyear)
                export['CVV'] = card.cvv
                export['id'] = str(uuid.uuid4())
                export['group'] = self.generator.groupid
                writer.writerow(export)

    def readCSV(self):
        cardlist = []
        with open(self.infile, newline='') as cardfile:
            reader = csv.DictReader(cardfile)
            i = 0
            for row in reader:
                i+=1
                print(row)
                cardlist.append(Card("Card{}".format(i), row['CardType'], row['CardNumber'], row['CardCVV'], row['CardMonth'], row['CardYear'], True))
        return cardlist
