# -*- coding: utf-8 -*-
import os
import json
import time
from functools import reduce
from datetime import datetime
from jinja2 import Template


mean = lambda l: reduce(lambda x, y: x + y, l) / len(l)
seconds_to_run = 20
results = {}
with open('sw-people.json', 'r') as f:
    people = json.load(f)

context = {'people': people}


def render_j2_hello():
    with open(os.path.join('templates', 'hello_world.html')) as f2:
        return Template(f2.read()).render()


def render_tempy_hello():
    from tempy_templates.hello_world import page as tempy_template
    return tempy_template.render()


def render_j2_sw_mono(context1):
    with open(os.path.join('templates', 'j2_sw_monofile.html')) as f2:
        return Template(f2.read()).render(context1)


def render_tempy_sw_mono(context1):
    from tempy_templates.sw_monofile import page as tempy_template
    return tempy_template.render(characters=context1['people'].values())

# def render_j2_sw_multifile(context):
#    with open(os.path.join('templates', 'sw_characters.html')) as f:
#        return Template(f.read()).render(context)
#
# def render_tempy_sw_multifile(context):
#    from tempy_templates.sw_multifile import page as tempy_template
#    return tempy_template.render(characters=context['people'].values())


for test in (render_j2_hello, render_tempy_hello, render_j2_sw_mono, render_tempy_sw_mono):  # , render_j2_sw_multifile,render_tempy_sw_multifile):
    measures = []
    t_end = time.time() + seconds_to_run
    while time.time() < t_end:
        start = datetime.now()
        test(context)
        measures.append(datetime.now() - start)
    results[test.__name__] = measures

print('render_j2_hello', len(results['render_j2_hello']), mean(results['render_j2_hello']),
      len(results['render_j2_hello'])/seconds_to_run)
print('render_tempy_hello', len(results['render_tempy_hello']), mean(results['render_tempy_hello']),
      len(results['render_tempy_hello'])/seconds_to_run)
print('render_j2_sw_mono', len(results['render_j2_sw_mono']), mean(results['render_j2_sw_mono']),
      len(results['render_j2_sw_mono'])/seconds_to_run)
print('render_tempy_sw_mono', len(results['render_tempy_sw_mono']), mean(results['render_tempy_sw_mono']),
      len(results['render_tempy_sw_mono'])/seconds_to_run)
# print(len(results['render_j2_sw_multifile']), mean(results['render_j2_sw_multifile']))
# print(len(results['render_tempy_sw_multifile']), mean(results['render_tempy_sw_multifile']))
