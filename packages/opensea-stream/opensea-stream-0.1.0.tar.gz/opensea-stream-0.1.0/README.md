# OpenSea Stream API - python SDK

A python SDK for receiving updates from the OpenSea Stream API - pushed over websockets. We currently support the following event types on a per-collection basis:

- Item Listed
- Item Sold
- Item Transferred
- Item Metadata updates
- Item Cancelled
- Item Received offer
- Item Received bid


Documentation: https://docs.opensea.io/reference/stream-api-overview

# Installation
This module requires Python 3 or later. 
[Python 3](https://www.python.org/downloads/)

```
pip install opensea_sdk
```

# Getting Started

## Authentication

In order to make onboarding easy, we've integrated the OpenSea Stream API with our existing API key system. The API keys you have been using for the REST API should work here as well. If you don't already have one, request an API key from us [here](https://docs.opensea.io/reference/request-an-api-key).

## Simple example

```python
from opensea_sdk import *

api_key = '' # Your opensea api key

def callback(payload: dict):
    # handle event
    return

Client = OpenseaStreamClient(api_key, Network.MAINNET)
Client.onItemListed('collection-slug', callback)
Client.onItemSold('collection-slug', callback)

Client.startListening()
```

You can also optionally pass in:

- a `network` if you would like to access testnet networks.
    - The default value is `Network.MAINNET`, which represents the following blockchains: Ethereum, Polygon mainnet, Klaytn mainnet, and Solana mainnet
    - Can also select `Network.TESTNET`, which represents the following blockchains: Rinkeby, Polygon testnet (Mumbai), and Klaytn testnet (Baobab).


## Available Networks

The OpenSea Stream API is available on the following networks:

### Mainnet

`wss://stream.openseabeta.com/socket`

Mainnet support events from the following blockchains: Ethereum, Polygon mainnet, Klaytn mainnet, and Solana mainnet.

### Testnet

`wss://testnets-stream.openseabeta.com/socket`

Testnet support events from the following blockchains: Rinkeby, Polygon testnet (Mumbai), and Klaytn testnet (Baobab).

To create testnet instance of the client, you can create it with the following arguments:

```python
from opensea_sdk import *

api_key = '' # Opensea api key

def callback(payload: dict):
    # handle event
    return

Client = OpenseaStreamClient(api_key, Network.TESTNET)

```

## Manually connecting to the socket (optional)

The client will automatically connect to the socket as soon as you subscribe to the first channel.
If you would like to connect to the socket manually (before that), you can do so:

```python
Client.connect()
```

After successfully connecting to our websocket it is time to listen to specific events you're interested in!

## Streaming metadata updates

We will only send out metadata updates when we detect that the metadata provided in `tokenURI` has changed from what OpenSea has previously cached.

```python
Client.onItemMetadataUpdated('collection-slug', callback)
```

## Streaming item listed events

```python
Client.onItemListed('collection-slug', callback)
```

## Streaming item sold events

```python
Client.onItemSold('collection-slug', callback)
```

## Streaming item transferred events

```python
Client.onItemTransferred('collection-slug', callback)
```

## Streaming bids and offers

```python
Client.onItemReceivedBid('collection-slug', callback)

Client.onItemReceivedOffer('collection-slug', callback)
```

## Streaming order cancellation events

```python
Client.onItemCancelled('collection-slug', callback)
```

## Streaming multiple event types and multiple collections

```python
Client.onEvents(
    ['collection-slug', 'collection_slug']
    [EventTypes.ITEM_RECEIVED_OFFER, EventTypes.ITEM_TRANSFERRED],
    callback
    )
```


# Subscribing to events from all collections

If you'd like to listen to an event from all collections use wildcard `*` for the `slug` parameter.

# Types

Types are included to make working with our event payload objects easier.

# Webhook

You might want to use our predefined but fully Customizable discord webhook management 

```python
from opensea_sdk import *
from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(url='') # Webhook Url
api_key = '' # Opensea api key

Client = OpenseaStreamClient(api_key, Network.MAINNET)

Client.onItemListed('collection-slug', Webhook(webhook).send)

Client.startListening()

```

You can change the color, the footer and the thumbnail of the webhook with the following arguments: 

```python
from opensea_sdk import *
from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(url='') # Webhook Url
api_key = '' # Opensea api key

custom_footer = 'My custom footer'
custom_thumbnail = '' # Image url
color_ = '' # Hexadecimal color e.g ff0000 (red)

Client = OpenseaStreamClient(api_key, Network.MAINNET)

Client.onItemListed('collection-slug', Webhook(webhook, color=color_,     thumbnail=custom_thumbnail, footer=custom_footer).send)

Client.startListening()
```
