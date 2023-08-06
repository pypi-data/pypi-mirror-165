# SearchGooglePy Copyright (c) Boubajoker 2022. All right reserved. Project under MIT License.
# See https://github.com/Boubajoker/SearchGooglePy/blob/master/CopyRight.txt for more info.
from typing import *
import webbrowser

class GoogleSearchEngine:
    def __init__(self) -> Any:
        super(GoogleSearchEngine, self).__init__()
        print('<!--SearchGooglePy module started-->')

    def search_text(self, text, log=None) -> Any:
        self.base_google_search_url = 'https://www.google.com/search?q=' + text

        if text == None:
            pass
        else:
            webbrowser.open(self.base_google_search_url)
            
        if log:
            print('Redirecting to URL:', self.base_google_search_url)
        else: 
            pass

    def search_img(self, text, log=None) -> Any:
        self.base_google_img_url = 'https://www.google.com/search?q=' + text + '&sxsrf=ALiCzsYlU6o2Uq4WIlhJlkHR20Dh5VFItQ:1661285028951&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjXupWA4d35AhVE-YUKHQIaBFIQ_AUoAXoECAIQAw&biw=1879&bih=1008&dpr=1'

        if text == None:
            pass
        else:
            webbrowser.open(self.base_google_img_url)

        if log:
            print('Redirecting to URL:', self.base_google_img_url)
        else: 
            pass
    
    def search_news(self, text, log=None) -> Any:
        self.base_google_news_url = 'https://www.google.com/search?q=' + text + '!&source=lmns&tbm=nws&bih=990&biw=909&hl=fr&sa=X&ved=2ahUKEwj5zdSq4d_5AhUfQvEDHYvQAxUQ_AUoA3oECAEQAw'

        if text == None:
            pass
        else:
            webbrowser.open(self.base_google_news_url)
        
        if log:
            print('Redirecting to URL:', self.base_google_news_url)
        else: 
            pass

    def search_shop(self, text, log=None) -> Any:
        self.base_google_shop_url = 'https://www.google.com/search?q='+ text + '&client=opera-gx&hs=H7r&source=lnms&tbm=shop&sa=X&ved=2ahUKEwjBzIjdkPT5AhUUgHMKHeNICIkQ_AUoBHoECAEQBg&biw=1879&bih=1008&dpr=1'

        if text == None:
            pass
        else:
            webbrowser.open(self.base_google_shop_url)

        if log:
            print('Redirecting to URL:', self.base_google_shop_url)
        else: 
            pass
    
if __name__ == '__main__':
    webbrowser.open('https://boubajoker.github.io/SearchGooglePy/?link=Home')