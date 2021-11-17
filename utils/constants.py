import re as regex
from PyInquirer import style_from_dict, Token, ValidationError, Validator

CUSTOM_STYLE = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Answer: '#5F819D bold',
})

STATES_LIST = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
'VI', 'VA', 'WA', 'WV', 'WI', 'WY']


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match(
            r'^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


class EmailValidator(Validator):
    def validate(self, document):
        ok = "@" in document.text
        if not ok:
            raise ValidationError(
                message='Please enter a valid email',
                cursor_position=len(document.text))  # Move cursor to end

class NotBlankValidator(Validator):
    def validate(self, document):
        ok = len(document.text) > 0
        if not ok:
            raise ValidationError(
                message='Please do not enter a null field.',
                cursor_position=len(document.text))  # Move cursor to end

class ZipCodeValidator(Validator):
    def validate(self, document):
        ok = regex.match(r'^[\d]{5}(?:-[\d]{4})?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please do not enter a null field.',
                cursor_position=len(document.text))  # Move cursor to end

class StateValidator(Validator):
    def validate(self, document):
        ok = document.text in STATES_LIST
        if not ok:
            raise ValidationError(
                message='Please do not enter a null field.',
                cursor_position=len(document.text))  # Move cursor to end



LOAD_SETTINGS = [
    {
        'type': 'confirm',
        'name': 'useSaved',
        'message': 'Do you have settings saved here?'
    },
    {
        'type': 'input',
        'name': 'loadFile',
        'message': 'Enter a filename to load settings from:',
        'when': lambda answers: answers['useSaved'] == True,
        'validate': NotBlankValidator
    },
    {
        'type': 'input',
        'name': 'quantity',
        'message': 'How many times do you want to run the script?',
        'validate': NotBlankValidator
    }
]

QUESTIONS = [
    {
        'type': 'list',
        'name': 'cardProvider',
        'message': 'Export Privacy, Stripe or your own cards?',
        'choices': ['Privacy', 'Stripe', 'Own'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'ownImport',
        'message': 'What is the filename of the csv import?',
        'when': lambda answers: answers['cardProvider'] == 'own'
    },
    {
        'type': 'input',
        'name': 'privacyEmail',
        'message': 'What is your Privacy email?',
        'validate': EmailValidator,
        'when': lambda answers: answers['cardProvider'] == 'privacy'
    },
    {
        'type': 'password',
        'name': 'privacyPassword',
        'message': 'What is your Privacy password?',
        'when': lambda answers: answers['cardProvider'] == 'privacy',
        'validate': NotBlankValidator
    },
    {
        'type': 'list',
        'name': 'privacyUnused',
        'message': 'Would you like to get only unused Privacy cards, or all?',
        'choices': ['Unused', 'All'],
        'filter': lambda val: val.lower(),
        'when': lambda answers: answers['cardProvider'] == 'privacy'
    },
    {
        'type': 'input',
        'name': 'stripeToken',
        'message': 'What is your Stripe secret token?',
        'when': lambda answers: answers['cardProvider'] == 'stripe',
        'validate': NotBlankValidator
    },
    {
        'type': 'list',
        'name': 'stripeNewCards',
        'message': 'Would you like to create new Stripe cards, or just get the existing ones?',
        'choices': ['New', 'Preexisting'],
        'filter': lambda val: val.lower(),
        'when': lambda answers: answers['cardProvider'] == 'stripe'
    },
    {
        'type': 'input',
        'name': 'stripeCardholderPreexisting',
        'message': 'Enter a cardholder id for the cards you want to get. (or leave blank for all)',
        'when': lambda answers: answers.get('stripeNewCards', "") == 'preexisting'
    },
    {
        'type': 'input',
        'name': 'stripeValue',
        'message': 'How many Stripe cards would you like to create?',
        'when': lambda answers: answers.get('stripeNewCards', "") == 'new',
        'validate': NotBlankValidator
    },
    {
        'type': 'input',
        'name': 'stripeCardholder',
        'message': 'Enter a cardholder id which you would like to create new cards under. (or leave blank for new cardholders)',
        'when': lambda answers: answers.get('stripeNewCards', "") == 'new'
    },
    {
        'type': 'list',
        'name': 'export',
        'message': 'Which style would you like the cards exported in?',
        'choices': ['EzMode', 'Wop', 'Hayha'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'wopWebhook',
        'message': 'Enter a webhook to use for tasks (or leave blank)',
        'when': lambda answers: answers.get('export', "") == 'wop'
    },
    {
        'type': 'input',
        'name': 'wopProxy',
        'message': 'Enter a proxy to use for tasks (or leave blank)',
        'when': lambda answers: answers.get('export', "") == 'wop'
    },
    {
        'type': 'input',
        'name': 'hayhaGroupID',
        'message': 'Enter a group ID from the Hayha Export',
        'when': lambda answers: answers.get('export', "") == 'hayha'
    },
    {
        'type': 'input',
        'name': 'email',
        'message': 'Enter an email (or catchall with @catchall.com) to use for creating profiles.',
        'validate': EmailValidator
    },
    {
        'type': 'input',
        'name': 'emailPrefix',
        'message': 'Enter an email prefix for your catchall, otherwise leave blank and one will be generated randomly.',
        'when': lambda answers: answers['email'][0] == "@"
    },
    {
        'type': 'confirm',
        'name': 'addressJig',
        'message': 'Do you need address line 1 jigging?',
    },
    {
        'type': 'confirm',
        'name': 'addressJig2',
        'message': 'Do you need address line 2 jigging?',
    },
    {
        'type': 'confirm',
        'name': 'phoneJig',
        'message': 'Do you need phone jigging?'
    },
    {
        'type': 'input',
        'name': 'firstNames',
        'message': 'Enter a comma separated list of first names to use for jigging. (alternatively, enter 1 name for no jigging.)',
        'validate': NotBlankValidator
    },
    {
        'type': 'input',
        'name': 'lastNames',
        'message': 'Enter a comma separated list of last names to use for jigging. (alternatively, enter 1 name for no jigging.)',
        'validate': NotBlankValidator
    },
    {
        'type': 'input',
        'name': 'addressLine1',
        'message': 'Enter line 1 of an address to use for creating profiles.',
        'validate': NotBlankValidator
    },
    {
        'type': 'input',
        'name': 'addressLine2',
        'message': 'Enter line 2 of an address to use for creating profiles. (Leave blank for none)',
    },
    {
        'type': 'input',
        'name': 'city',
        'message': 'Enter a city to use for profiles.',
        'validate': NotBlankValidator
    },
    {
        'type': 'input',
        'name': 'state',
        'message': 'Enter a state to use for profiles (two letter code)',
        'validate': StateValidator
    },
    {
        'type': 'input',
        'name': 'zipCode',
        'message': 'Enter a zip code to use for profiles.',
        'validate': ZipCodeValidator
    },
    {
        'type': 'input',
        'name': 'phoneNumber',
        'message': 'Enter a phone number to use for profiles.',
        'validate': PhoneNumberValidator
    }
]

CHECK_SETTINGS = [
    {
        'type': 'confirm',
        'name': 'settingsOkay',
        'message': 'Do these settings look good?',
    }
]

SAVE_SETTINGS = [
    {
        'type': 'confirm',
        'name': 'saveSettings',
        'message': 'Would you like to save these settings for future use?',
    },
    {
        'type': 'input',
        'name': 'saveFile',
        'message': 'Enter a filename to save settings to:',
        'when': lambda answers: answers['saveSettings'] == True
    }
]