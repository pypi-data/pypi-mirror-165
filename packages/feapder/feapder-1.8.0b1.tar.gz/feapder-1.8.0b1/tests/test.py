# import re
import regex as re

with open("temp.html", "r") as file:
    html = file.read()

regex = "<a.*?href='(.*?)'"
print(re.findall(regex, html, re.S))