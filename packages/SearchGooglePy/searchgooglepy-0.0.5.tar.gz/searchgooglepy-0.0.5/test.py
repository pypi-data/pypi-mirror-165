import searchgpy

# Initialize the module.
google_search_engine = searchgpy.GoogleSearchEngine()

# Search related results to the sentence `Hello Python !` on Google.
google_search_engine.search_text('Hello Python !', log=True)

# Search related image to the sentence `Hello Python !` on GoogleImage.
google_search_engine.search_img('Hello Python !', log=True)

# Search related news to the sentence `Hello Python !` on Google's news section.
google_search_engine.search_news('Hello Python !')

# Search related products to the sentence `Hello Python !` on Google's shopping section.
google_search_engine.search_shop('Hello Python !', log=False)