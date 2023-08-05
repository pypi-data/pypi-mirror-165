# embed_builder

[![PyPI](https://img.shields.io/pypi/v/embed_builder?color=0073b7&label=version&logo=python&logoColor=white&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dd/embed_builder?color=0073b7&logo=python&logoColor=white&style=flat-square)](https://pypi.org/project/embed-builder/)

I got tired of manually writing dictionaries to send embeds via Discord webhooks, so I made this package to do it effortlessly.

This package was developed on Python 3.10.x but has not been tested on earlier versions. If you happen to successfully use this package on an older version then do let me know.

## Installation

```shell
$ pip install embed-builder
```

## Usage

```python
from embed_builder import Embed

embed = Embed()
embed.set_title("Hello")
embed.set_description("How are you?")
embed.set_color("#ff69b4")

# New in 1.4.0 - Validating embed limits - https://discord.com/developers/docs/resources/channel#embed-object-embed-limits
if not embed.is_valid():
    raise Exception("woops! embed has exceeded Discord's limits")

my_embed = embed.build()

# Or via chaining...

my_embed = Embed().set_title("Hello").set_description("How are you?").build()

# Example usage with Discord webhooks and requests package

requests.post("webhook url", json={
    "content": "here is an embed",
    "embeds": [my_embed]
})
```
