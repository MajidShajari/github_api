import base64
import re
from io import BytesIO

import requests


class GoogleFontConverter:
    @staticmethod
    def fetchFontCSS(font, weight, text):
        url = "https://fonts.googleapis.com/css2?"
        params = {
            "family": font + ":wght@" + weight,
            "text": text,
            "display": "fallback",
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return GoogleFontConverter.encodeFonts(response.text)
        except (requests.RequestException, ValueError):
            return ""

    @staticmethod
    def encodeFonts(css):
        urlRegex = r"\((https:\/\/fonts\.gstatic\.com.+?)\) format\(\'(.*?)\'\)"
        urls = re.findall(urlRegex, css)
        for url, fontType in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                fontData = BytesIO(response.content).getvalue()
                encodedFont = base64.b64encode(fontData).decode("utf-8")
                dataURI = f"data:font/{fontType};base64,{encodedFont}"
                css = css.replace(url, dataURI)
            except (requests.RequestException, ValueError):
                pass
        return css
