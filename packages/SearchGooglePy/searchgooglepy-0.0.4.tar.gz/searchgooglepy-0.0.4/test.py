import searchgpy

# Initialize the module.
google_search_engine = searchgpy.GoogleSearchEngine()

# Search related results to the sentence `Hello World !` on Google.
google_search_engine.search_text('Hello Python !')

# Search related image to the sentence `Hello World !` on GoogleImage.
google_search_engine.search_img('Hello Python !')

# Search related news to the sentence `Hello World !` on GoogleNews.
google_search_engine.search_news('Hello Python !')