# SearchGooglePy

SearchGooglePy is a simple (un-official) Google Search API under python.

This page will help you to [install](#install) and get a [quick start](#quick-start)
___
**!WARNNING!: This isn't an official google project it is just an API under python.**
___

**A few advertisement and credits before you start :**

***Dependencies***

- Python 3
- pip 22.2.2

***Credits***

See [ThirdPartyNotices.md](./ThirdPartyNotices.md) file to watch credits

___

## Install

To install SearchGooglePy follow the steps behavior:

### Windows:

1. Open the `Command Prompt` or the `PowerShell` app.
2. type on your prompt the command behavior:
```powershell
pip install SearchGooglePy
```

### Linux / MacOS

1. Open the `Shell`
2. type on your prompt:
```
python3 -m pip install SearchGooglePy
```

## Quick Start

A quick piece of code to get a quick start:

```py
import searchgpy

google_search_engine = searchgpy.GoogleSearchEngine()
google_search_engine.search_text('Hello World !')
```

This piece of code will search on google the sentence : `Hello World !`. Take a look at the `Table of Content` at https://boubajoker.github.io/SearchGooglePy/Link=Table_Of_Content for more content !