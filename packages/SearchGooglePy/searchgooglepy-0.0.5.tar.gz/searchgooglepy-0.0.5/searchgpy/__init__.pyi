"""
# SearchGooglePy `searchgpy`

SearchGooglePy is a simple (un-official) Google Search API under python.

## User-Manual

### `GoogleSearchEngine` SuperClass:

The SuperClass that initialize the module.

### `search_text` function:

The `search_text` function is the function that is used to search on Google's (`www.google.com`) web-engine.

@param `text` --- the text that you want to search on google.

### `search_img` function:

The `search_img` function has the role to search images on Google's (`www.google.com`) web-engine.

@param `text` --- The text that you want to search on google to display images.

### Quick Start:

A quick piece of code to get a quick start:

```py
import searchgpy

google_search_engine = searchgpy.GoogleSearchEngine()
google_search_engine.search_text('Hello World !')
```

This piece of code will search on google the sentence : `Hello World !`. Take a look at the `Table of Content` at https://www.github.com/Boubajoker/SearchGooglePy/blob/master/FEATURE_CONTRIBUTIONS.md or at https://boubajoker.github.io/SearchGooglePy/Link=Table_Of_Content for more content !

"""
from typing import *

class GoogleSearchEngine:
    def __init__(self) -> Any: 
        """
        ### `GoogleSearchEngine` SuperClass:

        The SuperClass that initialize the module.
        """
        pass

    def search_text(self, text: str, log: str) -> Any: 
        """
        ### `search_text` function:

        The `search_text` function has the role to search on Google's (`www.google.com`) web-engine.

        @param `text` --- The text that you want to search on google.
        @param `log` --- Print the URL that wil be given when the value is `True`.
        """
        pass
    
    def search_img(self, text: str, log: str) -> Any:
        """
        ### `search_img` function:

        The `search_img` function has the role to search images on Google's (`www.google.com`) web-engine.

        @param `text` --- The text that you want to search on google to display images.
        @param `log` --- Print the URL that wil be given when the value is `True`.
        """
        pass
    
    def search_news(self, text: str, log: str) -> Any:
        """
        ### `search_news` function:

        The `search_news` function has the role to search news on Google's (`www.google.com`) web-engine.
        
        @param `text` --- The text that you want to search on google to display news.
        @param `log` --- Print the URL that wil be given when the value is `True`.
        """
        pass
    
    def search_shop(self, text: str, log: str) -> Any:
        """
        ### `search_shop` function:

        The `shearch_shop` function has the role to search products on Google's (`wwww.google.com`) web-engine.

        @param `text` --- The text that you want to search on google to display products.
        @param `log` --- Print the URL that wil be given when the value is `True`.
        """
        pass