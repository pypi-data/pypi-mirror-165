# cryptodweet

[![PayPal Donate][paypal_img]][paypal_link]
[![PyPI version][pypi_img]][pypi_link]
[![Downloads][downloads_img]][downloads_link]

  [paypal_img]: https://github.com/jacklinquan/images/blob/master/paypal_donate_badge.svg
  [paypal_link]: https://www.paypal.me/jacklinquan
  [pypi_img]: https://badge.fury.io/py/cryptodweet.svg
  [pypi_link]: https://badge.fury.io/py/cryptodweet
  [downloads_img]: https://pepy.tech/badge/cryptodweet
  [downloads_link]: https://pepy.tech/project/cryptodweet

[Documentation](https://jacklinquan.github.io/cryptodweet)

A python module for very basic APIs of the free dweet service with encryption.

Dweet is a simple machine-to-machine (M2M) service from https://dweet.io/ .
The free service is public and any data is accessible by anyone.
This package adds encryption to it and make it a bit more secure.
Only the minimal APIs are supported.

## Installation

`pip install cryptodweet`

## Usage

```python
>>> from cryptodweet import CryptoDweet
>>> cd = CryptoDweet("YOUR KEY")
>>> cd.dweet_for("YOUR THING", {"YOUR DATA": "YOUR VALUE"})
{'thing': '9ee9b47833d5a13043c5f47e8802596a', 'created': '2022-08-30T05:40:44.885Z',
'content': {'8c94428bc640de621c7c3ceea1d00b96': '05d6f2dbc1ce3afa7e6072c0c4c6f6a7'},
'transaction': '5786ee01-ef5c-4bd1-9734-ed9334180600'}
>>> cd.get_latest_dweet_for("YOUR THING")
[{'thing': 'YOUR THING', 'created': '2022-08-30T05:40:44.885Z',
'content': {'YOUR DATA': 'YOUR VALUE'}}]
```
