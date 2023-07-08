from typing import Dict
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from ...utils.google_font_convertor import GoogleFontConverter

initial_dict: Dict = {
    "separator": ";",
    "font": "Fira Code",
    "weight": "400",
    "size": "20",
    "color": "36BCF7",
    "duration": "5000",
    "pause": "1000",
    "background": "00000000",
    "center": "false",
    "v_center": "false",
    "multiline": "false",
    "repeat": "true",
    "width": "435",
    "height": "50",
}


class Svg:
    def __init__(self, parameters: Dict) -> None:
        self.param_dict = parameters
        self._modified_lines()
        google_font = GoogleFontConverter()
        self.svg_style = google_font.fetch_font_css(
            font=self._get_param("font"),
            weight=self._get_param("weight"),
            text=self._get_param("lines"),
        )
        self.svg = Element("svg")
        self.create_svg()

    def _get_param(self, key: str):
        if key == "lines":
            return self.param_dict.get(key)
        if self.param_dict.get(key, initial_dict[key]).isdigit():
            return int(self.param_dict.get(key, initial_dict[key]))
        if self.param_dict.get(key, initial_dict[key]) == "false":
            return False
        if self.param_dict.get(key, initial_dict[key]) == "true":
            return True
        return self.param_dict.get(key, initial_dict[key])

    def _modified_lines(self):
        self.param_dict["lines"] = self.param_dict["lines"].split(
            self._get_param("separator")
        )

    def create_svg(self):
        self.svg.set("xmlns", "http://www.w3.org/2000/svg")
        self.svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        self.svg.set(
            "viewBox", f'0 0 {self._get_param("width")} {self._get_param("height")}'
        )
        self.svg.set("style", f'background-color: #{self._get_param("background")};')
        self.svg.set("width", f'{self._get_param("width")}px')
        self.svg.set("height", f'{self._get_param("height")}px')

        font_css_element = SubElement(self.svg, "style")
        font_css_element.text = self.svg_style
        last_line_index = len(self._get_param("lines")) - 1
        for i, line in enumerate(self._get_param("lines")):
            path = SubElement(self.svg, "path")
            path.set("id", f"path{i}")
            if not self._get_param("multiline"):
                if i != 0:
                    begin = f"d{i - 1}.end"
                elif self._get_param("repeat"):
                    begin = f"0s;d{last_line_index}.end"
                else:
                    begin = "0s"
                freeze = not self._get_param("repeat") and i == last_line_index
                y_offset = self._get_param("height") / 2
                empty_line = f"m0,{y_offset} h0"
                full_line = f'm0,{y_offset} h{self._get_param("width")}'
                values = [
                    empty_line,
                    full_line,
                    full_line,
                    full_line if freeze else empty_line,
                ]
                key_times = [
                    "0",
                    f'{0.8 * self._get_param("duration") / (self._get_param("duration") + self._get_param("pause"))}',
                    f'{(0.8 * self._get_param("duration") + self._get_param("pause")) / (self._get_param("duration") + self._get_param("pause"))}',
                    "1",
                ]

                animate = SubElement(path, "animate")
                animate.set("id", f"d{i}")
                animate.set("attributeName", "d")
                animate.set("begin", begin)
                animate.set(
                    "dur", f'{self._get_param("duration") + self._get_param("pause")}ms'
                )
                animate.set("fill", "freeze" if freeze else "remove")
                animate.set("values", " ; ".join(values))
                animate.set("keyTimes", ";".join(key_times))
            else:
                next_index = i + 1
                line_height = self._get_param("size") + 5
                line_duration = (
                    self._get_param("duration") + self._get_param("pause")
                ) * next_index
                y_offset = next_index * line_height
                empty_line = f"m0,{y_offset} h0"
                full_line = f'm0,{y_offset} h{self._get_param("width")}'
                values = [empty_line, empty_line, full_line, full_line]
                key_times = [
                    "0",
                    f"{i / next_index}",
                    f'{i / next_index + self._get_param("duration") / line_duration}',
                    "1",
                ]

                animate = SubElement(path, "animate")
                animate.set("id", f"d{i}")
                animate.set("attributeName", "d")
                animate.set(
                    "begin",
                    f'0s{f";d{last_line_index}.end" if self._get_param("repeat") else ""}',
                )
                animate.set("dur", f"{line_duration}ms")
                animate.set("fill", "freeze")
                animate.set("values", " ; ".join(values))
                animate.set("keyTimes", ";".join(key_times))

            text = SubElement(self.svg, "text")
            text.set("font-family", f'"{self._get_param("font")}", monospace')
            text.set("fill", f'#{self._get_param("color")}')
            text.set("font-size", str(self._get_param("size")))
            text.set(
                "dominant-baseline", "middle" if self._get_param("v_center") else "auto"
            )
            text.set("x", "50%" if self._get_param("center") else "0%")
            text.set("text-anchor", "middle" if self._get_param("center") else "start")

            text_path = SubElement(text, "textPath")
            text_path.set("xlink:href", f"#path{i}")
            text_path.text = line + "\n"
        return self.svg

    # Convert SVG element to a formatted string
    def svg_string(self):
        return minidom.parseString(tostring(self.svg)).toprettyxml(indent="  ")
