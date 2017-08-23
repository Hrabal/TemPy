# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
Tools for Tempy
"""


class AdjustableList(list):
    def ljust(self, n, fillvalue=''):
        return self + [fillvalue] * (n - len(self))
