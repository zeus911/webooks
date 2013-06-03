# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from webooks.utils import const
from webooks.utils.util import md5
import requests
import os

class SpiderHelper(object):
    def __init__(self, suffix="xml"):
        self.suffix = suffix

    def name_hash(self, name):
        name = name.replace(".", "")
        number = int(name, base=36)
        return str(number % const.SPIDER_HASH)

    def get_path(self, url):
        name = md5(url) + '.' + self.suffix
        hash_dir = self.name_hash(name)
        path = os.path.join(const.SPIDER_BASE_PATH, hash_dir, name)
        return path

    def read(self, path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content

    def save(self, url):
        res = requests.get(url, headers=const.SPIDER_HEADERS)
        content = res.content
        name = md5(url) + ".xml"
        hash_dir = self.name_hash(name)
        path = os.path.join(const.SPIDER_BASE_PATH, hash_dir, name)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        file = open(path, "w")
        file.write(content)
        file.close()

    def get(self, url, *args, **kwargs):
        path = self.get_path(url)
        if os.path.exists(path):
            return self.read(path)

        self.save(url)
        return self.read(path)