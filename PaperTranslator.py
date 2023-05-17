import flet as ft
import re
import clipboard
import requests


def main(page):
    pure_text_field = ft.TextField(label="متن اصلی", autofocus=True, border_color="#2196f3", hint_text="متن مقاله را وارد کنید", multiline="True")
    translated_text_field = ft.TextField(label="ترجمه", border_color="#ff3d00", hint_text="ترجمه اینجا قرار می گیرد", text_align=ft.TextAlign.RIGHT, multiline=True)
    greetings = ft.Column()

    def btn_click(e):
        # greetings.controls.append(ft.Text(f"Hello, {first_name.value} {last_name.value}!"))
        # first_name.value = ""
        # last_name.value = ""
        # page.update()
        # first_name.focus()
        pure_text = pure_text_field.value
        cleaned_text = clean_text(pure_text)
        translated_text = translate(cleaned_text)
        translated_text_field.value = translated_text
        translated_text_field.focus()
        page.update()

    page.add(
        pure_text_field,
        translated_text_field,
        ft.ElevatedButton("ترجمه کن", on_click=btn_click),
        greetings,
    )


def clean_text(pure_text):
    if pure_text != "":
        step1 = pure_text.replace("", "").replace("\r", "")
        # ord() returns Ascci code of an character
        i = 0
        cleaned_text = ""

        for ch in step1:
            # 10 is Ascci code of \r
            if ord(ch) != 10:
                cleaned_text += ch
            else:
                cleaned_text += " "

        return cleaned_text

# TODO: It's time to translate cleaned text :)
def translate(cleaned_text):
    translated_text = post_data(cleaned_text)
    return translated_text


def post_data(user_text):
    data = {
            'ln': 'en',
            'exp': f'{user_text}'
        }

    res = requests.post('http://abadis.ir/ajaxcmd/inlinetranslate/', data, headers=get_post_headers())
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
            'scheme': "http",
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


if __name__ == '__main__':
    ft.app(target=main)
