# -*- coding: utf-8 -*-
import re

separators = ['~', ',', '+', '>', ' ']
regexPattern = '|'.join(map(re.escape, separators))
selector = '#someId > div.someClass'
spl = re.split(regexPattern, selector)

print spl
