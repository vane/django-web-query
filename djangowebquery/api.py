#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'
from django.http import HttpResponse

from decorator import ObjectDecorator
from validators import SchemaValidator
import utils
import inspect
import types


class ApiProcessor():
    '''
    CONSTRUCTOR
    '''
    def __init__(self):
        self.registry = {}

    '''
    PUBLIC
    '''
    def register_dict(self, path, data):
        self.path = path
        flag = True
        for d in data:
            f = self.register_one(d, data[d])
            if f is False:
                flag = f
        return flag

    def quick_register(self, path, model):
        self.path = path
        members = inspect.getmembers(model)
        for m in members:
            if type(m[0]) is types.StringType and inspect.isclass(m[1]):
                self.register_one(m[0], ObjectDecorator(m[1]))

    def register_one(self, name, clazz):
        if self.checkreg(name):
            return False
        self.registry[name] = clazz
        return True

    def unregister_one(self, name, clazz):
        if self.checkreg(name):
            del self.registry[name]
            return True
        return False

    def checkreg(self, name):
        return self.registry.has_key(name)

    def filter(self, request):
        out = {"state":"null"}
        #request = HttpRequest()
        path = request.path_info
        path = path[len(self.path):]
        path_a = path.split("/")
        if self.checkreg(path_a[0]):
            c = self.registry.get(path_a[0])
            if request.method == 'GET':
                out = c.GET(request)
            elif request.method == 'POST':
                out = c.POST(request)
            elif request.method == 'PUT':
                out = c.PUT(request)
            elif request.method == 'OPTIONS':
                out = SchemaValidator.get(c.clazz, c.get_FIELDS())
            elif request.method == 'DELETE':
                out = c.DELETE(request)
        return utils.tojson(out)

class Api():
    registry = ApiProcessor()

    @classmethod
    def serialize(self, name, data):
        o = self.registry.registry.get(name)
        if o != None:
            return o.SERIALIZE(data)
        return {'error':'problem no such data'}

    @classmethod
    def urls(self, request):
        out = self.registry.filter(request)
        return HttpResponse(out, content_type="application/json")