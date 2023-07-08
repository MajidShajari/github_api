import base64
import re
from io import BytesIO

import requests


class GoogleFontConverter:
    @staticmethod
    def fetch_font_css(font, weight, text):
        url = "https://fonts.googleapis.com/css2?"
        params = {
            "family": font + ":wght@" + str(weight),
            "text": text,
            "display": "fallback",
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return GoogleFontConverter.encode_fonts(response.text)
        except (requests.RequestException, ValueError):
            return ""

    @staticmethod
    def encode_fonts(css):
        url_regex = r"\((https:\/\/fonts\.gstatic\.com.+?)\) format\(\'(.*?)\'\)"
        urls = re.findall(url_regex, css)
        for url, font_type in urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                font_data = BytesIO(response.content).getvalue()
                encoded_font = base64.b64encode(font_data).decode("utf-8")
                data_uri = f"data:font/{font_type};base64,{encoded_font}"
                css = css.replace(url, data_uri)
            except (requests.RequestException, ValueError):
                return ""
        return css
