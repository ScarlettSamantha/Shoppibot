# Installation #

## HyperNode ##
This module is usable on a hyper on my request pip3 was added to the platform.
The installation instructions are the same as a normal server.

## Normal ##
You can execute the following commands to do a request.

Quick:
```bash
# Clone repo
git clone bitbucket.org:arekana/shoppibot.git

# Go into shoppibot folder
cd shoppibot

# Install dependancies
pip3 install -r requirements.txt
```

This will install the module into the current pwd you are in.

Better:
Quick:
```bash
# Clone repo
git clone git@github.com:ScarlettSamantha/Shoppibot.git ~/scripts/shoppibot
# Go into shoppibot folder
cd ~/scripts/shoppibot
# Install dependancies
pip3 install -r requirements.txt
# Open vim to input your options.
vim config.py
```

# Config #
There are 2 ways to give the script the arguments it needs ether via the config file or via CLI arguments.
The latter will override the former if the arguments are present in the config file.

The default config is as follows:
```python
ENDPOINT_OAUTH = "https://api.shoppimon.com/oauth"
ENDPOINT_WEBSITE = "https://api.shoppimon.com/website/%s"
ENDPOINT_WEBSITES = "https://api.shoppimon.com/website?account_id=%s"
ENDPOINT_USER_INFO = "https://api.shoppimon.com/account"

SHOPPIMON_API_ACCOUNT_PAGE = 'https://app.shoppimon.com/user/api'

ACTION_HELP = "This is the action you wish to execute."
CLIENT_ID_HELP = "The client id of the shoppimon account can be found at %s, Needed for all calls, Can be set in config"
CLIENT_SECRET_HELP = "The client secret of the shoppimon account can be found at %s, Needed for all calls, Can be set in config"
CONTEXT_ID_HELP = "The context id is needed for website_id and shop_id is always website_id except for in the shops call then its shop_id, Needed for all calls except shops, Can be set in config"

CLIENT_ID = None
CLIENT_SECRET = None
WEBSITE_ID = None
SHOP_ID = None
```
If one of the bottom 4 values is None it will require CLI input of the matching var.

# Usage #
There is a --help command available if you require more in-depth explanation of the arguments.

| Command | Argument | Description | Usage |
|----------|-----------|-------------------------------------------------------------|-------------------------------------------------|
| online | WebsiteId | Will start the shoppimon monitoring | ```python3 . -action="online" -context_id="{websiteid}" -client_id="{client}" -client_secret="{secret}"``` |
| offline | WebsiteId | Will stop the shoppimon monitoring | ```python3 . -action="offline" -context_id="{websiteid}" -client_id="{client}" -client_secret="{secret}"``` |
| shops |  | Here you can get the ShopId, will print a list of customers | ```python3 . -action="shops" -client_id="{client}" -client_secret="{secret}"``` |
| websites | ShopId | Here you can get the website id | ```python3 . -action="websites" -context_id="{shopid}" -client_id="{client}" -client_secret="{secret}"``` |
| websites-all | | Here you get a structured list of all the websites and the shops above it | ```python3 . -action="websites-all" -context_id="{shopid}" -client_id="{client}" -client_secret="{secret}"``` |