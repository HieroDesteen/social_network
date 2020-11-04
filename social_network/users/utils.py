import requests
import clearbit

from django.conf import settings
from django.core.exceptions import ValidationError


def verify_email(email):
    email_verification = HunterEmailVerification(email=email)
    email_verification.verify_email()


class HunterEmailVerification:
    def __init__(self, email):
        self._api_key = settings.HUNTER_API_KEY
        self._email = email
        self.email_verification_data = self._get_email_verification_data()

    def get_email_status(self):
        return self.email_verification_data.json()['data']['status']

    def _get_email_verification_data(self):
        response = requests.get("https://api.hunter.io/v2/email-verifier",
                                params={'email': self._email, 'api_key': self._api_key})
        return response

    def verify_email(self):
        status = self.get_email_status()
        if status == "invalid":
            raise ValidationError("Invalid email")


class ClearbitUserEnrichment:
    def __init__(self, data):
        clearbit.key = settings.CLEARBIT_API_KEY
        self._data = data
        self._email = self._data.get('email')
        self._clearbit_data = self._get_data_by_email()

    def _get_data_by_email(self):
        response = clearbit.Person.find(email=self._email, stream=True)
        print(response)
        return response

    def _update_user_data(self):
        if self._field_validation('first_name'):
            self._data['first_name'] = self._clearbit_data['name']['givenName']
        if self._field_validation('last_name'):
            self._data['last_name'] = self._clearbit_data['name']['familyName']

    def _field_validation(self, field_name):
        return field_name not in self._data or not self._data[field_name]

    @property
    def data(self):
        if self._clearbit_data:
            self._update_user_data()
        return self._data
