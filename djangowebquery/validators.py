#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'

import types
from dateutil import parser

'''
VALIDATORS
'''
class SchemaValidator():
    @classmethod
    def get(self, clazz, fields):
        out = clazz().__dict__
        for key in out.keys():
            if key.startswith("__") or key.startswith("_"):
                out.pop(key)
            elif fields and not key in fields:
                out.pop(key)
        return out

    @classmethod
    def values(self, clazz):
        c = clazz().__dict__
        out = []
        for key in c.keys():
            if not key.startswith("__") and not key.startswith("_"):
                out.append(key)
        return out

    @classmethod
    def schema(self, clazz):
        out = clazz().__dict__
        for key in out.keys():
            if key.startswith("__") or key.startswith("_"):
                out.pop(key)
        return out

class DateValidator():
    @classmethod
    def get(self, data):
        if type(data) == types.ListType:
            for i in range(0, len(data)):
                data[i] = self.get_date(data[i])
        elif type(data) == types.StringType:
            data = self.get_date(data)
        return data

    @classmethod
    def get_str(self, data):
        return data.strip("\" ")

    @classmethod
    def get_date(self, data):
        return parser.parse(self.get_str(data))

class AuthValidator():
    def check(self, c, user, t=None):
        if c.has_key('auth'):
            if type(c['auth']) is types.StringType:
                if c['auth'] == True and user.is_authenticated():
                    return True
                else:
                    return False
            elif type(c['auth']) is types.DictType:
                m = c['auth']
                if m.has_key(t):
                    if m[t] == True:
                        return True
                    else:
                        return False
                else:
                    return True
        else:
            return True
        return False

    def fields(c, user):
        if c.has_key('auth'):
            if type(c['auth']) is types.DictType:
                m = c['auth']
                if m.has_key('fields'):
                    return m['fields']
        return None

class LimitFilterValidator():
    @classmethod
    def get(self, data):
        start = None
        end = None
        out = 0
        if data.has_key("start"):
            start = data['start']
        if data.has_key("end"):
            end = data['end']
        if start == None:
            out = 1
        if end == None:
            out = 2
        if start == None and end == None:
            raise RuntimeError("no such method")
        return {"type":out, "start":start, "end":end}
