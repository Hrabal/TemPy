# -*- coding: utf-8 -*-
import os
import json
import time
from functools import reduce
from datetime import datetime
from jinja2 import Template
from tempy_templates.sw import page as tempy_template

mean = lambda l: reduce(lambda x, y: x + y, l) / len(l)
sencond_to_run = 20
results = {}
with open('sw-people.json', 'r') as f:
    people = json.load(f)

j2_temp_file = os.path.join('templates', 'j2_sw_local.html')
context = {'people': people}


def render_j2(tpl_path, context):
    with open(tpl_path) as f:
        return Template(f.read()).render(context)


def render_tempy(_, context):
    return tempy_template.render(characters=context['people'].values())

for test in (render_tempy, render_j2):
    measures = []
    t_end = time.time() + sencond_to_run
    while time.time() < t_end:
        start = datetime.now()
        test(j2_temp_file, context)
        measures.append(datetime.now() - start)
    results[test.__name__] = measures

print(len(results['render_j2']), mean(results['render_j2']))
print(len(results['render_tempy']), mean(results['render_tempy']))
