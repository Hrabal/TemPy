# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>')
import sys
import argparse

from .t import T

def translate(origin, destination, pretty=False):
    if not destination:
        destination = origin.split('.')[0] + '.py'
    with open(origin, 'r') as html:
        tempy_tree = T.from_string(html.read())
    T.dump(tempy_tree, destination, pretty=pretty)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--translate', help='Translates a .html file into a Tempy .py file.', action="store_true")

    actions, rem_args = parser.parse_known_args()
    if actions.translate:
        translate_group = parser.add_argument_group('Translation of html into Tempy python files')
        translate_group.add_argument('origin', help='original .html file', action="store")
        translate_group.add_argument('destination', nargs='?', help='detination .py file', action="store")
        translate_group.add_argument('-p', '--pretty', help='Makes the output file indented.', action="store_true")

    args = parser.parse_args(rem_args, namespace=actions)
    if not len(sys.argv) > 1:
        parser.print_help()
    else:
        if actions.translate:
            translate(args.origin, args.destination, pretty=args.pretty)

if __name__ == '__main__':
    main()
