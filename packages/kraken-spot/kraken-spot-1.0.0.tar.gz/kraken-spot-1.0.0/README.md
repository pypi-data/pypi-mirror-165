# Kraken Spot

[![Build Status](https://app.travis-ci.com/kevbradwick/kraken-spot.svg?branch=master)](https://app.travis-ci.com/kevbradwick/kraken-spot)

A Python library for interacting with the [Kraken Spot REST API](https://docs.kraken.com/rest/).

## Quick Start

Install from source of via `pip`

    pip install kraken-spot

```python
from kraken_spot import DefaultClient

client = DefaultClient()
client.get_account_balance()
```

The default client will attempt to configure the client with api keys from environment variables. Both `KRAKEN_API_KEY` and `KRAKEN_PRIVATE_KEY` needs to be set.

## OTP Authentication

If the API key has 2FA enabled, you will need to provide a one time password with your call.

```python
client.set_otp(123456)
client.get_account_balance()
```

The OTP is reset after each request.

## Features

The following endpoints are currently supported;

| Endpoint Set | Supported |
| ------ | ------- |
| Market Data | ✅ |
| User Data | ✅ |
| User Trading | ✅ (except batch orders) |
| User Funding | ✅ |
| User staking | ✅ |
| Websocket Authentication | ✅ |
