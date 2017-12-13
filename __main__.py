# build-ins
import argparse
import logging
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
            r[domain['id']] = {'id': domain['id'], 'name': domain['name'], 'url': domain['base_url']}
        return r

    def __init__(self, client_id, secret):
        self.client_id = client_id
        self.secret = secret
        self.bearer = None

    def post_request(self, endpoint, request, add_key=True):
        response = requests.post(endpoint, json=request, headers=self.get_headers(
            {'Authorization': "Bearer " + self.get_key()} if add_key else {}))
        logging.debug(response.text)
        return response.json()

    def get_request(self, endpoint):
        response = requests.get(endpoint, headers=self.get_headers({'Authorization': "Bearer " + self.get_key()}))
        logging.debug(response.text)
        return response.json()

    def patch_request(self, endpoint, payload):
        response = requests.patch(endpoint, json=payload,
                              headers=self.get_headers({'Authorization': "Bearer " + self.get_key()}))
        logging.debug(response.text)
        return response.json()

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
        return self.get_request(config.ENDPOINT_USER_INFO)

    def get_websites(self, customer_id):
        return self.get_request(config.ENDPOINT_WEBSITES % customer_id)

    def disable_testing(self, website_id):
        return self.patch_request(config.ENDPOINT_WEBSITE % website_id, {"active": False})

    def enable_testing(self, website_id):
        return self.patch_request(config.ENDPOINT_WEBSITE % website_id, {"active": True})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['offline', 'online', 'shops', 'websites'], help=config.ACTION_HELP)
    parser.add_argument('website_id', nargs='?', help=config.WEBSITE_ID_HELP)
    parser.add_argument('client_id', nargs='?', help=config.CLIENT_ID_HELP % config.SHOPPIMON_API_ACCOUNT_PAGE)
    parser.add_argument('client_secret', nargs='?', help=config.CLIENT_SECRET_HELP % config.SHOPPIMON_API_ACCOUNT_PAGE)
    parser.add_argument("--debug", "-d", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.client_id is None and config.CLIENT_ID is None:
        parser.error('client_id is not set in config or given')
    if args.client_secret is None and config.CLIENT_SECRET is None:
        parser.error('client_secret is not set in the config')
    if args.action != 'shops' and args.website_id is None and config.WEBSITE_ID is None:
        parser.error('website_id is required for this method call')

    if args.client_id is not None:
        config.CLIENT_ID = args.client_id
    if args.client_secret is not None:
        config.CLIENT_SECRET = args.client_secret
    if args.website_id is not None:
        config.WEBSITE_ID = args.website_id

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('Chosen action: %s' % args.action)
    logging.debug('Using Client_id: %s' % config.CLIENT_ID)
    logging.debug('Using Client_secret: %s ' % config.CLIENT_SECRET)
    logging.debug('Using Website_id: %s' % config.WEBSITE_ID)

    if args.action == 'offline':
        Shoppimon.offline(config.CLIENT_ID, config.CLIENT_SECRET, config.WEBSITE_ID)
    elif args.action == 'online':
        Shoppimon.online(config.CLIENT_ID, config.CLIENT_SECRET, config.WEBSITE_ID)
    elif args.action == 'shops':
        for index, value in Shoppimon.get_shops(config.CLIENT_ID, config.CLIENT_SECRET).items():
            print("id: %s | name: %s" % (index, value))
    elif args.action == 'websites':
        for index, website in Shoppimon.get_website_for_account(config.CLIENT_ID, config.CLIENT_SECRET, config.WEBSITE_ID).items():
            print("website-id: %s | name: %s | url: %s" % (website['id'], website['name'], website['url']))
