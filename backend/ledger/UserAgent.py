import requests
import random 
from collections import OrderedDict

class NewUserAgent:
    def __init__(self):
        self.headers_list = [
            # Safari 17 Mac
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us",
                "Connection": "keep-alive",
                "Referer": "https://www.apple.com/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Edge 115 Windows
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36 Edg/115.0.1901.183",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Referer": "https://www.bing.com/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Chrome 115 Linux
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Firefox 116 Windows
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Referer": "https://www.mozilla.org/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Safari 17 iPhone
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us",
                "Connection": "keep-alive",
                "Referer": "https://www.apple.com/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Chrome 115 Android
            {
                "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.166 Mobile Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Firefox 116 Linux
            {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:116.0) Gecko/20100101 Firefox/116.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Referer": "https://www.mozilla.org/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Safari 17 iPad
            {
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-us",
                "Connection": "keep-alive",
                "Referer": "https://www.apple.com/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Chrome 115 Windows
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            },
            # Firefox 116 Mac
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:116.0) Gecko/20100101 Firefox/116.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-GB,en;q=0.5",
                "Connection": "keep-alive",
                "Referer": "https://www.mozilla.org/",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br"
            }
        ]


    
    # Create ordered dict from Headers above
    def order_headers(self, headers_list):
        ordered_headers_list = []
        for headers in headers_list:
            h = OrderedDict()
            for header,value in headers.items():
                h[header] = value
            ordered_headers_list.append(h)

        return headers_list
    
    def connect_url(self, url):
        headers_list = self.order_headers(self.headers_list)
        # # pick browser header
        headers = random.choice(headers_list)
        ## create session
        r = requests.Session()
        r.headers = headers
        
        response = r.get(url)
        if response.status_code == 200:

            return response
        else:
            return None
