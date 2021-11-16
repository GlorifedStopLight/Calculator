import re

item = "[0424]"

print(re.findall("\[([0-9]*)\]", item))