# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
import re


class MarkdownParser:
    # Main return result
    _result = []

    # Defaults
    tab_width = 4

    _empty_line_re = re.compile(r"^[ \t]+$", re.M)

    @property
    def result(self):
        for tempy_tag in self._result:
            yield tempy_tag

    def _reset(self):
        self._result = []
        pass

    def feed(self, raw_markdown):
        # Cycle through clean text
        for line in self._prepare_split_text(raw_markdown):
            # TODO
            pass

    def _prepare_split_text(self, text):
        # Uniform newlines
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        for line in text.splitlines():
            if set(line).issubset({'\t', ' '}):
                # If the line is only made of tabs and spaces, go ahead
                continue
            output = []
            # Replace tabs with spaces
            part, rest = line.split('\t', 1)
            while rest:
                output.append(part)
                spaces = (' ' * (self.tab_width - len(part) % self.tab_width))
                output.append(spaces)
                try:
                    part, rest = rest.split('\t', 1)
                except ValueError:
                    part, rest = rest, None
            yield ''.join(output)
