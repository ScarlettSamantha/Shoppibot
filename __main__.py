# build-ins
import os
import sys
# dep: requests
import requests
# ./config.py
import config


class Shoppimon:

    @staticmethod
    def get_headers(data):
        return {**{
            "Accept": "application/json",
            "content-type": "application/json",
        }, **data}

    @classmethod
    def offline(cls, client_id, secret, website_id):
        cls(client_id, secret).disable_testing(website_id)

    @classmethod
    def online(cls, client_id, secret, website_id):
        cls(client_id, secret).enable_testing(website_id)

    @classmethod
    def get_shops(cls, client_id, secret):
        r = {}
        for account in cls(client_id, secret).get_account_details()['_embedded']['account']:
            r[account['id']] = account['name']
        return r

    @classmethod
    def get_website_for_account(cls, client_id, secret, customer_id):
        r = {}
        for domain in cls(client_id, secret).get_websites(customer_id)['_embedded']['website']:
            r[domain['id']] = {domain['id'], domain['name'], domain['base_url']}
        return r

    def __init__(self, client_id, secret):
        self.client_id = client_id
        self.secret = secret
        self.bearer = None

    def post_request(self, endpoint, request, add_key=True):
        return requests.post(endpoint, json=request, headers=self.get_headers(
            {'Authorization': "Bearer " + self.get_key()} if add_key else {})).json()

    def get_request(self, endpoint):
        return requests.get(endpoint, headers=self.get_headers({'Authorization': "Bearer " + self.get_key()})).json()

    def patch_request(self, endpoint, payload):
        return requests.patch(endpoint, json=payload,
                              headers=self.get_headers({'Authorization': "Bearer " + self.get_key()})).json()

    def fetch_key(self):
        r = self.post_request(config.ENDPOINT_OAUTH, {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.secret
        }, False)
        self.bearer = r['access_token']

    def get_key(self):
        """
        :return: str 
        """
        if self.bearer is None:
            self.fetch_key()
        return self.bearer

    def get_account_details(self):
        return self.get_request(config.ENDPOINT_CURRENT_USER)

    def get_websites(self, customer_id):
        return self.get_request(config.ENDPOINT_WEBSITES % customer_id)

    def disable_testing(self, website_id):
        return self.patch_request(config.ENDPOINT_WEBSITE % website_id, {"active": False})

    def enable_testing(self, website_id):
        return self.patch_request(config.ENDPOINT_WEBSITE % website_id, {"active": True})


def argument_check(req=4):
    req += 1
    if sys.argv.__len__() < req:
        print('We need %s arguments we got %s' % (req, sys.argv.__len__()))
        if req == 5:
            if sys.argv[1] == 'websites':
                argument = 'client_id'
            elif sys.argv[1] in ('online', 'offline'):
                argument = 'website_id'
            else:
                argument = 'unknown'
            print("python3 %s %s [client_id] [client_secret] [argument(%s)]" % (
             os.path.abspath(__file__), sys.argv[1] if sys.argv.__len__() > 1 else '[action]', argument))
            exit(2)
        elif req == 4:
            print("python3 %s %s [client_id] [client_secret]" % (
             os.path.abspath(__file__), sys.argv[1] if sys.argv.__len__() > 1 else '[action]'))
            exit(2)


if __name__ == "__main__":
    action = sys.argv[1]

    if action == 'offline':
        argument_check(4)
        Shoppimon.offline(sys.argv[2], sys.argv[3], sys.argv[4])
    elif action == 'online':
        argument_check(4)
        Shoppimon.online(sys.argv[2], sys.argv[3], sys.argv[4])
    elif action == 'shops':
        argument_check(3)
        for index, value in Shoppimon.get_shops(sys.argv[2], sys.argv[3]).items():
            print("id: %s | name: %s" % (index, value))
    elif action == 'websites':
        argument_check(4)
        for index, website in Shoppimon.get_website_for_account(sys.argv[2], sys.argv[3], sys.argv[4]).items():
            print("id: %s | name: %s | url: %s" % tuple(website))
