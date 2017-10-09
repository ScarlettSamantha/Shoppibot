# Installation #

## HyperNode ##
Waiting for reaction from byte on pip3 avaliblity on the hypernode platform.

## Normal ##
You can execute the following commands to do a request.

```bash
# Clone repo
git clone bitbucket.org:arekana/shoppibot.git

# Go into shoppibot folder
cd shoppibot

# Install dependancies
pip3 install -r requirements.txt
```

# Usage #

| Command | Argument | Description | Usage |
|----------|-----------|-------------------------------------------------------------|-------------------------------------------------|
| online | WebsiteId | Will start the shoppimon monitoring | python3 . online {client} {secret} {websiteid} |
| offline | WebsiteId | Will stop the shoppimon monitoring | python3 . offline {client} {secret} {websiteid} |
| shops |  | Here you can get the ShopId, will print a list of customers | python3 . shops {client} {secret} |
| websites | ShopId | Here you can get the website id | python3 . websites {client} {secret} {shopid} |