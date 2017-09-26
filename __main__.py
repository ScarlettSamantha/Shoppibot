import os,sys
import requests

class shoppimon:

    BEARER = None
    ENDPOINT = "https://app.shoppimon.com"
    ENDPOINT_OAUTH = "https://api.shoppimon.com/oauth"
    ENDPOINT_CURRENT_USER = "https://api.shoppimon.com/account"
    ENDPOINT_WEBSITE = "https://api.shoppimon.com/website/%s"
    ENDPOINT_WEBSITES = "https://api.shoppimon.com/website?account_id=%s"

    def __init__(self, id, secret):
        self.id = id
        self.secret = secret

    def fetchKey(self):
        r = self.postRequest(self.ENDPOINT_OAUTH, {
            "grant_type": "client_credentials",
            "client_id": self.id,
            "client_secret": self.secret
        }, False)
        self.BEARER = r['access_token']

    def getKey(self):
        """
        :return: str 
        """
        if self.BEARER is None:
            self.fetchKey()
        return self.BEARER

    def postRequest(self, endpoint, request, addKey=True):
        headers = {
            "Accept": "application/json",
            "content-type": "application/json",
        }
        if addKey == True:
            headers['Authorization'] = "Bearer " + self.getKey()
            r = requests.post(endpoint, json=request, headers=headers)
        else:
            r = requests.post(endpoint, json=request)
        return r.json()

    def getRequest(self, endpoint, addKey=True):
        headers = {
            "Accept": "application/json",
            "content-type": "application/json",
        }
        if addKey == True:
            headers['Authorization'] = "Bearer " + self.getKey()
            r = requests.get(endpoint, headers=headers)
        else:
            r = requests.get(endpoint)
        return r.json()

    def getHeaders(self, data):
        return {**{
            "Accept": "application/json",
            "content-type": "application/json",
        }, **data}

    def patchRequest(self, endpoint, payload):
        r = requests.patch(endpoint, json=payload, headers=self.getHeaders({'Authorization': "Bearer " + self.getKey()}))
        return r.json()

    def setInterval(self, time = None):
        self.postRequest(self.ENDPOINT, {
            "active" : "false" if time == None else "true",
            "execution_interval": time if time is not None else 0
        })

    def getAccountDetails(self):
        r = self.getRequest(self.ENDPOINT_CURRENT_USER)
        return r

    def getWebsites(self, customerid):
        r = self.getRequest(self.ENDPOINT_WEBSITES % customerid)
        return r

    def disableTesting(self, websiteId):
        r = self.patchRequest(self.ENDPOINT_WEBSITE % websiteId, {
            "active": False
        })
        return r

    def enableTesting(self, websiteId):
        r = self.patchRequest(self.ENDPOINT_WEBSITE % websiteId, {
            "active": True
        })
        return r

    @classmethod
    def offline(cls, id, secret, websiteId):
        obj = cls(id, secret)
        obj.disableTesting(websiteId)

    @classmethod
    def online(cls, id, secret, websiteId):
        obj = cls(id, secret)
        obj.enableTesting(websiteId)

    @classmethod
    def getShops(cls, id, secret):
        obj = cls(id, secret)
        r = {}
        for account in obj.getAccountDetails()['_embedded']['account']:
            r[account['id']] = account['name']
            #print("id: %s | name: %s" % (account['id'], account['name']))
        return r

    @classmethod
    def getWebsitesForAccount(cls, id, secret, customerid):
        obj = cls(id, secret)
        r = {}
        for website in obj.getWebsites(customerid)['_embedded']['website']:
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
