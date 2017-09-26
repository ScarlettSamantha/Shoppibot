import os,sys
import requests

class shoppimon:

    ENDPOINT_OAUTH = "https://api.shoppimon.com/oauth"
    ENDPOINT_WEBSITE = "https://api.shoppimon.com/website/%s"
    ENDPOINT_WEBSITES = "https://api.shoppimon.com/website?account_id=%s"

    def __init__(self, id, secret):
        self.id = id
        self.secret = secret
        self.bearer = None

    def getHeaders(self, data):
        return {**{
            "Accept": "application/json",
            "content-type": "application/json",
        }, **data}

    def postRequest(self, endpoint, request, addKey=True):
        return requests.post(endpoint, json=request, headers=self.getHeaders({'Authorization': "Bearer " + self.getKey()} if addKey else {})).json()

    def getRequest(self, endpoint):
        return requests.get(endpoint, headers=self.getHeaders({'Authorization': "Bearer " + self.getKey()})).json()

    def patchRequest(self, endpoint, payload):
        return requests.patch(endpoint, json=payload, headers=self.getHeaders({'Authorization': "Bearer " + self.getKey()})).json()

    def fetchKey(self):
        r = self.postRequest(self.ENDPOINT_OAUTH, {
            "grant_type": "client_credentials",
            "client_id": self.id,
            "client_secret": self.secret
        }, False)
        self.bearer = r['access_token']

    def getKey(self):
        """
        :return: str 
        """
        if self.bearer is None:
            self.fetchKey()
        return self.bearer

    def getAccountDetails(self):
        return self.getRequest(self.ENDPOINT_CURRENT_USER)

    def getWebsites(self, customerid):
        return self.getRequest(self.ENDPOINT_WEBSITES % customerid)

    def disableTesting(self, websiteId):
        return self.patchRequest(self.ENDPOINT_WEBSITE % websiteId, {"active": False})

    def enableTesting(self, websiteId):
        return self.patchRequest(self.ENDPOINT_WEBSITE % websiteId, {"active": True})

    @classmethod
    def offline(cls, id, secret, websiteId):
        cls(id, secret).disableTesting(websiteId)

    @classmethod
    def online(cls, id, secret, websiteId):
        cls(id, secret).enableTesting(websiteId)

    @classmethod
    def getShops(cls, id, secret):
        r = {}
        for account in cls(id, secret).getAccountDetails()['_embedded']['account']:
            r[account['id']] = account['name']
        return r

    @classmethod
    def getWebsitesForAccount(cls, id, secret, customerid):
        r = {}
        for website in cls(id, secret).getWebsites(customerid)['_embedded']['website']:
            r[website['id']] = {website['id'], website['name'], website['base_url']}
        return r

def argumentCheck(req = 4):
    req += 1
    if sys.argv.__len__() < req:
        print('We need %s arguments we got %s' % (req, sys.argv.__len__()))
        if req == 5:
            if sys.argv[1] == 'websites':
                argument = 'clientid'
            elif sys.argv[1] in ('online', 'offline'):
                argument = 'websiteid'
            else:
                argument = 'unknown'
            print("python3 %s %s [clientid] [clientsecret] [argument(%s)]" % (os.path.abspath(__file__), sys.argv[1] if sys.argv.__len__() > 1 else '[action]', argument))
            exit(2)
        elif req == 4:
            print("python3 %s %s [clientid] [clientsecret]" % (os.path.abspath(__file__), sys.argv[1] if sys.argv.__len__() > 1 else '[action]'))
            exit(2)

if __name__ == "__main__":
    action = sys.argv[1]

    if action == 'offline':
        argumentCheck(4)
        shoppimon.offline(sys.argv[2], sys.argv[3], sys.argv[4])
    elif action == 'online':
        argumentCheck(4)
        shoppimon.online(sys.argv[2], sys.argv[3], sys.argv[4])
    elif action == 'shops':
        argumentCheck(3)
        for index, value in shoppimon.getShops(sys.argv[2], sys.argv[3]).items():
            print("id: %s | name: %s" % (index, value))
    elif action == 'websites':
        argumentCheck(4)
        for index, website in shoppimon.getWebsitesForAccount(sys.argv[2], sys.argv[3], sys.argv[4]).items():
            print("id: %s | name: %s | url: %s" % tuple(website))
