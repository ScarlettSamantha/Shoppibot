# build-ins
import argparse
import logging

# dep: requests
import requests

# ./config.py
import config


class Shoppimon:
    @staticmethod
    def get_headers(data: dict) -> dict:
        return {**{
            "Accept": "application/json",
            "content-type": "application/json",
        }, **data}

    @classmethod
    def offline(cls, client_id: str, secret: str, website_id: str) -> None:
        """Tell shoppinmon to disable the testing.

        Args:
           client_id (str): The client id can be found at https://app.shoppimon.com/user/api
           secret (str): The client secret can be found at https://app.shoppimon.com/user/api 
           website_id (str): The website id can be found using the web_websites call.
        """
        cls(client_id, secret).disable_testing(website_id)

    @classmethod
    def online(cls, client_id: str, secret: str, website_id: str) -> None:
        """Tell shoppinmon to re-enable the testing (to 15min).
       
       Args:
           client_id (str): The client id can be found at https://app.shoppimon.com/user/api
           secret (str): The client secret can be found at https://app.shoppimon.com/user/api 
           website_id (str): The website id can be found using the web_websites call.
       """
        cls(client_id, secret).enable_testing(website_id)

    @classmethod
    def get_shops(cls, client_id: str, secret: str) -> dict:
        """Will return the websites linked to the customer
 
         Args:
             client_id (str): The client id can be found at https://app.shoppimon.com/user/api
             secret (str): The client secret can be found at https://app.shoppimon.com/user/api 
         Returns:
             Dict<int, str>: A dict with the shop id as key and the name of the shop as value str
        
        """
        r = {}
        for account in cls(client_id, secret).get_account_details()['_embedded']['account']:
            r[account['id']] = account['name']
        return r

    @classmethod
    def get_website_for_account(cls, client_id: str, secret: str, customer_id: str) -> dict:
        """Will return the websites linked to the customer
        
        Args:
            client_id (str): The client id can be found at https://app.shoppimon.com/user/api
            secret (str): The client secret can be found at https://app.shoppimon.com/user/api 
            customer_id (str): The customer id can be found using the get_shops call.
        Returns:
            Dict<int, dict>: A dict with the shop id as key and the id, name, url as keys in a sub dict.

        """
        r = {}
        for domain in cls(client_id, secret).get_websites(customer_id)['_embedded']['website']:
            r[domain['id']] = {'id': domain['id'], 'name': domain['name'], 'url': domain['base_url']}
        return r

    def __init__(self, client_id: str, secret: str) -> None:
        """Constructor will load the given args into their properties.
        
        Args:
            client_id (str): The client id can be found at https://app.shoppimon.com/user/api
            secret (str): The client secret can be found at https://app.shoppimon.com/user/api
        """
        self.client_id = client_id
        self.secret = secret
        self.bearer = None

    def post_request(self, endpoint: str, request: dict, add_key=True) -> dict:
        """Will send a post request to the given endpoint with the given payload formatted as json.

        Args:
            endpoint (str): The endpoint to talk to. 
            request (dict): What you want to send the endpoint (will be converted to json)
            add_key (bool): If true it will add the authorization bearer if false not this 
                is due to the key request also being a post.
        Returns:
            A dict with the decoded response json
        """
        response = requests.post(endpoint, json=request, headers=self.get_headers(
            {'Authorization': "Bearer " + self.get_key()} if add_key else {}))
        logging.debug(response.text)
        return response.json()

    def get_request(self, endpoint) -> dict:
        """:obj:`dict`: Will perform a get request
        
        Args:
            endpoint (str): What endpoint to perform the operation against.
        
        Returns:
            Dict with the parsed json.
        """
        response = requests.get(endpoint, headers=self.get_headers({'Authorization': "Bearer " + self.get_key()}))
        logging.debug(response.text)
        return response.json()

    def patch_request(self, endpoint: str, payload: dict) -> dict:
        """Will send a patch request to the given endpoint with the given payload formatted as json.
        
        Args:
            endpoint (str): The endpoint to talk to. 
            payload (dict): What you want to send the endpoint (will be converted to json)
        Returns:
            A dict with the decoded response json
        """
        response = requests.patch(endpoint, json=payload,
                                  headers=self.get_headers({'Authorization': "Bearer " + self.get_key()}))
        logging.debug(response.text)
        return response.json()

    def fetch_key(self) -> None:
        """Will fetch the key from the shoppimon server and cache it in a local property
        
        Returns:
            None
        """
        r = self.post_request(config.ENDPOINT_OAUTH, {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.secret
        }, False)
        self.bearer = r['access_token']

    def get_key(self) -> str:
        """This method will check the cache for a key and if one is not found fetch and cache it.
        
        Returns:
            Str: Will Return the ether cached or fetched key.
        """
        if self.bearer is None:
            self.fetch_key()
        return self.bearer

    def get_account_details(self) -> dict:
        """Will fetch the account details this contains the customers beneath the account.
        
        Returns:
            Dict: The dictionary contains the decoded json response text.
        """
        return self.get_request(config.ENDPOINT_USER_INFO)

    def get_websites(self, customer_id: str) -> dict:
        """Will fetch the websites connected to a customer.
        
        Args:
            customer_id (str): The customer id which can be gotten from the get_account_details funciton.

        Returns:
            Dict: containing the decoded JSON.
        """
        return self.get_request(config.ENDPOINT_WEBSITES % customer_id)

    def disable_testing(self, website_id: str) -> dict:
        """Will instruct shoppimon to never test a given website.
        
        Args:
            website_id (str): The shoppimon id of a website, can be found using get_websites 

        Returns:
            Dict: The decoded response json.
        """
        return self.patch_request(config.ENDPOINT_WEBSITE % website_id, {"active": False})

    def enable_testing(self, website_id: str) -> dict:
        """Will re-enable testing for a given store, and set it to every 15 min.
        
        Args:
            website_id (str): The shoppimon id of a website, can be found using get_websites 
        Returns:
            Dict: The decoded json.
        """
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
        for index, website in Shoppimon.get_website_for_account(config.CLIENT_ID, config.CLIENT_SECRET,
                                                                config.WEBSITE_ID).items():
            print("website-id: %s | name: %s | url: %s" % (website['id'], website['name'], website['url']))
