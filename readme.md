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
git clone bitbucket.org:arekana/shoppibot.git ~/scripts/shoppibot

# Go into shoppibot folder
cd ~/scripts/shoppibot

# Install dependancies
pip3 install -r requirements.txt
```

# Config #
There are 2 ways to give the script the arguments it needs ether via the config file or via CLI arguments.
The latter will override the former if the arguments are present in the config file.



# Usage #
There is a --help command avalible if you require more indepth explonation of the arguments.

| Command | Argument | Description | Usage |
|----------|-----------|-------------------------------------------------------------|-------------------------------------------------|
| online | WebsiteId | Will start the shoppimon monitoring | ```python3 . online {websiteid} {client} {secret}``` |
| offline | WebsiteId | Will stop the shoppimon monitoring | ```python3 . offline {websiteid} {client} {secret}``` |
| shops |  | Here you can get the ShopId, will print a list of customers | ```python3 . shops {client} {secret}``` |
| websites | ShopId | Here you can get the website id | ```python3 . websites {client} {secret} {shopid}``` |