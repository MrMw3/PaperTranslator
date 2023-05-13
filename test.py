import requests
import clipboard
import re

def post_data():
    data = {
            'ln': 'en',
            'exp': 'hello world'
        }

    res = requests.post('https://abadis.ir/ajaxcmd/inlinetranslate/', data, headers=get_post_headers())
    if res.status_code == 200:
        translated_text = parse_result(res.text)
        return translated_text
    else:
        return "An error accourd during post data"

def get_post_headers():
    headers = {
            "authority": "abadis.ir",
            "method": "POST",
            "path": "/ajaxcmd/inlinetranslate/",
            'scheme': "https",
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://abadis.ir',
            'referer': 'https://abadis.ir/translator/',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        }
    
    return headers

def parse_result(response):
    translated_text = re.search("delnTitle=\'\w+'>([\w|\W]*)</div>\n", response).group(1)
    return translated_text




if __name__ == "__main__":
    post_data()